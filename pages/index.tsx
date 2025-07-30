import React, { useEffect } from 'react';
import { GetStaticProps } from 'next';
import dynamic from 'next/dynamic';
import { useLanguage } from '../contexts/LanguageContext';
import { Layout } from '../components/Layout';
import ErrorBoundary from '../components/ErrorBoundary';
import SEOHead from '../components/SEO/SEOHead';
import { ChampionDataLoader, ItemDataLoader } from '../utils/dataLoader';
import { ChampionData } from '../types/champion';
import { Item } from '../types/item';

const HeroSection = dynamic(() => import('../components/HeroSection'));
const ChampionsSection = dynamic(() => import('../components/ChampionsSection'));
const ItemsSection = dynamic(() => import('../components/ItemsSection'));
const RunesSection = dynamic(() => import('../components/RunesSection'));

interface HomePageContentProps {
  champions: ChampionData[];
  items: Item[];
}

const HomePageContent: React.FC<HomePageContentProps> = ({ champions, items }) => {
  const { t } = useLanguage();

  return (
    <Layout currentPage="/">
      <SEOHead
        title={`Wild Rift ${t('navigation.champions')} Guide - ${t('hero.title')}`}
        description={`${t('hero.description')} - Wild Rift ${t('navigation.champions')}, ${t('navigation.items')}, ${t('navigation.runes')} guides and tier lists.`}
        keywords={`Wild Rift, League of Legends, ${t('navigation.champions')}, ${t('navigation.items')}, ${t('navigation.runes')}, tier list, guide, meta, builds`}
        url="https://wildriftguide.com/"
        image="https://wildriftguide.com/og-image.jpg"
        type="website"
      />

      <div>
        <ErrorBoundary
          fallback={
            <div>
              <h2>
                Hero Section Unavailable
              </h2>
              <p>
                The hero section could not be loaded. Please refresh the page.
              </p>
            </div>
          }
        >
          <HeroSection
            onViewChampions={() => window.location.href = '/champions'}
            onViewTierList={() => window.location.href = '/tier-list'}
          />
        </ErrorBoundary>
      </div>

      <div>
        <div>
          <div>
            <ErrorBoundary
              fallback={
                <div>
                  <h2>
                    {t('sections.champions')} Section Error
                  </h2>
                  <p>
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

          <div>
            <ErrorBoundary
              fallback={
                <div>
                  <h2>
                    {t('sections.items')} Section Error
                  </h2>
                  <p>
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

            <ErrorBoundary
              fallback={
                <div>
                  <h2>
                    {t('sections.runes')} Section Error
                  </h2>
                  <p>
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
    </Layout>
  );
}; interface H
omePageProps {
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
    console.error('Error loading data:', error);

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