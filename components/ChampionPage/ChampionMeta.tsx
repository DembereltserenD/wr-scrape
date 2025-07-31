import React from "react";
import { ChampionData } from "../../types/champion";

interface ChampionMetaProps {
    championData: ChampionData;
    t: (key: string) => string;
}

const ChampionMeta: React.FC<ChampionMetaProps> = ({ championData, t }) => {
    return (
        <div className="bg-slate-800/90 rounded-2xl border border-slate-600/50 p-1 shadow-2xl hover:border-slate-500/70 transition-all duration-300">
            <div className="bg-gradient-to-br from-slate-700/60 to-slate-800/60 rounded-xl p-6">
                <h3 className="text-2xl font-black mb-6 bg-gradient-to-r from-yellow-400 to-yellow-300 bg-clip-text text-transparent flex items-center">
                    📈 {t("meta.title")}
                </h3>
                <div className="space-y-4">
                    <div className="flex justify-between items-center p-3 bg-black/30 rounded-lg border border-green-500/30">
                        <span className="text-gray-200 font-semibold flex items-center">
                            🏆 {t("champion.win_rate")}:
                        </span>
                        <span className="font-black text-green-400 text-lg">
                            {championData.meta.win_rate}
                        </span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-black/30 rounded-lg border border-blue-500/30">
                        <span className="text-gray-200 font-semibold flex items-center">
                            📊 {t("champion.pick_rate")}:
                        </span>
                        <span className="font-black text-blue-400 text-lg">
                            {championData.meta.pick_rate}
                        </span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-black/30 rounded-lg border border-purple-500/30">
                        <span className="text-gray-200 font-semibold flex items-center">
                            🔄 {t("champion.patch")}:
                        </span>
                        <span className="font-black text-purple-400 text-lg">
                            {championData.meta.patch}
                        </span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-black/30 rounded-lg border border-yellow-500/30">
                        <span className="text-gray-200 font-semibold flex items-center">
                            👁️ {t("champion.views")}:
                        </span>
                        <span className="font-black text-yellow-400 text-lg">
                            {championData.meta.views}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChampionMeta;