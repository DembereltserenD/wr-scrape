import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useLanguage } from '../contexts/LanguageContext';
import { ChampionData, ChampionCard as ChampionCardType } from '../types/champion';
import ChampionCard from './ChampionCard';
import Dropdown, { DropdownOption } from './UI/Dropdown';
import PatchInfo from './PatchInfo';

interface ChampionsSectionProps {
    champions: ChampionData[];
    showPatchInfo?: boolean;
    maxDisplayed?: number;
}

const ChampionsSection: React.FC<ChampionsSectionProps> = ({
    champions,
    showPatchInfo = true,
    maxDisplayed = 8
}) => {
    const { t, locale } = useLanguage();
    const [selectedLane, setSelectedLane] = useState<string>('all');
    const [filteredChampions, setFilteredChampions] = useState<ChampionCardType[]>([]);

    const convertToChampionCard = (championData: ChampionData): ChampionCardType | null => {
        if (!championData?.champion?.id || !championData?.champion?.name) {
            console.warn('Invalid champion data:', championData);
            return null;
        }

        return {
            id: championData.champion.id,
            name: championData.champion.name,
            role: championData.champion.role || 'Unknown',
            tier: championData.champion.tier || 'C',
            image: championData.champion.image || '/placeholder-champion.png',
            lanes: championData.champion.lanes || [],
            difficulty: championData.champion.difficulty || 'Medium',
            winRate: championData.meta?.win_rate,
            pickRate: championData.meta?.pick_rate
        };
    };

    const laneOptions: DropdownOption[] = [
        { value: 'all', label: t('common.filter') },
        { value: 'Baron', label: 'Baron Lane' },
        { value: 'Mid', label: 'Mid Lane' },
        { value: 'Jungle', label: 'Jungle' },
        { value: 'Dragon', label: 'Dragon Lane (ADC)' },
        { value: 'Support', label: 'Support' }
    ];

    useEffect(() => {
        let filtered = champions.map(convertToChampionCard).filter((champion): champion is ChampionCardType => champion !== null);

        if (selectedLane !== 'all') {
            filtered = filtered.filter(champion => {
                return champion.lanes.some(lane =>
                    lane === selectedLane ||
                    lane.toLowerCase().includes(selectedLane.toLowerCase()) ||
                    (selectedLane === 'Dragon' && lane.toLowerCase().includes('dragon')) ||
                    (selectedLane === 'Baron' && lane.toLowerCase().includes('baron'))
                );
            });
        }

        filtered.sort((a, b) => a.name.localeCompare(b.name));

        if (maxDisplayed > 0) {
            filtered = filtered.slice(0, maxDisplayed);
        }

        setFilteredChampions(filtered);
    }, [champions, selectedLane, maxDisplayed]);
    return (
        <section>
            <div>
                <div>
                    <div>
                        <div>
                            <h2>
                                {t('sections.champions')}
                            </h2>
                            {showPatchInfo && (
                                <PatchInfo showLink={true} />
                            )}
                        </div>
                        {showPatchInfo && (
                            <p>
                                {locale === 'mn'
                                    ? 'Одоогийн мета дэх баатруудын зэрэглэл'
                                    : 'Current meta champion rankings'}
                            </p>
                        )}
                    </div>

                    <div>
                        <div>
                            <Dropdown
                                options={laneOptions}
                                value={selectedLane}
                                onChange={setSelectedLane}
                                placeholder="Filter by Lane"
                            />
                        </div>
                        {selectedLane !== 'all' && (
                            <button
                                onClick={() => setSelectedLane('all')}
                            >
                                {locale === 'mn' ? 'Цэвэрлэх' : 'Clear Filter'}
                            </button>
                        )}
                    </div>
                </div>

                {filteredChampions.length > 0 ? (
                    <div>
                        {filteredChampions.map((champion) => (
                            <ChampionCard
                                key={champion.id}
                                champion={champion}
                            />
                        ))}
                    </div>
                ) : (
                    <div>
                        <p>
                            {locale === 'mn'
                                ? 'Сонгосон lane-д тохирох баатар олдсонгүй.'
                                : 'No champions found for the selected lane.'}
                        </p>
                    </div>
                )}

                <div>
                    <Link href="/champions">
                        <span>
                            {t('common.viewAll')} {t('sections.champions')}
                        </span>
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                    </Link>
                </div>
            </div>
        </section>
    );
};

export default ChampionsSection;