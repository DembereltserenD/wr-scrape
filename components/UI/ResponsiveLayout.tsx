import React from 'react';

interface ResponsiveLayoutProps {
    children: React.ReactNode;
    className?: string;
    variant?: 'container' | 'section' | 'grid' | 'flex';
    gridCols?: 1 | 2 | 3 | 4 | 5;
    spacing?: 'compact' | 'comfortable' | 'spacious';
}

const ResponsiveLayout: React.FC<ResponsiveLayoutProps> = ({
    children,
    className = '',
    variant = 'container',
    gridCols = 3,
    spacing = 'comfortable'
}) => {
    const getBaseClasses = () => {
        switch (variant) {
            case 'container':
                return 'responsive-container';
            case 'section':
                return 'responsive-section';
            case 'grid':
                return getGridClasses();
            case 'flex':
                return 'responsive-flex-center';
            default:
                return '';
        }
    };

    const getGridClasses = () => {
        const gridClass = `responsive-grid-${gridCols}`;
        const spacingClass = spacing === 'compact' ? 'gap-3 xs:gap-4' :
            spacing === 'comfortable' ? 'gap-4 xs:gap-5 sm:gap-6' :
                'gap-6 xs:gap-7 sm:gap-8 md:gap-10';
        return `${gridClass} ${spacingClass}`;
    };

    const getSpacingClasses = () => {
        switch (spacing) {
            case 'compact':
                return 'p-3 xs:p-4 sm:p-5';
            case 'comfortable':
                return 'p-4 xs:p-5 sm:p-6 md:p-8';
            case 'spacious':
                return 'p-6 xs:p-7 sm:p-8 md:p-10 lg:p-12';
            default:
                return '';
        }
    };

    const combinedClasses = `${getBaseClasses()} ${getSpacingClasses()} ${className}`.trim();

    return (
        <div className={combinedClasses}>
            {children}
        </div>
    );
};

export default ResponsiveLayout;