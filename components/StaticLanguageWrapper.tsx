import React, { ReactNode } from 'react';
import { LanguageProvider, Locale } from '../contexts/LanguageContext';

interface StaticLanguageWrapperProps {
    children: ReactNode;
    locale: Locale;
}

/**
 * Wrapper component for static pages that need language context
 * This provides the LanguageProvider with a fixed locale for SSG/SSR
 */
export const StaticLanguageWrapper: React.FC<StaticLanguageWrapperProps> = ({
    children,
    locale
}) => {
    return (
        <LanguageProvider initialLocale={locale}>
            {children}
        </LanguageProvider>
    );
};

export default StaticLanguageWrapper;