import React from 'react';
import { useTranslation } from '../utils/i18n';
import { Ability } from '../types/champion';

interface AbilitiesProps {
  abilities: {
    passive: Ability;
    q: Ability;
    w: Ability;
    e: Ability;
    r: Ability;
  };
}

const AbilitiesI18n: React.FC<AbilitiesProps> = ({ abilities }) => {
  const { t } = useTranslation();
  const abilityOrder = ['passive', 'q', 'w', 'e', 'r'] as const;

  const getAbilityKeyColor = (key: string) => {
    const colors = {
      P: 'bg-purple-500',
      Q: 'bg-green-500',
      W: 'bg-blue-500',
      E: 'bg-yellow-500',
      R: 'bg-red-500'
    };
    return colors[key as keyof typeof colors] || 'bg-gray-500';
  };

  const getAbilityTypeTranslation = (type: string) => {
    switch (type.toLowerCase()) {
      case 'passive':
        return t('abilities.passive');
      case 'ultimate':
        return t('abilities.ultimate');
      default:
        return t('abilities.active');
    }
  };

  const getDamageTypeTranslation = (damageType: string) => {
    const key = damageType.toLowerCase();
    return t(`abilities.damage_type.${key}`) || damageType;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold mb-4 text-gray-800">
        {t('abilities.title')}
      </h3>
      <div className="space-y-4">
        {abilityOrder.map((abilityKey) => {
          const ability = abilities[abilityKey];
          return (
            <div key={abilityKey} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold ${getAbilityKeyColor(ability.key)}`}>
                  {ability.key}
                </div>
                <div className="flex-1">
                  <h4 className="font-bold text-lg text-gray-800">{ability.name}</h4>
                  <p className="text-sm text-gray-600 mb-2">
                    {getAbilityTypeTranslation(ability.type)}
                    {ability.damage_type && (
                      <span className="ml-2 text-xs bg-gray-100 px-2 py-1 rounded">
                        {getDamageTypeTranslation(ability.damage_type)}
                      </span>
                    )}
                  </p>
                  <p className="text-gray-700 mb-3">{ability.description}</p>

                  {ability.damage && ability.damage.length > 0 && (
                    <div className="mb-2">
                      <span className="font-medium text-red-600">
                        {t('abilities.damage')}:
                      </span>
                      <span className="ml-1">{ability.damage.join(' / ')}</span>
                      {ability.scaling && (
                        <span className="text-orange-600 ml-1">
                          (+{Array.isArray(ability.scaling) ? ability.scaling.join(' / ') : ability.scaling})
                        </span>
                      )}
                    </div>
                  )}



                  {ability.notes && ability.notes.length > 0 && (
                    <div className="mt-3">
                      <h5 className="font-medium text-gray-700 mb-1">
                        {t('abilities.notes')}:
                      </h5>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {ability.notes.map((note, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-blue-500 mr-2">•</span>
                            {note}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
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
