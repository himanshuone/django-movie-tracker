/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './movies/**/*.html',
    './movietracker/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        // Your custom color palette
        'gray': {
          400: '#9ca3af', // Light gray for secondary text
          600: '#4b5563', // Medium gray for primary text
        },
        'orange': {
          700: '#c2410c', // Dark orange for accents
        },
        'teal': {
          DEFAULT: '#14b8a6', // Primary teal color
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6', // Main teal
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        // Additional colors for a complete movie tracker palette
        'dark': {
          DEFAULT: '#1f2937',
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
        }
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'movie-card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'movie-card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
    },
  },
  plugins: [],
}
