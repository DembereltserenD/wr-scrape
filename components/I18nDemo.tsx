import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import GameStatDisplay, { GameStatsGrid, TierDisplay } from './GameStatDisplay';
import { GAME_TERMS } from '../utils/gameTerms';

const I18nDemo: React.FC = () => {
    const { t, locale } = useLanguage();

    const sampleStats = {
        HP: 580,
        AD: 68,
        AP: 0,
        ARMOR: 33,
        MAGIC_RESISTANCE: 32,
        MOVEMENT_SPEED: 345,
        ATTACK_SPEED: 0.625
    };

    return (
        <div className="p-6 bg-white rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-4">
                {t('sections.champions')} - {locale === 'mn' ? 'Монгол' : 'English'}
            </h2>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">{t('navigation.home')} Navigation:</h3>
                <div className="flex space-x-4">
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                        {t('navigation.champion')}
                    </span>
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                        {t('navigation.tierList')}
                    </span>
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                        {t('navigation.items')}
                    </span>
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                        {t('navigation.comment')}
                    </span>
                </div>
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Hero Section:</h3>
                <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4 rounded">
                    <h4 className="text-xl font-bold">{t('hero.title')}</h4>
                    <p className="mb-3">{t('hero.description')}</p>
                    <div className="flex space-x-3">
                        <button className="px-4 py-2 bg-white text-purple-600 rounded font-medium">
                            {t('hero.viewChampions')}
                        </button>
                        <button className="px-4 py-2 bg-purple-700 text-white rounded font-medium">
                            {t('hero.tierList')}
                        </button>
                    </div>
                </div>
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Sections:</h3>
                <div className="grid grid-cols-3 gap-4">
                    <div className="text-center p-4 border rounded">
                        <h4 className="font-semibold">{t('sections.champions')}</h4>
                        <p className="text-sm text-gray-600">{t('sections.patch')}</p>
                        <button className="mt-2 text-blue-600 text-sm">
                            {t('sections.details')}
                        </button>
                    </div>
                    <div className="text-center p-4 border rounded">
                        <h4 className="font-semibold">{t('sections.items')}</h4>
                        <p className="text-sm text-gray-600">{t('sections.patch')}</p>
                        <button className="mt-2 text-blue-600 text-sm">
                            {t('sections.details')}
                        </button>
                    </div>
                    <div className="text-center p-4 border rounded">
                        <h4 className="font-semibold">{t('sections.runes')}</h4>
                        <p className="text-sm text-gray-600">{t('sections.patch')}</p>
                        <button className="mt-2 text-blue-600 text-sm">
                            {t('sections.details')}
                        </button>
                    </div>
                </div>
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Tier Roles:</h3>
                <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-red-100 text-red-800 rounded">
                        {t('tier_roles.strongest')}
                    </span>
                    <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded">
                        {t('tier_roles.strong')}
                    </span>
                    <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded">
                        {t('tier_roles.good')}
                    </span>
                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded">
                        {t('tier_roles.average')}
                    </span>
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                        {t('tier_roles.weak')}
                    </span>
                </div>
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">
                    Game Stats (Always English):
                </h3>
                <GameStatsGrid
                    stats={sampleStats}
                    variant="badge"
                    showAbbreviations={true}
                />
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">
                    Game Terms (Always English):
                </h3>
                <div className="flex flex-wrap gap-2">
                    <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm font-medium">
                        {GAME_TERMS.PASSIVE}
                    </span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm font-medium">
                        {GAME_TERMS.ACTIVE}
                    </span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm font-medium">
                        {GAME_TERMS.ULTIMATE}
                    </span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm font-medium">
                        {GAME_TERMS.TRUE_DAMAGE}
                    </span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm font-medium">
                        {GAME_TERMS.STACK}
                    </span>
                </div>
            </div>

            <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Tier Display:</h3>
                <div className="flex space-x-2">
                    <TierDisplay tier="S+" size="sm" />
                    <TierDisplay tier="S" size="md" />
                    <TierDisplay tier="A" size="lg" />
                    <TierDisplay tier="B" />
                    <TierDisplay tier="C" />
                    <TierDisplay tier="D" />
                </div>
            </div>

            <div className="bg-gray-800 text-white p-4 rounded">
                <p className="text-sm">{t('footer.copyright')}</p>
                <p className="text-xs text-gray-400 mt-1">{t('footer.disclaimer')}</p>
            </div>
        </div>
    );
};

export default I18nDemo;