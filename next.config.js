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

module.exports = nextConfig
