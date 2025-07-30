import React, { useEffect } from "react";
import { GetStaticProps } from "next";
import dynamic from "next/dynamic";
import { useLanguage } from "../contexts/LanguageContext";
import { Layout } from "../components/Layout";
import ErrorBoundary from "../components/ErrorBoundary";
import SEOHead from "../components/SEO/SEOHead";
import { ChampionDataLoader, ItemDataLoader } from "../utils/dataLoader";
import { ChampionData } from "../types/champion";
import { Item } from "../types/item";

const HeroSection = dynamic(() => import("../components/HeroSection"));
const ChampionsSection = dynamic(
  () => import("../components/ChampionsSection"),
);
const ItemsSection = dynamic(() => import("../components/ItemsSection"));
const RunesSection = dynamic(() => import("../components/RunesSection"));

interface HomePageContentProps {
  champions: ChampionData[];
  items: Item[];
}

const HomePageContent: React.FC<HomePageContentProps> = ({
  champions,
  items,
}) => {
  const { t } = useLanguage();

  return (
    <Layout currentPage="/">
      <SEOHead
        title={`Wild Rift ${t("navigation.champions")} Guide - ${t("hero.title")}`}
        description={`${t("hero.description")} - Wild Rift ${t("navigation.champions")}, ${t("navigation.items")}, ${t("navigation.runes")} guides and tier lists.`}
        keywords={`Wild Rift, League of Legends, ${t("navigation.champions")}, ${t("navigation.items")}, ${t("navigation.runes")}, tier list, guide, meta, builds`}
        url="https://wildriftguide.com/"
        image="https://wildriftguide.com/og-image.jpg"
        type="website"
      />

      {/* Hero Section - Full Width */}
      <div className="w-full">
        <ErrorBoundary
          fallback={
            <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-purple-900 to-black">
              <div className="text-center text-white">
                <h2 className="text-2xl font-bold mb-4">
                  Hero Section Unavailable
                </h2>
                <p className="text-gray-300">
                  The hero section could not be loaded. Please refresh the page.
                </p>
              </div>
            </div>
          }
        >
          <HeroSection
            onViewChampions={() => (window.location.href = "/champions")}
            onViewTierList={() => (window.location.href = "/tier-list")}
          />
        </ErrorBoundary>
      </div>

      {/* Main Content - Constrained Width */}
      <div className="w-full bg-gradient-to-b from-slate-900 to-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
          {/* Champions Section */}
          <div className="champions-container">
            <ErrorBoundary
              fallback={
                <div className="bg-slate-800/50 rounded-xl p-8 text-center">
                  <h2 className="text-xl font-bold text-red-400 mb-2">
                    {t("sections.champions")} Section Error
                  </h2>
                  <p className="text-gray-400">
                    Champions data could not be loaded.
                  </p>
                </div>
              }
            >
              <ChampionsSection
                champions={champions}
                showPatchInfo={true}
                maxDisplayed={8}
              />
            </ErrorBoundary>
          </div>

          {/* Items and Runes Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="items-container">
              <ErrorBoundary
                fallback={
                  <div className="bg-slate-800/50 rounded-xl p-8 text-center">
                    <h2 className="text-xl font-bold text-red-400 mb-2">
                      {t("sections.items")} Section Error
                    </h2>
                    <p className="text-gray-400">
                      Items section could not be loaded.
                    </p>
                  </div>
                }
              >
                <ItemsSection
                  items={items}
                  showPatchInfo={true}
                  maxDisplayed={6}
                />
              </ErrorBoundary>
            </div>

            <div className="runes-container">
              <ErrorBoundary
                fallback={
                  <div className="bg-slate-800/50 rounded-xl p-8 text-center">
                    <h2 className="text-xl font-bold text-red-400 mb-2">
                      {t("sections.runes")} Section Error
                    </h2>
                    <p className="text-gray-400">
                      Runes section could not be loaded.
                    </p>
                  </div>
                }
              >
                <RunesSection
                  champions={champions}
                  showPatchInfo={true}
                  maxDisplayed={4}
                />
              </ErrorBoundary>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

interface HomePageProps {
  champions: ChampionData[];
  items: Item[];
}

const HomePage: React.FC<HomePageProps> = ({ champions, items }) => {
  return <HomePageContent champions={champions} items={items} />;
};

export const getStaticProps: GetStaticProps<HomePageProps> = async () => {
  try {
    const champions = ChampionDataLoader.loadAllChampions();
    const items = ItemDataLoader.loadAllItems();

    return {
      props: {
        champions,
        items,
      },
      revalidate: 3600,
    };
  } catch (error) {
    console.error("Error loading data:", error);

    return {
      props: {
        champions: [],
        items: [],
      },
      revalidate: 3600,
    };
  }
};

export default HomePage;
