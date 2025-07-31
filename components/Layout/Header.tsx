import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useLanguage } from '../../contexts/LanguageContext';
import LanguageSwitcher from '../LanguageSwitcher';
import { ChampionData } from '../../types/champion';

interface HeaderProps {
    currentPage?: string;
}

const Header: React.FC<HeaderProps> = ({ currentPage }) => {
    const { t } = useLanguage();
    const router = useRouter();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [isScrolled, setIsScrolled] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState<ChampionData[]>([]);
    const [showSearchResults, setShowSearchResults] = useState(false);
    const [champions, setChampions] = useState<ChampionData[]>([]);
    const searchRef = useRef<HTMLDivElement>(null);
    const mobileSearchRef = useRef<HTMLDivElement>(null);

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

    // Load champions data on component mount
    useEffect(() => {
        const loadChampions = async () => {
            try {
                const response = await fetch('/api/champions');
                if (response.ok) {
                    const championsData = await response.json();
                    setChampions(championsData);
                } else {
                    // Fallback: try to get from static data if API fails
                    console.warn('Champions API failed, using fallback');
                }
            } catch (error) {
                console.error('Error loading champions:', error);
            }
        };
        loadChampions();
    }, []);

    // Handle search input changes for real-time suggestions
    useEffect(() => {
        if (searchQuery.trim().length > 0) {
            const filtered = champions.filter(champion =>
                champion.champion.name.toLowerCase().includes(searchQuery.toLowerCase())
            ).slice(0, 5); // Limit to 5 results
            setSearchResults(filtered);
            setShowSearchResults(true);
        } else {
            setSearchResults([]);
            setShowSearchResults(false);
        }
    }, [searchQuery, champions]);

    // Close search results when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (searchRef.current && !searchRef.current.contains(event.target as Node) &&
                mobileSearchRef.current && !mobileSearchRef.current.contains(event.target as Node)) {
                setShowSearchResults(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

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

    // Handle search
    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            router.push(`/champions?search=${encodeURIComponent(searchQuery.trim())}`);
            setSearchQuery('');
            setShowSearchResults(false);
            setIsMobileMenuOpen(false);
        }
    };

    // Handle champion selection from search results
    const handleChampionSelect = (champion: ChampionData) => {
        router.push(`/champion/${champion.champion.id}`);
        setSearchQuery('');
        setShowSearchResults(false);
        setIsMobileMenuOpen(false);
    };

    // Get tier color for champion cards
    const getTierColor = (tier: string) => {
        switch (tier) {
            case 'S+': return 'text-red-400';
            case 'S': return 'text-orange-400';
            case 'A': return 'text-yellow-400';
            case 'B': return 'text-green-400';
            case 'C': return 'text-blue-400';
            default: return 'text-gray-400';
        }
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
                    <nav className="hidden lg:flex items-center space-x-1">
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

                    {/* Desktop Search */}
                    <div className="hidden md:block w-56 mx-4" ref={searchRef}>
                        <form onSubmit={handleSearch} className="relative">
                            <input
                                type="text"
                                placeholder={t('common.search') + ' champions...'}
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                onFocus={() => searchQuery.trim() && setShowSearchResults(true)}
                                className="w-full px-3 py-2 pl-8 text-sm bg-slate-800/80 border border-primary-purple/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:bg-slate-700/90 focus:scale-105 active:scale-95 transition-all duration-200 ease-out"
                            />
                            <svg
                                className="absolute left-2.5 top-1/2 transform -translate-y-1/2 w-3.5 h-3.5 text-text-secondary"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                />
                            </svg>
                        </form>

                        {/* Desktop Search Results */}
                        {showSearchResults && searchResults.length > 0 && (
                            <div className="absolute top-full left-0 right-0 mt-1 bg-slate-800/95 backdrop-blur-sm border border-slate-600/50 rounded-lg shadow-xl z-50 max-h-64 overflow-y-auto">
                                {searchResults.map((champion) => (
                                    <div
                                        key={champion.champion.id}
                                        onClick={() => handleChampionSelect(champion)}
                                        className="flex items-center p-2.5 hover:bg-primary-purple/20 cursor-pointer transition-colors border-b border-primary-purple/10 last:border-b-0"
                                    >
                                        <img
                                            src={champion.champion.image || '/placeholder-champion.png'}
                                            alt={champion.champion.name}
                                            className="w-7 h-7 rounded-full object-cover mr-3 flex-shrink-0"
                                            onError={(e) => {
                                                (e.target as HTMLImageElement).src = '/placeholder-champion.png';
                                            }}
                                        />
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center justify-between">
                                                <span className="text-white font-medium text-sm truncate">
                                                    {champion.champion.name}
                                                </span>
                                                <span className={`text-xs font-bold ml-2 ${getTierColor(champion.champion.tier)}`}>
                                                    {champion.champion.tier}
                                                </span>
                                            </div>
                                            <div className="text-xs text-text-secondary truncate">
                                                {champion.champion.role}
                                                {champion.champion.lanes.length > 0 && ` • ${champion.champion.lanes[0]}`}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Desktop Language Switcher */}
                    <div className="hidden md:block">
                        <LanguageSwitcher className="bg-card-background border-primary-purple/30" />
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={toggleMobileMenu}
                        className="lg:hidden p-2 rounded-lg text-text-secondary hover:text-white hover:bg-primary-purple/50 transition-colors"
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
                    className={`lg:hidden transition-all duration-300 ease-in-out overflow-hidden ${isMobileMenuOpen
                        ? 'max-h-[500px] opacity-100 pb-4'
                        : 'max-h-0 opacity-0'
                        }`}
                >
                    <nav className="flex flex-col space-y-2 pt-4 border-t border-primary-purple/30">
                        {/* Mobile Search */}
                        <div className="px-4 py-2" ref={mobileSearchRef}>
                            <form onSubmit={handleSearch} className="relative">
                                <input
                                    type="text"
                                    placeholder={t('common.search') + ' champions...'}
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    onFocus={() => searchQuery.trim() && setShowSearchResults(true)}
                                    className="w-full px-4 py-3 pl-10 bg-slate-800/80 border border-primary-purple/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:bg-slate-700/90 focus:scale-105 active:scale-95 transition-all duration-200 ease-out"
                                />
                                <svg
                                    className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-text-secondary"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                    />
                                </svg>
                            </form>

                            {/* Mobile Search Results */}
                            {showSearchResults && searchResults.length > 0 && (
                                <div className="mt-2 bg-slate-800/95 backdrop-blur-sm border border-slate-600/50 rounded-lg shadow-xl max-h-60 overflow-y-auto">
                                    {searchResults.map((champion) => (
                                        <div
                                            key={champion.champion.id}
                                            onClick={() => handleChampionSelect(champion)}
                                            className="flex items-center p-3 hover:bg-primary-purple/20 cursor-pointer transition-colors border-b border-primary-purple/10 last:border-b-0"
                                        >
                                            <img
                                                src={champion.champion.image || '/placeholder-champion.png'}
                                                alt={champion.champion.name}
                                                className="w-10 h-10 rounded-full object-cover mr-3"
                                                onError={(e) => {
                                                    (e.target as HTMLImageElement).src = '/placeholder-champion.png';
                                                }}
                                            />
                                            <div className="flex-1 min-w-0">
                                                <div className="flex items-center justify-between">
                                                    <span className="text-white font-medium truncate">
                                                        {champion.champion.name}
                                                    </span>
                                                    <span className={`text-sm font-bold ${getTierColor(champion.champion.tier)}`}>
                                                        {champion.champion.tier}
                                                    </span>
                                                </div>
                                                <div className="flex items-center text-sm text-text-secondary">
                                                    <span className="truncate">{champion.champion.role}</span>
                                                    {champion.champion.lanes.length > 0 && (
                                                        <>
                                                            <span className="mx-1">•</span>
                                                            <span className="truncate">{champion.champion.lanes[0]}</span>
                                                        </>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

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