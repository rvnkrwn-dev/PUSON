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
            apiUrl: "https://puso-be.vercel.app"
        }
    },
    app: {
        head: {
            title: "PUSON | Posyandu Untuk Stunting Online",
            htmlAttrs: {
                lang: 'id'
            }
        }
    }
})
