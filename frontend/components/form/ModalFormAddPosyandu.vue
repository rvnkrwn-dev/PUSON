<template>
  <button type="button"
          class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
          aria-haspopup="dialog" aria-expanded="false" aria-controls="hs-scale-animation-modal-form-posyandu"
          data-hs-overlay="#hs-scale-animation-modal-form-posyandu">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
      <path fill="currentColor"
            d="M12 4c4.411 0 8 3.589 8 8s-3.589 8-8 8s-8-3.589-8-8s3.589-8 8-8m0-2C6.477 2 2 6.477 2 12s4.477 10 10 10s10-4.477 10-10S17.523 2 12 2m5 9h-4V7h-2v4H7v2h4v4h2v-4h4z"/>
    </svg>
    Posyandu
  </button>

  <div id="hs-scale-animation-modal-form-posyandu"
       class="hs-overlay hidden size-full fixed top-0 start-0 z-[80] overflow-x-hidden overflow-y-auto pointer-events-none"
       role="dialog" tabindex="-1" aria-labelledby="hs-scale-animation-modal-form-posyandu-label">
    <div
        class="hs-overlay-animation-target hs-overlay-open:scale-100 hs-overlay-open:opacity-100 scale-95 opacity-0 ease-in-out transition-all duration-200 sm:max-w-lg sm:w-full m-3 sm:mx-auto min-h-[calc(100%-3.5rem)] flex items-center">
      <div
          class="w-full flex flex-col bg-white border shadow-sm rounded-xl pointer-events-auto dark:bg-neutral-800 dark:border-neutral-700 dark:shadow-neutral-700/70">
        <div class="flex justify-between items-center py-3 px-4 border-b dark:border-neutral-700">
          <h3 id="hs-scale-animation-modal-form-posyandu-label" class="font-bold text-gray-800 dark:text-white">
            Tambah Posyandu
          </h3>
          <button type="button"
                  class="size-8 inline-flex justify-center items-center gap-x-2 rounded-full border border-transparent bg-gray-100 text-gray-800 hover:bg-gray-200 focus:outline-none focus:bg-gray-200 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-700 dark:hover:bg-neutral-600 dark:text-neutral-400 dark:focus:bg-neutral-600"
                  aria-label="Close" data-hs-overlay="#hs-scale-animation-modal-form-posyandu">
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
          <form id="add-posyandu" @submit.prevent="handleAddPosyandu">
            <div class="max-w-sm">
              <label for="puskesmas-id">Puskesmas:</label>
              <select v-model="selectedPuskesmas" id="puskesmas-id"
                      class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                      required>
                <option v-for="puskesmas in puskesmasList" :key="puskesmas.id" :value="puskesmas.id">
                  {{ puskesmas.name }}
                </option>
              </select>
            </div>
            <div class="max-w-sm mt-2">
              <label for="nama-posyandu">Nama Posyandu:</label>
              <input v-model="name" type="text" id="nama-posyandu"
                     class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                     placeholder="Posyandu Sokaraja" required>
            </div>
            <div class="max-w-sm mt-2">
              <label for="phone-posyandu">Nomer HP:</label>
              <input v-model="phone" type="text" id="phone-posyandu"
                     class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                     placeholder="Posyandu Sokaraja" required>
            </div>
            <div class="max-w-sm mt-2">
              <label for="address-posyandu">Alamat:</label>
              <input v-model="address" type="text" id="address-posyandu"
                     class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                     placeholder="Alamat Posyandu" required>
            </div>
          </form>
        </div>
        <div class="flex justify-end items-center gap-x-2 py-3 px-4 border-t dark:border-neutral-700">
          <button type="button"
                  class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-700 dark:focus:bg-neutral-700"
                  data-hs-overlay="#hs-scale-animation-modal-form-posyandu">
            Close
          </button>
          <button type="submit"
                  form="add-posyandu"
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

// Reactive references
const name = ref<string>("");
const address = ref<string>("");
const phone = ref<string>("");
const selectedPuskesmas = ref<number | null>(null);
const isLoading = ref<boolean>(false);
const puskesmasList = ref<Array<{ id: number, name: string }>>([]);

// Fetch list of Puskesmas
const getPuskesmasList = async () => {
  try {
    isLoading.value = true;
    await sleep(2000);
    puskesmasList.value = await useFetchApi('https://puso-be.vercel.app/auth/puskesmas', {
      method: 'GET',
    });
  } catch (error) {
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Gagal memuat data Puskesmas",
      showConfirmButton: false,
      timer: 1500,
      toast: true,
    });
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  getPuskesmasList();
});

// Define emits
const emit = defineEmits(['posyanduAdded'])

// Clear form
const clearFormAddPosyandu = () => {
  name.value = "";
  address.value = "";
  phone.value = "";
  selectedPuskesmas.value = null;
};

// Add Posyandu
const handleAddPosyandu = async () => {
  if (!selectedPuskesmas.value) {
    await Swal.fire({
      icon: 'warning',
      title: 'Pilih Puskesmas terlebih dahulu!',
      showConfirmButton: true,
    });
    return;
  }

  try {
    isLoading.value = true;

    const response = await useFetchApi('https://puso-be.vercel.app/auth/posyandu', {
      method: 'POST',
      body: {
        puskesmas_id: selectedPuskesmas.value,
        name: name.value,
        address: address.value,
        phone: phone.value,
      },
    });

    await Swal.fire({
      position: "bottom-end",
      icon: "success",
      title: "Sukses menambah data Posyandu",
      showConfirmButton: false,
      timer: 1500,
      toast: true,
    });

    emit('posyanduAdded', response);
    clearFormAddPosyandu();

    // Trigger modal close
    const button = document.querySelector('[data-hs-overlay="#hs-scale-animation-modal-form-posyandu"]');
    if (button) {
      button.click();
    }
  } catch (e) {
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Gagal menambah data Posyandu",
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
