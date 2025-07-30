import React from 'react';
import Head from 'next/head';
import { useLanguage } from '../contexts/LanguageContext';
import { Layout } from '../components/Layout';

const ResponsiveTestPage: React.FC = () => {
    const { t } = useLanguage();

    return (
        <Layout currentPage="/responsive-test">
            <Head>
                <title>Responsive Design Test - Wild Rift Guide</title>
                <meta name="description" content="Testing responsive design system" />
            </Head>

            <div className="responsive-container responsive-section">
                {/* Page Title */}
                <div className="text-center mb-12">
                    <h1 className="responsive-heading-1 text-primary-purple mb-4">
                        Responsive Design Test
                    </h1>
                    <p className="responsive-body text-text-secondary">
                        Testing the responsive design system across different screen sizes
                    </p>
                </div>

                {/* Responsive Grid Tests */}
                <section className="mb-16">
                    <h2 className="responsive-heading-2 text-white mb-8">Grid System Tests</h2>

                    {/* 1 Column Grid */}
                    <div className="mb-8">
                        <h3 className="responsive-heading-3 text-text-secondary mb-4">1 Column Grid</h3>
                        <div className="responsive-grid-1">
                            <div className="card-comfortable bg-card-background text-white">Item 1</div>
                            <div className="card-comfortable bg-card-background text-white">Item 2</div>
                            <div className="card-comfortable bg-card-background text-white">Item 3</div>
                        </div>
                    </div>

                    {/* 2 Column Grid */}
                    <div className="mb-8">
                        <h3 className="responsive-heading-3 text-text-secondary mb-4">2 Column Grid (1 on mobile, 2 on tablet+)</h3>
                        <div className="responsive-grid-2">
                            <div className="card-comfortable bg-card-background text-white">Item 1</div>
                            <div className="card-comfortable bg-card-background text-white">Item 2</div>
                            <div className="card-comfortable bg-card-background text-white">Item 3</div>
                            <div className="card-comfortable bg-card-background text-white">Item 4</div>
                        </div>
                    </div>

                    {/* 3 Column Grid */}
                    <div className="mb-8">
                        <h3 className="responsive-heading-3 text-text-secondary mb-4">3 Column Grid (1 on mobile, 2 on tablet, 3 on desktop)</h3>
                        <div className="responsive-grid-3">
                            <div className="card-comfortable bg-card-background text-white">Item 1</div>
                            <div className="card-comfortable bg-card-background text-white">Item 2</div>
                            <div className="card-comfortable bg-card-background text-white">Item 3</div>
                            <div className="card-comfortable bg-card-background text-white">Item 4</div>
                            <div className="card-comfortable bg-card-background text-white">Item 5</div>
                            <div className="card-comfortable bg-card-background text-white">Item 6</div>
                        </div>
                    </div>

                    {/* Champion Grid */}
                    <div className="mb-8">
                        <h3 className="responsive-heading-3 text-text-secondary mb-4">Champion Grid (1→2→3→4→5 columns)</h3>
                        <div className="champion-grid">
                            {Array.from({ length: 10 }, (_, i) => (
                                <div key={i} className="champion-card text-white">
                                    <div className="responsive-image-container bg-primary-purple mb-4">
                                        <div className="absolute inset-0 flex items-center justify-center">
                                            Champion {i + 1}
                                        </div>
                                    </div>
                                    <h4 className="text-lg font-semibold mb-2">Champion {i + 1}</h4>
                                    <div className="tier-badge tier-s mb-2">S</div>
                                    <p className="responsive-caption text-text-secondary">Sample champion card</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Typography Tests */}
                <section className="mb-16">
                    <h2 className="responsive-heading-2 text-white mb-8">Typography Tests</h2>

                    <div className="space-y-6">
                        <div>
                            <h1 className="responsive-heading-1 text-primary-purple">Heading 1 - Responsive</h1>
                            <p className="responsive-caption text-text-secondary">text-2xl xs:text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl</p>
                        </div>

                        <div>
                            <h2 className="responsive-heading-2 text-white">Heading 2 - Responsive</h2>
                            <p className="responsive-caption text-text-secondary">text-xl xs:text-2xl sm:text-3xl md:text-4xl lg:text-5xl</p>
                        </div>

                        <div>
                            <h3 className="responsive-heading-3 text-text-secondary">Heading 3 - Responsive</h3>
                            <p className="responsive-caption text-text-secondary">text-lg xs:text-xl sm:text-2xl md:text-3xl lg:text-4xl</p>
                        </div>

                        <div>
                            <p className="responsive-body text-white">Body Text - Responsive</p>
                            <p className="responsive-caption text-text-secondary">text-sm xs:text-base sm:text-lg md:text-xl</p>
                        </div>

                        <div>
                            <p className="responsive-caption text-text-secondary">Caption Text - Responsive</p>
                            <p className="responsive-caption text-text-secondary">text-xs xs:text-sm sm:text-base</p>
                        </div>
                    </div>
                </section>

                {/* Button Tests */}
                <section className="mb-16">
                    <h2 className="responsive-heading-2 text-white mb-8">Button Tests</h2>

                    <div className="space-y-6">
                        <div>
                            <h3 className="responsive-heading-3 text-text-secondary mb-4">Gaming Buttons</h3>
                            <div className="flex flex-col sm:flex-row gap-4">
                                <button className="gaming-button text-white">Primary Button</button>
                                <button className="gaming-button text-white">Secondary Button</button>
                                <button className="gaming-button text-white">Action Button</button>
                            </div>
                        </div>

                        <div>
                            <h3 className="responsive-heading-3 text-text-secondary mb-4">Touch Targets (Mobile Optimized)</h3>
                            <div className="flex flex-wrap gap-2">
                                <button className="touch-target bg-primary-purple text-white rounded-lg">✓</button>
                                <button className="touch-target bg-accent-pink text-white rounded-lg">✗</button>
                                <button className="touch-target bg-tier-s text-black rounded-lg">★</button>
                                <button className="touch-target bg-tier-a text-black rounded-lg">♦</button>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Layout Tests */}
                <section className="mb-16">
                    <h2 className="responsive-heading-2 text-white mb-8">Layout Tests</h2>

                    <div className="space-y-8">
                        <div>
                            <h3 className="responsive-heading-3 text-text-secondary mb-4">Responsive Flex Column → Row</h3>
                            <div className="responsive-flex-col responsive-gap">
                                <div className="card-compact bg-card-background text-white flex-1">Item 1</div>
                                <div className="card-compact bg-card-background text-white flex-1">Item 2</div>
                                <div className="card-compact bg-card-background text-white flex-1">Item 3</div>
                            </div>
                        </div>

                        <div>
                            <h3 className="responsive-heading-3 text-text-secondary mb-4">Responsive Flex Between</h3>
                            <div className="responsive-flex-between responsive-gap bg-card-background rounded-lg p-6">
                                <div className="text-white">Left Content</div>
                                <div className="text-text-secondary">Right Content</div>
                            </div>
                        </div>

                        <div>
                            <h3 className="responsive-heading-3 text-text-secondary mb-4">Responsive Flex Center</h3>
                            <div className="responsive-flex-center responsive-gap bg-card-background rounded-lg p-6">
                                <div className="text-white">Centered</div>
                                <div className="text-text-secondary">Content</div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Gaming Elements Tests */}
                <section className="mb-16">
                    <h2 className="responsive-heading-2 text-white mb-8">Gaming Elements Tests</h2>

                    <div className="space-y-8">
                        <div>
                            <h3 className="responsive-heading-3 text-text-secondary mb-4">Tier Badges</h3>
                            <div className="flex flex-wrap gap-4">
                                <div className="tier-badge tier-s">S</div>
                                <div className="tier-badge tier-a">A</div>
                                <div className="tier-badge tier-b">B</div>
                                <div className="tier-badge tier-c">C</div>
                                <div className="tier-badge tier-d">D</div>
                            </div>
                        </div>

                        <div>
                            <h3 className="responsive-heading-3 text-text-secondary mb-4">Gaming Glow Effects</h3>
                            <div className="responsive-grid-3">
                                <div className="card-comfortable bg-card-background text-white gaming-glow">Hover for glow</div>
                                <div className="card-comfortable bg-card-background text-white gaming-glow">Hover for glow</div>
                                <div className="card-comfortable bg-card-background text-white gaming-glow">Hover for glow</div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Breakpoint Indicators */}
                <section className="mb-16">
                    <h2 className="responsive-heading-2 text-white mb-8">Current Breakpoint</h2>
                    <div className="bg-card-background rounded-lg p-6">
                        <div className="block xs:hidden text-red-400 font-bold">📱 Extra Small (&lt; 475px)</div>
                        <div className="hidden xs:block sm:hidden text-orange-400 font-bold">📱 Small (475px - 639px)</div>
                        <div className="hidden sm:block md:hidden text-yellow-400 font-bold">📱 Small Tablet (640px - 767px)</div>
                        <div className="hidden md:block lg:hidden text-green-400 font-bold">📱 Tablet (768px - 1023px)</div>
                        <div className="hidden lg:block xl:hidden text-blue-400 font-bold">💻 Desktop (1024px - 1279px)</div>
                        <div className="hidden xl:block 2xl:hidden text-purple-400 font-bold">💻 Large Desktop (1280px - 1535px)</div>
                        <div className="hidden 2xl:block 3xl:hidden text-pink-400 font-bold">💻 Extra Large (1536px - 1919px)</div>
                        <div className="hidden 3xl:block text-indigo-400 font-bold">💻 Ultra Wide (1920px+)</div>
                    </div>
                </section>

                {/* Screen Size Info */}
                <section className="mb-16">
                    <h2 className="responsive-heading-2 text-white mb-8">Screen Size Information</h2>
                    <div className="bg-card-background rounded-lg p-6">
                        <div className="responsive-grid-2">
                            <div>
                                <h4 className="text-lg font-semibold text-white mb-2">Breakpoints:</h4>
                                <ul className="text-text-secondary space-y-1 text-sm">
                                    <li>xs: 475px (Extra small devices)</li>
                                    <li>sm: 640px (Small tablets)</li>
                                    <li>md: 768px (Tablets)</li>
                                    <li>lg: 1024px (Small desktops)</li>
                                    <li>xl: 1280px (Large desktops)</li>
                                    <li>2xl: 1536px (Extra large screens)</li>
                                    <li>3xl: 1920px (Ultra-wide screens)</li>
                                </ul>
                            </div>
                            <div>
                                <h4 className="text-lg font-semibold text-white mb-2">Grid Behavior:</h4>
                                <ul className="text-text-secondary space-y-1 text-sm">
                                    <li>Mobile: 1 column</li>
                                    <li>Small tablet: 2 columns</li>
                                    <li>Desktop: 3 columns</li>
                                    <li>Large desktop: 4 columns</li>
                                    <li>Extra large: 5 columns</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </Layout>
    );
};

export default ResponsiveTestPage;