import React from 'react';
import { useTranslation } from '../utils/i18n';
import { ChampionBuilds, ChampionRunes } from '../types/champion';

interface BuildGuideProps {
  builds: ChampionBuilds;
  runes: ChampionRunes;
}

const BuildGuideI18n: React.FC<BuildGuideProps> = ({ builds, runes }) => {
  const { t } = useTranslation();

  const getRuneTreeTranslation = (tree: string) => {
    const key = tree.toLowerCase();
    return t(`runes.trees.${key}`) || tree;
  };

  const renderItem = (item: any, index: number, showNumber = false) => (
    <div key={index} className="flex items-center gap-3 bg-black/30 rounded-lg p-3 border border-slate-600/50 hover:border-cyan-500/50 transition-all duration-200">
      {showNumber && (
        <span className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold">
          {index + 1}
        </span>
      )}
      <div className="relative">
        <img
          src={item.image}
          alt={item.alt || item.name}
          className="w-10 h-10 rounded-lg border-2 border-cyan-500/50 shadow-lg"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.style.display = 'none';
            const fallback = target.nextElementSibling as HTMLElement;
            if (fallback) fallback.style.display = 'flex';
          }}
        />
        <div className="w-10 h-10 rounded-lg border-2 border-cyan-500/50 bg-gradient-to-br from-slate-600 to-slate-700 hidden items-center justify-center text-white font-bold text-xs">
          {item.name?.charAt(0)}
        </div>
      </div>
      <div className="flex-1">
        <h5 className="font-semibold text-white text-sm">{item.name}</h5>
        {item.cost && (
          <span className="text-yellow-400 text-xs">{item.cost}g</span>
        )}
      </div>
    </div>
  );

  const renderRune = (rune: any, index: number, isKeystone = false) => (
    <div key={index} className={`flex items-center gap-3 rounded-lg p-3 border transition-all duration-200 ${isKeystone
        ? 'bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border-yellow-500/50 hover:border-yellow-400/70'
        : 'bg-black/30 border-slate-600/50 hover:border-cyan-500/50'
      }`}>
      <div className="relative">
        <img
          src={rune.image}
          alt={rune.alt || rune.name}
          className="w-8 h-8 rounded-lg border-2 border-cyan-500/50 shadow-lg"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.style.display = 'none';
            const fallback = target.nextElementSibling as HTMLElement;
            if (fallback) fallback.style.display = 'flex';
          }}
        />
        <div className="w-8 h-8 rounded-lg border-2 border-cyan-500/50 bg-gradient-to-br from-slate-600 to-slate-700 hidden items-center justify-center text-white font-bold text-xs">
          {rune.name?.charAt(0)}
        </div>
      </div>
      <div className="flex-1">
        <h5 className={`font-semibold text-sm ${isKeystone ? 'text-yellow-300' : 'text-white'}`}>
          {rune.name}
          {isKeystone && <span className="text-xs text-yellow-500 ml-2">({t('runes.keystone')})</span>}
        </h5>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Items Build */}
      <div className="space-y-4">
        <h3 className="text-2xl font-black mb-6 bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent flex items-center">
          🛡️ {t('builds.title')}
        </h3>

        <div className="space-y-4">
          <div>
            <h4 className="font-bold text-green-300 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              {t('builds.starting_items')}
            </h4>
            <div className="space-y-2">
              {builds.starting_items.map((item, index) => renderItem(item, index))}
            </div>
          </div>

          <div>
            <h4 className="font-bold text-blue-300 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 bg-blue-400 rounded-full"></span>
              {t('builds.core_items')}
            </h4>
            <div className="space-y-2">
              {builds.core_items.map((item, index) => renderItem(item, index, true))}
            </div>
          </div>

          <div>
            <h4 className="font-bold text-yellow-300 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 bg-yellow-400 rounded-full"></span>
              {t('builds.boots')}
            </h4>
            <div className="space-y-2">
              {builds.boots.map((item, index) => renderItem(item, index))}
            </div>
          </div>
        </div>
      </div>

      {/* Runes */}
      <div className="space-y-4">
        <h3 className="text-2xl font-black mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent flex items-center">
          ⚡ {t('runes.title')}
        </h3>

        <div className="space-y-4">
          <div>
            <h4 className="font-bold text-purple-300 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 bg-purple-400 rounded-full"></span>
              {t('runes.primary')} ({getRuneTreeTranslation(runes.primary.tree)})
            </h4>
            <div className="space-y-2">
              {typeof runes.primary.keystone === 'object' && runes.primary.keystone.name &&
                renderRune(runes.primary.keystone, 0, true)
              }
              {runes.primary.runes.map((rune, index) => renderRune(rune, index))}
            </div>
          </div>

          <div>
            <h4 className="font-bold text-pink-300 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 bg-pink-400 rounded-full"></span>
              {t('runes.secondary')} ({getRuneTreeTranslation(runes.secondary.tree)})
            </h4>
            <div className="space-y-2">
              {runes.secondary.runes.map((rune, index) => renderRune(rune, index))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BuildGuideI18n;
