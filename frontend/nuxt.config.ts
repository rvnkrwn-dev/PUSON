// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2024-04-03',
    devtools: {enabled: false},
    modules: [
        '@nuxtjs/tailwindcss'
    ],
    plugins: ["~/plugins/preline.client.ts"],
    runtimeConfig: {
        public: {
            apiUrl: "http://127.0.0.1:5000"
        }
    }
})
