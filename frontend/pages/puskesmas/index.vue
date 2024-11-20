<template>
  <div
      class="sticky top-0 inset-x-0 z-20 bg-white border-y px-4 sm:px-6 lg:px-8 lg:hidden dark:bg-neutral-800 dark:border-neutral-700">
    <div class="flex items-center py-2">
      <!-- Navigation Toggle -->
      <button type="button"
              class="size-8 flex justify-center items-center gap-x-2 border border-gray-200 text-gray-800 hover:text-gray-500 rounded-lg focus:outline-none focus:text-gray-500 disabled:opacity-50 disabled:pointer-events-none dark:border-neutral-700 dark:text-neutral-200 dark:hover:text-neutral-500 dark:focus:text-neutral-500"
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
        <li class="flex items-center text-sm text-gray-800 dark:text-neutral-400">
          Application Layout
          <svg class="shrink-0 mx-3 overflow-visible size-2.5 text-gray-400 dark:text-neutral-500" width="16"
               height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 1L10.6869 7.16086C10.8637 7.35239 10.8637 7.64761 10.6869 7.83914L5 14" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round"/>
          </svg>
        </li>
        <li class="text-sm font-semibold text-gray-800 truncate dark:text-neutral-400" aria-current="page">
          Dashboard
        </li>
      </ol>
      <!-- End Breadcrumb -->
    </div>
  </div>

  <div class="w-full min-h-screen bg-gray-50 lg:ps-64">
    <div class="p-4 sm:p-6 space-y-4 sm:space-y-6">
      <div class="flex flex-col">
        <div class="-m-1.5 overflow-x-auto">
          <div class="p-1.5 min-w-full inline-block align-middle">
            <div class="border rounded-lg divide-y divide-gray-200 bg-white">
              <div class="py-3 px-4">
                <!-- Search Input -->
                <div class="relative max-w-xs">
                  <label for="hs-table-search" class="sr-only">Search</label>
                  <input
                      type="text"
                      id="hs-table-search"
                      v-model="searchQuery"
                      class="py-2 px-3 ps-9 block w-full border border-gray-200 shadow-sm rounded-lg text-sm focus:z-10 focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                      placeholder="Search for Puskesmas"
                  />
                  <div class="absolute inset-y-0 start-0 flex items-center pointer-events-none ps-3">
                    <svg class="size-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                         stroke-linejoin="round">
                      <circle cx="11" cy="11" r="8"></circle>
                      <path d="m21 21-4.3-4.3"></path>
                    </svg>
                  </div>
                </div>
              </div>

              <!-- Table -->
              <div class="overflow-hidden">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase">Name</th>
                    <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase">Address
                    </th>
                    <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase">Phone</th>
                    <th scope="col" class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase">Action</th>
                  </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-200">
                  <!-- Loop through filtered data -->
                  <tr v-for="(item, index) in filteredData" :key="index">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">{{ item.name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{{ item.address }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{{ item.phone }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                      <button type="button"
                              @click="handleDelete(item?.id)"
                              class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 focus:outline-none focus:text-blue-800 disabled:opacity-50 disabled:pointer-events-none">
                        Delete
                      </button>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue';
import {sleep} from '@antfu/utils';

// Declare state variables
const searchQuery = ref(''); // Search query input
const dataPosyandu = ref<any[]>([]); // API data

// Fetch function
const fetchPosyandu = async () => {
  try {
    await sleep(2000); // Simulate delay if server is slow
    const response = await useFetchApi('https://puso-be.vercel.app/auth/puskesmas');
    dataPosyandu.value = response ?? []; // Assign fetched data
  } catch (err) {
    console.error('Error fetching data: ', err);
    alert('Gagal memuat data posyandu');
  }
};

// Computed property to filter data based on search query
const filteredData = computed(() => {
  return dataPosyandu.value.filter(item => {
    return item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        item.address.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        item.phone.toLowerCase().includes(searchQuery.value.toLowerCase());
  });
});

const handleDelete = async (id: number) => {
  try {
    await sleep(2000); // Simulate delay if server is slow
    await useFetchApi(`https://puso-be.vercel.app/auth/puskesmas/${id}` ,{
      method: 'DELETE',
    });
    alert('Sukses mengahapus data posyandu');
  } catch (err) {
    console.error('Error fetching data: ', err);
    alert('Gagal menghapus data posyandu');
  }
}

// On component mounted, fetch data
onMounted(() => {
  fetchPosyandu();
});
</script>

<style scoped>
/* Scoped CSS can be added here */
</style>
