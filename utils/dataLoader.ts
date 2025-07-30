import fs from "fs";
import path from "path";
import { ChampionData } from "../types/champion";
import { Item } from "../types/item";

// Interface for the new scraped champion data format
interface ScrapedChampionData {
  name: string;
  roles: string[];
  image: string;
  tier: number;
  balance_status: string;
  stats: {
    damage: number;
    toughness: number;
    utility: number;
    difficulty: number;
  };
  base_stats: any;
  abilities: Array<{
    image: string;
    alt_text: string;
    key: string;
    description: string;
    name: string;
  }>;
  lanes: string[];
  builds: Array<{
    lane: string;
    start_items: any[];
    core_items: any[];
    boots_enchants: any[];
    example_build: any[];
    situational_items: Array<{
      purpose: string;
      items: any[];
      tips: string;
    }>;
    summoner_spells: any[];
    runes: {
      primary: any[];
      secondary: any[];
      keystone: any;
    };
    situational_runes: any[];
  }>;
  change_history: any[];
}

/**
 * Load champion data from JSON files
 */
export class ChampionDataLoader {
  private static championsPath = path.join(process.cwd(), "champions_clean");

  /**
   * Get all champion file names
   */
  static getChampionFiles(): string[] {
    try {
      const files = fs.readdirSync(this.championsPath);
      return files.filter((file) => file.endsWith(".json"));
    } catch (error) {
      console.error("Error reading champions directory:", error);
      return [];
    }
  }

  /**
   * Transform scraped champion data to our expected format
   */
  private static transformChampionData(
    scrapedData: ScrapedChampionData,
  ): ChampionData {
    const championName = scrapedData.name || "Unknown";
    const championId = championName.toLowerCase().replace(/[^a-z0-9]/g, "_");

    // Create URL-friendly slug
    const championSlug = championName
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "");

    // Get the first build for default data
    const firstBuild = scrapedData.builds?.[0] || {};

    return {
      champion: {
        id: championSlug, // Use URL-friendly slug as ID
        name: championName,
        title: championName, // Using name as title for now
        role: scrapedData.roles?.[0] || "Unknown",
        lanes: scrapedData.lanes || [],
        difficulty: this.mapDifficultyToString(
          scrapedData.stats?.difficulty || 50,
        ),
        tier: this.mapTierToString(scrapedData.tier || 3),
        image: scrapedData.image || "",
        splash_art: scrapedData.image || "",
      },
      stats: {
        // Map the actual stats from the JSON data
        damage: { base: scrapedData.stats?.damage || 0, per_level: 0 },
        toughness: { base: scrapedData.stats?.toughness || 0, per_level: 0 },
        utility: { base: scrapedData.stats?.utility || 0, per_level: 0 },
        difficulty: { base: scrapedData.stats?.difficulty || 0, per_level: 0 },
        // Keep space for base_stats that will be added later
        attack_damage: { base: 0, per_level: 0 },
        health: { base: 0, per_level: 0 },
        health_regeneration: { base: 0, per_level: 0 },
        attack_speed: { base: 0, per_level: 0 },
        mana: { base: 0, per_level: 0 },
        mana_regeneration: { base: 0, per_level: 0 },
        movement_speed: { base: 0, per_level: 0 },
        armor: { base: 0, per_level: 0 },
        magic_resistance: { base: 0, per_level: 0 },
        critical_strike: { base: 0, per_level: 0 },
      },
      abilities: {
        passive: this.transformAbility(
          scrapedData.abilities?.find((a) => a.key === "P"),
        ),
        q: this.transformAbility(
          scrapedData.abilities?.find((a) => a.key === "Q"),
        ),
        w: this.transformAbility(
          scrapedData.abilities?.find((a) => a.key === "W"),
        ),
        e: this.transformAbility(
          scrapedData.abilities?.find((a) => a.key === "E"),
        ),
        r: this.transformAbility(
          scrapedData.abilities?.find((a) => a.key === "R"),
        ),
      },
      builds: {
        lanes: scrapedData.lanes || [],
        starting_items:
          firstBuild.start_items?.map((item: any) => item.name) || [],
        core_items: firstBuild.core_items?.map((item: any) => item.name) || [],
        boots: [],
        situational_items:
          firstBuild.situational_items?.flatMap(
            (cat: any) => cat.items?.map((item: any) => item.name) || [],
          ) || [],
        situational:
          firstBuild.situational_items?.flatMap(
            (cat: any) => cat.items?.map((item: any) => item.name) || [],
          ) || [],
        example_build:
          firstBuild.example_build?.map((item: any) => item.name) || [],
        enchants:
          firstBuild.boots_enchants?.map((item: any) => item.name) || [],
        alternative_builds: [],
        lane_specific: {},
        core_items_detailed: [],
      },
      runes: {
        primary: {
          tree: "Unknown",
          keystone: firstBuild.runes?.keystone?.name || "Unknown",
          runes: firstBuild.runes?.primary?.map((rune: any) => rune.name) || [],
        },
        secondary: {
          tree: "Unknown",
          keystone: "",
          runes:
            firstBuild.runes?.secondary?.map((rune: any) => rune.name) || [],
        },
        stat_shards: [],
      },
      summoner_spells:
        firstBuild.summoner_spells?.map((spell: any) => spell.name) || [],
      counters: {
        strong_against: [],
        weak_against: [],
      },
      tips: [],
      meta: {
        tier: scrapedData.tier?.toString() || "3",
        win_rate: "50%",
        pick_rate: "5%",
        ban_rate: "2%",
        patch: "6.0",
        last_updated: new Date().toISOString(),
        views: "1000",
      },
    };
  }

  /**
   * Transform ability data
   */
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
      description: abilityData.description || "",
      damage: [],
      scaling: "",
      damage_type: "Physical" as const,
      image: abilityData.image || "",
      notes: [],
    };
  }

  /**
   * Map difficulty number to string
   */
  private static mapDifficultyToString(difficulty: number): string {
    if (difficulty <= 33) return "Low";
    if (difficulty <= 66) return "Medium";
    return "High";
  }

  /**
   * Map tier number to string
   */
  private static mapTierToString(tier: number): string {
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
   * Load a single champion's data
   */
  static loadChampion(filename: string): ChampionData | null {
    try {
      const filePath = path.join(this.championsPath, filename);
      const fileContent = fs.readFileSync(filePath, "utf-8");
      const scrapedData = JSON.parse(fileContent) as ScrapedChampionData;

      // Transform the scraped data to our expected format
      const championData = this.transformChampionData(scrapedData);

      return championData;
    } catch (error) {
      console.error(`Error loading champion ${filename}:`, error);
      return null;
    }
  }

  /**
   * Load champion by slug (URL-friendly identifier)
   */
  static loadChampionBySlug(slug: string): ChampionData | null {
    try {
      const files = this.getChampionFiles();

      for (const file of files) {
        const championData = this.loadChampion(file);
        if (championData && championData.champion.id === slug) {
          return championData;
        }
      }

      // If no exact match found, try to find by filename (fallback)
      const possibleFilename = `${slug}.json`;
      if (files.includes(possibleFilename)) {
        return this.loadChampion(possibleFilename);
      }

      return null;
    } catch (error) {
      console.error(`Error loading champion by slug ${slug}:`, error);
      return null;
    }
  }

  /**
   * Load all champions data
   */
  static loadAllChampions(): ChampionData[] {
    try {
      const files = this.getChampionFiles();
      const champions: ChampionData[] = [];

      for (const file of files) {
        const championData = this.loadChampion(file);
        if (championData) {
          champions.push(championData);
        }
      }

      // Filter and validate champions with comprehensive checks
      const validChampions = champions.filter((champion) => {
        if (!champion || !champion.champion) {
          console.warn(`Champion data missing basic structure`);
          return false;
        }

        const basic = champion.champion;
        const isValid =
          basic.id &&
          basic.name &&
          basic.role &&
          basic.tier &&
          basic.image &&
          Array.isArray(basic.lanes) &&
          basic.difficulty;

        if (!isValid) {
          console.warn(
            `Filtering out invalid champion: ${basic?.name || "unknown"}`,
          );
          console.warn(`Missing fields:`, {
            id: !basic.id,
            name: !basic.name,
            role: !basic.role,
            tier: !basic.tier,
            image: !basic.image,
            lanes: !Array.isArray(basic.lanes),
            difficulty: !basic.difficulty,
          });
        }

        return isValid;
      });

      console.log(
        `Loaded ${validChampions.length} valid champions out of ${champions.length} total`,
      );
      return validChampions;
    } catch (error) {
      console.error("Error in loadAllChampions:", error);
      return [];
    }
  }

  /**
   * Load champions by tier
   */
  static loadChampionsByTier(tier: string): ChampionData[] {
    const allChampions = this.loadAllChampions();
    return allChampions.filter(
      (champion) =>
        champion.champion?.tier?.toLowerCase() === tier.toLowerCase(),
    );
  }

  /**
   * Load champions by role
   */
  static loadChampionsByRole(role: string): ChampionData[] {
    const allChampions = this.loadAllChampions();
    return allChampions.filter((champion) =>
      champion.champion?.role?.toLowerCase().includes(role.toLowerCase()),
    );
  }

  /**
   * Search champions by name
   */
  static searchChampions(query: string): ChampionData[] {
    const allChampions = this.loadAllChampions();
    const lowerQuery = query.toLowerCase();

    return allChampions.filter(
      (champion) =>
        champion.champion?.name?.toLowerCase().includes(lowerQuery) ||
        champion.champion?.role?.toLowerCase().includes(lowerQuery),
    );
  }
}

/**
 * Load item data from JSON files
 */
export class ItemDataLoader {
  private static itemsPath = path.join(process.cwd(), "items");

  /**
   * Get all item file names
   */
  static getItemFiles(): string[] {
    try {
      const files = fs.readdirSync(this.itemsPath);
      return files.filter((file) => file.endsWith(".json"));
    } catch (error) {
      console.error("Error reading items directory:", error);
      return [];
    }
  }

  /**
   * Load a single item's data
   */
  static loadItem(filename: string): Item | null {
    try {
      const filePath = path.join(this.itemsPath, filename);
      const fileContent = fs.readFileSync(filePath, "utf-8");
      return JSON.parse(fileContent) as Item;
    } catch (error) {
      console.error(`Error loading item ${filename}:`, error);
      return null;
    }
  }

  /**
   * Load all items data
   */
  static loadAllItems(): Item[] {
    const files = this.getItemFiles();
    const items: Item[] = [];

    for (const file of files) {
      const itemData = this.loadItem(file);
      if (itemData) {
        items.push(itemData);
      }
    }

    return items;
  }

  /**
   * Load items by category
   */
  static loadItemsByCategory(category: string): Item[] {
    const allItems = this.loadAllItems();
    return allItems.filter(
      (item) => item.category.toLowerCase() === category.toLowerCase(),
    );
  }

  /**
   * Load items by tier
   */
  static loadItemsByTier(tier: string): Item[] {
    const allItems = this.loadAllItems();
    return allItems.filter(
      (item) => item.tier.toLowerCase() === tier.toLowerCase(),
    );
  }

  /**
   * Search items by name
   */
  static searchItems(query: string): Item[] {
    const allItems = this.loadAllItems();
    const lowerQuery = query.toLowerCase();

    return allItems.filter(
      (item) =>
        item.name.toLowerCase().includes(lowerQuery) ||
        item.tags?.some((tag) => tag.toLowerCase().includes(lowerQuery)),
    );
  }
}
