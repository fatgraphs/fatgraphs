module.exports = {
    important: true,
    purge: [],
    darkMode: false,
    theme: {
        extend: {
            gridTemplateColumns: {
                'tokenGraphLayout': 'minmax(0, 0.15fr) minmax(0, 0.7fr) minmax(0, 0.15fr)'
            },
            gridTemplateRows: {
                'tokenGraphLayout': 'minmax(0, 0.10fr) minmax(0, 0.90fr)'
            }
        },
    },
    variants: {
        extend: {
            backgroundColor: ['odd'],
            fontSize: ['active'],
        },
    },
    plugins: [],
}
