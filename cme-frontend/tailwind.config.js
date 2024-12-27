/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        wine: {
          200: '#D1A7AC',
          700: '#722F37',
          800: '#5E2A30',
        },
      },
    },
  },
  plugins: [],
}

