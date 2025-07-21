import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { GetStaticPaths, GetStaticProps } from 'next';
import { useRouter } from 'next/router';
import { useTranslation, getStaticTranslations } from '../../utils/i18n';
import { ChampionData } from '../../types/champion';
import ChampionStatsI18n from '../../components/ChampionStatsI18n';
import AbilitiesI18n from '../../components/AbilitiesI18n';
import BuildGuideI18n from '../../components/BuildGuideI18n';
import LanguageSwitcher from '../../components/LanguageSwitcher';

interface ChampionPageProps {
  championData: ChampionData;
  translations: any;
}

const ChampionPage: React.FC<ChampionPageProps> = ({ championData, translations }) => {
  const { t, locale } = useTranslation();
  const router = useRouter();

  if (router.isFallback) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-xl font-semibold text-gray-600">
          {t('common.loading')}
        </div>
      </div>
    );
  }

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

  const getDifficultyTranslation = (difficulty: string) => {
    const key = difficulty.toLowerCase();
    return t(`difficulty.${key}`) || difficulty;
  };

  return (
    <>
      <Head>
        <title>{championData.champion.name} - {t('champion.title')} - Wild Rift</title>
        <meta name="description" content={`${t('champion.title')} ${championData.champion.name} ${t('navigation.guides')}`} />
        <meta property="og:title" content={`${championData.champion.name} - ${t('champion.title')}`} />
        <meta property="og:description" content={`${t('champion.title')} ${championData.champion.name} ${t('navigation.guides')}`} />
        <meta property="og:image" content={championData.champion.image} />
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
        <div className="bg-gradient-to-r from-red-600 to-red-800 text-white">
          <div className="container mx-auto px-4 py-12">
            <div className="flex items-center space-x-6">
              <img 
                src={championData.champion.image} 
                alt={championData.champion.name}
                className="w-24 h-24 rounded-full border-4 border-white shadow-lg"
              />
              <div>
                <h1 className="text-4xl font-bold">{championData.champion.name}</h1>
                <p className="text-xl opacity-90">{championData.champion.title}</p>
                <div className="flex items-center space-x-4 mt-2">
                  <span className="bg-white text-red-600 px-3 py-1 rounded-full text-sm font-medium">
                    {getRoleTranslation(championData.champion.role)}
                  </span>
                  <span className={`text-white px-3 py-1 rounded-full text-sm font-bold ${getTierColor(championData.meta.tier)}`}>
                    {t('champion.tier')} {championData.meta.tier}
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
              <BuildGuideI18n builds={championData.builds} runes={championData.runes} />
              
              {/* Meta Info */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold mb-4 text-gray-800">
                  {t('meta.title')}
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">{t('champion.win_rate')}:</span>
                    <span className="font-semibold text-green-600">{championData.meta.win_rate}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">{t('champion.pick_rate')}:</span>
                    <span className="font-semibold">{championData.meta.pick_rate}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">{t('champion.patch')}:</span>
                    <span className="font-semibold">{championData.meta.patch}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">{t('champion.views')}:</span>
                    <span className="font-semibold">{championData.meta.views}</span>
                  </div>
                </div>
              </div>

              {/* Tips */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold mb-4 text-gray-800">
                  {t('tips.title')}
                </h3>
                <ul className="space-y-2">
                  {championData.tips.map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-blue-500 mr-2 mt-1">💡</span>
                      <span className="text-gray-700 text-sm">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export const getStaticPaths: GetStaticPaths = async () => {
  const champions = ['aatrox'];
  
  const paths = [];
  for (const champion of champions) {
    paths.push({ params: { slug: champion }, locale: 'mn' });
    paths.push({ params: { slug: champion }, locale: 'en' });
  }

  return {
    paths,
    fallback: false,
  };
};

export const getStaticProps: GetStaticProps = async ({ params, locale }) => {
  // Sample champion data - replace with actual data fetching
  const championData = {
    champion: {
      id: 'aatrox',
      name: 'Aatrox',
      title: 'The Darkin Blade',
      role: 'Fighter / Tank',
      lanes: ['Baron Lane', 'Jungle'],
      difficulty: 'High',
      tier: 'S',
      image: 'https://wr-meta.com/uploads/posts/2023-01/1675024764_1656622041_aatrox_10-min.jpg',
      splash_art: 'https://wr-meta.com/uploads/posts/2023-01/1675024764_1656622041_aatrox_10-min.jpg'
    },
    stats: {
      attack_damage: { base: 62, per_level: 5.5 },
      health: { base: 630, per_level: 136 },
      health_regeneration: { base: 6, per_level: 1 },
      attack_speed: { base: 0.73, per_level: 0.008 },
      mana: { base: 0, per_level: 0 },
      mana_regeneration: { base: 0, per_level: 0 },
      movement_speed: { base: 355, per_level: 0 },
      armor: { base: 46, per_level: 4.5 },
      magic_resistance: { base: 40, per_level: 2 },
      critical_strike: { base: 175, per_level: 0 }
    },
    abilities: {
      passive: {
        name: 'Deathbringer Stance',
        key: 'P',
        type: 'Passive',
        description: 'Enhances his attack every 24 seconds to deal bonus physical damage.',
        damage: [],
        scaling: '4-13% of target max health',
        damage_type: 'Physical',
        image: '',
        notes: ['Max 50 damage against monsters'],
        cooldown: 24
      },
      q: {
        name: 'The Darkin Blade',
        key: 'Q',
        type: 'Active',
        description: 'Aatrox slams his greatsword down, dealing physical damage.',
        damage: [10, 40, 70, 100],
        scaling: ['75%', '80%', '85%', '90%'],
        damage_type: 'Physical',
        image: '',
        notes: ['Can be cast 3 times total']
      },
      w: {
        name: 'Infernal Chains',
        key: 'W',
        type: 'Active',
        description: 'Aatrox smashes the ground, dealing physical damage.',
        damage: [25, 40, 55, 70],
        scaling: '40% AD',
        damage_type: 'Physical',
        image: '',
        notes: ['Slows by 25%']
      },
      e: {
        name: 'Umbral Dash',
        key: 'E',
        type: 'Active',
        description: 'Aatrox dashes in a direction.',
        damage: [],
        scaling: '',
        damage_type: 'None',
        image: '',
        notes: ['Provides mobility']
      },
      r: {
        name: 'World Ender',
        key: 'R',
        type: 'Ultimate',
        description: 'Aatrox unleashes his demonic form.',
        damage: [],
        scaling: '',
        damage_type: 'None',
        image: '',
        notes: ['Duration extended by takedowns'],
        duration: 10
      }
    },
    builds: {
      core_items: ['Black Cleaver', 'Death\'s Dance', 'Sterak\'s Gage'],
      starting_items: ['Long Sword'],
      boots: ['Plated Steelcaps', 'Mercury\'s Treads'],
      situational: ['Mortal Reminder', 'Guardian Angel']
    },
    runes: {
      primary: {
        tree: 'Precision',
        keystone: 'Conqueror',
        runes: ['Triumph', 'Legend: Alacrity', 'Last Stand']
      },
      secondary: {
        tree: 'Resolve',
        runes: ['Bone Plating', 'Revitalize']
      }
    },
    summoner_spells: ['Flash', 'Ignite'],
    counters: {
      strong_against: ['Tanks', 'Melee Champions'],
      weak_against: ['Ranged Champions', 'High Mobility Champions']
    },
    tips: [
      'Focus on hitting Q sweet spots for maximum damage',
      'Use passive on champions for better healing',
      'Master Flash + Q combos for surprise engages',
      'Time ultimate carefully for team fights'
    ],
    meta: {
      tier: 'S',
      win_rate: '90%',
      pick_rate: '10%',
      ban_rate: 'Low',
      patch: '6.1f',
      last_updated: '2025-07-02',
      views: '141,494'
    }
  };

  const translations = getStaticTranslations(locale as 'mn' | 'en');

  return {
    props: {
      championData,
      translations,
    },
  };
};

export default ChampionPage;
