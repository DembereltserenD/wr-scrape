import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useLanguage } from '../contexts/LanguageContext';
import { ChampionData } from '../types/champion';

interface RuneInfo {
    name: string;
    tree: string;
    usage: number;
    type: 'keystone' | 'primary' | 'secondary';
}

interface RunesSectionProps {
    champions: ChampionData[];
    showPatchInfo?: boolean;
    maxDisplayed?: number;
}

const RunesSection: React.FC<RunesSectionProps> = ({
    champions,
    showPatchInfo = true,
    maxDisplayed = 4
}) => {
    const { t, locale } = useLanguage();
    const [popularRunes, setPopularRunes] = useState<RuneInfo[]>([]);

    useEffect(() => {
        const loadPopularRunes = () => {
            const runeUsage: Record<string, { count: number; tree: string; type: 'keystone' | 'primary' | 'secondary' }> = {};

            // Count rune usage across all champions
            champions.forEach(champion => {
                if (champion.runes) {
                    // Count keystone
                    if (champion.runes.primary?.keystone) {
                        const keystone = champion.runes.primary.keystone;
                        if (!runeUsage[keystone]) {
                            runeUsage[keystone] = {
                                count: 0,
                                tree: champion.runes.primary.tree || 'Unknown',
                                type: 'keystone'
                            };
                        }
                        runeUsage[keystone].count++;
                    }

                    // Count primary runes
                    if (champion.runes.primary?.runes) {
                        champion.runes.primary.runes.forEach(rune => {
                            if (!runeUsage[rune]) {
                                runeUsage[rune] = {
                                    count: 0,
                                    tree: champion.runes.primary.tree || 'Unknown',
                                    type: 'primary'
                                };
                            }
                            runeUsage[rune].count++;
                        });
                    }

                    // Count secondary runes
                    if (champion.runes.secondary?.runes) {
                        champion.runes.secondary.runes.forEach(rune => {
                            if (!runeUsage[rune]) {
                                runeUsage[rune] = {
                                    count: 0,
                                    tree: champion.runes.secondary.tree || 'Unknown',
                                    type: 'secondary'
                                };
                            }
                            runeUsage[rune].count++;
                        });
                    }
                }
            });

            // Convert to array and sort by usage
            const sortedRunes = Object.entries(runeUsage)
                .map(([name, data]) => ({
                    name,
                    tree: data.tree,
                    usage: data.count,
                    type: data.type
                }))
                .sort((a, b) => b.usage - a.usage)
                .slice(0, maxDisplayed);

            setPopularRunes(sortedRunes);
        };

        loadPopularRunes();
    }, [champions, maxDisplayed]);

    const getTreeColor = (tree: string) => {
        switch (tree.toLowerCase()) {
            case 'precision': return 'text-yellow-500';
            case 'domination': return 'text-red-500';
            case 'sorcery': return 'text-blue-500';
            case 'resolve': return 'text-green-500';
            case 'inspiration': return 'text-purple-500';
            default: return 'text-gray-500';
        }
    };

    const getTreeIcon = (tree: string) => {
        switch (tree.toLowerCase()) {
            case 'precision': return '⚔️';
            case 'domination': return '🗡️';
            case 'sorcery': return '🔮';
            case 'resolve': return '🛡️';
            case 'inspiration': return '💡';
            default: return '🔸';
        }
    };

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'keystone': return '👑';
            case 'primary': return '🔹';
            case 'secondary': return '🔸';
            default: return '⭐';
        }
    };



    return (
        <section className="bg-card-background rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
                <h2 className="responsive-heading-3 text-white">
                    {t('sections.runes')}
                </h2>
                {showPatchInfo && (
                    <span className="bg-primary-purple text-white px-3 py-1 rounded-full text-sm font-medium">
                        Patch 6.2b
                    </span>
                )}
            </div>

            <div className="responsive-grid-2 mb-6">
                {popularRunes.map((rune) => (
                    <div
                        key={rune.name}
                        className="bg-background-dark rounded-lg p-4 hover:bg-primary-purple/20 transition-colors cursor-pointer group"
                    >
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                                <span className="text-lg">{getTreeIcon(rune.tree)}</span>
                                <span className="text-xs">{getTypeIcon(rune.type)}</span>
                            </div>
                            <span className="text-accent-gold text-xs font-medium">
                                {rune.usage} uses
                            </span>
                        </div>

                        <h3 className="text-white font-semibold text-sm mb-1 group-hover:text-primary-purple transition-colors">
                            {rune.name}
                        </h3>

                        <div className="flex items-center justify-between">
                            <span className={`text-xs font-medium ${getTreeColor(rune.tree)}`}>
                                {rune.tree}
                            </span>
                            <span className="text-xs text-text-secondary capitalize">
                                {rune.type}
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="text-center">
                <Link href="/runes" className="gaming-button text-white inline-flex items-center">
                    {t('sections.viewAll')}
                    <svg
                        className="w-4 h-4 ml-2"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M13 7l5 5m0 0l-5 5m5-5H6"
                        />
                    </svg>
                </Link>
            </div>

            <div className="mt-4 text-center">
                <p className="responsive-caption text-text-secondary">
                    {locale === 'mn'
                        ? 'Хамгийн түгээмэл хэрэглэгддэг рунууд'
                        : 'Most popular runes across all champions'}
                </p>
            </div>
        </section>
    );
};

export default RunesSection;