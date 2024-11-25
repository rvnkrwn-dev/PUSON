<template>
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
          <svg class="shrink-0 mx-3 overflow-visible size-2.5 text-gray-400" width="16"
               height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 1L10.6869 7.16086C10.8637 7.35239 10.8637 7.64761 10.6869 7.83914L5 14" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round"/>
          </svg>
        </li>
        <li class="flex items-center text-sm text-gray-800 truncate">
          <NuxtLink to="/">Dashboard</NuxtLink>
          <svg class="shrink-0 mx-3 overflow-visible size-2.5 text-gray-400" width="16"
               height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 1L10.6869 7.16086C10.8637 7.35239 10.8637 7.64761 10.6869 7.83914L5 14" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round"/>
          </svg>
        </li>
        <li class="flex items-center text-sm font-semibold text-gray-800 truncate"
            aria-current="page">
          Puskesmas
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
              <div class="py-3 px-4 flex justify-between gap-2">
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

                <ModalFormAddPuskesmas @puskesmasAdded="handlePuskesmasAdded"/>
              </div>

              <!-- Table -->
              <div class="overflow-hidden">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase">Nama</th>
                    <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase">Alamat
                    </th>
                    <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase">Nomor</th>
                    <th scope="col" class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase">Aksi</th>
                  </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-200">
                  <!-- Loop through filtered data -->
                  <template v-if="filteredData.length > 0">
                    <tr v-for="(item, index) in filteredData" :key="index">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">{{ item.name }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{{ item.address }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{{ item.phone }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                        <button type="button"
                                @click="handleDelete(item?.id)"
                                class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 focus:outline-none focus:text-blue-800 disabled:opacity-50 disabled:pointer-events-none">
                          Hapus
                        </button>
                      </td>
                    </tr>
                  </template>
                  <template v-else-if="isLoading">
                    <tr>
                      <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500">
                        Memuat...
                      </td>
                    </tr>
                  </template>
                  <template v-else>
                    <tr>
                      <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500">
                        Tidak ada data yang ditemukan.
                      </td>
                    </tr>
                  </template>
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
import Swal from 'sweetalert2'
import ModalFormAddPuskesmas from "~/components/form/ModalFormAddPuskesmas.vue";
import { sleep } from "@antfu/utils";

// Mendeklarasikan variabel state
const searchQuery = ref(''); // Input pencarian
const dataPuskesmas = ref<any[]>([]); // Menyimpan data Puskesmas dari API
const isLoading = ref<boolean>(false); // Status loading untuk menampilkan spinner

// Fungsi untuk mengambil data puskesmas dari API
const fetchPuskesmas = async () => {
  try {
    isLoading.value = true; // Menandakan proses sedang berlangsung
    await sleep(2000) // Menunggu beberapa detik untuk simulasi loading
    const response = await useFetchApi('https://puso-be.vercel.app/auth/puskesmas'); // Mengambil data puskesmas
    dataPuskesmas.value = response ?? []; // Menyimpan data yang berhasil diambil, jika tidak ada data kosongkan array
  } catch (err) {
    // Menampilkan alert error jika terjadi kesalahan saat mengambil data
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Gagal memuat data puskesmas",
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  } finally {
    isLoading.value = false; // Menandakan proses selesai, baik sukses maupun gagal
  }
};

// Properti computed untuk memfilter data berdasarkan query pencarian
const filteredData = computed(() => {
  return dataPuskesmas.value.filter(item => {
    // Memeriksa apakah nama, alamat, atau nomor telepon mengandung teks pencarian
    return item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        item.address.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        item.phone.toLowerCase().includes(searchQuery.value.toLowerCase());
  });
});

// Fungsi untuk menangani penambahan puskesmas baru
const handlePuskesmasAdded = (newPuskesmas: { name: string, address: string, phone: string }) => {
  // Menambahkan puskesmas baru ke dalam daftar yang ada
  puskesmasList.value.push(newPuskesmas);
}

// Fungsi untuk menangani penghapusan puskesmas
const handleDelete = async (id: number) => {
  // Menampilkan konfirmasi penghapusan
  Swal.fire({
    title: "Anda yakin?",
    text: "Anda tidak dapat mengembalikan ini!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    cancelButtonText: "Batal",
    confirmButtonText: "Ya, hapus!"
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        // Mengirim permintaan DELETE ke API untuk menghapus data
        await useFetchApi(`https://puso-be.vercel.app/auth/puskesmas/${id}`, {
          method: 'DELETE',
        });

        // Menghapus data lokal setelah berhasil dihapus dari server
        dataPuskesmas.value = dataPuskesmas.value.filter(item => item.id !== id);

        // Menampilkan notifikasi sukses
        await Swal.fire({
          position: "bottom-end",
          icon: "success",
          title: "Sukses mengahapus data puskesmas",
          showConfirmButton: false,
          timer: 1500,
          toast: true
        });
      } catch (err) {
        // Menampilkan notifikasi error jika terjadi kesalahan
        await Swal.fire({
          position: "bottom-end",
          icon: "error",
          title: "Gagal menghapus data puskesmas",
          showConfirmButton: false,
          timer: 1500,
          toast: true
        });
      }
    }
  })
}

// Fungsi ini dipanggil saat komponen pertama kali dimuat untuk mengambil data puskesmas
onMounted(async () => {
  await fetchPuskesmas();
});
</script>

<style lang="css" scoped>

</style>