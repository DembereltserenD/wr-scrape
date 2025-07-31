/** @type {import('next').NextConfig} */
const nextConfig = {
  i18n: {
    // Default locale (Mongolian)
    defaultLocale: 'mn',
    // Supported locales
    locales: ['mn', 'en'],
    // Locale detection
    localeDetection: false,
  },
  // Image optimization
  images: {
    remotePatterns: [{
        protocol: 'https',
        hostname: 'wr-meta.com',
        port: '',
        pathname: '/uploads/**',
      },
      {
        protocol: 'https',
        hostname: 'cdn.wr-meta.com',
        port: '',
        pathname: '/**',
      },
    ],
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60,
  },
  // Performance optimizations
  experimental: {
    scrollRestoration: true,
    optimizePackageImports: ['recharts'],
  },
  // Compression
  compress: true,
  // Static optimization
  trailingSlash: false,
  // Webpack optimizations
  webpack: (config, {
    dev,
    isServer
  }) => {
    if (!dev && !isServer) {
      // Optimize for production builds
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          default: false,
          vendors: false,
          // Vendor chunk
          vendor: {
            name: 'vendor',
            chunks: 'all',
            test: /node_modules/,
            priority: 20,
          },
          // Common chunk
          common: {
            name: 'common',
            minChunks: 2,
            chunks: 'all',
            priority: 10,
            reuseExistingChunk: true,
            enforce: true,
          },
        },
      };
    }
    return config;
  },
  // Bundle analyzer (enable when needed)
  // bundleAnalyzer: {
  //   enabled: process.env.ANALYZE === 'true',
  // },
  // Optional: domain-based routing
  // domains: [
  //   {
  //     domain: 'example.mn',
  //     defaultLocale: 'mn',
  //   },
  //   {
  //     domain: 'example.com',
  //     defaultLocale: 'en',
  //   },
  // ],
}

// Bundle analyzer (conditionally loaded)
let finalConfig = nextConfig;

if (process.env.ANALYZE === 'true') {
  try {
    const withBundleAnalyzer = require('@next/bundle-analyzer')({
      enabled: true,
    });
    finalConfig = withBundleAnalyzer(nextConfig);
  } catch (error) {
    console.warn('Bundle analyzer not available, skipping...');
  }
}

module.exports = finalConfig;