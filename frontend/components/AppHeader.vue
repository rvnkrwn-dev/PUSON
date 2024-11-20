<template>
  <header
      class="sticky top-0 inset-x-0 flex flex-wrap md:justify-start md:flex-nowrap z-[48] w-full bg-white border-b text-sm py-2.5 lg:ps-[260px]">
    <nav class="px-4 sm:px-6 flex basis-full items-center w-full mx-auto">
      <div class="me-5 lg:me-0 lg:hidden">
        <!-- Logo -->
        <NuxtLink to="/" class="flex-none rounded-xl text-xl inline-block font-bold text-blue-600 focus:outline-none focus:opacity-80" href="#"
                  aria-label="Puson">
          PUSON
        </NuxtLink>
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
            <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
              <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
            </svg>
            <span class="sr-only">Notifications</span>
          </button>

          <button type="button"
                  class="size-[38px] relative inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none">
            <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>
            <span class="sr-only">Activity</span>
          </button>

          <!-- Dropdown -->
          <div class="hs-dropdown [--placement:bottom-right] relative inline-flex">
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
                <p class="text-sm text-gray-500">Signed in as</p>
                <p class="text-sm font-medium text-gray-800">{{ user?.email }}</p>
              </div>
              <div class="p-1.5 space-y-0.5">
                <NuxtLink class="cursor-pointer flex items-center gap-x-3.5 py-2 px-3 rounded-lg text-sm text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100"
                   @click="handleLogout">
                  <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M4 12a1 1 0 0 0 1 1h7.59l-2.3 2.29a1 1 0 0 0 0 1.42a1 1 0 0 0 1.42 0l4-4a1 1 0 0 0 .21-.33a1 1 0 0 0 0-.76a1 1 0 0 0-.21-.33l-4-4a1 1 0 1 0-1.42 1.42l2.3 2.29H5a1 1 0 0 0-1 1M17 2H7a3 3 0 0 0-3 3v3a1 1 0 0 0 2 0V5a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-3a1 1 0 0 0-2 0v3a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3"/></svg>
                  Sign Out
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
const {useAuthUser, logout} = useAuth()

const user = computed(() => useAuthUser().value)

onMounted(() => {
  console.log(user.value)
})

const handleLogout = async () => {
  const confirmLogout = confirm("Apakah Anda yakin ingin logout?");
  if (!confirmLogout) return; // Jika pengguna membatalkan, keluar dari fungsi

  try {
    // Memanggil fungsi logout dari useAuth
    await logout();

    // Redirect atau tindakan lain setelah logout berhasil
    alert('Anda telah berhasil logout.');
    window.location.href = '/login'; // Redirect ke halaman login atau halaman lain
  } catch (error) {
    console.error('Gagal logout:', error);
    alert('Terjadi kesalahan saat logout.');
  }
};
</script>

<style scoped>

</style>