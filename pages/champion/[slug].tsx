import React, { useEffect, useState } from "react";
import Head from "next/head";
import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";
import { useLanguage, Locale } from "../../contexts/LanguageContext";
import { ChampionData } from "../../types/champion";
import { getStaticTranslations } from "../../utils/i18n";
import StaticLanguageWrapper from "../../components/StaticLanguageWrapper";
import ChampionStatsPieChart from "../../components/ChampionStatsPieChart";
import AbilitiesI18n from "../../components/AbilitiesI18n";
import BuildGuideI18n from "../../components/BuildGuideI18n";
import LanguageSwitcher from "../../components/LanguageSwitcher";
import Layout from "../../components/Layout/Layout";
import fs from "fs";
import path from "path";

interface ChampionPageProps {
  championData: ChampionData;
  translations: any;
  locale: Locale;
}

const ChampionPageContent: React.FC<ChampionPageProps> = ({
  championData,
  translations,
  locale,
}) => {
  const router = useRouter();

  // Use static translations for SSG
  const t = (key: string) => {
    const keys = key.split(".");
    let value = translations;
    for (const k of keys) {
      value = value?.[k];
    }
    return value || key;
  };

  if (router.isFallback) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-xl font-semibold text-gray-600">
          {t("common.loading")}
        </div>
      </div>
    );
  }

  const getTierColor = (tier: string): string => {
    const tierColors: Record<string, string> = {
      "S+": "bg-gradient-to-r from-red-500 to-red-600",
      S: "bg-gradient-to-r from-red-400 to-red-500",
      A: "bg-gradient-to-r from-orange-400 to-orange-500",
      B: "bg-gradient-to-r from-yellow-400 to-yellow-500",
      C: "bg-gradient-to-r from-green-400 to-green-500",
      D: "bg-gradient-to-r from-blue-400 to-blue-500",
    };
    return tierColors[tier] || "bg-gradient-to-r from-gray-400 to-gray-500";
  };

  const getRoleTranslation = (role: string) => {
    const key = role.toLowerCase().replace(" / ", "_").replace(" ", "_");
    return t(`roles.${key}`) || role;
  };

  const getDifficultyTranslation = (difficulty: string) => {
    const key = difficulty.toLowerCase();
    return t(`difficulty.${key}`) || difficulty;
  };

  return (
    <Layout currentPage={`/champion/${championData.champion.id}`}>
      <Head>
        <title>{`${championData.champion.name} - ${t("champion.title")} - Wild Rift`}</title>
        <meta
          name="description"
          content={`${t("champion.title")} ${championData.champion.name} ${t("navigation.guides")}`}
        />
        <meta
          property="og:title"
          content={`${championData.champion.name} - ${t("champion.title")}`}
        />
        <meta
          property="og:description"
          content={`${t("champion.title")} ${championData.champion.name} ${t("navigation.guides")}`}
        />
        <meta property="og:image" content={championData.champion.image} />
      </Head>

      <div
        className="min-h-screen bg-cover bg-center bg-fixed relative"
        style={{
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8)), url('https://wr-meta.com/uploads/posts/2020-12/1607436548_ahri_skin01-min.jpg')`,
        }}
      >
        {/* Overlay for better readability */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-black/80 pointer-events-none" />

        {/* Hero Section */}
        <div className="relative z-10 bg-gradient-to-r from-black/80 via-purple-900/40 to-blue-900/40 backdrop-blur-sm border-b border-gold-500/30">
          <div className="container mx-auto px-4 py-16">
            <div className="flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-8">
              <div className="relative group">
                <div className="absolute -inset-1 bg-gradient-to-r from-yellow-400 via-purple-500 to-blue-500 rounded-full blur opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200 animate-pulse"></div>
                <img
                  src={championData.champion.image}
                  alt={championData.champion.name}
                  className="relative w-32 h-32 md:w-40 md:h-40 rounded-full border-4 border-yellow-400 shadow-2xl object-cover transform group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.src = "/placeholder-champion.png";
                  }}
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
                    📊{" "}
                    {getDifficultyTranslation(championData.champion.difficulty)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="relative z-10 container mx-auto px-4 py-12">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
              <div className="bg-black/60 backdrop-blur-md rounded-2xl border border-yellow-400/30 p-1 shadow-2xl">
                <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 rounded-xl p-6">
                  <ChampionStatsPieChart stats={championData.stats} />
                </div>
              </div>
              <div className="bg-black/60 backdrop-blur-md rounded-2xl border border-yellow-400/30 p-1 shadow-2xl">
                <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 rounded-xl p-6">
                  <AbilitiesI18n abilities={championData.abilities} />
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-8">
              <div className="bg-black/60 backdrop-blur-md rounded-2xl border border-yellow-400/30 p-1 shadow-2xl">
                <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 rounded-xl p-6">
                  <BuildGuideI18n
                    builds={championData.builds}
                    runes={championData.runes}
                  />
                </div>
              </div>

              {/* Meta Info */}
              <div className="bg-black/70 backdrop-blur-md rounded-2xl border border-yellow-400/40 p-1 shadow-2xl hover:border-yellow-400/60 transition-all duration-300">
                <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 rounded-xl p-6">
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

              {/* Tips */}
              <div className="bg-black/70 backdrop-blur-md rounded-2xl border border-yellow-400/40 p-1 shadow-2xl hover:border-yellow-400/60 transition-all duration-300">
                <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 rounded-xl p-6">
                  <h3 className="text-2xl font-black mb-6 bg-gradient-to-r from-yellow-400 to-yellow-300 bg-clip-text text-transparent flex items-center">
                    💡 {t("tips.title")}
                  </h3>
                  <ul className="space-y-3">
                    {championData.tips.map((tip, index) => (
                      <li
                        key={index}
                        className="flex items-start p-3 bg-black/30 rounded-lg border border-cyan-500/20 hover:border-cyan-500/40 transition-all duration-200"
                      >
                        <span className="text-cyan-400 mr-3 mt-1 text-lg">
                          ⚡
                        </span>
                        <span className="text-gray-200 font-medium leading-relaxed">
                          {tip}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export const getStaticPaths: GetStaticPaths = async () => {
  try {
    // Use the data loader to get all champions and their proper slugs
    const { ChampionDataLoader } = await import("../../utils/dataLoader");
    const champions = ChampionDataLoader.loadAllChampions();

    const paths = champions.map((champion) => ({
      params: { slug: champion.champion.id },
    }));

    // Also include file-based paths as fallback
    const championsDir = path.join(process.cwd(), "champions_clean");
    const championFiles = fs.readdirSync(championsDir);
    const filePaths = championFiles
      .filter((file) => file.endsWith(".json"))
      .map((file) => ({
        params: { slug: file.replace(".json", "") },
      }));

    // Combine and deduplicate paths
    const allPaths = [...paths, ...filePaths];
    const uniquePaths = allPaths.filter(
      (path, index, self) =>
        index === self.findIndex((p) => p.params.slug === path.params.slug),
    );

    return {
      paths: uniquePaths,
      fallback: false,
    };
  } catch (error) {
    console.error("Error generating static paths:", error);

    // Fallback to file-based approach
    const championsDir = path.join(process.cwd(), "champions_clean");
    const championFiles = fs.readdirSync(championsDir);
    const paths = championFiles
      .filter((file) => file.endsWith(".json"))
      .map((file) => ({
        params: { slug: file.replace(".json", "") },
      }));

    return {
      paths,
      fallback: false,
    };
  }
};

export const getStaticProps: GetStaticProps = async ({
  params,
  locale = "en",
}) => {
  const slug = params?.slug as string;

  try {
    // Try to load champion by slug first using the data loader
    const { ChampionDataLoader } = await import("../../utils/dataLoader");
    let championData = ChampionDataLoader.loadChampionBySlug(slug);

    // If not found by slug, try direct file access (fallback)
    if (!championData) {
      const championPath = path.join(
        process.cwd(),
        "champions_clean",
        `${slug}.json`,
      );
      const championFileContent = fs.readFileSync(championPath, "utf8");
      const rawChampionData = JSON.parse(championFileContent);

      // Transform the raw data to match our ChampionData interface (fallback)
      championData = {
        champion: {
          id: slug,
          name:
            rawChampionData.name ||
            slug.charAt(0).toUpperCase() + slug.slice(1),
          title: rawChampionData.title || "",
          role: rawChampionData.roles
            ? rawChampionData.roles.join(" / ")
            : "Unknown",
          lanes: rawChampionData.lanes || ["Mid"],
          difficulty: rawChampionData.stats?.difficulty
            ? rawChampionData.stats.difficulty > 66
              ? "High"
              : rawChampionData.stats.difficulty > 33
                ? "Medium"
                : "Low"
            : "Medium",
          tier:
            rawChampionData.tier === 1
              ? "S+"
              : rawChampionData.tier === 2
                ? "S"
                : rawChampionData.tier === 3
                  ? "A"
                  : rawChampionData.tier === 4
                    ? "B"
                    : rawChampionData.tier === 5
                      ? "C"
                      : "D",
          image: rawChampionData.image || "/placeholder-champion.png",
          splash_art: rawChampionData.image || "/placeholder-champion.png",
        },
        stats: {
          // Champion performance stats from the JSON
          damage: { base: rawChampionData.stats?.damage || 0, per_level: 0 },
          toughness: {
            base: rawChampionData.stats?.toughness || 0,
            per_level: 0,
          },
          utility: { base: rawChampionData.stats?.utility || 0, per_level: 0 },
          difficulty: {
            base: rawChampionData.stats?.difficulty || 0,
            per_level: 0,
          },
          // Base stats (placeholder for future implementation)
          attack_damage: { base: 60, per_level: 5 },
          health: { base: 600, per_level: 100 },
          health_regeneration: { base: 6, per_level: 1 },
          attack_speed: { base: 0.7, per_level: 0.01 },
          mana: { base: 300, per_level: 50 },
          mana_regeneration: { base: 8, per_level: 1 },
          movement_speed: { base: 350, per_level: 0 },
          armor: { base: 35, per_level: 4 },
          magic_resistance: { base: 35, per_level: 2 },
          critical_strike: { base: 175, per_level: 0 },
        },
        abilities: {
          passive: rawChampionData.abilities?.[0]
            ? {
                name: rawChampionData.abilities[0].name || "Passive",
                key: rawChampionData.abilities[0].key || "P",
                type: "Passive",
                description: rawChampionData.abilities[0].description || "",
                damage: [],
                scaling: "",
                damage_type: "None",
                image: rawChampionData.abilities[0].image || "",
                notes: [],
              }
            : {
                name: "Passive",
                key: "P",
                type: "Passive",
                description: "Champion passive ability",
                damage: [],
                scaling: "",
                damage_type: "None",
                image: "",
                notes: [],
              },
          q: rawChampionData.abilities?.[1] || {
            name: "Q Ability",
            key: "Q",
            type: "Active",
            description: "First active ability",
            damage: [],
            scaling: "",
            damage_type: "Physical",
            image: "",
            notes: [],
          },
          w: rawChampionData.abilities?.[2] || {
            name: "W Ability",
            key: "W",
            type: "Active",
            description: "Second active ability",
            damage: [],
            scaling: "",
            damage_type: "Physical",
            image: "",
            notes: [],
          },
          e: rawChampionData.abilities?.[3] || {
            name: "E Ability",
            key: "E",
            type: "Active",
            description: "Third active ability",
            damage: [],
            scaling: "",
            damage_type: "Physical",
            image: "",
            notes: [],
          },
          r: rawChampionData.abilities?.[4] || {
            name: "R Ability",
            key: "R",
            type: "Ultimate",
            description: "Ultimate ability",
            damage: [],
            scaling: "",
            damage_type: "Physical",
            image: "",
            notes: [],
          },
        },
        builds: rawChampionData.builds?.[0]
          ? {
              core_items:
                rawChampionData.builds[0].core_items?.map(
                  (item: any) => item.name,
                ) || [],
              starting_items:
                rawChampionData.builds[0].start_items?.map(
                  (item: any) => item.name,
                ) || [],
              boots:
                rawChampionData.builds[0].boots_enchants?.map(
                  (item: any) => item.name,
                ) || [],
              situational:
                rawChampionData.builds[0].situational_items?.flatMap(
                  (cat: any) => cat.items?.map((item: any) => item.name) || [],
                ) || [],
            }
          : {
              core_items: [],
              starting_items: [],
              boots: [],
              situational: [],
            },
        runes: rawChampionData.builds?.[0]?.runes
          ? {
              primary: {
                tree: "Domination",
                keystone:
                  rawChampionData.builds[0].runes.keystone?.name ||
                  "Electrocute",
                runes:
                  rawChampionData.builds[0].runes.primary?.map(
                    (rune: any) => rune.name,
                  ) || [],
              },
              secondary: {
                tree: "Resolve",
                runes:
                  rawChampionData.builds[0].runes.secondary?.map(
                    (rune: any) => rune.name,
                  ) || [],
              },
            }
          : {
              primary: {
                tree: "Domination",
                keystone: "Electrocute",
                runes: [],
              },
              secondary: {
                tree: "Resolve",
                runes: [],
              },
            },
        summoner_spells: rawChampionData.builds?.[0]?.summoner_spells?.map(
          (spell: any) => spell.name,
        ) || ["Flash", "Ignite"],
        counters: {
          strong_against: ["Squishy Champions", "Low Mobility Champions"],
          weak_against: ["Tanky Champions", "High Mobility Champions"],
        },
        tips: [
          "Focus on positioning in team fights",
          "Use abilities efficiently to maximize damage",
          "Ward key areas to avoid ganks",
          "Practice combo execution for better performance",
        ],
        meta: {
          tier:
            rawChampionData.tier === 1
              ? "S+"
              : rawChampionData.tier === 2
                ? "S"
                : rawChampionData.tier === 3
                  ? "A"
                  : rawChampionData.tier === 4
                    ? "B"
                    : rawChampionData.tier === 5
                      ? "C"
                      : "D",
          win_rate: "52%",
          pick_rate: "8%",
          ban_rate: "Medium",
          patch: "6.1f",
          last_updated: new Date().toISOString().split("T")[0],
          views: "50,000",
        },
      };
    }

    const translations = getStaticTranslations(locale as "mn" | "en");

    return {
      props: {
        championData,
        translations,
        locale: locale as Locale,
      },
    };
  } catch (error) {
    console.error(`Error loading champion data for ${slug}:`, error);

    return {
      notFound: true,
    };
  }
};

const ChampionPage: React.FC<ChampionPageProps> = ({
  championData,
  translations,
  locale,
}) => {
  return (
    <StaticLanguageWrapper locale={locale}>
      <ChampionPageContent
        championData={championData}
        translations={translations}
        locale={locale}
      />
    </StaticLanguageWrapper>
  );
};

export default ChampionPage;
