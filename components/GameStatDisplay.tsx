import React from 'react';
import { formatStatDisplay, getStatColor, getStatBgColor, isGameTerm } from '../utils/gameTerms';

interface GameStatDisplayProps {
  statKey: string;
  value: number | string;
  showAbbreviation?: boolean;
  variant?: 'text' | 'badge' | 'inline';
  className?: string;
}

const GameStatDisplay: React.FC<GameStatDisplayProps> = ({
  statKey,
  value,
  showAbbreviation = false,
  variant = 'text',
  className = ''
}) => {
  const { displayText, colorClass, bgColorClass } = formatStatDisplay(statKey, value, showAbbreviation);

  switch (variant) {
    case 'badge':
      return (
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${bgColorClass} ${className}`}>
          {displayText}
        </span>
      );
    
    case 'inline':
      return (
        <span className={`font-semibold ${colorClass} ${className}`}>
          {displayText}
        </span>
      );
    
    default:
      return (
        <div className={`flex items-center space-x-2 ${className}`}>
          <span className={`font-semibold ${colorClass}`}>
            {value}
          </span>
          <span className="text-sm text-gray-600">
            {showAbbreviation ? statKey.toUpperCase() : statKey}
          </span>
        </div>
      );
  }
};

export default GameStatDisplay;

// Component for displaying multiple stats
interface GameStatsGridProps {
  stats: Record<string, number | string>;
  showAbbreviations?: boolean;
  variant?: 'text' | 'badge' | 'inline';
  className?: string;
}

export const GameStatsGrid: React.FC<GameStatsGridProps> = ({
  stats,
  showAbbreviations = false,
  variant = 'text',
  className = ''
}) => {
  return (
    <div className={`grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 ${className}`}>
      {Object.entries(stats).map(([statKey, value]) => (
        <GameStatDisplay
          key={statKey}
          statKey={statKey}
          value={value}
          showAbbreviation={showAbbreviations}
          variant={variant}
        />
      ))}
    </div>
  );
};

// Component for tier display
interface TierDisplayProps {
  tier: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const TierDisplay: React.FC<TierDisplayProps> = ({
  tier,
  size = 'md',
  className = ''
}) => {
  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base'
  };

  const getTierColor = (tier: string): string => {
    const tierColors: Record<string, string> = {
      'S+': 'bg-gradient-to-r from-red-500 to-pink-500 text-white',
      'S': 'bg-red-500 text-white',
      'A': 'bg-orange-500 text-white',
      'B': 'bg-yellow-500 text-white',
      'C': 'bg-green-500 text-white',
      'D': 'bg-blue-500 text-white'
    };
    return tierColors[tier] || 'bg-gray-500 text-white';
  };

  return (
    <span className={`inline-flex items-center rounded font-bold ${sizeClasses[size]} ${getTierColor(tier)} ${className}`}>
      {tier}
    </span>
  );
};