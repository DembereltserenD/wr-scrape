import React from 'react';
import { useTranslation } from '../utils/i18n';
import { ChampionAbilities } from '../types/champion';

interface AbilitiesProps {
  abilities: ChampionAbilities;
}

const AbilitiesI18n: React.FC<AbilitiesProps> = ({ abilities }) => {
  const { t } = useTranslation();
  const abilityOrder = ['passive', 'q', 'w', 'e', 'r'] as const;

  const getAbilityTypeTranslation = (key: string) => {
    switch (key) {
      case 'P':
        return t('abilities.passive');
      case 'R':
        return t('abilities.ultimate');
      default:
        return t('abilities.active');
    }
  };

  return (
    <div className="space-y-6">
      <h3 className="text-2xl font-black mb-6 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent flex items-center">
        ⚡ {t('abilities.title')}
      </h3>
      <div className="space-y-4">
        {abilityOrder.map((abilityKey) => {
          const ability = abilities[abilityKey];
          if (!ability) return null;

          return (
            <div key={abilityKey} className="bg-black/40 rounded-xl border border-slate-600/50 p-4 hover:border-cyan-500/50 transition-all duration-300">
              <div className="flex items-start space-x-4">
                <div className="relative">
                  <img
                    src={ability.image}
                    alt={ability.name}
                    className="w-12 h-12 rounded-lg border-2 border-cyan-500/50 shadow-lg"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                      const fallback = target.nextElementSibling as HTMLElement;
                      if (fallback) fallback.style.display = 'flex';
                    }}
                  />
                  <div className="w-12 h-12 rounded-lg border-2 border-cyan-500/50 bg-gradient-to-br from-cyan-500 to-blue-600 hidden items-center justify-center text-white font-bold text-lg">
                    {ability.key}
                  </div>
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h4 className="font-bold text-lg text-white">{ability.name}</h4>
                    <span className="text-xs bg-cyan-500/20 text-cyan-300 px-2 py-1 rounded-full border border-cyan-500/30">
                      {getAbilityTypeTranslation(ability.key)}
                    </span>
                  </div>
                  <p className="text-gray-300 leading-relaxed text-sm">
                    {ability.description}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AbilitiesI18n;
