import fs from "fs";
import path from "path";
import { ChampionData } from "../types/champion";

interface CacheEntry {
  data: ChampionData;
  timestamp: number;
}

interface ChampionIndex {
  [slug: string]: {
    filename: string;
    name: string;
    tier: string;
    role: string;
  };
}

/**
 * High-performance champion data cache with pre-built index
 */
export class ChampionCache {
  private static cache = new Map<string, CacheEntry>();
  private static index: ChampionIndex | null = null;
  private static readonly CACHE_TTL = 1000 * 60 * 60; // 1 hour
  private static readonly championsPath = path.join(
    process.cwd(),
    "champions_clean"
  );
  private static readonly indexPath = path.join(
    process.cwd(),
    "champion_index.json"
  );

  /**
   * Build and cache champion index for O(1) lookups
   */
  static buildIndex(): ChampionIndex {
    if (this.index) return this.index;

    try {
      // Try to load existing index
      if (fs.existsSync(this.indexPath)) {
        const indexData = fs.readFileSync(this.indexPath, "utf-8");
        this.index = JSON.parse(indexData);
        return this.index!;
      }
    } catch (error) {
      console.warn("Failed to load champion index, rebuilding...");
    }

    // Build new index
    const index: ChampionIndex = {};
    const files = fs.readdirSync(this.championsPath);

    for (const file of files) {
      if (!file.endsWith(".json")) continue;

      try {
        const filePath = path.join(this.championsPath, file);
        const content = fs.readFileSync(filePath, "utf-8");
        const data = JSON.parse(content);

        const slug = file.replace(".json", "");
        index[slug] = {
          filename: file,
          name: data.name || slug,
          tier: data.tier?.toString() || "3",
          role: data.roles?.[0] || "Unknown",
        };
      } catch (error) {
        console.warn(`Failed to index champion ${file}:`, error);
      }
    }

    // Save index for future use
    try {
      fs.writeFileSync(this.indexPath, JSON.stringify(index, null, 2));
    } catch (error) {
      console.warn("Failed to save champion index:", error);
    }

    this.index = index;
    return index;
  }

  /**
   * Get champion data with caching
   */
  static getChampion(slug: string): ChampionData | null {
    // Check cache first
    const cached = this.cache.get(slug);
    if (cached && Date.now() - cached.timestamp < this.CACHE_TTL) {
      return cached.data;
    }

    // Get from index
    const index = this.buildIndex();
    const entry = index[slug];
    if (!entry) return null;

    try {
      const filePath = path.join(this.championsPath, entry.filename);
      const content = fs.readFileSync(filePath, "utf-8");
      const rawData = JSON.parse(content);

      // Lightweight transformation - only essential data
      const championData = this.transformChampionData(rawData, slug);

      // Cache the result
      this.cache.set(slug, {
        data: championData,
        timestamp: Date.now(),
      });

      return championData;
    } catch (error) {
      console.error(`Failed to load champion ${slug}:`, error);
      return null;
    }
  }

  /**
   * Optimized data transformation - minimal processing
   */
  private static transformChampionData(
    rawData: any,
    slug: string
  ): ChampionData {
    const firstBuild = rawData.builds?.[0] || {};

    return {
      champion: {
        id: slug,
        name: rawData.name || slug,
        title: rawData.name || slug,
        role: rawData.roles?.[0] || "Unknown",
        lanes: rawData.lanes || ["Mid"],
        difficulty:
          rawData.stats?.difficulty > 66
            ? "High"
            : rawData.stats?.difficulty > 33
            ? "Medium"
            : "Low",
        tier: this.mapTier(rawData.tier),
        image: rawData.image || "/placeholder-champion.svg",
        splash_art: rawData.image || "/placeholder-champion.svg",
      },
      stats: {
        damage: { base: rawData.stats?.damage || 0, per_level: 0 },
        toughness: { base: rawData.stats?.toughness || 0, per_level: 0 },
        utility: { base: rawData.stats?.utility || 0, per_level: 0 },
        difficulty: { base: rawData.stats?.difficulty || 0, per_level: 0 },
        attack_damage: {
          base: rawData.base_stats?.attack_damage || 60,
          per_level: 5,
        },
        health: { base: rawData.base_stats?.health || 600, per_level: 100 },
        health_regeneration: {
          base: rawData.base_stats?.health_regen || 6,
          per_level: 1,
        },
        attack_speed: {
          base: rawData.base_stats?.attack_speed || 0.7,
          per_level: 0.01,
        },
        mana: { base: rawData.base_stats?.mana || 300, per_level: 50 },
        mana_regeneration: {
          base: rawData.base_stats?.mana_regen || 8,
          per_level: 1,
        },
        movement_speed: {
          base: rawData.base_stats?.movement_speed || 350,
          per_level: 0,
        },
        armor: { base: rawData.base_stats?.armor || 35, per_level: 4 },
        magic_resistance: {
          base: rawData.base_stats?.magic_resist || 35,
          per_level: 2,
        },
        critical_strike: { base: 175, per_level: 0 },
      },
      abilities: {
        passive: this.transformAbility(rawData.abilities?.[0]),
        q: this.transformAbility(rawData.abilities?.[1]),
        w: this.transformAbility(rawData.abilities?.[2]),
        e: this.transformAbility(rawData.abilities?.[3]),
        r: this.transformAbility(rawData.abilities?.[4]),
      },
      builds: {
        lanes: rawData.lanes || ["Mid"],
        starting_items: firstBuild.start_items?.slice(0, 3) || [],
        core_items: firstBuild.core_items?.slice(0, 3) || [],
        boots: firstBuild.boots_enchants?.slice(0, 2) || [],
        situational_items:
          firstBuild.situational_items
            ?.slice(0, 2)
            .flatMap((cat: any) => cat.items?.slice(0, 2) || []) || [],
        situational: [],
        example_build: firstBuild.example_build?.slice(0, 4) || [],
        enchants: [],
        alternative_builds: [],
        lane_specific: {},
        core_items_detailed: [],
      },
      runes: {
        primary: {
          tree: "Domination",
          keystone: firstBuild.runes?.keystone || {
            name: "Electrocute",
            image: "",
            description: "",
          },
          runes: firstBuild.runes?.primary?.slice(0, 3) || [],
        },
        secondary: {
          tree: "Resolve",
          keystone: "",
          runes: firstBuild.runes?.secondary?.slice(0, 2) || [],
        },
        stat_shards: ["Adaptive Force", "Armor", "Magic Resist"],
      },
      summoner_spells: firstBuild.summoner_spells
        ?.slice(0, 2)
        .map((spell: any) => spell.name) || ["Flash", "Ignite"],
      counters: {
        strong_against: ["Squishy Champions", "Low Mobility Champions"],
        weak_against: ["Tanky Champions", "High Mobility Champions"],
      },
      tips: [
        "Focus on positioning in team fights",
        "Use abilities efficiently to maximize damage",
        "Ward key areas to avoid ganks",
      ],
      meta: {
        tier: this.mapTier(rawData.tier),
        win_rate: "52%",
        pick_rate: "8%",
        ban_rate: "Medium",
        patch: "6.1f",
        last_updated: new Date().toISOString().split("T")[0],
        views: "50,000",
      },
    };
  }

  private static transformAbility(abilityData: any): any {
    if (!abilityData) {
      return {
        name: "Unknown",
        key: "",
        type: "Active" as const,
        description: "",
        damage: [],
        scaling: "",
        damage_type: "Physical" as const,
        image: "",
        notes: [],
      };
    }

    return {
      name: abilityData.name || "Unknown",
      key: abilityData.key || "",
      type:
        abilityData.key === "P"
          ? ("Passive" as const)
          : abilityData.key === "R"
          ? ("Ultimate" as const)
          : ("Active" as const),
      description: abilityData.description?.slice(0, 200) + "..." || "", // Truncate long descriptions
      damage: [],
      scaling: "",
      damage_type: "Physical" as const,
      image: abilityData.image || "",
      notes: [],
    };
  }

  private static mapTier(tier: number): string {
    switch (tier) {
      case 1:
        return "S+";
      case 2:
        return "S";
      case 3:
        return "A";
      case 4:
        return "B";
      case 5:
        return "C";
      default:
        return "B";
    }
  }

  /**
   * Get all champion slugs for static paths
   */
  static getAllSlugs(): string[] {
    const index = this.buildIndex();
    return Object.keys(index);
  }

  /**
   * Clear cache (useful for development)
   */
  static clearCache(): void {
    this.cache.clear();
    this.index = null;
  }
}
