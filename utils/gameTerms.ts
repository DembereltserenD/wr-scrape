// Game terminology that should remain in English regardless of UI language

export interface GameStat {
  key: string;
  displayName: string;
  color: string;
  bgColor: string;
  abbreviation?: string;
}

// Game stats that always remain in English
export const GAME_STATS: Record<string, GameStat> = {
  HP: {
    key: "HP",
    displayName: "Health",
    color: "text-green-600",
    bgColor: "bg-green-100 text-green-800",
    abbreviation: "HP",
  },
  HEALTH: {
    key: "HEALTH",
    displayName: "Health",
    color: "text-green-600",
    bgColor: "bg-green-100 text-green-800",
  },
  AP: {
    key: "AP",
    displayName: "Ability Power",
    color: "text-blue-600",
    bgColor: "bg-blue-100 text-blue-800",
    abbreviation: "AP",
  },
  ABILITY_POWER: {
    key: "ABILITY_POWER",
    displayName: "Ability Power",
    color: "text-blue-600",
    bgColor: "bg-blue-100 text-blue-800",
  },
  AD: {
    key: "AD",
    displayName: "Attack Damage",
    color: "text-red-600",
    bgColor: "bg-red-100 text-red-800",
    abbreviation: "AD",
  },
  ATTACK_DAMAGE: {
    key: "ATTACK_DAMAGE",
    displayName: "Attack Damage",
    color: "text-red-600",
    bgColor: "bg-red-100 text-red-800",
  },
  MP: {
    key: "MP",
    displayName: "Mana",
    color: "text-blue-400",
    bgColor: "bg-blue-50 text-blue-600",
    abbreviation: "MP",
  },
  MANA: {
    key: "MANA",
    displayName: "Mana",
    color: "text-blue-400",
    bgColor: "bg-blue-50 text-blue-600",
  },
  ARMOR: {
    key: "ARMOR",
    displayName: "Armor",
    color: "text-yellow-600",
    bgColor: "bg-yellow-100 text-yellow-800",
  },
  MAGIC_RESISTANCE: {
    key: "MAGIC_RESISTANCE",
    displayName: "Magic Resistance",
    color: "text-purple-600",
    bgColor: "bg-purple-100 text-purple-800",
  },
  MOVEMENT_SPEED: {
    key: "MOVEMENT_SPEED",
    displayName: "Movement Speed",
    color: "text-gray-600",
    bgColor: "bg-gray-100 text-gray-800",
  },
  ATTACK_SPEED: {
    key: "ATTACK_SPEED",
    displayName: "Attack Speed",
    color: "text-orange-600",
    bgColor: "bg-orange-100 text-orange-800",
  },
  CRITICAL_STRIKE: {
    key: "CRITICAL_STRIKE",
    displayName: "Critical Strike",
    color: "text-yellow-500",
    bgColor: "bg-yellow-50 text-yellow-700",
  },
  LIFE_STEAL: {
    key: "LIFE_STEAL",
    displayName: "Life Steal",
    color: "text-red-400",
    bgColor: "bg-red-50 text-red-600",
  },
  SPELL_VAMP: {
    key: "SPELL_VAMP",
    displayName: "Spell Vamp",
    color: "text-purple-400",
    bgColor: "bg-purple-50 text-purple-600",
  },
  TRUE_DAMAGE: {
    key: "TRUE_DAMAGE",
    displayName: "True Damage",
    color: "text-white",
    bgColor: "bg-gray-800 text-white",
  },
  PHYSICAL_DAMAGE: {
    key: "PHYSICAL_DAMAGE",
    displayName: "Physical Damage",
    color: "text-red-500",
    bgColor: "bg-red-100 text-red-700",
  },
  MAGIC_DAMAGE: {
    key: "MAGIC_DAMAGE",
    displayName: "Magic Damage",
    color: "text-blue-500",
    bgColor: "bg-blue-100 text-blue-700",
  },
  COOLDOWN_REDUCTION: {
    key: "COOLDOWN_REDUCTION",
    displayName: "Cooldown Reduction",
    color: "text-cyan-600",
    bgColor: "bg-cyan-100 text-cyan-800",
  },
  ARMOR_PENETRATION: {
    key: "ARMOR_PENETRATION",
    displayName: "Armor Penetration",
    color: "text-yellow-700",
    bgColor: "bg-yellow-200 text-yellow-900",
  },
  MAGIC_PENETRATION: {
    key: "MAGIC_PENETRATION",
    displayName: "Magic Penetration",
    color: "text-purple-700",
    bgColor: "bg-purple-200 text-purple-900",
  },
};

// Game terms that should never be translated
export const GAME_TERMS = {
  // Ability types
  PASSIVE: "Passive",
  ACTIVE: "Active",
  ULTIMATE: "Ultimate",

  // Damage types
  TRUE_DAMAGE: "True Damage",
  PHYSICAL_DAMAGE: "Physical Damage",
  MAGIC_DAMAGE: "Magic Damage",

  // Game mechanics
  STACK: "Stack",
  COOLDOWN: "Cooldown",
  DURATION: "Duration",
  RANGE: "Range",
  COST: "Cost",

  // Common abbreviations
  CDR: "CDR",
  MS: "MS",
  AS: "AS",
  MR: "MR",
};

// Tier colors
export const TIER_COLORS = {
  "S+": "bg-gradient-to-r from-red-500 to-pink-500 text-white",
  S: "bg-red-500 text-white",
  A: "bg-orange-500 text-white",
  B: "bg-yellow-500 text-white",
  C: "bg-green-500 text-white",
  D: "bg-blue-500 text-white",
};

// Helper functions
export const getStatColor = (statKey: string): string => {
  const stat = GAME_STATS[statKey.toUpperCase()];
  return stat?.color || "text-gray-600";
};

export const getStatBgColor = (statKey: string): string => {
  const stat = GAME_STATS[statKey.toUpperCase()];
  return stat?.bgColor || "bg-gray-100 text-gray-800";
};

export const getTierColor = (tier: string): string => {
  return (
    TIER_COLORS[tier as keyof typeof TIER_COLORS] || "bg-gray-500 text-white"
  );
};

export const isGameTerm = (term: string): boolean => {
  const upperTerm = term.toUpperCase();
  return (
    Object.keys(GAME_STATS).includes(upperTerm) ||
    Object.values(GAME_TERMS).includes(term) ||
    Object.keys(TIER_COLORS).includes(term)
  );
};

// Format stat display with proper styling
export const formatStatDisplay = (
  statKey: string,
  value: number | string,
  showAbbreviation = false
): {
  displayText: string;
  colorClass: string;
  bgColorClass: string;
} => {
  const stat = GAME_STATS[statKey.toUpperCase()];

  if (!stat) {
    return {
      displayText: `${value} ${statKey}`,
      colorClass: "text-gray-600",
      bgColorClass: "bg-gray-100 text-gray-800",
    };
  }

  const displayName =
    showAbbreviation && stat.abbreviation
      ? stat.abbreviation
      : stat.displayName;

  return {
    displayText: `${value} ${displayName}`,
    colorClass: stat.color,
    bgColorClass: stat.bgColor,
  };
};

// Champion names that should remain in English
export const CHAMPION_NAMES_ENGLISH = true;

// Item names that should remain in English
export const ITEM_NAMES_ENGLISH = true;

// Rune names that should remain in English
export const RUNE_NAMES_ENGLISH = true;
