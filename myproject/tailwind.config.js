const plugin = require('tailwindcss/plugin');
const colors = require('tailwindcss/colors')

module.exports = {
    darkMode: 'class',
    content: [
        './templates/**/*.html',
        './static_src/**/*.{js,ts}',
    ],
    theme: {
        // Properties directly inside of theme will overwrite all tailwinds default properties for that attribute
        screens: {
            'tall': 
            {
                'raw': '(min-height: 840px)'
            },
            // Override default breakpoints removing sm
            sm: '412px',
            // => @media (min-width: 420px) { ... }
            md: '768px',
            // => @media (min-width: 768px) { ... }
            lg: '1024px',
            // => @media (min-width: 1024px) { ...
        },
        colors: {
            ...colors,
            'white': '#FFFFFF',
            'black': '#000000',
            'mackerel': {
                100: '#7777774D',
                200: '#96D7E5',
                300: '#26899E',
                400: '#1A2A2E',
            },
            'grey': {
                100: '#EFEFEF',
                200: '#E6E6E6',
                300: '#CCCCCC',
                400: '#B3B3B3',
                500: '#999999',
                600: '#808080',
                700: '#4D4D4D',
                800: '#3A3A3A',
                900: '#1E1E1E',
            },
            'inherit': 'inherit',
            'current': 'currentColor',
            'transparent': 'transparent',
        },
        fontSize: {
            // Sizes are 12 16 20 22 25 28 32 36 40 48 60
            'xs': ['12px', '1.2'],
            'sm': ['14px', '1.2'],
            'base': ['16px', '1.2'],
            'lg': ['18px', '1.2'],
            'xl': ['20px', '1.2'],
            '2xl': ['24px', '1.2'],
            '3xl': ['28px', '1.2'],
            '4xl': ['36px', '1.2'],
            '5xl': ['38px', '1.2'],
            '6xl': ['48px', '1.2'],
            '7xl': ['60px', '1.2'],
            '8xl': ['70px', '1.2'],
            '9xl': ['80px', '1.2'],
            '10xl': ['100px', '1.2'],
        },
        fontFamily: {
            sans3: ["'Source Sans 3', sans-serif"],
            serif4: ["'Source Serif 4', serif"],
            codepro: ["'Source Code Pro', monospace"],
        },
        extend: {
            backgroundImage: {
                'slash': `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='#26899E' viewBox='0 0 11 11'%3E%3Cpath d='M1.78239 10.8013L0.900391 9.99126L4.19439 6.60726L4.78839 7.14726L1.78239 10.8013ZM7.39839 4.33926L6.80439 3.79926L9.81039 0.145264L10.6924 0.955263L7.39839 4.33926Z' /%3E%3C/svg%3E");`
            },
        },
    }
};
