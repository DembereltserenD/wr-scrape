import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useLanguage } from '../contexts/LanguageContext';
import { Item, ItemCard } from '../types/item';

interface ItemsSectionProps {
    items: Item[];
    showPatchInfo?: boolean;
    maxDisplayed?: number;
}

const ItemsSection: React.FC<ItemsSectionProps> = ({
    items: allItems,
    showPatchInfo = true,
    maxDisplayed = 6
}) => {
    const { t } = useLanguage();
    const [displayItems, setDisplayItems] = useState<ItemCard[]>([]);

    useEffect(() => {
        // Convert to ItemCard format and filter for top tier items
        const itemCards: ItemCard[] = allItems
            .filter((item: Item) => item.tier === 'S' || item.tier === 'A')
            .map((item: Item) => ({
                name: item.name,
                cost: item.cost,
                tier: item.tier,
                category: item.category,
                stats: item.stats,
                passive: item.passive
            }))
            .sort((a: ItemCard, b: ItemCard) => {
                // Sort by tier (S > A) then by cost (higher first)
                if (a.tier !== b.tier) {
                    return a.tier === 'S' ? -1 : 1;
                }
                return b.cost - a.cost;
            })
            .slice(0, maxDisplayed);

        setDisplayItems(itemCards);
    }, [allItems, maxDisplayed]);

    const getTierColor = (tier: string) => {
        switch (tier) {
            case 'S': return 'text-red-500';
            case 'A': return 'text-orange-500';
            case 'B': return 'text-yellow-500';
            case 'C': return 'text-green-500';
            default: return 'text-gray-500';
        }
    };

    const getCategoryIcon = (category: string) => {
        switch (category) {
            case 'legendary': return '⚔️';
            case 'mythic': return '🔮';
            case 'boots': return '👢';
            case 'enchant': return '✨';
            default: return '🛡️';
        }
    };



    return (
        <section className="bg-card-background rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
                <h2 className="responsive-heading-3 text-white">
                    {t('sections.items')}
                </h2>
                {showPatchInfo && (
                    <span className="bg-primary-purple text-white px-3 py-1 rounded-full text-sm font-medium">
                        Patch 6.2b
                    </span>
                )}
            </div>

            <div className="responsive-grid-2 mb-6">
                {displayItems.map((item) => (
                    <div
                        key={item.name}
                        className="bg-background-dark rounded-lg p-4 hover:bg-primary-purple/20 transition-colors cursor-pointer group"
                    >
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                                <span className="text-lg">{getCategoryIcon(item.category)}</span>
                                <span className={`text-sm font-bold ${getTierColor(item.tier)}`}>
                                    {item.tier}
                                </span>
                            </div>
                            <span className="text-accent-gold text-sm font-medium">
                                {item.cost}g
                            </span>
                        </div>

                        <h3 className="text-white font-semibold text-sm mb-2 group-hover:text-primary-purple transition-colors">
                            {item.name}
                        </h3>

                        <div className="text-xs text-text-secondary">
                            {Object.entries(item.stats).slice(0, 2).map(([stat, data]) => (
                                <div key={stat} className="flex justify-between">
                                    <span className="capitalize">{stat.replace('_', ' ')}</span>
                                    <span>
                                        {data.type === 'percentage' ? `${data.value}%` : `+${data.value}`}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            <div className="text-center">
                <Link href="/items" className="gaming-button text-white inline-flex items-center">
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
        </section>
    );
};

export default ItemsSection;