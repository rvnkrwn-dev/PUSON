<template>
  <header
      class="sticky top-0 inset-x-0 flex flex-wrap md:justify-start md:flex-nowrap z-[48] w-full bg-white border-b text-sm py-2.5 lg:ps-[260px]">
    <nav class="px-4 sm:px-6 flex basis-full items-center w-full mx-auto">
      <div class="me-5 lg:me-0 lg:hidden">
        <!-- Logo -->
        <AppLogo />
        <!-- End Logo -->
      </div>

      <div class="w-full flex items-center justify-end ms-auto md:justify-between gap-x-1 md:gap-x-3">

        <div class="hidden md:block">
          <!-- Search Input -->
          <!-- End Search Input -->
        </div>

        <div class="flex flex-row items-center justify-end gap-1">
          <button type="button"
                  class="md:hidden size-[38px] relative inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none">
            <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.3-4.3"/>
            </svg>
            <span class="sr-only">Search</span>
          </button>

          <button type="button"
                  class="size-[38px] relative inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="M11.962 17.986h6.81a1.555 1.555 0 0 0 1.512-2.175c-.36-1.088-1.795-2.393-1.795-3.677c0-2.85 0-3.6-1.404-5.276a5 5 0 0 0-1.653-1.283l-.783-.38a1.1 1.1 0 0 1-.511-.73a2.023 2.023 0 0 0-2.176-1.707a2.023 2.023 0 0 0-2.12 1.707a1.09 1.09 0 0 1-.567.73l-.783.38A5 5 0 0 0 6.84 6.858c-1.403 1.676-1.403 2.426-1.403 5.276c0 1.284-1.37 2.458-1.73 3.611c-.217.697-.337 2.241 1.48 2.241z"/><path d="M15.225 17.986a3.2 3.2 0 0 1-3.263 3.263A3.195 3.195 0 0 1 8.7 17.986"/></g></svg>
            <span class="sr-only">Notifications</span>
          </button>

          <button type="button"
                  class="size-[38px] relative inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14.706 4.313H9.294a4.98 4.98 0 0 0-4.982 4.981v5.412a4.98 4.98 0 0 0 4.982 4.982h5.412a4.98 4.98 0 0 0 4.982-4.982V9.294a4.98 4.98 0 0 0-4.982-4.982Z"/><path d="M19.606 15.588h1.619a1.025 1.025 0 0 0 1.025-1.025V9.438a1.025 1.025 0 0 0-1.025-1.025h-1.62m-15.21 7.175h-1.62a1.025 1.025 0 0 1-1.025-1.025V9.438a1.025 1.025 0 0 1 1.025-1.025h1.62"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.765 8.413v-4.1m18.46 4.1l-.01-4.1m-7.185 6.662h2.049M8.925 9.796v2.05m1.025 3.229a2.91 2.91 0 0 0 4.1 0"/></g></svg>
            <span class="sr-only">Chat AI</span>
          </button>

          <!-- Dropdown -->
          <div class="hs-dropdown [--placement:bottom-right] relative inline-flex ml-2">
            <button id="hs-dropdown-account" type="button"
                    class="size-[38px] inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent text-gray-800 focus:outline-none disabled:opacity-50 disabled:pointer-events-none"
                    aria-haspopup="menu" aria-expanded="false" aria-label="Dropdown">
              <img class="shrink-0 size-[38px] rounded-full"
                   src="https://images.unsplash.com/photo-1568602471122-7832951cc4c5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=facearea&facepad=2&w=320&h=320&q=80"
                   alt="Avatar">
            </button>

            <div
                class="hs-dropdown-menu transition-[opacity,margin] duration hs-dropdown-open:opacity-100 opacity-0 hidden min-w-60 bg-white shadow-md rounded-lg mt-2 after:h-4 after:absolute after:-bottom-4 after:start-0 after:w-full before:h-4 before:absolute before:-top-4 before:start-0 before:w-full"
                role="menu" aria-orientation="vertical" aria-labelledby="hs-dropdown-account">
              <div class="py-3 px-5 bg-gray-100 rounded-t-lg">
                <p class="text-sm text-gray-500">Masuk sebagai</p>
                <p class="text-sm font-medium text-gray-800">{{ user?.full_name }}</p>
              </div>
              <div class="p-1.5 space-y-0.5">
                <NuxtLink class="cursor-pointer flex items-center gap-x-3.5 py-2 px-3 rounded-lg text-sm text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100"
                   @click="handleLogout">
                  <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M4 12a1 1 0 0 0 1 1h7.59l-2.3 2.29a1 1 0 0 0 0 1.42a1 1 0 0 0 1.42 0l4-4a1 1 0 0 0 .21-.33a1 1 0 0 0 0-.76a1 1 0 0 0-.21-.33l-4-4a1 1 0 1 0-1.42 1.42l2.3 2.29H5a1 1 0 0 0-1 1M17 2H7a3 3 0 0 0-3 3v3a1 1 0 0 0 2 0V5a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-3a1 1 0 0 0-2 0v3a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3"/></svg>
                  Keluar
                </NuxtLink>
              </div>
            </div>
          </div>
          <!-- End Dropdown -->
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import Swal from 'sweetalert2'
import AppLogo from "~/components/AppLogo.vue";
const {useAuthUser, logout} = useAuth()

const user = computed(() => useAuthUser().value)

const handleLogout = async () => {
  Swal.fire({
    title: "Anda yakin?",
    text: "Anda ingin keluar dari sini!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    cancelButtonText: "Batal",
    confirmButtonText: "Ya, Keluar!"
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        // Memanggil fungsi logout dari useAuth
        await logout();

        // Redirect atau tindakan lain setelah logout berhasil
        return await navigateTo('/login')
      } catch (error) {
        await Swal.fire({
          position: "bottom-end",
          icon: "error",
          title: "Terjadi kesalahan saat logout.",
          showConfirmButton: false,
          timer: 1500,
          toast: true
        });
      } finally {

      }
    }
  });
};
</script>

<style lang="css" scoped>

</style>