/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {},
    listStyleType: {
      none: 'none',
      disc: 'disc',
      decimal: 'decimal',
      square: 'square',
      roman: 'upper-roman',
    },
    brightness: {
      25: '.25',
      50: '.50',
      100: '1',
    }
  },
  darkMode: 'class',
  plugins: [],
}
