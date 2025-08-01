import React from "react";
import { ChampionData } from "../../types/champion";
import LazyImage from "../LazyImage";

interface ChampionHeroProps {
  championData: ChampionData;
  t: (key: string) => string;
  getTierColor: (tier: string) => string;
  getRoleTranslation: (role: string) => string;
  getDifficultyTranslation: (difficulty: string) => string;
}

const ChampionHero: React.FC<ChampionHeroProps> = ({
  championData,
  t,
  getTierColor,
  getRoleTranslation,
  getDifficultyTranslation,
}) => {
  return (
    <div className="relative z-10 bg-gradient-to-br from-slate-900/95 via-purple-900/40 to-blue-900/40 border-b border-slate-600/30 backdrop-blur-sm">
      <div className="px-4 py-20">
        <div className="flex flex-col md:flex-row items-center md:items-start space-y-8 md:space-y-0 md:space-x-12">
          <div className="relative group">
            <div className="absolute -inset-2 bg-gradient-to-r from-yellow-400 via-purple-500 to-cyan-400 rounded-full blur-lg opacity-60 group-hover:opacity-90 transition duration-700 animate-pulse"></div>
            <div className="absolute -inset-1 bg-gradient-to-r from-yellow-300 to-purple-400 rounded-full blur opacity-40 group-hover:opacity-70 transition duration-500"></div>
            <LazyImage
              src={championData.champion.image}
              alt={championData.champion.name}
              className="relative w-36 h-36 md:w-48 md:h-48 rounded-full border-4 border-yellow-400/80 shadow-2xl object-cover transform group-hover:scale-110 transition-all duration-500 ring-4 ring-purple-500/30"
            />
          </div>
          <div className="text-center md:text-left flex-1">
            <div className="mb-4">
              <h1 className="text-6xl md:text-7xl font-black bg-gradient-to-r from-yellow-300 via-yellow-200 to-amber-300 bg-clip-text text-transparent drop-shadow-2xl mb-3 tracking-tight">
                {championData.champion.name}
              </h1>
              <div className="h-1 w-24 bg-gradient-to-r from-yellow-400 to-purple-500 rounded-full mx-auto md:mx-0 mb-4"></div>
            </div>
            <p className="text-2xl md:text-3xl text-gray-100 font-bold mb-8 drop-shadow-lg tracking-wide">
              {championData.champion.title}
            </p>
            <div className="flex flex-wrap justify-center md:justify-start items-center gap-4">
              <span className="bg-gradient-to-r from-purple-600 via-purple-700 to-purple-800 text-yellow-200 px-6 py-3 rounded-xl text-base font-bold border border-purple-400/60 shadow-xl transform hover:scale-110 transition-all duration-300 backdrop-blur-sm">
                🎯 {getRoleTranslation(championData.champion.role)}
              </span>
              <span
                className={`text-black px-6 py-3 rounded-xl text-base font-black border-2 border-yellow-300 shadow-xl transform hover:scale-110 transition-all duration-300 ${getTierColor(championData.meta.tier)}`}
              >
                ⭐ {t("champion.tier")} {championData.meta.tier}
              </span>
              <span className="bg-gradient-to-r from-cyan-600 via-blue-600 to-blue-700 text-white px-6 py-3 rounded-xl text-base font-bold border border-cyan-400/60 shadow-xl transform hover:scale-110 transition-all duration-300 backdrop-blur-sm">
                📊 {getDifficultyTranslation(championData.champion.difficulty)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChampionHero;
