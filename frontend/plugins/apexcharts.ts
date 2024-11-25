// plugins/apexcharts.ts
import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(async (nuxtApp) => {
    if (process.client) {
        // Dynamic import for client-side
        const VueApexCharts = (await import('vue3-apexcharts')).default
        nuxtApp.vueApp.use(VueApexCharts)
        nuxtApp.vueApp.component('ApexCharts', VueApexCharts)
    }
})