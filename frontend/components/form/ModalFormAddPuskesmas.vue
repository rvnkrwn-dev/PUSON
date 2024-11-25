<template>
  <button type="button"
          class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
          aria-haspopup="dialog" aria-expanded="false" aria-controls="hs-scale-animation-modal-form-puskesmas"
          data-hs-overlay="#hs-scale-animation-modal-form-puskesmas">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
      <path fill="currentColor"
            d="M12 4c4.411 0 8 3.589 8 8s-3.589 8-8 8s-8-3.589-8-8s3.589-8 8-8m0-2C6.477 2 2 6.477 2 12s4.477 10 10 10s10-4.477 10-10S17.523 2 12 2m5 9h-4V7h-2v4H7v2h4v4h2v-4h4z"/>
    </svg>
    Puskesmas
  </button>

  <div id="hs-scale-animation-modal-form-puskesmas"
       class="hs-overlay hidden size-full fixed top-0 start-0 z-[80] overflow-x-hidden overflow-y-auto pointer-events-none"
       role="dialog" tabindex="-1" aria-labelledby="hs-scale-animation-modal-form-puskesmas-label">
    <div
        class="hs-overlay-animation-target hs-overlay-open:scale-100 hs-overlay-open:opacity-100 scale-95 opacity-0 ease-in-out transition-all duration-200 sm:max-w-lg sm:w-full m-3 sm:mx-auto min-h-[calc(100%-3.5rem)] flex items-center">
      <div
          class="w-full flex flex-col bg-white border shadow-sm rounded-xl pointer-events-auto ">
        <div class="flex justify-between items-center py-3 px-4 border-b">
          <h3 id="hs-scale-animation-modal-form-puskesmas-label" class="font-bold text-gray-800">
            Tambah Puskesmas
          </h3>
          <button type="button"
                  class="size-8 inline-flex justify-center items-center gap-x-2 rounded-full border border-transparent bg-gray-100 text-gray-800 hover:bg-gray-200 focus:outline-none focus:bg-gray-200 disabled:opacity-50 disabled:pointer-events-none"
                  aria-label="Close" data-hs-overlay="#hs-scale-animation-modal-form-puskesmas">
            <span class="sr-only">Close</span>
            <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                 viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 6 6 18"></path>
              <path d="m6 6 12 12"></path>
            </svg>
          </button>
        </div>
        <div class="p-4 overflow-y-auto">
          <form id="add-puskesmas" @submit.prevent="handleAddPuskesmas">
            <div class="max-w-sm">
              <label for="nama-puskesmas">Nama :</label>
              <input v-model="name" type="text" id="nama-puskesmas"
                     class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                     placeholder="Puskesmas Sokaraja" required>
            </div>
            <div class="max-w-sm mt-2">
              <label for="phone-puskesmas">Nomer HP:</label>
              <input v-model="phone" type="text" id="phone-puskesmas"
                     class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                     placeholder="Puskesmas Sokaraja" required>
            </div>
            <div class="max-w-sm mt-2">
              <label for="address-puskesmas">Alamat :</label>
              <input v-model="address" type="text" id="address-puskesmas"
                     class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                     placeholder="Puskesmas Sokaraja" required>
            </div>
          </form>
        </div>
        <div class="flex justify-end items-center gap-x-2 py-3 px-4 border-t">
          <button type="button"
                  class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none"
                  data-hs-overlay="#hs-scale-animation-modal-form-puskesmas">
            Close
          </button>
          <button type="submit"
                  form="add-puskesmas"
                  class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
                  :disabled="isLoading">
            Save changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Swal from "sweetalert2";

// Mendeklarasikan variabel yang digunakan untuk menyimpan input pengguna
const name = ref<string>()
const address = ref<string>()
const phone = ref<string>()
const isLoading = ref<boolean>(false);

// Mendeklarasikan event emitter untuk mengirimkan event setelah data berhasil ditambahkan
const emit = defineEmits(['puskesmasAdded'])

// Fungsi untuk membersihkan form setelah data berhasil ditambahkan
const clearFormAddPuskesmas = () => {
  name.value = "";
  address.value = "";
  phone.value = "";
};

// Fungsi utama untuk menangani proses penambahan data puskesmas
const handleAddPuskesmas = async () => {
  try {
    // Mengatur status loading menjadi true sebelum memulai proses
    isLoading.value = true;

    if (!name.value || !address.value || !phone.value) {
      await Swal.fire({
        position: "bottom-end",
        icon: "warning",
        title: "Harap isi semua field",
        showConfirmButton: false,
        timer: 1500,
        toast: true
      });
      return;
    }

    // Mengirimkan data ke API
    const data = await useFetchApi('https://puso-be.vercel.app/auth/puskesmas', {
      method: 'POST',
      body: {
        name: name.value,
        address: address.value,
        phone: phone.value
      }
    })

    // Menampilkan notifikasi jika data berhasil ditambahkan
    await Swal.fire({
      position: "bottom-end",
      icon: "success",
      title: "Sukses menambah data puskesmas",
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });

    // Membersihkan form dan mengirimkan event 'puskesmasAdded'
    clearFormAddPuskesmas();
    emit('puskesmasAdded', data);

    // Menutup modal dengan mensimulasikan klik pada tombol
    const button = document.querySelector('[data-hs-overlay="#hs-scale-animation-modal-form-puskesmas"]');
    if (button) {
      button.click();
    }
  } catch (e) {
    // Menampilkan notifikasi jika terjadi error saat menambah data
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Gagal menambah data puskemas",
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  } finally {
    // Menetapkan status loading menjadi false setelah proses selesai
    isLoading.value = false;
  }
}
</script>


<style scoped>

</style>