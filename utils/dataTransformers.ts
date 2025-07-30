import { ChampionData, ChampionCard, Item, ItemCard } from "../types";

/**
 * Transform champion data for homepage display
 */
export class DataTransformers {
  /**
   * Transform full champion data to simplified card format
   */
  static championToCard(champion: ChampionData): ChampionCard {
    return {
      id: champion.champion?.id || "",
      name: champion.champion?.name || "Unknown",
      role: this.cleanRole(champion.champion?.role || ""),
      tier: champion.champion?.tier || "C",
      image: champion.champion?.image || "",
      lanes: champion.champion?.lanes || [],
      difficulty: champion.champion?.difficulty || "Medium",
      winRate: champion.meta?.win_rate,
      pickRate: champion.meta?.pick_rate,
    };
  }

  /**
   * Transform multiple champions to card format
   */
  static championsToCards(champions: ChampionData[]): ChampionCard[] {
    return champions.map((champion) => this.championToCard(champion));
  }

  /**
   * Transform item data to simplified card format
   */
  static itemToCard(item: Item): ItemCard {
    return {
      name: item.name,
      cost: item.cost,
      tier: item.tier,
      category: item.category,
      stats: item.stats,
      passive: item.passive || undefined,
    };
  }

  /**
   * Transform multiple items to card format
   */
  static itemsToCards(items: Item[]): ItemCard[] {
    return items.map((item) => this.itemToCard(item));
  }

  /**
   * Clean role text by removing HTML tags
   */
  static cleanRole(role: string): string {
    return role.replace(/<[^>]*>/g, "").trim();
  }

  /**
   * Get tier color for styling
   */
  static getTierColor(tier: string): string {
    switch (tier.toUpperCase()) {
      case "S":
        return "#ffd700"; // Gold
      case "A":
        return "#c0c0c0"; // Silver
      case "B":
        return "#cd7f32"; // Bronze
      case "C":
        return "#8b7355"; // Brown
      default:
        return "#ffffff"; // White
    }
  }

  /**
   * Get difficulty color for styling
   */
  static getDifficultyColor(difficulty: string): string {
    switch (difficulty.toLowerCase()) {
      case "low":
        return "#22c55e"; // Green
      case "medium":
        return "#f59e0b"; // Yellow
      case "high":
        return "#ef4444"; // Red
      default:
        return "#6b7280"; // Gray
    }
  }

  /**
   * Format cost with proper separators
   */
  static formatCost(cost: number): string {
    return cost.toLocaleString();
  }

  /**
   * Get stat display name
   */
  static getStatDisplayName(statKey: string): string {
    const statNames: Record<string, string> = {
      attack_damage: "AD",
      ability_power: "AP",
      attack_speed: "AS",
      critical_strike: "Crit",
      armor: "Armor",
      magic_resistance: "MR",
      health: "HP",
      mana: "Mana",
      ability_haste: "AH",
      movement_speed: "MS",
      life_steal: "Life Steal",
      omnivamp: "Omnivamp",
    };

    return statNames[statKey] || statKey.replace(/_/g, " ");
  }

  /**
   * Format stat value with proper suffix
   */
  static formatStatValue(value: number, type: "flat" | "percentage"): string {
    if (type === "percentage") {
      return `${value}%`;
    }
    return value.toString();
  }

  /**
   * Sort champions by tier and name
   */
  static sortChampionsByTier(champions: ChampionCard[]): ChampionCard[] {
    const tierOrder = { S: 0, A: 1, B: 2, C: 3 };

    return [...champions].sort((a, b) => {
      const tierA = tierOrder[a.tier as keyof typeof tierOrder] ?? 999;
      const tierB = tierOrder[b.tier as keyof typeof tierOrder] ?? 999;

      if (tierA !== tierB) {
        return tierA - tierB;
      }

      return a.name.localeCompare(b.name);
    });
  }

  /**
   * Sort items by tier and cost
   */
  static sortItemsByTier(items: ItemCard[]): ItemCard[] {
    const tierOrder = { S: 0, A: 1, B: 2, C: 3 };

    return [...items].sort((a, b) => {
      const tierA = tierOrder[a.tier as keyof typeof tierOrder] ?? 999;
      const tierB = tierOrder[b.tier as keyof typeof tierOrder] ?? 999;

      if (tierA !== tierB) {
        return tierA - tierB;
      }

      return b.cost - a.cost; // Higher cost first within same tier
    });
  }

  /**
   * Filter champions by role keywords
   */
  static filterChampionsByRole(
    champions: ChampionCard[],
    roleFilter: string
  ): ChampionCard[] {
    if (!roleFilter || roleFilter === "all") {
      return champions;
    }

    const roleKeywords: Record<string, string[]> = {
      tank: ["tank", "support"],
      fighter: ["fighter", "bruiser"],
      assassin: ["assassin"],
      mage: ["mage", "ap"],
      marksman: ["marksman", "adc", "ad carry"],
      support: ["support", "enchanter"],
    };

    const keywords = roleKeywords[roleFilter.toLowerCase()] || [
      roleFilter.toLowerCase(),
    ];

    return champions.filter((champion) =>
      keywords.some((keyword) => champion.role.toLowerCase().includes(keyword))
    );
  }

  /**
   * Get top champions by tier (for homepage display)
   */
  static getTopChampions(
    champions: ChampionCard[],
    limit: number = 12
  ): ChampionCard[] {
    const sorted = this.sortChampionsByTier(champions);
    return sorted.slice(0, limit);
  }

  /**
   * Get featured items (for homepage display)
   */
  static getFeaturedItems(items: ItemCard[], limit: number = 8): ItemCard[] {
    const sorted = this.sortItemsByTier(items);
    return sorted.slice(0, limit);
  }
}
