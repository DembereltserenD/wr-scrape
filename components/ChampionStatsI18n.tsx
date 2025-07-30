import React from 'react';
import { useTranslation, formatNumber } from '../utils/i18n';
import { ChampionStats, StatValue } from '../types/champion';

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
      attack_damage: 'text-red-600',
      health: 'text-green-600',
      armor: 'text-yellow-600',
      magic_resistance: 'text-blue-600',
      movement_speed: 'text-purple-600',
      attack_speed: 'text-orange-600',
    };
    return colorMap[statName] || 'text-gray-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold mb-4 text-gray-800">
        {t('stats.title')}
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {Object.entries(stats).map(([key, stat]) => (
          <div key={key} className="bg-gray-50 p-3 rounded-md">
            <div className="text-sm font-medium text-gray-600">
              {formatStatName(key)}
            </div>
            <div className={`text-lg font-bold ${getStatColor(key)}`}>
              {formatNumber(stat.base, locale)}
            </div>
            {stat.per_level > 0 && (
              <div className="text-xs text-gray-500">
                +{formatNumber(stat.per_level, locale)} {t('stats.per_level')}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChampionStatsI18n;
