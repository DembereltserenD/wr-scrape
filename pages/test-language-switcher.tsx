import React from 'react';
import Head from 'next/head';
import { LanguageProvider, useLanguage } from '../contexts/LanguageContext';
import LanguageSwitcher from '../components/LanguageSwitcher';

const TestLanguageSwitcherContent: React.FC = () => {
    const { t, locale } = useLanguage();

    return (
        <div className="min-h-screen bg-background-dark text-text-primary">
            <Head>
                <title>Language Switcher Test</title>
            </Head>

            <div className="container mx-auto px-4 py-8">
                <div className="max-w-2xl mx-auto">
                    <h1 className="text-3xl font-bold mb-8 text-center">
                        Language Switcher Test
                    </h1>

                    {/* Language Switcher Test */}
                    <div className="bg-card-background rounded-lg p-6 mb-8">
                        <h2 className="text-xl font-semibold mb-4">Language Switcher Component</h2>
                        <div className="flex justify-center mb-4">
                            <LanguageSwitcher />
                        </div>
                        <p className="text-center text-text-secondary">
                            Current locale: <span className="text-primary-purple font-mono">{locale}</span>
                        </p>
                    </div>

                    {/* Translation Test */}
                    <div className="bg-card-background rounded-lg p-6 mb-8">
                        <h2 className="text-xl font-semibold mb-4">Translation Test</h2>
                        <div className="space-y-2">
                            <p><strong>Navigation Champion:</strong> {t('navigation.champion')}</p>
                            <p><strong>Navigation Tier List:</strong> {t('navigation.tierList')}</p>
                            <p><strong>Navigation Items:</strong> {t('navigation.items')}</p>
                            <p><strong>Hero Title:</strong> {t('hero.title')}</p>
                            <p><strong>Hero Description:</strong> {t('hero.description')}</p>
                            <p><strong>Sections Champions:</strong> {t('sections.champions')}</p>
                            <p><strong>Common Loading:</strong> {t('common.loading')}</p>
                        </div>
                    </div>

                    {/* Accessibility Test */}
                    <div className="bg-card-background rounded-lg p-6">
                        <h2 className="text-xl font-semibold mb-4">Accessibility Features</h2>
                        <ul className="space-y-2 text-text-secondary">
                            <li>✅ Keyboard navigation (Tab, Enter, Escape)</li>
                            <li>✅ Screen reader support with ARIA labels</li>
                            <li>✅ Focus management and indicators</li>
                            <li>✅ Smooth transition animations</li>
                            <li>✅ Gaming theme styling</li>
                            <li>✅ Click outside to close</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

const TestLanguageSwitcher: React.FC = () => {
    return (
        <LanguageProvider>
            <TestLanguageSwitcherContent />
        </LanguageProvider>
    );
};

export default TestLanguageSwitcher;