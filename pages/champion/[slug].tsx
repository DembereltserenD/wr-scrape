import React, { useState } from "react";
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
import LazyImage from "../../components/LazyImage";
import { Tooltip } from "../../components/UI";

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
  const [activeTab, setActiveTab] = useState('BUILD');

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

  // Render stat circles like wr-meta.com
  const renderStatCircles = () => {
    const stats = [
      { name: 'Damage', value: championData.stats.damage?.base || 0, color: 'text-red-400', icon: '⚔️' },
      { name: 'Toughness', value: championData.stats.toughness?.base || 0, color: 'text-green-400', icon: '🛡️' },
      { name: 'Utility', value: championData.stats.utility?.base || 0, color: 'text-blue-400', icon: '🔧' },
      { name: 'Difficulty', value: championData.stats.difficulty?.base || 0, color: 'text-purple-400', icon: '📚' }
    ];

    return (
      <div className="flex justify-center gap-8 mb-8">
        {stats.map((stat, index) => (
          <div key={index} className="text-center">
            <div className="relative w-16 h-16 mx-auto mb-2">
              <svg className="w-16 h-16 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-gray-700"
                  stroke="currentColor"
                  strokeWidth="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className={stat.color}
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeDasharray={`${stat.value}, 100`}
                  strokeLinecap="round"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-lg">{stat.icon}</span>
              </div>
            </div>
            <div className="text-sm text-gray-300">{stat.name}</div>
          </div>
        ))}
      </div>
    );
  };

  // Render navigation tabs
  const renderTabs = () => {
    const tabs = ['BUILD', 'COUNTERS', 'COUNTER ITEMS', 'TIPS', 'CON', 'GAME PLAN', 'POWER SPIKES'];
    
    return (
      <div className="flex justify-center mb-8">
        <div className="flex bg-black/60 backdrop-blur-sm rounded-lg p-1 border border-cyan-500/30">
          {tabs.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 text-sm font-bold transition-all duration-300 ${
                activeTab === tab
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-md shadow-lg transform scale-105'
                  : 'text-gray-300 hover:text-white hover:bg-gray-700/50 rounded-md'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>
    );
  };

  // Render build section content
  const renderBuildContent = () => {
    return (
      <div className="space-y-8">
        {/* Build Description */}
        <div className="text-center text-gray-300 max-w-4xl mx-auto">
          <p className="mb-4">
            The information below will help you get familiar with the game on the Mid Lane {championData.champion.name.toUpperCase()}. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Key Items Section */}
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-white text-center bg-gradient-to-r from-gray-700 to-gray-800 py-3 rounded-lg border border-cyan-500/30 shadow-lg">
              🔧 KEY ITEMS
            </h3>
            
            {/* Starting Items */}
            <div className="space-y-4">
              <div className="text-sm text-gray-400">
                <strong>TIPS:</strong> Start your build with 🧪 <span className="text-orange-400">Amplifying Tome</span>. Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy 👢 <span className="text-blue-400">Boots of Speed</span> at an early stage.
              </div>
              
              <div className="bg-black/40 backdrop-blur-sm rounded-lg p-4 border border-cyan-500/30">
                <h4 className="text-lg font-bold text-cyan-300 mb-3">✨ START</h4>
                <div className="flex justify-center">
                  {championData.builds.starting_items.slice(0, 1).map((item, index) => (
                    <Tooltip
                      key={index}
                      content={
                        <div className="text-white max-w-xs">
                          <h4 className="font-bold text-yellow-300 mb-2">{item.name}</h4>
                          <p className="text-sm text-gray-300">{item.description || 'Starting item for early game'}</p>
                          {item.cost && (
                            <div className="text-yellow-400 font-bold mt-2">{item.cost} Gold</div>
                          )}
                        </div>
                      }
                    >
                      <div className="text-center cursor-pointer">
                        <div className="w-24 h-24 bg-gray-700 rounded-lg border-2 border-gray-600 flex items-center justify-center mb-2 hover:border-cyan-500 transition-colors">
                          <LazyImage
                            src={item.image || '/placeholder-champion.svg'}
                            alt={item.name}
                            className="w-20 h-20 rounded"
                          />
                        </div>
                        <div className="text-xs text-gray-300">{item.name}</div>
                      </div>
                    </Tooltip>
                  ))}
                </div>
              </div>

              <div className="bg-black/40 backdrop-blur-sm rounded-lg p-4 border border-purple-500/30">
                <h4 className="text-lg font-bold text-purple-300 mb-3">🔥 CORE</h4>
                <div className="flex justify-center gap-4">
                  {championData.builds.core_items.slice(0, 3).map((item, index) => (
                    <Tooltip
                      key={index}
                      content={
                        <div className="text-white max-w-xs">
                          <h4 className="font-bold text-yellow-300 mb-2">{item.name}</h4>
                          <p className="text-sm text-gray-300">{item.description || 'Core item for mid game power spike'}</p>
                          {item.cost && (
                            <div className="text-yellow-400 font-bold mt-2">{item.cost} Gold</div>
                          )}
                        </div>
                      }
                    >
                      <div className="text-center cursor-pointer">
                        <div className="w-24 h-24 bg-gray-700 rounded-lg border-2 border-purple-500 flex items-center justify-center mb-2 hover:border-yellow-500 transition-colors">
                          <LazyImage
                            src={item.image || '/placeholder-champion.svg'}
                            alt={item.name}
                            className="w-20 h-20 rounded"
                          />
                        </div>
                        <div className="text-xs text-gray-300">{item.name}</div>
                      </div>
                    </Tooltip>
                  ))}
                </div>
              </div>

              <div className="bg-black/40 backdrop-blur-sm rounded-lg p-4 border border-yellow-500/30">
                <h4 className="text-lg font-bold text-yellow-300 mb-3">👟 BOOTS/ENCHANT</h4>
                <div className="flex justify-center gap-4">
                  {championData.builds.boots.slice(0, 3).map((item, index) => (
                    <Tooltip
                      key={index}
                      content={
                        <div className="text-white max-w-xs">
                          <h4 className="font-bold text-yellow-300 mb-2">{item.name}</h4>
                          <p className="text-sm text-gray-300">{item.description || 'Boots for mobility and utility'}</p>
                          {item.cost && (
                            <div className="text-yellow-400 font-bold mt-2">{item.cost} Gold</div>
                          )}
                        </div>
                      }
                    >
                      <div className="text-center cursor-pointer">
                        <div className="w-24 h-24 bg-gray-700 rounded-lg border-2 border-yellow-500 flex items-center justify-center mb-2 hover:border-orange-500 transition-colors">
                          <LazyImage
                            src={item.image || '/placeholder-champion.svg'}
                            alt={item.name}
                            className="w-20 h-20 rounded"
                          />
                        </div>
                        <div className="text-xs text-gray-300">{item.name}</div>
                      </div>
                    </Tooltip>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Runes Section */}
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-white text-center bg-gradient-to-r from-gray-700 to-gray-800 py-3 rounded-lg border border-cyan-500/30 shadow-lg">
              ⚡ RUNES BUILD
            </h3>
            
            <div className="space-y-4">
              {/* Primary Runes */}
              <div className="bg-black/40 backdrop-blur-sm rounded-lg p-4 border border-purple-500/30">
                <h4 className="text-lg font-bold text-purple-300 mb-3 flex items-center gap-2">
                  <Tooltip
                    content={
                      <div className="text-white max-w-xs">
                        <h4 className="font-bold text-yellow-300 mb-2">
                          {typeof championData.runes.primary.keystone === 'object' ? championData.runes.primary.keystone.name : championData.runes.primary.keystone}
                        </h4>
                        <p className="text-sm text-gray-300">
                          {typeof championData.runes.primary.keystone === 'object' && championData.runes.primary.keystone.description ? 
                            championData.runes.primary.keystone.description : 
                            'Hitting a champion with successive attacks or abilities deals bonus adaptive damage.'}
                        </p>
                      </div>
                    }
                  >
                    <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center shadow-lg cursor-pointer hover:scale-110 transition-transform">
                      {typeof championData.runes.primary.keystone === 'object' && championData.runes.primary.keystone.image ? (
                        <LazyImage
                          src={championData.runes.primary.keystone.image}
                          alt={championData.runes.primary.keystone.alt || championData.runes.primary.keystone.name}
                          className="w-12 h-12 rounded-full"
                        />
                      ) : (
                        <span className="text-white text-xl">⚡</span>
                      )}
                    </div>
                  </Tooltip>
                  {typeof championData.runes.primary.keystone === 'object' ? championData.runes.primary.keystone.name : championData.runes.primary.keystone}
                </h4>
                <div className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-3 py-1 rounded text-sm font-bold inline-block mb-2">
                  Burst Damage
                </div>
              </div>

              {/* Secondary Runes */}
              <div className="space-y-3">
                {championData.runes.primary.runes.slice(0, 3).map((rune, index) => (
                  <div key={index} className="bg-black/40 backdrop-blur-sm rounded-lg p-3 border border-yellow-500/30">
                    <div className="flex items-center gap-3">
                      <Tooltip
                        content={
                          <div className="text-white max-w-xs">
                            <h4 className="font-bold text-yellow-300 mb-2">
                              {typeof rune === 'object' ? rune.name : rune}
                            </h4>
                            <p className="text-sm text-gray-300">
                              {typeof rune === 'object' && rune.description ? rune.description : 'Provides additional power and utility'}
                            </p>
                          </div>
                        }
                      >
                        <div className="w-14 h-14 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full flex items-center justify-center shadow-lg cursor-pointer hover:scale-110 transition-transform">
                          {typeof rune === 'object' && rune.image ? (
                            <LazyImage
                              src={rune.image}
                              alt={rune.alt || rune.name}
                              className="w-10 h-10 rounded-full"
                            />
                          ) : (
                            <span className="text-white text-sm">🔥</span>
                          )}
                        </div>
                      </Tooltip>
                      <div>
                        <h5 className="text-yellow-200 font-bold">
                          {typeof rune === 'object' ? rune.name : rune}
                        </h5>
                        <div className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-2 py-1 rounded text-xs font-bold inline-block">
                          Bonus Damage
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Example Build */}
        <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-purple-500/30">
          <h3 className="text-xl font-bold text-purple-300 text-center mb-6">🔧 EXAMPLE BUILD</h3>
          <div className="grid grid-cols-3 md:grid-cols-6 gap-4 justify-items-center">
            {championData.builds.example_build.slice(0, 6).map((item, index) => (
              <Tooltip
                key={index}
                content={
                  <div className="text-white max-w-xs relative z-[100001]">
                    <h4 className="font-bold text-yellow-300 mb-2">{item.name}</h4>
                    <p className="text-sm text-gray-300">{item.description || 'Essential item for this build'}</p>
                    {item.cost && (
                      <div className="text-yellow-400 font-bold mt-2">{item.cost} Gold</div>
                    )}
                  </div>
                }
              >
                <div className="text-center cursor-pointer relative z-10">
                  <div className="w-24 h-24 bg-gray-700 rounded-lg border-2 border-blue-500 flex items-center justify-center mb-2 hover:border-cyan-500 transition-colors">
                    <LazyImage
                      src={item.image || '/placeholder-champion.svg'}
                      alt={item.name}
                      className="w-20 h-20 rounded"
                    />
                  </div>
                  <div className="text-xs text-gray-300">{item.name}</div>
                </div>
              </Tooltip>
            ))}
          </div>
        </div>

        {/* Summoner Spells */}
        <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-cyan-500/30">
          <h3 className="text-xl font-bold text-white text-center bg-gradient-to-r from-gray-700 to-gray-800 py-3 rounded-lg mb-6 border border-cyan-500/30">
            ✨ SUMMONER SPELLS
          </h3>
          <div className="text-sm text-gray-400 mb-4">
            If you want to use this {championData.champion.name.toUpperCase()} {championData.champion.lanes[0] || 'Mid'} build, you should take the following summoner spells for optimal performance.
          </div>
          <div className="flex justify-center gap-8">
            {championData.summoner_spells.slice(0, 3).map((spell, index) => (
              <Tooltip
                key={index}
                content={
                  <div className="text-white max-w-xs">
                    <h4 className="font-bold text-yellow-300 mb-2">{spell.name}</h4>
                    <p className="text-sm text-gray-300">{spell.description || 'Essential summoner spell for this champion'}</p>
                    {spell.cooldown && (
                      <div className="text-cyan-400 font-bold mt-2">Cooldown: {spell.cooldown}s</div>
                    )}
                  </div>
                }
              >
                <div className="text-center cursor-pointer">
                  <div className="w-24 h-24 bg-yellow-500 rounded-lg flex items-center justify-center mb-2 hover:bg-yellow-400 transition-colors">
                    <LazyImage
                      src={spell.image || '/placeholder-champion.svg'}
                      alt={spell.name}
                      className="w-20 h-20 rounded"
                    />
                  </div>
                  <div className="text-sm text-white font-bold">{spell.name}</div>
                </div>
              </Tooltip>
            ))}
          </div>
        </div>

        {/* Skills Order */}
        <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-yellow-500/30">
          <h3 className="text-xl font-bold text-yellow-300 text-center mb-6">⚔️ SKILLS ORDER</h3>
          <div className="text-sm text-gray-400 mb-4">
            For the skill order, you want to stick with [Q] > [W] > [E]. You can learn more about abilities order at all levels by studying the diagram below.
          </div>
          
          <div className="space-y-4">
            {Object.entries(championData.abilities).filter(([key]) => key !== 'passive').map(([key, ability]) => (
              <div key={key} className="flex items-center gap-4">
                <Tooltip
                  content={
                    <div className="text-white max-w-xs">
                      <h4 className="font-bold text-yellow-300 mb-2">{ability.name}</h4>
                      <p className="text-sm text-gray-300">{ability.description}</p>
                    </div>
                  }
                >
                  <div className="w-16 h-16 bg-blue-500 rounded-lg flex items-center justify-center cursor-pointer hover:bg-blue-400 transition-colors">
                    <LazyImage
                      src={ability.image}
                      alt={ability.name}
                      className="w-12 h-12 rounded"
                    />
                  </div>
                </Tooltip>
                <div className="flex-1">
                  <div className="text-white font-bold">[{key.toUpperCase()}] {ability.name}</div>
                  <div className="flex gap-1 mt-2">
                    {Array.from({ length: 15 }, (_, i) => (
                      <div
                        key={i}
                        className={`w-6 h-6 rounded text-xs flex items-center justify-center font-bold ${
                          (key === 'q' && [0, 2, 4, 7, 9].includes(i)) ||
                          (key === 'w' && [1, 8, 10, 12, 13].includes(i)) ||
                          (key === 'e' && [3, 11, 14].includes(i)) ||
                          (key === 'r' && [5, 6].includes(i))
                            ? 'bg-green-500 text-black'
                            : 'bg-gray-600 text-gray-400'
                        }`}
                      >
                        {i + 1}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <Layout currentPage={`/champion/${championData.champion.id}`}>
      <Head>
        <title>{`WILD RIFT: ${championData.champion.name.toUpperCase()} BUILD GUIDE`}</title>
        <meta
          name="description"
          content={`League of Legends: Wild Rift ${championData.champion.name.toUpperCase()}, role - ${getRoleTranslation(championData.champion.role)}. Use the guidelines to take your ${championData.champion.name.toUpperCase()} Wild Rift champion play style to the next level.`}
        />
        <meta property="og:image" content={championData.champion.image} />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900 relative overflow-hidden">
        {/* Background with champion splash art */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-15"
          style={{ backgroundImage: `url(${championData.champion.image})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-gray-900/85 via-slate-900/40 to-gray-900/90" />

        {/* Hero Section */}
        <div className="relative z-10 pt-20 pb-12">
          <div className="max-w-6xl mx-auto px-4">
            {/* Title */}
            <div className="text-center mb-12">
              <h1 className="text-4xl md:text-6xl font-black mb-4">
                <span className="text-white">WILD RIFT: </span>
                <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">{championData.champion.name.toUpperCase()}</span>
                <span className="text-white"> BUILD GUIDE</span>
              </h1>
            </div>

            {/* Champion Info Row */}
            <div className="flex flex-col lg:flex-row items-center gap-8 mb-8">
              {/* Champion Image */}
              <div className="relative">
                <div className="w-48 h-48 relative">
                  <div className="absolute -inset-3 bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 rounded-full opacity-75 blur"></div>
                  <div className="relative w-full h-full bg-gray-800/80 rounded-full border-4 border-cyan-500 overflow-hidden backdrop-blur-sm">
                    <LazyImage
                      src={championData.champion.image}
                      alt={championData.champion.name}
                      className="w-full h-full object-cover"
                    />
                    {/* Tier Badge */}
                    <div className="absolute top-2 left-2">
                      <div className={`px-3 py-1 rounded-lg font-black text-lg ${getTierColor(championData.meta.tier)} shadow-lg`}>
                        {championData.meta.tier}
                      </div>
                    </div>
                    {/* Buffed Badge */}
                    <div className="absolute top-2 right-2">
                      <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-2 py-1 rounded text-xs font-bold shadow-lg">
                        BUFFED ↑
                      </div>
                    </div>
                  </div>
                </div>
                {/* Win Rate and Views */}
                <div className="text-center mt-4">
                  <div className="flex items-center justify-center gap-4 mb-2">
                    <div className="bg-black/60 backdrop-blur-sm rounded-lg px-3 py-2 border border-cyan-500/30">
                      <span className="text-cyan-300 text-lg font-bold">{championData.meta.win_rate}</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-center gap-2">
                    <div className="bg-black/60 backdrop-blur-sm rounded-lg px-3 py-2 border border-yellow-500/30">
                      <span className="text-yellow-300">{championData.meta.views}</span>
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-2 rounded-lg font-bold text-sm mt-2 shadow-lg">
                    {championData.meta.patch}
                  </div>
                </div>
              </div>

              {/* Stats Circles */}
              <div className="flex-1">
                {renderStatCircles()}
                
                {/* Champion Description */}
                <div className="text-center text-gray-300 max-w-3xl mx-auto">
                  <p className="text-lg leading-relaxed">
                    League of Legends: Wild Rift <span className="text-green-400 font-bold">{championData.champion.name.toUpperCase()}</span>, role - <span className="text-blue-400 font-bold">{getRoleTranslation(championData.champion.role)}</span>. Use the guidelines to take your <span className="text-green-400 font-bold">{championData.champion.name.toUpperCase()}</span> Wild Rift champion play style to the next level. Study in detail the build of items, runes, spells, skills that need to be developed in the first place. In order to find out what position <span className="text-green-400 font-bold">{championData.champion.name.toUpperCase()}</span> is in the rating table, go to the - Tier List page.
                  </p>
                </div>

                {/* Meta Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                  <div className="text-center">
                    <div className="text-orange-400 text-2xl font-bold">52 [3.6]</div>
                    <div className="text-gray-400 text-sm">📊 0.75 [0]</div>
                    <div className="text-gray-400 text-sm">💎 355 [0]</div>
                    <div className="text-gray-400 text-sm">🔴 175 [0]</div>
                  </div>
                  <div className="text-center">
                    <div className="text-blue-400 text-2xl font-bold">630 [120]</div>
                    <div className="text-gray-400 text-sm">💙 435 [69]</div>
                    <div className="text-gray-400 text-sm">🟡 34 [4.5]</div>
                  </div>
                  <div className="text-center">
                    <div className="text-cyan-400 text-2xl font-bold">8 [0.7]</div>
                    <div className="text-gray-400 text-sm">⚡ 18 [1.1]</div>
                    <div className="text-gray-400 text-sm">🔵 36 [1.2]</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Abilities Row */}
            <div className="flex justify-center gap-4 mb-8">
              {Object.entries(championData.abilities).map(([key, ability]) => (
                <Tooltip
                  key={key}
                  content={
                    <div className="text-white max-w-xs">
                      <h4 className="font-bold text-yellow-300 mb-2">{ability.name}</h4>
                      <p className="text-sm text-gray-300">{ability.description}</p>
                    </div>
                  }
                >
                  <div className="relative cursor-pointer">
                    <div className="w-16 h-16 bg-slate-800 rounded-lg border-2 border-cyan-500 overflow-hidden hover:border-yellow-400 transition-colors">
                      <LazyImage
                        src={ability.image}
                        alt={ability.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -bottom-1 -right-1 bg-cyan-500 text-black w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold">
                      {key === 'passive' ? 'P' : key.toUpperCase()}
                    </div>
                  </div>
                </Tooltip>
              ))}
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="relative z-10">
          {renderTabs()}
        </div>

        {/* Content Section */}
        <div className="relative z-10 px-4 pb-12">
          <div className="max-w-6xl mx-auto">
            {/* Section Title */}
            <div className="text-center mb-8">
              <h2 className="text-3xl font-black text-white mb-4">
                ⚔️ MID {championData.champion.name.toUpperCase()} BUILD ITEMS AND RUNES
              </h2>
            </div>

            {/* Tab Content */}
            <div className="bg-black/60 backdrop-blur-sm rounded-2xl border border-cyan-500/30 p-8 shadow-2xl">
              {activeTab === 'BUILD' && renderBuildContent()}
              {activeTab === 'COUNTERS' && (
                <div className="text-center text-white">
                  <h3 className="text-2xl font-bold mb-4 text-cyan-300">🛡️ Champion Counters</h3>
                  <p className="text-gray-300">Counter information coming soon...</p>
                </div>
              )}
              {activeTab === 'TIPS' && (
                <div className="text-center text-white">
                  <h3 className="text-2xl font-bold mb-4 text-yellow-300">💡 Pro Tips</h3>
                  <div className="space-y-4 text-left max-w-4xl mx-auto">
                    <div className="bg-black/40 backdrop-blur-sm rounded-lg p-4 border border-cyan-500/30">
                      <p className="text-cyan-200">Focus on landing your skill combos for maximum damage output.</p>
                    </div>
                    <div className="bg-black/40 backdrop-blur-sm rounded-lg p-4 border border-purple-500/30">
                      <p className="text-purple-200">Position carefully in team fights to avoid being caught out.</p>
                    </div>
                    <div className="bg-black/40 backdrop-blur-sm rounded-lg p-4 border border-yellow-500/30">
                      <p className="text-yellow-200">Use your mobility to roam and help other lanes when possible.</p>
                    </div>
                  </div>
                </div>
              )}
              {/* Add other tab contents as needed */}
              {!['BUILD', 'COUNTERS', 'TIPS'].includes(activeTab) && (
                <div className="text-center text-white">
                  <h3 className="text-2xl font-bold mb-4 text-cyan-300">{activeTab}</h3>
                  <p className="text-gray-300">Content coming soon...</p>
                </div>
              )}
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