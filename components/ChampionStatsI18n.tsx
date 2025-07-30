import React from "react";
import { useTranslation, formatNumber } from "../utils/i18n";
import { ChampionStats, StatValue } from "../types/champion";

interface ChampionStatsProps {
  stats: ChampionStats;
}

const ChampionStatsI18n: React.FC<ChampionStatsProps> = ({ stats }) => {
  const { t, locale } = useTranslation();

  const formatStatName = (key: string) => {
    return t(`stats.${key}`);
  };

  const getStatColor = (statName: string): string => {
    const colorMap: Record<string, string> = {
      damage: "text-red-600",
      toughness: "text-green-600",
      utility: "text-blue-600",
      difficulty: "text-purple-600",
      attack_damage: "text-red-600",
      health: "text-green-600",
      armor: "text-yellow-600",
      magic_resistance: "text-blue-600",
      movement_speed: "text-purple-600",
      attack_speed: "text-orange-600",
    };
    return colorMap[statName] || "text-gray-600";
  };

  // Separate champion stats from base stats
  const championStats = ["damage", "toughness", "utility", "difficulty"];
  const baseStats = Object.keys(stats).filter(
    (key) => !championStats.includes(key),
  );

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
      <h3 className="text-xl font-bold mb-4 text-white">{t("stats.title")}</h3>

      {/* Champion Performance Stats */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold mb-3 text-gray-300">
          Champion Performance
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {championStats.map((key) => {
            const stat = stats[key as keyof ChampionStats];
            if (!stat) return null;
            return (
              <div
                key={key}
                className="bg-slate-700/50 p-3 rounded-md border border-slate-600/50"
              >
                <div className="text-sm font-medium text-gray-300">
                  {formatStatName(key)}
                </div>
                <div className={`text-lg font-bold ${getStatColor(key)}`}>
                  {formatNumber(stat.base, locale)}
                </div>
                {stat.per_level > 0 && (
                  <div className="text-xs text-gray-400">
                    +{formatNumber(stat.per_level, locale)}{" "}
                    {t("stats.per_level")}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Base Stats - Space reserved for future implementation */}
      <div>
        <h4 className="text-lg font-semibold mb-3 text-gray-300">
          Base Stats (Coming Soon)
        </h4>
        <div className="bg-slate-700/30 p-4 rounded-md border border-slate-600/30">
          <p className="text-gray-400 text-sm italic">
            Base stats like attack damage, health, armor, etc. will be displayed
            here once available.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChampionStatsI18n;
