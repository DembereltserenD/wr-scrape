import React, { useState, useRef, useEffect } from 'react';
import { useLanguage, Locale } from '../contexts/LanguageContext';

interface LanguageSwitcherProps {
  className?: string;
}

// Language display names and flags
const languageNames: Record<Locale, string> = {
  mn: 'Монгол',
  en: 'English'
};

const languageFlags: Record<Locale, string> = {
  mn: '🇲🇳',
  en: '🇺🇸'
};

const locales: Locale[] = ['mn', 'en'];

const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({
  className = ''
}) => {
  const { locale, setLocale } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // Handle language change with enhanced smooth transition
  const handleLanguageChange = (newLocale: Locale) => {
    if (newLocale === locale) {
      setIsOpen(false);
      return;
    }

    setIsTransitioning(true);

    // Create a gaming-style transition effect
    const transitionOverlay = document.createElement('div');
    transitionOverlay.className = 'fixed inset-0 bg-gradient-to-br from-background-dark/90 via-primary-purple/30 to-background-dark/90 backdrop-blur-md z-[9999] flex items-center justify-center transition-all duration-500';
    transitionOverlay.innerHTML = `
      <div class="flex flex-col items-center space-y-6 text-text-primary">
        <div class="relative">
          <div class="w-12 h-12 border-4 border-primary-purple/40 border-t-primary-purple rounded-full animate-spin"></div>
          <div class="absolute inset-0 w-12 h-12 border-4 border-transparent border-r-accent-pink rounded-full animate-spin" style="animation-direction: reverse; animation-duration: 0.6s;"></div>
          <div class="absolute inset-2 w-8 h-8 border-2 border-transparent border-b-text-secondary rounded-full animate-spin" style="animation-duration: 1.2s;"></div>
        </div>
        <div class="text-center">
          <div class="text-lg font-bold bg-gradient-to-r from-primary-purple via-accent-pink to-primary-purple bg-clip-text text-transparent animate-pulse mb-2">
            ${languageFlags[newLocale]} ${languageNames[newLocale]}
          </div>
          <div class="text-sm font-medium text-text-secondary animate-pulse">
            ${locale === 'mn' ? 'Хэл солиж байна...' : 'Switching language...'}
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(transitionOverlay);

    // Add gaming-style page transition
    const mainContent = document.querySelector('main') || document.body;
    mainContent.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
    mainContent.style.transform = 'scale(0.95) rotateX(2deg)';
    mainContent.style.opacity = '0.6';
    mainContent.style.filter = 'blur(2px)';

    setTimeout(() => {
      setLocale(newLocale);
      setIsOpen(false);

      // Restore page with new language
      setTimeout(() => {
        mainContent.style.transform = 'scale(1) rotateX(0deg)';
        mainContent.style.opacity = '1';
        mainContent.style.filter = 'blur(0px)';

        setTimeout(() => {
          if (document.body.contains(transitionOverlay)) {
            document.body.removeChild(transitionOverlay);
          }
          mainContent.style.transition = '';
          mainContent.style.transform = '';
          mainContent.style.filter = '';
          setIsTransitioning(false);
        }, 500);
      }, 150);
    }, 300);
  };

  // Close dropdown when clicking outside or pressing Escape
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        buttonRef.current &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
        buttonRef.current?.focus();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleKeyDown);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
        document.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, [isOpen]);

  // Handle keyboard navigation in dropdown
  const handleDropdownKeyDown = (event: React.KeyboardEvent, targetLocale: Locale) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleLanguageChange(targetLocale);
    }
  };

  return (
    <div className={`relative ${className}`}>
      <button
        ref={buttonRef}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            setIsOpen(!isOpen);
          }
          // Arrow key navigation
          if (e.key === 'ArrowDown' && !isOpen) {
            e.preventDefault();
            setIsOpen(true);
          }
        }}
        className={`
          group relative flex items-center space-x-3 px-4 py-2.5 rounded-lg 
          bg-gradient-to-r from-card-background via-card-background/95 to-card-background/80
          border border-primary-purple/40 
          hover:border-primary-purple hover:from-primary-purple/25 hover:to-primary-purple/15
          hover:shadow-lg hover:shadow-primary-purple/30
          focus:outline-none focus:ring-2 focus:ring-primary-purple/60 focus:ring-offset-2 focus:ring-offset-background-dark
          active:scale-95 active:shadow-inner
          transition-all duration-300 ease-in-out
          ${isTransitioning ? 'opacity-50 cursor-wait pointer-events-none' : 'cursor-pointer'}
          ${isOpen ? 'ring-2 ring-primary-purple/60 ring-offset-2 ring-offset-background-dark shadow-lg shadow-primary-purple/25' : ''}
          before:absolute before:inset-0 before:rounded-lg before:bg-gradient-to-r before:from-transparent before:via-primary-purple/10 before:to-transparent before:opacity-0 hover:before:opacity-100 before:transition-opacity before:duration-300
        `}
        disabled={isTransitioning}
        aria-label={`Language selector. Current language: ${languageNames[locale]}. Press Enter or Space to open language menu`}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-describedby="language-switcher-description"
        role="combobox"
        aria-controls="language-dropdown"
      >
        {/* Gaming-style glow effect */}
        <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-primary-purple/20 via-accent-pink/10 to-primary-purple/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur-sm"></div>

        <span className="relative text-lg" role="img" aria-label={`${languageNames[locale]} flag`}>
          {languageFlags[locale]}
        </span>
        <span className="relative text-sm font-semibold text-text-primary min-w-[65px] text-left group-hover:text-white transition-colors duration-200">
          {languageNames[locale]}
        </span>
        <svg
          className={`relative w-4 h-4 text-text-secondary group-hover:text-primary-purple transition-all duration-300 ease-in-out ${isOpen ? 'rotate-180 text-primary-purple' : ''
            }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>

        {/* Gaming-style corner accents */}
        <div className="absolute top-0 left-0 w-2 h-2 border-l-2 border-t-2 border-primary-purple/30 rounded-tl-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <div className="absolute top-0 right-0 w-2 h-2 border-r-2 border-t-2 border-primary-purple/30 rounded-tr-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <div className="absolute bottom-0 left-0 w-2 h-2 border-l-2 border-b-2 border-primary-purple/30 rounded-bl-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <div className="absolute bottom-0 right-0 w-2 h-2 border-r-2 border-b-2 border-primary-purple/30 rounded-br-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      </button>

      {/* Hidden description for screen readers */}
      <div id="language-switcher-description" className="sr-only">
        Use arrow keys to navigate language options. Press Enter to select.
      </div>

      {/* Dropdown with enhanced gaming-style animations */}
      <div
        ref={dropdownRef}
        id="language-dropdown"
        className={`
          absolute right-0 mt-3 w-56 
          bg-gradient-to-b from-card-background via-card-background/98 to-card-background/95
          rounded-xl shadow-2xl border border-primary-purple/40 
          z-50 overflow-hidden backdrop-blur-md
          transition-all duration-400 ease-out origin-top-right
          ${isOpen
            ? 'opacity-100 scale-100 translate-y-0 rotate-0'
            : 'opacity-0 scale-90 -translate-y-4 rotate-1 pointer-events-none'
          }
        `}
        role="listbox"
        aria-label="Language selection menu"
        aria-activedescendant={`language-option-${locale}`}
      >
        {/* Gaming-style header glow */}
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-primary-purple/60 to-transparent"></div>

        <div className="py-3 relative">
          {locales.map((lang, index) => (
            <button
              key={lang}
              id={`language-option-${lang}`}
              onClick={() => handleLanguageChange(lang)}
              onKeyDown={(e) => {
                handleDropdownKeyDown(e, lang);
                // Enhanced keyboard navigation
                if (e.key === 'ArrowDown') {
                  e.preventDefault();
                  const nextIndex = (index + 1) % locales.length;
                  document.getElementById(`language-option-${locales[nextIndex]}`)?.focus();
                }
                if (e.key === 'ArrowUp') {
                  e.preventDefault();
                  const prevIndex = index === 0 ? locales.length - 1 : index - 1;
                  document.getElementById(`language-option-${locales[prevIndex]}`)?.focus();
                }
              }}
              className={`
                group relative w-full text-left px-5 py-3.5 text-sm 
                flex items-center space-x-4 
                transition-all duration-300 ease-out
                hover:bg-gradient-to-r hover:from-primary-purple/25 hover:via-primary-purple/15 hover:to-primary-purple/10
                hover:shadow-lg hover:shadow-primary-purple/20
                focus:outline-none focus:bg-gradient-to-r focus:from-primary-purple/35 focus:via-primary-purple/20 focus:to-primary-purple/15
                focus:ring-2 focus:ring-primary-purple/50 focus:ring-inset
                active:scale-98 active:bg-gradient-to-r active:from-primary-purple/40 active:to-primary-purple/20
                ${locale === lang
                  ? 'bg-gradient-to-r from-primary-purple/35 via-primary-purple/20 to-primary-purple/15 text-text-primary border-l-4 border-primary-purple shadow-lg shadow-primary-purple/20'
                  : 'text-text-secondary hover:text-text-primary'
                }
                ${index === 0 ? 'rounded-t-lg' : ''}
                ${index === locales.length - 1 ? 'rounded-b-lg' : ''}
              `}
              role="option"
              aria-selected={locale === lang}
              aria-label={`Switch to ${languageNames[lang]}`}
              tabIndex={isOpen ? 0 : -1}
            >
              {/* Gaming-style selection indicator */}
              {locale === lang && (
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-primary-purple via-accent-pink to-primary-purple rounded-r-full"></div>
              )}

              {/* Hover glow effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-primary-purple/10 via-accent-pink/5 to-primary-purple/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg"></div>

              <span className="relative text-xl" role="img" aria-label={`${languageNames[lang]} flag`}>
                {languageFlags[lang]}
              </span>
              <span className="relative flex-1 font-semibold group-hover:text-white transition-colors duration-200">
                {languageNames[lang]}
              </span>

              {locale === lang && (
                <div className="relative flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary-purple rounded-full animate-pulse"></div>
                  <svg
                    className="w-5 h-5 text-primary-purple"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    aria-hidden="true"
                  >
                    <path
                      fillRule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
              )}

              {/* Gaming-style corner highlights */}
              <div className="absolute top-1 right-1 w-1 h-1 bg-primary-purple/40 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="absolute bottom-1 left-1 w-1 h-1 bg-accent-pink/40 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </button>
          ))}
        </div>

        {/* Enhanced gaming-style accent borders */}
        <div className="absolute inset-0 rounded-xl border border-primary-purple/30 pointer-events-none">
          {/* Top accent line */}
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-12 h-px bg-gradient-to-r from-transparent via-primary-purple/80 to-transparent"></div>
          {/* Bottom accent line */}
          <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-12 h-px bg-gradient-to-r from-transparent via-accent-pink/60 to-transparent"></div>
          {/* Side accent dots */}
          <div className="absolute top-4 left-0 w-px h-4 bg-gradient-to-b from-primary-purple/60 to-transparent"></div>
          <div className="absolute top-4 right-0 w-px h-4 bg-gradient-to-b from-primary-purple/60 to-transparent"></div>
          <div className="absolute bottom-4 left-0 w-px h-4 bg-gradient-to-t from-accent-pink/40 to-transparent"></div>
          <div className="absolute bottom-4 right-0 w-px h-4 bg-gradient-to-t from-accent-pink/40 to-transparent"></div>
        </div>

        {/* Gaming-style footer glow */}
        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-accent-pink/40 to-transparent"></div>
      </div>

      {/* Loading overlay during transition */}
      {isTransitioning && (
        <div className="fixed inset-0 bg-background-dark/50 backdrop-blur-sm z-40 flex items-center justify-center">
          <div className="flex items-center space-x-2 text-text-primary">
            <div className="w-4 h-4 border-2 border-primary-purple border-t-transparent rounded-full animate-spin"></div>
            <span className="text-sm">Switching language...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default LanguageSwitcher;
