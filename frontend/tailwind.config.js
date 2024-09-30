/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './node_modules/preline/preline.js',
        './layouts/*.{vue,js,ts, html}',
        './pages/*.{vue,js,ts, html}',
        './pages/**/*.{vue,js,ts, html}',
        './pages/**/**/*.{vue,js,ts, html}',
        './components/*.{vue,js,ts, html}',
        './components/**/*.{vue,js,ts, html}',
        './components/**/**/*.{vue,js,ts, html}',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        // require('@tailwindcss/forms'),
        require('preline/plugin'),
    ],
}

