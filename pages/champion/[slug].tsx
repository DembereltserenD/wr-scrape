import React, { useEffect, useState } from "react";
import Head from "next/head";
import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";
import { useLanguage, Locale } from "../../contexts/LanguageContext";
import { ChampionData } from "../../types/champion";
import { getStaticTranslations } from "../../utils/i18n";
import StaticLanguageWrapper from "../../components/StaticLanguageWrapper";
import ChampionStatsI18n from "../../components/ChampionStatsI18n";
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
      "S+": "bg-red-500",
      S: "bg-red-400",
      A: "bg-orange-400",
      B: "bg-yellow-400",
      C: "bg-green-400",
      D: "bg-blue-400",
    };
    return tierColors[tier] || "bg-gray-400";
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

      <div className="min-h-screen bg-gradient-to-b from-slate-900 to-black">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-800 text-white">
          <div className="container mx-auto px-4 py-12">
            <div className="flex items-center space-x-6">
              <img
                src={championData.champion.image}
                alt={championData.champion.name}
                className="w-24 h-24 rounded-full border-4 border-white shadow-lg"
              />
              <div>
                <h1 className="text-4xl font-bold">
                  {championData.champion.name}
                </h1>
                <p className="text-xl opacity-90">
                  {championData.champion.title}
                </p>
                <div className="flex items-center space-x-4 mt-2">
                  <span className="bg-white text-purple-600 px-3 py-1 rounded-full text-sm font-medium">
                    {getRoleTranslation(championData.champion.role)}
                  </span>
                  <span
                    className={`text-white px-3 py-1 rounded-full text-sm font-bold ${getTierColor(championData.meta.tier)}`}
                  >
                    {t("champion.tier")} {championData.meta.tier}
                  </span>
                  <span className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-medium">
                    {getDifficultyTranslation(championData.champion.difficulty)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="container mx-auto px-4 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
              <ChampionStatsI18n stats={championData.stats} />
              <AbilitiesI18n abilities={championData.abilities} />
            </div>

            {/* Sidebar */}
            <div className="space-y-8">
              <BuildGuideI18n
                builds={championData.builds}
                runes={championData.runes}
              />

              {/* Meta Info */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                <h3 className="text-xl font-bold mb-4 text-white">
                  {t("meta.title")}
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-300">
                      {t("champion.win_rate")}:
                    </span>
                    <span className="font-semibold text-green-400">
                      {championData.meta.win_rate}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-300">
                      {t("champion.pick_rate")}:
                    </span>
                    <span className="font-semibold text-gray-100">
                      {championData.meta.pick_rate}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-300">
                      {t("champion.patch")}:
                    </span>
                    <span className="font-semibold text-gray-100">
                      {championData.meta.patch}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-300">
                      {t("champion.views")}:
                    </span>
                    <span className="font-semibold text-gray-100">
                      {championData.meta.views}
                    </span>
                  </div>
                </div>
              </div>

              {/* Tips */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                <h3 className="text-xl font-bold mb-4 text-white">
                  {t("tips.title")}
                </h3>
                <ul className="space-y-2">
                  {championData.tips.map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-blue-400 mr-2 mt-1">💡</span>
                      <span className="text-gray-300 text-sm">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export const getStaticPaths: GetStaticPaths = async () => {
  // Read all champion files from the champions_clean directory
  const championsDir = path.join(process.cwd(), "champions_clean");
  const championFiles = fs.readdirSync(championsDir);

  const champions = championFiles
    .filter((file) => file.endsWith(".json"))
    .map((file) => file.replace(".json", ""));

  const paths = [];
  for (const champion of champions) {
    paths.push({ params: { slug: champion } });
  }

  return {
    paths,
    fallback: false,
  };
};

export const getStaticProps: GetStaticProps = async ({
  params,
  locale = "en",
}) => {
  const slug = params?.slug as string;

  try {
    // Read champion data from JSON file
    const championPath = path.join(
      process.cwd(),
      "champions_clean",
      `${slug}.json`,
    );
    const championFileContent = fs.readFileSync(championPath, "utf8");
    const rawChampionData = JSON.parse(championFileContent);

    // Transform the raw data to match our ChampionData interface
    const championData: ChampionData = {
      champion: {
        id: slug,
        name:
          rawChampionData.name || slug.charAt(0).toUpperCase() + slug.slice(1),
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
      stats: rawChampionData.base_stats || {
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
                rawChampionData.builds[0].runes.keystone?.name || "Electrocute",
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
