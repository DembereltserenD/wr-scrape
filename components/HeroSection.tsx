import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

interface HeroSectionProps {
    onViewChampions?: () => void;
    onViewTierList?: () => void;
}

const HeroSection: React.FC<HeroSectionProps> = ({
    onViewChampions,
    onViewTierList
}) => {
    const { t } = useLanguage();

    const handleViewChampions = () => {
        if (onViewChampions) {
            onViewChampions();
        } else {
            window.location.href = '/champions';
        }
    };

    const handleViewTierList = () => {
        if (onViewTierList) {
            onViewTierList();
        } else {
            window.location.href = '/tier-list';
        }
    };

    return (
        <section>
            <div>
                <h1>
                    <span>
                        {t('hero.title')}
                    </span>
                </h1>

                <p>
                    {t('hero.description')}
                </p>

                <div>
                    <button
                        onClick={handleViewChampions}
                        aria-label={t('hero.viewChampions')}
                    >
                        <span>
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            <span>{t('hero.viewChampions')}</span>
                        </span>
                    </button>

                    <button
                        onClick={handleViewTierList}
                        aria-label={t('hero.tierList')}
                    >
                        <span>
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                            <span>{t('hero.tierList')}</span>
                        </span>
                    </button>
                </div>

                <div>
                    <div>
                        {t('sections.patch')}
                    </div>
                </div>
            </div>
        </section>
    );
};

export default HeroSection;