import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { GetStaticProps } from 'next';
import { useTranslation, getStaticTranslations } from '../utils/i18n';
import LanguageSwitcher from '../components/LanguageSwitcher';

interface HomePageProps {
  translations: any;
}

const HomePage: React.FC<HomePageProps> = ({ translations }) => {
  const { t, locale } = useTranslation();

  const champions = [
    {
      id: 'aatrox',
      name: 'Aatrox',
      title: 'The Darkin Blade',
      role: 'Fighter / Tank',
      tier: 'S',
      image: 'https://wr-meta.com/uploads/posts/2023-01/1675024764_1656622041_aatrox_10-min.jpg'
    }
  ];

  const getTierColor = (tier: string): string => {
    const tierColors: Record<string, string> = {
      'S+': 'bg-red-500',
      'S': 'bg-red-400',
      'A': 'bg-orange-400',
      'B': 'bg-yellow-400',
      'C': 'bg-green-400',
      'D': 'bg-blue-400',
    };
    return tierColors[tier] || 'bg-gray-400';
  };

  const getRoleTranslation = (role: string) => {
    const key = role.toLowerCase().replace(' / ', '_').replace(' ', '_');
    return t(`roles.${key}`) || role;
  };

  return (
    <>
      <Head>
        <title>Wild Rift Champions Guide - {t('navigation.champions')}</title>
        <meta name="description" content={`Wild Rift ${t('navigation.champions')} ${t('navigation.guides')}`} />
        <meta property="og:title" content={`Wild Rift ${t('navigation.champions')} Guide`} />
        <meta property="og:description" content={`Wild Rift ${t('navigation.champions')} ${t('navigation.guides')}`} />
      </Head>

      <div className="min-h-screen bg-gray-100">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b">
          <div className="container mx-auto px-4 py-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-4">
                <h1 className="text-xl font-bold text-gray-800">Wild Rift</h1>
                <span className="text-gray-500">|</span>
                <span className="text-gray-600">{t('navigation.champions')}</span>
              </div>
              <LanguageSwitcher />
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-800 text-white">
          <div className="container mx-auto px-4 py-16 text-center">
            <h1 className="text-5xl font-bold mb-4">Wild Rift</h1>
            <p className="text-xl opacity-90 mb-8">{t('navigation.champions')} {t('navigation.guides')}</p>
            <p className="text-lg opacity-80">
              {locale === 'mn' ? 'Монгол болон англи хэл дээрх дэлгэрэнгүй гарын авлага' : 'Comprehensive guides in Mongolian and English'}
            </p>
          </div>
        </div>

        {/* Champions Grid */}
        <div className="container mx-auto px-4 py-12">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">
              {t('navigation.champions')}
            </h2>
            <p className="text-gray-600">
              {locale === 'mn' ? 'Баатруудын дэлгэрэнгүй гарын авлага' : 'Detailed champion guides and builds'}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {champions.map((champion) => (
              <Link 
                key={champion.id} 
                href={`/champion/${champion.id}`}
                className="group"
              >
                <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 group-hover:scale-105 transform transition-transform">
                  <div className="relative">
                    <img 
                      src={champion.image} 
                      alt={champion.name}
                      className="w-full h-48 object-cover"
                    />
                    <div className="absolute top-2 right-2">
                      <span className={`text-white px-2 py-1 rounded text-sm font-bold ${getTierColor(champion.tier)}`}>
                        {champion.tier}
                      </span>
                    </div>
                  </div>
                  <div className="p-4">
                    <h3 className="text-xl font-bold text-gray-800 mb-1">
                      {champion.name}
                    </h3>
                    <p className="text-gray-600 text-sm mb-2">
                      {champion.title}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">
                        {getRoleTranslation(champion.role)}
                      </span>
                      <span className="text-blue-600 text-sm font-medium group-hover:text-blue-800">
                        {locale === 'mn' ? 'Үзэх →' : 'View Guide →'}
                      </span>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* Coming Soon */}
          <div className="mt-12 text-center">
            <div className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">
                {locale === 'mn' ? 'Удахгүй нэмэгдэх' : 'Coming Soon'}
              </h3>
              <p className="text-gray-600 mb-4">
                {locale === 'mn' 
                  ? 'Бусад баатруудын гарын авлага удахгүй нэмэгдэх болно!' 
                  : 'More champion guides will be added soon!'}
              </p>
              <div className="flex justify-center space-x-4 text-sm text-gray-500">
                <span>• Yasuo</span>
                <span>• Jinx</span>
                <span>• Lee Sin</span>
                <span>• Akali</span>
                <span>• {locale === 'mn' ? 'болон бусад...' : 'and more...'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="bg-gray-800 text-white py-8 mt-12">
          <div className="container mx-auto px-4 text-center">
            <p className="text-gray-400">
              {locale === 'mn' 
                ? 'Wild Rift баатруудын гарын авлага - Монгол & English' 
                : 'Wild Rift Champions Guide - Mongolian & English'}
            </p>
            <p className="text-gray-500 text-sm mt-2">
              {locale === 'mn' 
                ? 'Энэ төсөл нь League of Legends: Wild Rift-тэй албан ёсны холбоогүй юм.' 
                : 'This project is not officially affiliated with League of Legends: Wild Rift.'}
            </p>
          </div>
        </footer>
      </div>
    </>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = getStaticTranslations(locale as 'mn' | 'en');

  return {
    props: {
      translations,
    },
  };
};

export default HomePage;
