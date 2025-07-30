import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Import translation files
import mnTranslations from '../locales/mn.json';
import enTranslations from '../locales/en.json';

// Define supported locales
export type Locale = 'mn' | 'en';

// Language context interface
export interface LanguageContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: string, params?: Record<string, string | number>) => string;
  isLoading: boolean;
}

// Game terminology that remains in English
export const GAME_TERMS = {
  // Champion names remain in English
  championNames: true,
  // Item names remain in English  
  itemNames: true,
  // Game stats remain in English
  stats: {
    HP: 'HP',
    AP: 'AP',
    AD: 'AD',
    MP: 'MP',
    'Attack Speed': 'Attack Speed',
    'Critical Strike': 'Critical Strike',
    'Armor Penetration': 'Armor Penetration',
    'Magic Penetration': 'Magic Penetration',
    'Life Steal': 'Life Steal',
    'Spell Vamp': 'Spell Vamp',
    'Cooldown Reduction': 'Cooldown Reduction',
    'Movement Speed': 'Movement Speed',
    'True Damage': 'True Damage',
    'Physical Damage': 'Physical Damage',
    'Magic Damage': 'Magic Damage',
    'Stack': 'Stack',
    'Passive': 'Passive',
    'Active': 'Active',
    'Ultimate': 'Ultimate',
    'Ability Power': 'Ability Power',
    'Attack Damage': 'Attack Damage',
    'Health': 'Health',
    'Mana': 'Mana',
    'Armor': 'Armor',
    'Magic Resistance': 'Magic Resistance'
  }
};

// Create context
const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Provider props interface
interface LanguageProviderProps {
  children: ReactNode;
  initialLocale?: Locale;
}

// Translation data from JSON files
const translations = {
  mn: mnTranslations,
  en: enTranslations,
};

// Language provider component
export const LanguageProvider: React.FC<LanguageProviderProps> = ({
  children,
  initialLocale = 'mn'
}) => {
  const [locale, setLocaleState] = useState<Locale>(initialLocale);
  const [isLoading, setIsLoading] = useState(true);

  // Load locale from localStorage on mount
  useEffect(() => {
    const savedLocale = localStorage.getItem('preferred-locale') as Locale;
    if (savedLocale && (savedLocale === 'mn' || savedLocale === 'en')) {
      setLocaleState(savedLocale);
    }
    setIsLoading(false);
  }, []);

  // Save locale to localStorage when changed
  const setLocale = (newLocale: Locale) => {
    setLocaleState(newLocale);
    localStorage.setItem('preferred-locale', newLocale);
  };

  // Translation function with fallback handling
  const t = (key: string, params?: Record<string, string | number>): string => {
    try {
      // Get nested translation value
      const keys = key.split('.');
      let value: any = translations[locale];

      for (const k of keys) {
        value = value?.[k];
      }

      // Fallback to English if translation not found
      if (value === undefined && locale !== 'en') {
        let fallbackValue: any = translations.en;
        for (const k of keys) {
          fallbackValue = fallbackValue?.[k];
        }
        value = fallbackValue;
      }

      // If still not found, return the key
      if (value === undefined) {
        console.warn(`Translation key not found: ${key}`);
        return key;
      }

      let result = String(value);

      // Replace parameters if provided
      if (params) {
        Object.entries(params).forEach(([param, paramValue]) => {
          result = result.replace(`{{${param}}}`, String(paramValue));
        });
      }

      return result;
    } catch (error) {
      console.error(`Error translating key "${key}":`, error);
      return key;
    }
  };

  const contextValue: LanguageContextType = {
    locale,
    setLocale,
    t,
    isLoading
  };

  return (
    <LanguageContext.Provider value={contextValue}>
      {children}
    </LanguageContext.Provider>
  );
};

// Hook to use language context
export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Helper function to check if a term should remain in English
export const isGameTerm = (term: string): boolean => {
  return Object.values(GAME_TERMS.stats).includes(term) ||
    GAME_TERMS.championNames ||
    GAME_TERMS.itemNames;
};

// Helper function to get game stat color
export const getGameStatColor = (stat: string): string => {
  const statColors: Record<string, string> = {
    'HP': 'text-green-600',
    'Health': 'text-green-600',
    'AP': 'text-blue-600',
    'Ability Power': 'text-blue-600',
    'AD': 'text-red-600',
    'Attack Damage': 'text-red-600',
    'MP': 'text-blue-400',
    'Mana': 'text-blue-400',
    'Armor': 'text-yellow-600',
    'Magic Resistance': 'text-purple-600',
    'Movement Speed': 'text-gray-600',
    'Attack Speed': 'text-orange-600',
    'Critical Strike': 'text-yellow-500',
    'Life Steal': 'text-red-400',
    'Spell Vamp': 'text-purple-400',
    'True Damage': 'text-white',
    'Physical Damage': 'text-red-500',
    'Magic Damage': 'text-blue-500'
  };

  return statColors[stat] || 'text-gray-600';
};