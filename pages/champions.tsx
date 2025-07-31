import React, { useState, useEffect } from "react";
import { GetStaticProps } from "next";
import { useLanguage } from "../contexts/LanguageContext";
import { Layout } from "../components/Layout";
import ErrorBoundary from "../components/ErrorBoundary";
import SEOHead from "../components/SEO/SEOHead";
import { ChampionDataLoader } from "../utils/dataLoader";
import {
  ChampionData,
  ChampionCard as ChampionCardType,
} from "../types/champion";
import ChampionCard from "../components/ChampionCard";
import Dropdown, { DropdownOption } from "../components/UI/Dropdown";
import PatchInfo from "../components/PatchInfo";

interface ChampionsPageProps {
  champions: ChampionData[];
}

const ChampionsPageContent: React.FC<ChampionsPageProps> = ({ champions }) => {
  const { t, locale } = useLanguage();
  const [selectedLane, setSelectedLane] = useState<string>("all");
  const [selectedTier, setSelectedTier] = useState<string>("all");
  const [selectedRole, setSelectedRole] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
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

  const tierOptions: DropdownOption[] = [
    { value: "all", label: "All Tiers" },
    { value: "S+", label: "S+ Tier" },
    { value: "S", label: "S Tier" },
    { value: "A", label: "A Tier" },
    { value: "B", label: "B Tier" },
    { value: "C", label: "C Tier" },
    { value: "D", label: "D Tier" },
  ];

  const roleOptions: DropdownOption[] = [
    { value: "all", label: "All Roles" },
    { value: "Tank", label: "Tank" },
    { value: "Fighter", label: "Fighter" },
    { value: "Assassin", label: "Assassin" },
    { value: "Mage", label: "Mage" },
    { value: "Marksman", label: "Marksman" },
    { value: "Support", label: "Support" },
  ];

  useEffect(() => {
    let filtered = champions
      .map(convertToChampionCard)
      .filter((champion): champion is ChampionCardType => champion !== null);

    // Filter by search query
    if (searchQuery.trim()) {
      filtered = filtered.filter((champion) =>
        champion.name.toLowerCase().includes(searchQuery.toLowerCase()),
      );
    }

    // Filter by lane
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

    // Filter by tier
    if (selectedTier !== "all") {
      filtered = filtered.filter((champion) => champion.tier === selectedTier);
    }

    // Filter by role
    if (selectedRole !== "all") {
      filtered = filtered.filter((champion) =>
        champion.role.toLowerCase().includes(selectedRole.toLowerCase()),
      );
    }

    // Sort by tier first, then by name
    const tierOrder = { "S+": 0, S: 1, A: 2, B: 3, C: 4, D: 5 };
    filtered.sort((a, b) => {
      const tierA = tierOrder[a.tier as keyof typeof tierOrder] ?? 999;
      const tierB = tierOrder[b.tier as keyof typeof tierOrder] ?? 999;

      if (tierA !== tierB) {
        return tierA - tierB;
      }

      return a.name.localeCompare(b.name);
    });

    setFilteredChampions(filtered);
  }, [champions, selectedLane, selectedTier, selectedRole, searchQuery]);

  const clearAllFilters = () => {
    setSelectedLane("all");
    setSelectedTier("all");
    setSelectedRole("all");
    setSearchQuery("");
  };

  const hasActiveFilters =
    selectedLane !== "all" ||
    selectedTier !== "all" ||
    selectedRole !== "all" ||
    searchQuery.trim();

  return (
    <Layout currentPage="/champions">
      <SEOHead
        title={`Wild Rift ${t("navigation.champions")} - Complete Champion Guide`}
        description={`Comprehensive Wild Rift champion guide with tier lists, builds, and strategies. Find the best champions for each lane and role.`}
        keywords={`Wild Rift champions, League of Legends champions, tier list, champion builds, champion guides, meta champions`}
        url="https://wildriftguide.com/champions"
        image="https://wildriftguide.com/og-champions.jpg"
        type="website"
      />

      {/* Hero Header Section */}
      <div className="w-full bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center space-y-6">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold">
              <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                {t("navigation.champions")}
              </span>
            </h1>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              {locale === "mn"
                ? "Wild Rift-ийн бүх баатруудын дэлгэрэнгүй мэдээлэл, зэрэглэл, болон стратеги"
                : "Complete champion guide with tier lists, builds, and strategies for Wild Rift"}
            </p>
            <div className="inline-flex items-center px-6 py-3 bg-black/40 backdrop-blur-sm rounded-full border border-gray-700 hover:bg-black/60 hover:border-gray-600 transition-all duration-200 cursor-pointer group">
              <div className="flex items-center space-x-2 text-gray-300 group-hover:text-white">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <PatchInfo
                  showLink={true}
                  className="text-sm font-medium text-gray-300 group-hover:text-white transition-colors duration-200"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="w-full bg-gradient-to-b from-slate-900 to-black min-h-screen">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <ErrorBoundary
            fallback={
              <div className="bg-slate-800/50 rounded-xl p-8 text-center">
                <h2 className="text-xl font-bold text-red-400 mb-2">
                  Champions Section Error
                </h2>
                <p className="text-gray-400">
                  Champions data could not be loaded.
                </p>
              </div>
            }
          >
            <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl p-8 border border-slate-700/50">
              {/* Filters Section */}
              <div className="space-y-6 mb-8">
                {/* Search Bar */}
                <div className="max-w-md mx-auto">
                  <div className="relative">
                    <input
                      type="text"
                      placeholder={
                        locale === "mn"
                          ? "Баатар хайх..."
                          : "Search champions..."
                      }
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full px-4 py-3 pl-12 bg-slate-700/50 border border-slate-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
                    />
                    <svg
                      className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                      />
                    </svg>
                  </div>
                </div>

                {/* Filter Dropdowns */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      {locale === "mn" ? "Lane" : "Lane"}
                    </label>
                    <Dropdown
                      options={laneOptions}
                      value={selectedLane}
                      onChange={setSelectedLane}
                      placeholder="Filter by Lane"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      {locale === "mn" ? "Зэрэглэл" : "Tier"}
                    </label>
                    <Dropdown
                      options={tierOptions}
                      value={selectedTier}
                      onChange={setSelectedTier}
                      placeholder="Filter by Tier"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      {locale === "mn" ? "Үүрэг" : "Role"}
                    </label>
                    <Dropdown
                      options={roleOptions}
                      value={selectedRole}
                      onChange={setSelectedRole}
                      placeholder="Filter by Role"
                    />
                  </div>
                </div>

                {/* Clear Filters Button */}
                {hasActiveFilters && (
                  <div className="text-center">
                    <button
                      onClick={clearAllFilters}
                      className="px-6 py-2 bg-red-600/20 text-red-400 border border-red-600/30 rounded-lg hover:bg-red-600/30 transition-colors duration-200 font-medium"
                    >
                      {locale === "mn"
                        ? "Бүх шүүлтүүрийг цэвэрлэх"
                        : "Clear All Filters"}
                    </button>
                  </div>
                )}
              </div>

              {/* Results Count */}
              <div className="mb-6">
                <p className="text-gray-400 text-center">
                  {locale === "mn"
                    ? `${filteredChampions.length} баатар олдлоо`
                    : `Showing ${filteredChampions.length} champions`}
                </p>
              </div>

              {/* Champions Grid */}
              {filteredChampions.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {filteredChampions.map((champion) => (
                    <ChampionCard key={champion.id} champion={champion} />
                  ))}
                </div>
              ) : (
                <div className="text-center py-16 bg-slate-900/50 rounded-xl border border-slate-700/30">
                  <div className="space-y-4">
                    <svg
                      className="w-16 h-16 text-gray-500 mx-auto"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1}
                        d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 20a7.962 7.962 0 01-5-1.709M5 12a7 7 0 1114 0 7 7 0 01-14 0z"
                      />
                    </svg>
                    <div>
                      <h3 className="text-xl font-semibold text-gray-300 mb-2">
                        {locale === "mn"
                          ? "Баатар олдсонгүй"
                          : "No Champions Found"}
                      </h3>
                      <p className="text-gray-400">
                        {locale === "mn"
                          ? "Сонгосон шүүлтүүрт тохирох баатар олдсонгүй. Шүүлтүүрээ өөрчилж үзнэ үү."
                          : "No champions match your current filters. Try adjusting your search criteria."}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ErrorBoundary>
        </div>
      </div>
    </Layout>
  );
};

const ChampionsPage: React.FC<ChampionsPageProps> = ({ champions }) => {
  return <ChampionsPageContent champions={champions} />;
};

export const getStaticProps: GetStaticProps<ChampionsPageProps> = async () => {
  try {
    const champions = ChampionDataLoader.loadAllChampions();

    return {
      props: {
        champions,
      },
      revalidate: 3600, // Revalidate every hour
    };
  } catch (error) {
    console.error("Error loading champions data:", error);

    return {
      props: {
        champions: [],
      },
      revalidate: 3600,
    };
  }
};

export default ChampionsPage;
