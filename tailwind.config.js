/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'gold': {
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          600: '#d97706',
          800: '#92400e',
        }
      }
    },
  },
  plugins: [],
}
