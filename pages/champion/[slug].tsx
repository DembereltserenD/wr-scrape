import React from "react";
import Head from "next/head";
import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";
import { Locale } from "../../contexts/LanguageContext";
import { ChampionData } from "../../types/champion";
import { getStaticTranslations } from "../../utils/i18n";
import StaticLanguageWrapper from "../../components/StaticLanguageWrapper";
import ChampionStatsPieChart from "../../components/ChampionStatsPieChart";
import AbilitiesI18n from "../../components/AbilitiesI18n";
import BuildGuideI18n from "../../components/BuildGuideI18n";
import Layout from "../../components/Layout/Layout";
import ChampionHero from "../../components/ChampionPage/ChampionHero";
import ChampionMeta from "../../components/ChampionPage/ChampionMeta";

interface ChampionPageProps {
  championData: ChampionData;
  translations: any;
  locale: Locale;
}

const ChampionPageContent: React.FC<ChampionPageProps> = ({
  championData,
  translations,
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

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-800 to-gray-900 relative">
        {/* Clean gradient background */}
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/20 via-transparent to-slate-900/40 pointer-events-none" />

        {/* Hero Section with max width container */}
        <div className="relative z-10">
          <div className="max-w-7xl mx-auto">
            <ChampionHero
              championData={championData}
              t={t}
              getTierColor={getTierColor}
              getRoleTranslation={getRoleTranslation}
              getDifficultyTranslation={getDifficultyTranslation}
            />
          </div>
        </div>

        {/* Content */}
        <div className="relative z-10 px-4 sm:px-6 lg:px-8 py-12">
          <div className="max-w-[1200px] mx-auto">
            <div className="space-y-8">
              {/* Statistics Section */}
              <div className="bg-slate-800/80 backdrop-blur-sm rounded-3xl border border-slate-600/40 p-1 shadow-2xl hover:shadow-3xl transition-all duration-500">
                <div className="bg-gradient-to-br from-slate-700/50 to-slate-800/50 rounded-[22px] p-8">
                  <ChampionStatsPieChart stats={championData.stats} />
                </div>
              </div>

              {/* Abilities Section */}
              <div className="bg-slate-800/80 backdrop-blur-sm rounded-3xl border border-slate-600/40 p-1 shadow-2xl hover:shadow-3xl transition-all duration-500">
                <div className="bg-gradient-to-br from-slate-700/50 to-slate-800/50 rounded-[22px] p-8">
                  <AbilitiesI18n abilities={championData.abilities} />
                </div>
              </div>

              {/* Build Guide and Runes Section */}
              <div className="bg-slate-800/80 backdrop-blur-sm rounded-3xl border border-slate-600/40 p-1 shadow-2xl hover:shadow-3xl transition-all duration-500">
                <div className="bg-gradient-to-br from-slate-700/50 to-slate-800/50 rounded-[22px] p-8">
                  <BuildGuideI18n
                    builds={championData.builds}
                    runes={championData.runes}
                  />
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
    // Use optimized cache for O(1) path generation
    const { ChampionCache } = await import("../../utils/championCache");
    const slugs = ChampionCache.getAllSlugs();

    const paths = slugs.map((slug) => ({
      params: { slug },
    }));

    return {
      paths,
      fallback: false,
    };
  } catch (error) {
    console.error("Error generating static paths:", error);
    return {
      paths: [],
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
    // Use optimized cache for instant data retrieval
    const { ChampionCache } = await import("../../utils/championCache");
    const championData = ChampionCache.getChampion(slug);

    if (!championData) {
      return {
        notFound: true,
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
