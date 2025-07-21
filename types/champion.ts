export interface ChampionStats {
  base: number;
  per_level: number;
}

export interface Ability {
  name: string;
  key: string;
  type: string;
  description: string;
  damage?: number[];
  scaling?: string | string[];
  damage_type: string;
  image: string;
  notes: string[];
  cooldown?: number;
  duration?: number;
  ad_bonus?: string[];
  healing_increase?: string[];
  movement_speed?: string[];
}

export interface Champion {
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

export interface ChampionData {
  champion: Champion;
  stats: Record<string, ChampionStats>;
  abilities: {
    passive: Ability;
    q: Ability;
    w: Ability;
    e: Ability;
    r: Ability;
  };
  builds: {
    core_items: string[];
    starting_items: string[];
    boots: string[];
    situational: string[];
  };
  runes: {
    primary: {
      tree: string;
      keystone: string;
      runes: string[];
    };
    secondary: {
      tree: string;
      runes: string[];
    };
  };
  summoner_spells: string[];
  counters: {
    strong_against: string[];
    weak_against: string[];
  };
  tips: string[];
  meta: {
    tier: string;
    win_rate: string;
    pick_rate: string;
    ban_rate: string;
    patch: string;
    last_updated: string;
    views: string;
  };
}
