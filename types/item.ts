// Item data type definitions

export interface ItemStat {
  value: number;
  type: "flat" | "percentage";
}

export interface ItemStats {
  [statName: string]: ItemStat;
}

export interface Item {
  name: string;
  stats: ItemStats;
  cost: number;
  passive: string;
  active: string;
  description: string;
  category: "legendary" | "mythic" | "basic" | "boots" | "enchant";
  tier: "S" | "A" | "B" | "C";
  build_path?: string[];
  tags?: string[];
  tips?: string[];
}

// Simplified interface for homepage display
export interface ItemCard {
  name: string;
  cost: number;
  tier: string;
  category: string;
  image?: string;
  stats: ItemStats;
  passive?: string;
}
