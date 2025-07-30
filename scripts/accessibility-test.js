#!/usr/bin/env node

/**
 * Comprehensive Accessibility Testing Script
 * Tests keyboard navigation, screen reader compatibility, and WCAG compliance
 */

const fs = require('fs');
const path = require('path');

console.log('♿ Running Comprehensive Accessibility Tests...\n');

// Test 1: Check for proper semantic HTML
console.log('🏗️ Checking semantic HTML structure...');

const checkSemanticHTML = (filePath) => {
    if (!fs.existsSync(filePath)) return [];

    const content = fs.readFileSync(filePath, 'utf8');
    const issues = [];

    // Check for proper heading hierarchy
    const headings = content.match(/<h[1-6][^>]*>/g) || [];
    let previousLevel = 0;

    headings.forEach((heading, index) => {
        const level = parseInt(heading.match(/h([1-6])/)[1]);
        if (level > previousLevel + 1 && previousLevel !== 0) {
            issues.push(`Heading hierarchy skip: h${previousLevel} to h${level}`);
        }
        previousLevel = level;
    });

    // Check for missing alt text on images
    const images = content.match(/<img[^>]*>/g) || [];
    images.forEach((img, index) => {
        if (!img.includes('alt=')) {
            issues.push(`Image ${index + 1} missing alt attribute`);
        }
    });

    // Check for buttons without accessible names
    const buttons = content.match(/<button[^>]*>/g) || [];
    buttons.forEach((button, index) => {
        if (!button.includes('aria-label') && !button.includes('aria-labelledby')) {
            // Check if button has text content (simplified check)
            const buttonEnd = content.indexOf('</button>', content.indexOf(button));
            const buttonContent = content.substring(content.indexOf(button) + button.length, buttonEnd);
            if (!buttonContent.trim() || buttonContent.includes('<svg')) {
                issues.push(`Button ${index + 1} may need aria-label`);
            }
        }
    });

    // Check for form inputs without labels
    const inputs = content.match(/<input[^>]*>/g) || [];
    inputs.forEach((input, index) => {
        if (!input.includes('aria-label') && !input.includes('aria-labelledby') && !input.includes('id=')) {
            issues.push(`Input ${index + 1} missing label association`);
        }
    });

    return issues;
};

const componentFiles = [
    'pages/index.tsx',
    'components/Layout/Header.tsx',
    'components/Layout/Footer.tsx',
    'components/ChampionCard.tsx',
    'components/HeroSection.tsx',
    'components/UI/Button.tsx',
    'components/UI/Dropdown.tsx',
    'components/LanguageSwitcher.tsx'
];

let totalIssues = 0;

componentFiles.forEach(file => {
    const filePath = path.join(process.cwd(), file);
    const issues = checkSemanticHTML(filePath);

    if (issues.length === 0) {
        console.log(`✅ ${file}`);
    } else {
        console.log(`⚠️ ${file}:`);
        issues.forEach(issue => console.log(`   - ${issue}`));
        totalIssues += issues.length;
    }
});

console.log();

// Test 2: Check for keyboard navigation support
console.log('⌨️ Checking keyboard navigation support...');

const checkKeyboardNavigation = (filePath) => {
    if (!fs.existsSync(filePath)) return [];

    const content = fs.readFileSync(filePath, 'utf8');
    const issues = [];

    // Check for keyboard event handlers
    const hasKeyboardHandlers = content.includes('onKeyDown') ||
        content.includes('onKeyUp') ||
        content.includes('onKeyPress');

    // Check for interactive elements
    const hasInteractiveElements = content.includes('<button') ||
        content.includes('<input') ||
        content.includes('<select') ||
        content.includes('onClick');

    if (hasInteractiveElements && !hasKeyboardHandlers && !content.includes('tabIndex')) {
        issues.push('Interactive elements may need keyboard support');
    }

    // Check for focus management
    const hasFocusManagement = content.includes('focus()') ||
        content.includes('blur()') ||
        content.includes('focus:');

    if (hasInteractiveElements && !hasFocusManagement) {
        issues.push('May need focus management');
    }

    // Check for positive tabindex (anti-pattern)
    const positiveTabIndex = content.match(/tabIndex=["']?[1-9]/g);
    if (positiveTabIndex) {
        issues.push('Positive tabIndex found (anti-pattern)');
    }

    return issues;
};

componentFiles.forEach(file => {
    const filePath = path.join(process.cwd(), file);
    const issues = checkKeyboardNavigation(filePath);

    if (issues.length === 0) {
        console.log(`✅ ${file}`);
    } else {
        console.log(`⚠️ ${file}:`);
        issues.forEach(issue => console.log(`   - ${issue}`));
        totalIssues += issues.length;
    }
});

console.log();

// Test 3: Check for ARIA attributes and roles
console.log('🏷️ Checking ARIA attributes and roles...');

const checkARIA = (filePath) => {
    if (!fs.existsSync(filePath)) return [];

    const content = fs.readFileSync(filePath, 'utf8');
    const issues = [];

    // Check for proper ARIA roles
    const customComponents = content.match(/<[A-Z][a-zA-Z]*[^>]*>/g) || [];
    const hasARIARoles = content.includes('role=') || content.includes('aria-');

    if (customComponents.length > 0 && !hasARIARoles) {
        issues.push('Custom components may need ARIA roles');
    }

    // Check for aria-expanded on dropdowns
    if (content.includes('dropdown') && !content.includes('aria-expanded')) {
        issues.push('Dropdown may need aria-expanded');
    }

    // Check for aria-live regions
    if (content.includes('loading') && !content.includes('aria-live')) {
        issues.push('Loading states may need aria-live');
    }

    // Check for aria-hidden on decorative elements
    const svgElements = content.match(/<svg[^>]*>/g) || [];
    svgElements.forEach((svg, index) => {
        if (!svg.includes('aria-hidden') && !svg.includes('aria-label')) {
            issues.push(`SVG ${index + 1} may need aria-hidden or aria-label`);
        }
    });

    return issues;
};

componentFiles.forEach(file => {
    const filePath = path.join(process.cwd(), file);
    const issues = checkARIA(filePath);

    if (issues.length === 0) {
        console.log(`✅ ${file}`);
    } else {
        console.log(`⚠️ ${file}:`);
        issues.forEach(issue => console.log(`   - ${issue}`));
        totalIssues += issues.length;
    }
});

console.log();

// Test 4: Check for color contrast and visual accessibility
console.log('🎨 Checking visual accessibility...');

const checkVisualAccessibility = () => {
    const issues = [];

    // Check CSS for color contrast considerations
    const cssPath = path.join(process.cwd(), 'styles/globals.css');
    if (fs.existsSync(cssPath)) {
        const content = fs.readFileSync(cssPath, 'utf8');

        if (!content.includes('prefers-reduced-motion')) {
            issues.push('Missing prefers-reduced-motion support');
        }

        if (!content.includes('focus:')) {
            issues.push('Missing focus indicators');
        }

        // Check for high contrast mode support
        if (!content.includes('@media (prefers-contrast:')) {
            issues.push('Consider adding high contrast mode support');
        }
    }

    // Check Tailwind config for accessibility
    const tailwindPath = path.join(process.cwd(), 'tailwind.config.js');
    if (fs.existsSync(tailwindPath)) {
        const content = fs.readFileSync(tailwindPath, 'utf8');

        if (!content.includes('focus:')) {
            issues.push('Tailwind config may need focus utilities');
        }
    }

    return issues;
};

const visualIssues = checkVisualAccessibility();
if (visualIssues.length === 0) {
    console.log('✅ Visual accessibility checks passed');
} else {
    console.log('⚠️ Visual accessibility issues:');
    visualIssues.forEach(issue => console.log(`   - ${issue}`));
    totalIssues += visualIssues.length;
}

console.log();

// Test 5: Check for screen reader support
console.log('📢 Checking screen reader support...');

const checkScreenReaderSupport = () => {
    const issues = [];

    // Check for accessibility utilities
    const a11yUtilsPath = path.join(process.cwd(), 'utils/accessibility.ts');
    if (!fs.existsSync(a11yUtilsPath)) {
        issues.push('Missing accessibility utilities');
    } else {
        const content = fs.readFileSync(a11yUtilsPath, 'utf8');

        if (!content.includes('announce')) {
            issues.push('Missing screen reader announcement utility');
        }

        if (!content.includes('aria-live')) {
            issues.push('Missing aria-live region support');
        }
    }

    // Check for language support
    const indexPath = path.join(process.cwd(), 'pages/index.tsx');
    if (fs.existsSync(indexPath)) {
        const content = fs.readFileSync(indexPath, 'utf8');

        if (!content.includes('lang=') && !content.includes('locale')) {
            issues.push('Missing language attribute');
        }
    }

    return issues;
};

const screenReaderIssues = checkScreenReaderSupport();
if (screenReaderIssues.length === 0) {
    console.log('✅ Screen reader support checks passed');
} else {
    console.log('⚠️ Screen reader support issues:');
    screenReaderIssues.forEach(issue => console.log(`   - ${issue}`));
    totalIssues += screenReaderIssues.length;
}

console.log();

// Summary
console.log('📋 Accessibility Test Summary:');
console.log('==============================');

if (totalIssues === 0) {
    console.log('🎉 All accessibility checks passed!');
} else {
    console.log(`⚠️ Found ${totalIssues} potential accessibility issues`);
}

console.log();

// Recommendations
console.log('💡 Accessibility Recommendations:');
console.log('==================================');
console.log('1. Test with actual screen readers (NVDA, JAWS, VoiceOver)');
console.log('2. Test keyboard navigation on all interactive elements');
console.log('3. Verify color contrast ratios meet WCAG AA standards');
console.log('4. Test with users who have disabilities');
console.log('5. Use automated tools like axe-core for additional testing');
console.log('6. Test with high contrast mode enabled');
console.log('7. Test with reduced motion preferences');
console.log('8. Verify touch targets are at least 44x44px');

console.log('\n♿ Accessibility testing complete!');