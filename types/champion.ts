// Champion data type definitions

export interface ChampionBasicInfo {
  id: string;
  name: string;
  title: string;
  role: string;
  lanes: string[];
  difficulty: string;
  tier: string;
  image: string;
  splash_art: string;
}

export interface StatValue {
  base: number;
  per_level: number;
}

export interface ChampionStats {
  attack_damage: StatValue;
  health: StatValue;
  health_regeneration: StatValue;
  attack_speed: StatValue;
  mana: StatValue;
  mana_regeneration: StatValue;
  movement_speed: StatValue;
  armor: StatValue;
  magic_resistance: StatValue;
  critical_strike: StatValue;
  // Champion performance stats
  damage?: StatValue;
  toughness?: StatValue;
  utility?: StatValue;
  difficulty?: StatValue;
}

export interface Ability {
  name: string;
  key: string;
  type: "Passive" | "Active" | "Ultimate";
  description: string;
  damage: number[];
  scaling: string;
  damage_type: "Physical" | "Magic" | "True";
  image: string;
  notes: string[];
}

export interface ChampionAbilities {
  passive: Ability;
  q: Ability;
  w: Ability;
  e: Ability;
  r: Ability;
}

export interface ChampionItem {
  name: string;
  image?: string;
  alt?: string;
  description?: string;
  cost?: number;
  stats?: Record<string, any>;
  passive?: string;
  active?: string;
  category?: string;
  tier?: string;
}

export interface AlternativeBuild {
  lane: string;
  core_items: string[];
  description: string;
}

export interface ChampionBuilds {
  lanes: string[];
  starting_items: ChampionItem[];
  core_items: ChampionItem[];
  boots: ChampionItem[];
  situational_items: ChampionItem[];
  situational: string[]; // For compatibility with BuildGuideI18n component
  example_build: ChampionItem[];
  enchants: string[];
  alternative_builds: AlternativeBuild[];
  lane_specific: Record<string, any>;
  core_items_detailed: ChampionItem[];
}

export interface Rune {
  name: string;
  image?: string;
  alt?: string;
  description?: string;
}

export interface RuneTree {
  tree: string;
  keystone: Rune | string;
  runes: Rune[];
}

export interface ChampionRunes {
  primary: RuneTree;
  secondary: RuneTree;
  stat_shards: string[];
}

export interface ChampionCounters {
  strong_against: string[];
  weak_against: string[];
}

export interface ChampionMeta {
  tier: string;
  win_rate: string;
  pick_rate: string;
  ban_rate: string;
  patch: string;
  last_updated: string;
  views: string;
}

export interface ChampionData {
  champion: ChampionBasicInfo;
  stats: ChampionStats;
  abilities: ChampionAbilities;
  builds: ChampionBuilds;
  runes: ChampionRunes;
  summoner_spells: string[];
  counters: ChampionCounters;
  tips: string[];
  meta: ChampionMeta;
}

// Simplified interface for homepage display
export interface ChampionCard {
  id: string;
  name: string;
  role: string;
  tier: string;
  image: string;
  lanes: string[];
  difficulty: string;
  winRate?: string;
  pickRate?: string;
}
