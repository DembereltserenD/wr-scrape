import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useLanguage } from "../contexts/LanguageContext";
import {
  ChampionData,
  ChampionCard as ChampionCardType,
} from "../types/champion";
import ChampionCard from "./ChampionCard";
import Dropdown, { DropdownOption } from "./UI/Dropdown";
import PatchInfo from "./PatchInfo";

interface ChampionsSectionProps {
  champions: ChampionData[];
  showPatchInfo?: boolean;
  maxDisplayed?: number;
}

const ChampionsSection: React.FC<ChampionsSectionProps> = ({
  champions,
  showPatchInfo = true,
  maxDisplayed = 8,
}) => {
  const { t, locale } = useLanguage();
  const [selectedLane, setSelectedLane] = useState<string>("all");
  const [filteredChampions, setFilteredChampions] = useState<
    ChampionCardType[]
  >([]);

  const convertToChampionCard = (
    championData: ChampionData,
  ): ChampionCardType | null => {
    if (!championData?.champion?.id || !championData?.champion?.name) {
      console.warn("Invalid champion data:", championData);
      return null;
    }

    return {
      id: championData.champion.id,
      name: championData.champion.name,
      role: championData.champion.role || "Unknown",
      tier: championData.champion.tier || "C",
      image: championData.champion.image || "/placeholder-champion.png",
      lanes: championData.champion.lanes || [],
      difficulty: championData.champion.difficulty || "Medium",
      winRate: championData.meta?.win_rate,
      pickRate: championData.meta?.pick_rate,
    };
  };

  const laneOptions: DropdownOption[] = [
    { value: "all", label: t("common.filter") },
    { value: "Baron", label: "Baron Lane" },
    { value: "Mid", label: "Mid Lane" },
    { value: "Jungle", label: "Jungle" },
    { value: "Dragon", label: "Dragon Lane (ADC)" },
    { value: "Support", label: "Support" },
  ];

  useEffect(() => {
    let filtered = champions
      .map(convertToChampionCard)
      .filter((champion): champion is ChampionCardType => champion !== null);

    if (selectedLane !== "all") {
      filtered = filtered.filter((champion) => {
        return champion.lanes.some(
          (lane) =>
            lane === selectedLane ||
            lane.toLowerCase().includes(selectedLane.toLowerCase()) ||
            (selectedLane === "Dragon" &&
              lane.toLowerCase().includes("dragon")) ||
            (selectedLane === "Baron" && lane.toLowerCase().includes("baron")),
        );
      });
    }

    filtered.sort((a, b) => a.name.localeCompare(b.name));

    if (maxDisplayed > 0) {
      filtered = filtered.slice(0, maxDisplayed);
    }

    setFilteredChampions(filtered);
  }, [champions, selectedLane, maxDisplayed]);

  return (
    <section className="bg-slate-800/30 backdrop-blur-sm rounded-2xl p-8 border border-slate-700/50">
      <div className="space-y-8">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                {t("sections.champions")}
              </h2>
              {showPatchInfo && <PatchInfo showLink={true} />}
            </div>
            {showPatchInfo && (
              <p className="text-gray-400 text-lg">
                {locale === "mn"
                  ? "Одоогийн мета дэх баатруудын зэрэглэл"
                  : "Current meta champion rankings"}
              </p>
            )}
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <div className="min-w-[200px]">
              <Dropdown
                options={laneOptions}
                value={selectedLane}
                onChange={setSelectedLane}
                placeholder="Filter by Lane"
              />
            </div>
            {selectedLane !== "all" && (
              <button
                onClick={() => setSelectedLane("all")}
                className="px-4 py-2 bg-red-600/20 text-red-400 border border-red-600/30 rounded-lg hover:bg-red-600/30 transition-colors duration-200"
              >
                {locale === "mn" ? "Цэвэрлэх" : "Clear Filter"}
              </button>
            )}
          </div>
        </div>

        {filteredChampions.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredChampions.map((champion) => (
              <ChampionCard key={champion.id} champion={champion} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 bg-slate-900/50 rounded-xl border border-slate-700/30">
            <p className="text-gray-400 text-lg">
              {locale === "mn"
                ? "Сонгосон lane-д тохирох баатар олдсонгүй."
                : "No champions found for the selected lane."}
            </p>
          </div>
        )}

        <div className="text-center pt-6">
          <Link
            href="/champions"
            className="group inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-blue-600/20 to-purple-600/20 text-blue-400 border border-blue-600/30 rounded-lg hover:bg-gradient-to-r hover:from-blue-600/30 hover:to-purple-600/30 hover:border-blue-500/50 transition-all duration-300 transform hover:scale-105"
          >
            <span className="font-semibold text-lg">
              {t("common.viewAll")} {t("sections.champions")}
            </span>
            <svg
              className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M17 8l4 4m0 0l-4 4m4-4H3"
              />
            </svg>
          </Link>
        </div>
      </div>
    </section>
  );
};

export default ChampionsSection;
