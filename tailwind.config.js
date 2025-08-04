/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      maxWidth: {
        "7xl": "1200px",
      },
      colors: {
        spiritBlossom: {
          pink: {
            50: "#fdf2f8",
            100: "#fce7f3",
            200: "#fbcfe8",
            300: "#f9a8d4",
            400: "#f472b6",
            500: "#ec4899",
            600: "#db2777",
            700: "#be185d",
            800: "#9d174d",
            900: "#831843",
          },
          purple: {
            50: "#faf5ff",
            100: "#f3e8ff",
            200: "#e9d5ff",
            300: "#d8b4fe",
            400: "#c084fc",
            500: "#a855f7",
            600: "#9333ea",
            700: "#7c3aed",
            800: "#6b21a8",
            900: "#581c87",
          },
          gold: {
            50: "#fffbeb",
            100: "#fef3c7",
            200: "#fde68a",
            300: "#fcd34d",
            400: "#fbbf24",
            500: "#f59e0b",
            600: "#d97706",
            700: "#b45309",
            800: "#92400e",
            900: "#78350f",
          },
          teal: {
            50: "#f0fdfa",
            100: "#ccfbf1",
            200: "#99f6e4",
            300: "#5eead4",
            400: "#2dd4bf",
            500: "#14b8a6",
            600: "#0d9488",
            700: "#0f766e",
            800: "#115e59",
            900: "#134e4a",
          },
        },
      },
      animation: {
        float: "float 6s ease-in-out infinite",
        glow: "glow 2s ease-in-out infinite alternate",
        spiritGlow: "spiritGlow 3s ease-in-out infinite alternate",
        petalFloat: "petalFloat 8s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": {
            transform: "translateY(0px)",
          },
          "50%": {
            transform: "translateY(-20px)",
          },
        },
        glow: {
          from: {
            boxShadow: "0 0 20px rgba(59, 130, 246, 0.5)",
          },
          to: {
            boxShadow: "0 0 30px rgba(147, 51, 234, 0.8)",
          },
        },
        spiritGlow: {
          from: {
            boxShadow:
              "0 0 20px rgba(236, 72, 153, 0.4), 0 0 40px rgba(168, 85, 247, 0.3)",
          },
          to: {
            boxShadow:
              "0 0 30px rgba(236, 72, 153, 0.6), 0 0 60px rgba(168, 85, 247, 0.5)",
          },
        },
        petalFloat: {
          "0%, 100%": {
            transform: "translateY(0px) rotate(0deg)",
          },
          "33%": {
            transform: "translateY(-15px) rotate(5deg)",
          },
          "66%": {
            transform: "translateY(-10px) rotate(-3deg)",
          },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
      cursor: {
        hand: 'url("/Hand.cur"), auto',
        "hand-pointer": 'url("/Hand.cur"), pointer',
      },
    },
  },
  plugins: [],
};
