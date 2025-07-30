import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useLanguage } from '../../contexts/LanguageContext';
import LanguageSwitcher from '../LanguageSwitcher';

interface HeaderProps {
    currentPage?: string;
}

const Header: React.FC<HeaderProps> = ({ currentPage }) => {
    const { t } = useLanguage();
    const router = useRouter();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [isScrolled, setIsScrolled] = useState(false);

    // Handle scroll effect for header styling
    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 10);
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Close mobile menu when route changes
    useEffect(() => {
        setIsMobileMenuOpen(false);
    }, [router.asPath]);

    // Navigation items
    const navigationItems = [
        {
            key: 'home',
            label: t('navigation.home'),
            href: '/',
        },
        {
            key: 'champion',
            label: t('navigation.champion'),
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
            key: 'comment',
            label: t('navigation.comment'),
            href: '/comments',
        },
    ];

    // Check if current route is active
    const isActiveRoute = (href: string): boolean => {
        if (href === '/' && router.pathname === '/') return true;
        if (href !== '/' && router.pathname.startsWith(href)) return true;
        return currentPage === href;
    };

    // Toggle mobile menu
    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

    return (
        <header
            className={`sticky top-0 z-50 transition-all duration-300 ${isScrolled
                ? 'bg-dark-purple/95 backdrop-blur-md shadow-lg'
                : 'bg-dark-purple'
                }`}
        >
            <div className="container mx-auto px-4">
                <div className="flex items-center justify-between h-16">
                    {/* Logo/Brand */}
                    <Link href="/" className="flex items-center space-x-2 group">
                        <div className="w-8 h-8 bg-gradient-to-br from-primary-purple to-accent-pink rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold text-sm">WR</span>
                        </div>
                        <span className="text-text-primary font-bold text-xl group-hover:text-text-secondary transition-colors">
                            Wild Rift
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex items-center space-x-1">
                        {navigationItems.map((item) => (
                            <Link
                                key={item.key}
                                href={item.href}
                                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${isActiveRoute(item.href)
                                    ? 'bg-primary-purple text-white shadow-md'
                                    : 'text-text-secondary hover:text-white hover:bg-primary-purple/50'
                                    }`}
                            >
                                {item.label}
                            </Link>
                        ))}
                    </nav>

                    {/* Desktop Language Switcher */}
                    <div className="hidden md:block">
                        <LanguageSwitcher className="bg-card-background border-primary-purple/30" />
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={toggleMobileMenu}
                        className="md:hidden p-2 rounded-lg text-text-secondary hover:text-white hover:bg-primary-purple/50 transition-colors"
                        aria-label="Toggle mobile menu"
                    >
                        <svg
                            className={`w-6 h-6 transition-transform duration-300 ${isMobileMenuOpen ? 'rotate-90' : ''
                                }`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            {isMobileMenuOpen ? (
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            ) : (
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M4 6h16M4 12h16M4 18h16"
                                />
                            )}
                        </svg>
                    </button>
                </div>

                {/* Mobile Navigation Menu */}
                <div
                    className={`md:hidden transition-all duration-300 ease-in-out overflow-hidden ${isMobileMenuOpen
                        ? 'max-h-96 opacity-100 pb-4'
                        : 'max-h-0 opacity-0'
                        }`}
                >
                    <nav className="flex flex-col space-y-2 pt-4 border-t border-primary-purple/30">
                        {navigationItems.map((item) => (
                            <Link
                                key={item.key}
                                href={item.href}
                                className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 ${isActiveRoute(item.href)
                                    ? 'bg-primary-purple text-white shadow-md'
                                    : 'text-text-secondary hover:text-white hover:bg-primary-purple/50'
                                    }`}
                            >
                                {item.label}
                            </Link>
                        ))}

                        {/* Mobile Language Switcher */}
                        <div className="px-4 py-2">
                            <LanguageSwitcher className="w-full bg-card-background border-primary-purple/30" />
                        </div>
                    </nav>
                </div>
            </div>
        </header>
    );
};

export default Header;