#!/usr/bin/env node

/**
 * Performance and Accessibility Testing Script
 * Run this script to test the homepage for performance and accessibility issues
 */

const {
    execSync
} = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Starting Performance and Accessibility Tests...\n');

// Test 1: Build the application
console.log('📦 Building application...');
try {
    execSync('npm run build', {
        stdio: 'inherit'
    });
    console.log('✅ Build successful\n');
} catch (error) {
    console.error('❌ Build failed');
    process.exit(1);
}

// Test 2: Type checking
console.log('🔍 Running type check...');
try {
    execSync('npm run type-check', {
        stdio: 'inherit'
    });
    console.log('✅ Type check passed\n');
} catch (error) {
    console.error('❌ Type check failed');
    process.exit(1);
}

// Test 3: Linting
console.log('🧹 Running linter...');
try {
    execSync('npm run lint', {
        stdio: 'inherit'
    });
    console.log('✅ Linting passed\n');
} catch (error) {
    console.error('❌ Linting failed');
    process.exit(1);
}

// Test 4: Check bundle size
console.log('📊 Analyzing bundle size...');
try {
    // Check if .next directory exists
    const nextDir = path.join(process.cwd(), '.next');
    if (fs.existsSync(nextDir)) {
        const buildManifest = path.join(nextDir, 'build-manifest.json');
        if (fs.existsSync(buildManifest)) {
            const manifest = JSON.parse(fs.readFileSync(buildManifest, 'utf8'));
            console.log('Bundle analysis:');
            console.log('- Pages:', Object.keys(manifest.pages).length);
            console.log('- Static files:', manifest.devFiles?.length || 0);
            console.log('✅ Bundle analysis complete\n');
        }
    }
} catch (error) {
    console.warn('⚠️ Could not analyze bundle size');
}

// Test 5: Check for performance best practices
console.log('⚡ Checking performance best practices...');

const performanceChecks = [{
        name: 'Next.js Image optimization',
        check: () => {
            const files = ['components/ChampionCard.tsx', 'components/HeroSection.tsx'];
            return files.some(file => {
                const filePath = path.join(process.cwd(), file);
                if (fs.existsSync(filePath)) {
                    const content = fs.readFileSync(filePath, 'utf8');
                    return content.includes('next/image');
                }
                return false;
            });
        }
    },
    {
        name: 'Dynamic imports for code splitting',
        check: () => {
            const indexPath = path.join(process.cwd(), 'pages/index.tsx');
            if (fs.existsSync(indexPath)) {
                const content = fs.readFileSync(indexPath, 'utf8');
                return content.includes('dynamic') && content.includes('next/dynamic');
            }
            return false;
        }
    },
    {
        name: 'Loading states implemented',
        check: () => {
            const loadingPath = path.join(process.cwd(), 'components/UI/LoadingState.tsx');
            return fs.existsSync(loadingPath);
        }
    },
    {
        name: 'Performance monitoring utilities',
        check: () => {
            const perfPath = path.join(process.cwd(), 'utils/performance.ts');
            return fs.existsSync(perfPath);
        }
    }
];

performanceChecks.forEach(({
    name,
    check
}) => {
    if (check()) {
        console.log(`✅ ${name}`);
    } else {
        console.log(`❌ ${name}`);
    }
});

console.log();

// Test 6: Check for accessibility best practices
console.log('♿ Checking accessibility best practices...');

const accessibilityChecks = [{
        name: 'Accessibility utilities implemented',
        check: () => {
            const a11yPath = path.join(process.cwd(), 'utils/accessibility.ts');
            return fs.existsSync(a11yPath);
        }
    },
    {
        name: 'Focus management in components',
        check: () => {
            const dropdownPath = path.join(process.cwd(), 'components/UI/Dropdown.tsx');
            if (fs.existsSync(dropdownPath)) {
                const content = fs.readFileSync(dropdownPath, 'utf8');
                return content.includes('focus:') && content.includes('aria-');
            }
            return false;
        }
    },
    {
        name: 'ARIA labels and roles',
        check: () => {
            const buttonPath = path.join(process.cwd(), 'components/UI/Button.tsx');
            if (fs.existsSync(buttonPath)) {
                const content = fs.readFileSync(buttonPath, 'utf8');
                return content.includes('aria-') && content.includes('role');
            }
            return false;
        }
    },
    {
        name: 'Keyboard navigation support',
        check: () => {
            const dropdownPath = path.join(process.cwd(), 'components/UI/Dropdown.tsx');
            if (fs.existsSync(dropdownPath)) {
                const content = fs.readFileSync(dropdownPath, 'utf8');
                return content.includes('keydown') && content.includes('ArrowDown');
            }
            return false;
        }
    },
    {
        name: 'Reduced motion support',
        check: () => {
            const globalCssPath = path.join(process.cwd(), 'styles/globals.css');
            if (fs.existsSync(globalCssPath)) {
                const content = fs.readFileSync(globalCssPath, 'utf8');
                return content.includes('prefers-reduced-motion');
            }
            return false;
        }
    }
];

accessibilityChecks.forEach(({
    name,
    check
}) => {
    if (check()) {
        console.log(`✅ ${name}`);
    } else {
        console.log(`❌ ${name}`);
    }
});

console.log();

// Test 7: Check SEO optimization
console.log('🔍 Checking SEO optimization...');

const seoChecks = [{
        name: 'SEO Head component implemented',
        check: () => {
            const seoPath = path.join(process.cwd(), 'components/SEO/SEOHead.tsx');
            return fs.existsSync(seoPath);
        }
    },
    {
        name: 'Meta tags implemented',
        check: () => {
            const indexPath = path.join(process.cwd(), 'pages/index.tsx');
            if (fs.existsSync(indexPath)) {
                const content = fs.readFileSync(indexPath, 'utf8');
                return content.includes('SEOHead') || (
                    content.includes('meta name="description"') &&
                    content.includes('meta name="keywords"') &&
                    content.includes('og:title')
                );
            }
            return false;
        }
    },
    {
        name: 'Structured data (JSON-LD)',
        check: () => {
            const seoPath = path.join(process.cwd(), 'components/SEO/SEOHead.tsx');
            const indexPath = path.join(process.cwd(), 'pages/index.tsx');

            if (fs.existsSync(seoPath)) {
                const content = fs.readFileSync(seoPath, 'utf8');
                return content.includes('application/ld+json') && content.includes('@context');
            }

            if (fs.existsSync(indexPath)) {
                const content = fs.readFileSync(indexPath, 'utf8');
                return content.includes('application/ld+json') && content.includes('@context');
            }

            return false;
        }
    },
    {
        name: 'Canonical URL and language alternates',
        check: () => {
            const seoPath = path.join(process.cwd(), 'components/SEO/SEOHead.tsx');
            if (fs.existsSync(seoPath)) {
                const content = fs.readFileSync(seoPath, 'utf8');
                return content.includes('rel="canonical"') && content.includes('hrefLang');
            }
            return false;
        }
    },
    {
        name: 'Open Graph and Twitter Cards',
        check: () => {
            const seoPath = path.join(process.cwd(), 'components/SEO/SEOHead.tsx');
            if (fs.existsSync(seoPath)) {
                const content = fs.readFileSync(seoPath, 'utf8');
                return content.includes('og:image') && content.includes('twitter:card');
            }
            return false;
        }
    }
];

seoChecks.forEach(({
    name,
    check
}) => {
    if (check()) {
        console.log(`✅ ${name}`);
    } else {
        console.log(`❌ ${name}`);
    }
});

console.log();

// Summary
console.log('📋 Test Summary:');
console.log('================');

const allChecks = [...performanceChecks, ...accessibilityChecks, ...seoChecks];
const passedChecks = allChecks.filter(({
    check
}) => check()).length;
const totalChecks = allChecks.length;

console.log(`✅ Passed: ${passedChecks}/${totalChecks} checks`);

if (passedChecks === totalChecks) {
    console.log('🎉 All optimization checks passed!');
} else {
    console.log(`⚠️ ${totalChecks - passedChecks} checks need attention`);
}

console.log('\n🚀 Performance and Accessibility testing complete!');

// Recommendations
console.log('\n💡 Recommendations:');
console.log('===================');
console.log('1. Run `npm run analyze` to see detailed bundle analysis');
console.log('2. Test with screen readers (NVDA, JAWS, VoiceOver)');
console.log('3. Test keyboard navigation on all interactive elements');
console.log('4. Use Lighthouse for additional performance insights');
console.log('5. Test on various devices and network conditions');