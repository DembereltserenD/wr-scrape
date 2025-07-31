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
        <div className="relative z-10 bg-gradient-to-r from-slate-800/90 via-purple-900/30 to-blue-900/30 border-b border-slate-600/30">
            <div className="container mx-auto px-4 py-16">
                <div className="flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-8">
                    <div className="relative group">
                        <div className="absolute -inset-1 bg-gradient-to-r from-yellow-400 via-purple-500 to-blue-500 rounded-full blur opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200 animate-pulse"></div>
                        <LazyImage
                            src={championData.champion.image}
                            alt={championData.champion.name}
                            className="relative w-32 h-32 md:w-40 md:h-40 rounded-full border-4 border-yellow-400 shadow-2xl object-cover transform group-hover:scale-105 transition-transform duration-300"
                        />
                    </div>
                    <div className="text-center md:text-left flex-1">
                        <h1 className="text-5xl md:text-6xl font-black bg-gradient-to-r from-yellow-400 via-yellow-300 to-yellow-500 bg-clip-text text-transparent drop-shadow-2xl mb-2">
                            {championData.champion.name}
                        </h1>
                        <p className="text-2xl md:text-3xl text-gray-200 font-semibold mb-6 drop-shadow-lg">
                            {championData.champion.title}
                        </p>
                        <div className="flex flex-wrap justify-center md:justify-start items-center gap-3">
                            <span className="bg-gradient-to-r from-purple-600 to-purple-800 text-yellow-300 px-4 py-2 rounded-lg text-sm font-bold border border-purple-400/50 shadow-lg transform hover:scale-105 transition-transform">
                                🎯 {getRoleTranslation(championData.champion.role)}
                            </span>
                            <span
                                className={`text-black px-4 py-2 rounded-lg text-sm font-black border-2 border-yellow-400 shadow-lg transform hover:scale-105 transition-transform ${getTierColor(championData.meta.tier)}`}
                            >
                                ⭐ {t("champion.tier")} {championData.meta.tier}
                            </span>
                            <span className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-4 py-2 rounded-lg text-sm font-bold border border-blue-400/50 shadow-lg transform hover:scale-105 transition-transform">
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