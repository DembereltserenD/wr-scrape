import { useRouter } from 'next/router';
import { useCallback } from 'react';

// Import translation files
import mnTranslations from '../locales/mn.json';
import enTranslations from '../locales/en.json';

export type Locale = 'mn' | 'en';

export const translations = {
  mn: mnTranslations,
  en: enTranslations,
};

export const locales: Locale[] = ['mn', 'en'];

export const defaultLocale: Locale = 'mn';

// Language names for display
export const languageNames = {
  mn: 'Монгол',
  en: 'English',
};

// Language flags/icons
export const languageFlags = {
  mn: '🇲🇳',
  en: '🇺🇸',
};

// Get nested translation value
export function getNestedTranslation(obj: any, path: string): string {
  return path.split('.').reduce((current, key) => current?.[key], obj) || path;
}

// Translation hook
export function useTranslation() {
  const router = useRouter();
  const locale = (router.locale as Locale) || defaultLocale;

  const t = useCallback((key: string, params?: Record<string, string | number>): string => {
    const translation = getNestedTranslation(translations[locale], key);
    
    if (!params) return translation;

    // Replace parameters in translation
    return Object.entries(params).reduce(
      (text, [param, value]) => text.replace(`{{${param}}}`, String(value)),
      translation
    );
  }, [locale]);

  const changeLanguage = useCallback((newLocale: Locale) => {
    const { pathname, asPath, query } = router;
    router.push({ pathname, query }, asPath, { locale: newLocale });
  }, [router]);

  return {
    t,
    locale,
    changeLanguage,
    isRTL: false, // Neither Mongolian nor English are RTL
  };
}

// Get static translations for SSG/SSR
export function getStaticTranslations(locale: Locale) {
  return translations[locale] || translations[defaultLocale];
}

// Format numbers according to locale
export function formatNumber(number: number, locale: Locale): string {
  return new Intl.NumberFormat(locale === 'mn' ? 'mn-MN' : 'en-US').format(number);
}

// Format dates according to locale
export function formatDate(date: Date, locale: Locale): string {
  return new Intl.DateTimeFormat(locale === 'mn' ? 'mn-MN' : 'en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
}

// Get localized champion data
export function getLocalizedChampionData(championData: any, locale: Locale) {
  // For now, return original data
  // In the future, you could have localized champion names, descriptions, etc.
  return championData;
}
