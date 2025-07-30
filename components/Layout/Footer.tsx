import React from 'react';
import Link from 'next/link';
import { useLanguage } from '../../contexts/LanguageContext';

const Footer: React.FC = () => {
    const { t } = useLanguage();

    const navigationLinks = [
        {
            key: 'home',
            label: t('navigation.home'),
            href: '/',
        },
        {
            key: 'champions',
            label: t('navigation.champions'),
            href: '/champions',
        },
        {
            key: 'tierList',
            label: t('navigation.tierList'),
            href: '/tier-list',
        },
        {
            key: 'items',
            label: t('navigation.items'),
            href: '/items',
        },
        {
            key: 'runes',
            label: t('navigation.runes'),
            href: '/runes',
        },
    ];

    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-dark-purple border-t border-primary-purple/30 mt-auto">
            <div className="container mx-auto px-4 py-8">
                {/* Main Footer Content */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-8">
                    {/* Brand Section */}
                    <div className="space-y-4">
                        <div className="flex items-center space-x-2">
                            <div className="w-8 h-8 bg-gradient-to-br from-primary-purple to-accent-pink rounded-lg flex items-center justify-center">
                                <span className="text-white font-bold text-sm">WR</span>
                            </div>
                            <span className="text-text-primary font-bold text-xl">
                                Wild Rift Guide
                            </span>
                        </div>
                        <p className="text-text-secondary text-sm leading-relaxed">
                            {t('hero.description')}
                        </p>
                    </div>

                    {/* Navigation Links */}
                    <div className="space-y-4">
                        <h3 className="text-text-primary font-semibold text-lg">
                            {t('footer.navigation_title')}
                        </h3>
                        <nav className="flex flex-col space-y-2">
                            {navigationLinks.map((link) => (
                                <Link
                                    key={link.key}
                                    href={link.href}
                                    className="text-text-secondary hover:text-primary-purple transition-colors duration-200 text-sm"
                                >
                                    {link.label}
                                </Link>
                            ))}
                        </nav>
                    </div>

                    {/* Additional Info */}
                    <div className="space-y-4">
                        <h3 className="text-text-primary font-semibold text-lg">
                            {t('footer.info_title')}
                        </h3>
                        <div className="space-y-3">
                            <div className="inline-flex items-center px-3 py-1 rounded-full bg-primary-purple/20 border border-primary-purple/40">
                                <span className="text-primary-purple text-sm font-medium">
                                    {t('sections.patch')}
                                </span>
                            </div>
                            <p className="text-text-secondary text-sm leading-relaxed">
                                {t('footer.disclaimer')}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Bottom Section */}
                <div className="pt-8 border-t border-primary-purple/20">
                    <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
                        {/* Copyright */}
                        <div className="text-text-secondary text-sm text-center md:text-left">
                            {t('footer.copyright').replace('2024', currentYear.toString())}
                        </div>

                        {/* Made with love */}
                        <div className="flex items-center space-x-4">
                            <div className="text-text-secondary text-sm">
                                {t('footer.made_with_love')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;