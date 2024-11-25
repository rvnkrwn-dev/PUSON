<template>
  <button type="button"
          class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
          aria-haspopup="dialog" aria-expanded="false" aria-controls="hs-scale-animation-modal-form-anak"
          data-hs-overlay="#hs-scale-animation-modal-form-anak">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
      <path fill="currentColor"
            d="M12 4c4.411 0 8 3.589 8 8s-3.589 8-8 8s-8-3.589-8-8s3.589-8 8-8m0-2C6.477 2 2 6.477 2 12s4.477 10 10 10s10-4.477 10-10S17.523 2 12 2m5 9h-4V7h-2v4H7v2h4v4h2v-4h4z"/>
    </svg>
    Anak
  </button>

  <div id="hs-scale-animation-modal-form-anak"
       class="hs-overlay hidden size-full fixed top-0 start-0 z-[80] overflow-x-hidden overflow-y-auto pointer-events-none"
       role="dialog" tabindex="-1" aria-labelledby="hs-scale-animation-modal-form-anak-label">
    <div
        class="hs-overlay-animation-target hs-overlay-open:scale-100 hs-overlay-open:opacity-100 scale-95 opacity-0 ease-in-out transition-all duration-200 sm:max-w-lg sm:w-full m-3 sm:mx-auto min-h-[calc(100%-3.5rem)] flex items-center">
      <div
          class="w-full flex flex-col bg-white border shadow-sm rounded-xl pointer-events-auto ">
        <div class="flex justify-between items-center py-3 px-4 border-b">
          <h3 id="hs-scale-animation-modal-form-anak-label" class="font-bold text-gray-800">
            Tambah Anak
          </h3>
          <button type="button"
                  class="size-8 inline-flex justify-center items-center gap-x-2 rounded-full border border-transparent bg-gray-100 text-gray-800 hover:bg-gray-200 focus:outline-none focus:bg-gray-200 disabled:opacity-50 disabled:pointer-events-none"
                  aria-label="Close" data-hs-overlay="#hs-scale-animation-modal-form-anak">
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
          <form id="add-anak" @submit.prevent="handleAddAnak">
            <div class="max-w-sm">
              <label for="posyandu-id">Posyandu:</label>
              <select v-model="selectedPosyandu" id="posyandu-id"
                      class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                      required>
                <option v-for="posyandu in posyanduList" :key="posyandu.id" :value="posyandu.id">
                  {{ posyandu.name }}
                </option>
              </select>
            </div>
            <div class="max-w-sm mt-2">
              <label for="nama-anak">Nama Anak:</label>
              <input v-model="name" type="text" id="nama-anak"
                     class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                     placeholder="Nama Anak" required>
            </div>
            <div class="max-w-sm mt-2">
              <label for="age-anak">Usia:</label>
              <input v-model="age" type="number" id="age-anak"
                     class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                     placeholder="Usia Anak" required>
            </div>
            <div class="max-w-sm mt-2">
              <label for="gender-anak">Jenis Kelamin:</label>
              <select v-model="gender" id="gender-anak"
                      class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                      required>
                <option value="male">Laki-laki</option>
                <option value="female">Perempuan</option>
              </select>
            </div>
          </form>
        </div>
        <div class="flex justify-end items-center gap-x-2 py-3 px-4 border-t">
          <button type="button"
                  class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none"
                  data-hs-overlay="#hs-scale-animation-modal-form-anak">
            Close
          </button>
          <button type="submit"
                  form="add-anak"
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
import { sleep } from "@antfu/utils";

// Reactive references untuk mengikat data
const name = ref<string>("");
const age = ref<number | null>(null);
const gender = ref<string>("male");
const selectedPosyandu = ref<number | null>(null);
const isLoading = ref<boolean>(false);
const posyanduList = ref<Array<{ id: number, name: string }>>([]);

// Fungsi untuk mengambil daftar Posyandu
const getPosyanduList = async () => {
  try {
    isLoading.value = true;
    // Simulasi loading dengan sleep
    await sleep(2000);
    posyanduList.value = await useFetchApi('https://puso-be.vercel.app/auth/posyandu', {
      method: 'GET',
    });
  } catch (error) {
    // Menampilkan notifikasi error jika gagal memuat data
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Gagal memuat data Posyandu",
      showConfirmButton: false,
      timer: 1500,
      toast: true,
    });
  } finally {
    isLoading.value = false;
  }
};

// Menjalankan fungsi getPosyanduList saat komponen di-mount
onMounted(() => {
  getPosyanduList();
});

// Emit event ketika anak ditambahkan
const emit = defineEmits(['anakAdded']);

// Fungsi untuk membersihkan form setelah menambah anak
const clearFormAddAnak = () => {
  name.value = "";
  age.value = null;
  gender.value = "male";
  selectedPosyandu.value = null;
};

// Fungsi untuk menangani penambahan Anak
const handleAddAnak = async () => {
  // Validasi jika Posyandu belum dipilih
  if (!selectedPosyandu.value) {
    await Swal.fire({
      icon: 'warning',
      title: 'Pilih Posyandu terlebih dahulu!',
      showConfirmButton: true,
    });
    return;
  }

  // Validasi jika ada field yang kosong
  if (!name.value || !age.value || !gender.value) {
    await Swal.fire({
      position: "bottom-end",
      icon: "warning",
      title: "Harap isi semua field",
      showConfirmButton: false,
      timer: 1500,
      toast: true,
    });
    return;
  }

  try {
    isLoading.value = true;

    // Melakukan request untuk menambah data Anak
    const response = await useFetchApi('https://puso-be.vercel.app/auth/anak', {
      method: 'POST',
      body: {
        posyandu_id: selectedPosyandu.value,
        name: name.value,
        age: age.value,
        gender: gender.value,
      },
    });

    // Menampilkan notifikasi sukses
    await Swal.fire({
      position: "bottom-end",
      icon: "success",
      title: "Sukses menambah data Anak",
      showConfirmButton: false,
      timer: 1500,
      toast: true,
    });

    // Emit event bahwa anak telah ditambahkan
    emit('anakAdded', response);
    // Membersihkan form setelah data ditambahkan
    clearFormAddAnak();

    // Menutup modal jika ada
    const button = document.querySelector('[data-hs-overlay="#hs-scale-animation-modal-form-anak"]');
    if (button) {
      button.click();
    }
  } catch (e) {
    // Menampilkan notifikasi error jika gagal menambah data
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Gagal menambah data Anak",
      showConfirmButton: false,
      timer: 1500,
      toast: true,
    });
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* CSS styling if needed */
</style>
