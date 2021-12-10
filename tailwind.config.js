module.exports = {
  content: ["./static/src/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
purge: {
    enabled: true,
    content: [
        './**/*.html'
    ]
}
