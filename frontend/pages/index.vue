<template>
  <!-- Breadcrumb -->
  <div
      class="sticky top-0 inset-x-0 z-20 bg-white border-y px-4 sm:px-6 lg:px-8 lg:hidden">
    <div class="flex items-center py-2">
      <!-- Navigation Toggle -->
      <button type="button"
              class="size-8 flex justify-center items-center gap-x-2 border border-gray-200 text-gray-800 hover:text-gray-500 rounded-lg focus:outline-none focus:text-gray-500 disabled:opacity-50 disabled:pointer-events-none"
              aria-haspopup="dialog" aria-expanded="false" aria-controls="hs-application-sidebar"
              aria-label="Toggle navigation" data-hs-overlay="#hs-application-sidebar">
        <span class="sr-only">Toggle Navigation</span>
        <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
             fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect width="18" height="18" x="3" y="3" rx="2"/>
          <path d="M15 3v18"/>
          <path d="m8 9 3 3-3 3"/>
        </svg>
      </button>
      <!-- End Navigation Toggle -->

      <!-- Breadcrumb -->
      <ol class="ms-3 flex items-center whitespace-nowrap">
        <li class="flex items-center text-sm text-gray-800">
          Aplikasi
          <svg class="shrink-0 mx-3 overflow-visible size-2.5 text-gray-400 " width="16"
               height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 1L10.6869 7.16086C10.8637 7.35239 10.8637 7.64761 10.6869 7.83914L5 14" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round"/>
          </svg>
        </li>
        <li class="text-sm font-semibold text-gray-800 truncate" aria-current="page">
          Dashboard
        </li>
      </ol>
      <!-- End Breadcrumb -->
    </div>
  </div>
  <!-- End Breadcrumb -->

  <!-- Content -->
  <div class="w-full lg:ps-64">
    <div class="p-4 sm:p-6 space-y-4 sm:space-y-6">
      <!-- Grid -->
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <!-- Card -->
        <div class="flex flex-col bg-white border shadow-sm rounded-xl">
          <div class="p-4 md:p-5">
            <div class="flex items-center gap-x-2">
              <p class="text-xs uppercase tracking-wide text-gray-500">
                Total Puskesmas
              </p>
            </div>

            <div class="mt-1 flex items-center gap-x-2">
              <h3 class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.puskesmas?.total }}
              </h3>
<!--              <span class="flex items-center gap-x-1 text-green-600">-->
<!--                <svg class="inline-block size-4 self-center" xmlns="http://www.w3.org/2000/svg" width="24" height="24"-->
<!--                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"-->
<!--                     stroke-linejoin="round">-->
<!--                  <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>-->
<!--                  <polyline points="16 7 22 7 22 13"/>-->
<!--                </svg>-->
<!--                <span class="inline-block text-sm">-->
<!--                  1.7%-->
<!--                </span>-->
<!--              </span>-->
            </div>
          </div>
        </div>
        <!-- End Card -->

        <!-- Card -->
        <div class="flex flex-col bg-white border shadow-sm rounded-xl">
          <div class="p-4 md:p-5">
            <div class="flex items-center gap-x-2">
              <p class="text-xs uppercase tracking-wide text-gray-500">
                Total Posyandu
              </p>
            </div>

            <div class="mt-1 flex items-center gap-x-2">
              <h3 class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.posyandu?.total }}
              </h3>
            </div>
          </div>
        </div>
        <!-- End Card -->

        <!-- Card -->
        <div class="flex flex-col bg-white border shadow-sm rounded-xl">
          <div class="p-4 md:p-5">
            <div class="flex items-center gap-x-2">
              <p class="text-xs uppercase tracking-wide text-gray-500">
                Total Pengguna
              </p>
            </div>

            <div class="mt-1 flex items-center gap-x-2">
              <h3 class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.user?.total }}
              </h3>
<!--              <span class="flex items-center gap-x-1 text-red-600">-->
<!--                <svg class="inline-block size-4 self-center" xmlns="http://www.w3.org/2000/svg" width="24" height="24"-->
<!--                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"-->
<!--                     stroke-linejoin="round">-->
<!--                  <polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/>-->
<!--                  <polyline points="16 17 22 17 22 11"/>-->
<!--                </svg>-->
<!--                <span class="inline-block text-sm">-->
<!--                  1.7%-->
<!--                </span>-->
<!--              </span>-->
            </div>
          </div>
        </div>
        <!-- End Card -->

        <!-- Card -->
        <div class="flex flex-col bg-white border shadow-sm rounded-xl">
          <div class="p-4 md:p-5">
            <div class="flex items-center gap-x-2">
              <p class="text-xs uppercase tracking-wide text-gray-500">
                Total Anak
              </p>
              <div class="hs-tooltip">
                <div class="hs-tooltip-toggle">
                  <svg class="shrink-0 size-4 text-gray-500" xmlns="http://www.w3.org/2000/svg"
                       width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                       stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <path d="M12 17h.01"/>
                  </svg>
                  <span
                      class="hs-tooltip-content hs-tooltip-shown:opacity-100 hs-tooltip-shown:visible opacity-0 transition-opacity inline-block absolute invisible z-10 py-1 px-2 bg-gray-900 text-xs font-medium text-white rounded shadow-sm"
                      role="tooltip">
                    {{ stats?.anak?.lakiLaki }} laki dan {{ stats?.anak?.perempuan }} perempuan
                  </span>
                </div>
              </div>
            </div>

            <div class="mt-1 flex items-center gap-x-2">
              <h3 class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.anak?.total }}
              </h3>
            </div>
          </div>
        </div>
        <!-- End Card -->
      </div>
      <!-- End Grid -->

      <div class="grid lg:grid-cols-2 gap-4 sm:gap-6">
        <!-- Card -->
        <div
            class="p-4 md:p-5 min-h-[410px] flex flex-col bg-white border shadow-sm rounded-xl">
          <!-- Header -->
          <div class="flex justify-between items-center">
            <div>
              <h2 class="text-sm text-gray-500">
                Stunting
              </h2>
              <p class="text-xl sm:text-2xl font-medium text-gray-800">
                30
              </p>
            </div>

            <div>
              <span
                  class="py-[5px] px-1.5 inline-flex items-center gap-x-1 text-xs font-medium rounded-md bg-teal-100 text-teal-800">
                <svg class="inline-block size-3.5" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                     stroke-linejoin="round">
                  <path d="M12 5v14"/>
                  <path d="m19 12-7 7-7-7"/>
                </svg>
                25%
              </span>
            </div>
          </div>
          <!-- End Header -->

          <div id="hs-multiple-bar-charts" class="h-full w-full">
            <BarChart v-if="monthsOfBarChart.length > 0" :series="dataOfBarChart??[]" :categories="monthsOfBarChart??[]" :color="['#3347ff', '#d333ff']" />
            <div v-else-if="isLoadingBarChart" class="h-full w-full flex flex-col items-center justify-center">
              <p class="text-gray-500">Memuat...</p>
            </div>
            <div v-else class="h-full w-full flex flex-col items-center justify-center">
              <p class="text-gray-500">Tidak ada data</p>
            </div>
          </div>
        </div>
        <!-- End Card -->

        <!-- Card -->
        <div
            class="p-4 md:p-5 min-h-[410px] flex flex-col bg-white border shadow-sm rounded-xl">
          <!-- Header -->
          <div class="flex justify-between items-center">
            <div>
              <h2 class="text-sm text-gray-500">
                Anak
              </h2>
              <p class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.anak?.total }}
              </p>
            </div>

            <div>
              <span
                  class="py-[5px] px-1.5 inline-flex items-center gap-x-1 text-xs font-medium rounded-md bg-red-100 text-red-800">
                <svg class="inline-block size-3.5" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                     stroke-linejoin="round">
                  <path d="M12 5v14"/>
                  <path d="m19 12-7 7-7-7"/>
                </svg>
                2%
              </span>
            </div>
          </div>
          <!-- End Header -->

          <div id="hs-single-area-chart" class="h-full w-full">
            <AreaChart v-if="monthsOfAreaChart.length > 0" :series="dataOfAreaChart??[]" :categories="monthsOfAreaChart??[]" :color="['#3347ff', '#d333ff']" />
            <div v-else-if="isLoadingAreaChart" class="h-full w-full flex flex-col items-center justify-center">
              <p class="text-gray-500">Memuat...</p>
            </div>
            <div v-else class="h-full w-full flex flex-col items-center justify-center">
              <p class="text-gray-500">Tidak ada data</p>
            </div>
          </div>
        </div>
        <!-- End Card -->
      </div>

      <!-- Card -->

      <!-- End Card -->
    </div>
  </div>
</template>

<script setup lang="ts">
import Swal from 'sweetalert2'
import {sleep} from "@antfu/utils";
import BarChart from "~/components/chart/BarChart.vue";
import AreaChart from "~/components/chart/AreaChart.vue";

// config
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl;

const stats = ref({
  "anak": {
    "lakiLaki": 0,
    "perempuan": 0,
    "total": 0
  },
  "posyandu": {
    "total": 0
  },
  "puskesmas": {
    "total": 0
  },
  "user": {
    "total": 0
  }
});

const fetchStats = async () => {
  try {
    await sleep(2000)
    stats.value = await useFetchApi('https://puso-be.vercel.app/auth/stats/all-data')
  } catch (e) {
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Gagal memuat data statistik",
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  }
}

const monthsOfAreaChart = ref<string[]>([]);  // To store the months (bulan)
const dataOfAreaChart = ref<Array<{ name: string, data: number[] }>>([]);  // To store the series data (Laki-laki, Perempuan)
const isLoadingAreaChart = ref<boolean>(true)

const monthsOfBarChart = ref<string[]>([]);  // To store the months (bulan)
const dataOfBarChart = ref<Array<{ name: string, data: number[] }>>([]);  // To store the series data (Laki-laki, Perempuan)
const isLoadingBarChart = ref<boolean>(true)

// Function to fetch and process the data
const fetchGraphAnak = async () => {
  try {
    isLoadingAreaChart.value = true;
    await sleep(2000) // Menunggu beberapa detik untuk simulasi loading
    // Fetch data from the API
    const data = await useFetchApi(`${apiUrl}/auth/stats/grafik-anak`);

    // Initialize empty arrays for storing the processed data
    const lakiLakiData: number[] = [];
    const perempuanData: number[] = [];

    // Process the response data to fit the chart format
    data.forEach((item: { bulan: string, jumlah_laki_laki: number, jumlah_perempuan: number }) => {
      monthsOfAreaChart.value.push(item.bulan.slice(0, 3));  // Add month to categories
      lakiLakiData.push(item.jumlah_laki_laki);  // Add jumlah_laki_laki to the series data
      perempuanData.push(item.jumlah_perempuan);  // Add jumlah_perempuan to the series data
    });

    // Format chart data
    dataOfAreaChart.value = [
      { name: 'Laki-laki', data: lakiLakiData },
      { name: 'Perempuan', data: perempuanData }
    ];

  } catch (error) {
    console.error('Failed to fetch data:', error);
  } finally {
    isLoadingAreaChart.value = false;
  }
}

const fetchGraphStunting = async () => {
  try {
    isLoadingBarChart.value = true;
    await sleep(2000) // Menunggu beberapa detik untuk simulasi loading
    // Fetch data from the API
    const data = await useFetchApi(`${apiUrl}/auth/stats/grafik-stunting`);

    // Initialize empty arrays for storing the processed data
    const dataTotal: number[] = [];

    // Process the response data to fit the chart format
    data.forEach((item: { bulan: string, total: number }) => {
      monthsOfBarChart.value.push(item.bulan.slice(0, 3));
      dataTotal.push(item.total);  // Add total to the series data
    });

    // Format chart data
    dataOfBarChart.value = [
      { name: 'Total', data: dataTotal },
    ];
  } catch (error) {
    console.error('Failed to fetch data:', error);
  } finally {
    isLoadingBarChart.value = false;
  }
}

onMounted(async () => {
  await fetchStats()
  await fetchGraphAnak()
  await fetchGraphStunting()
})
</script>

<style scoped>

</style>