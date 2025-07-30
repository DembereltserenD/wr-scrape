import React from 'react';
import Head from 'next/head';
import { useLanguage } from '../../contexts/LanguageContext';

interface SEOHeadProps {
    title?: string;
    description?: string;
    keywords?: string;
    image?: string;
    url?: string;
    type?: 'website' | 'article';
    publishedTime?: string;
    modifiedTime?: string;
    author?: string;
    section?: string;
    tags?: string[];
}

const SEOHead: React.FC<SEOHeadProps> = ({
    title,
    description,
    keywords,
    image = '/og-image.jpg',
    url = 'https://wildriftguide.com/',
    type = 'website',
    publishedTime,
    modifiedTime,
    author = 'Wild Rift Guide',
    section,
    tags = []
}) => {
    const { t, locale } = useLanguage();

    const defaultTitle = `Wild Rift ${t('navigation.champions')} Guide - ${t('hero.title')}`;
    const defaultDescription = `${t('hero.description')} - Wild Rift ${t('navigation.champions')}, ${t('navigation.items')}, ${t('navigation.runes')} guides and tier lists.`;
    const defaultKeywords = `Wild Rift, League of Legends, ${t('navigation.champions')}, ${t('navigation.items')}, ${t('navigation.runes')}, tier list, guide, meta, builds`;

    const seoTitle = title || defaultTitle;
    const seoDescription = description || defaultDescription;
    const seoKeywords = keywords || defaultKeywords;

    const structuredData = {
        "@context": "https://schema.org",
        "@type": type === 'article' ? 'Article' : 'WebSite',
        "name": seoTitle,
        "url": url,
        "description": seoDescription,
        "inLanguage": locale === 'mn' ? 'mn' : 'en',
        ...(type === 'website' && {
            "potentialAction": {
                "@type": "SearchAction",
                "target": "https://wildriftguide.com/search?q={search_term_string}",
                "query-input": "required name=search_term_string"
            }
        }),
        ...(type === 'article' && {
            "headline": seoTitle,
            "author": {
                "@type": "Person",
                "name": author
            },
            ...(publishedTime && { "datePublished": publishedTime }),
            ...(modifiedTime && { "dateModified": modifiedTime }),
            ...(section && { "articleSection": section }),
            ...(tags.length > 0 && { "keywords": tags.join(', ') })
        })
    };

    return (
        <Head>
            {/* Basic Meta Tags */}
            <title>{seoTitle}</title>
            <meta name="description" content={seoDescription} />
            <meta name="keywords" content={seoKeywords} />
            <meta name="author" content={author} />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <meta name="robots" content="index, follow" />
            <link rel="canonical" href={url} />

            {/* Language and Locale */}
            <meta httpEquiv="content-language" content={locale} />
            <link rel="alternate" hrefLang="mn" href={url.replace(/\/(en\/)?/, '/mn/')} />
            <link rel="alternate" hrefLang="en" href={url.replace(/\/(mn\/)?/, '/en/')} />
            <link rel="alternate" hrefLang="x-default" href={url} />

            {/* Open Graph / Facebook */}
            <meta property="og:type" content={type} />
            <meta property="og:url" content={url} />
            <meta property="og:title" content={seoTitle} />
            <meta property="og:description" content={seoDescription} />
            <meta property="og:image" content={image} />
            <meta property="og:image:width" content="1200" />
            <meta property="og:image:height" content="630" />
            <meta property="og:locale" content={locale === 'mn' ? 'mn_MN' : 'en_US'} />
            <meta property="og:site_name" content="Wild Rift Guide" />

            {/* Twitter Card */}
            <meta name="twitter:card" content="summary_large_image" />
            <meta name="twitter:url" content={url} />
            <meta name="twitter:title" content={seoTitle} />
            <meta name="twitter:description" content={seoDescription} />
            <meta name="twitter:image" content={image} />
            <meta name="twitter:creator" content="@wildriftguide" />
            <meta name="twitter:site" content="@wildriftguide" />

            {/* Article specific meta tags */}
            {type === 'article' && (
                <>
                    {publishedTime && <meta property="article:published_time" content={publishedTime} />}
                    {modifiedTime && <meta property="article:modified_time" content={modifiedTime} />}
                    {author && <meta property="article:author" content={author} />}
                    {section && <meta property="article:section" content={section} />}
                    {tags.map((tag, index) => (
                        <meta key={index} property="article:tag" content={tag} />
                    ))}
                </>
            )}

            {/* Favicon and Icons */}
            <link rel="icon" href="/favicon.ico" />
            <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
            <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
            <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
            <link rel="manifest" href="/site.webmanifest" />
            <meta name="theme-color" content="#8b5cf6" />
            <meta name="msapplication-TileColor" content="#8b5cf6" />

            {/* Performance and Preconnect */}
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
            <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
            <link rel="dns-prefetch" href="https://fonts.gstatic.com" />

            {/* JSON-LD Structured Data */}
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{
                    __html: JSON.stringify(structuredData)
                }}
            />

            {/* Additional Performance Hints */}
            <meta name="format-detection" content="telephone=no" />
            <meta name="mobile-web-app-capable" content="yes" />
            <meta name="apple-mobile-web-app-capable" content="yes" />
            <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        </Head>
    );
};

export default SEOHead;