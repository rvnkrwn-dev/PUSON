<template>
  <div id="hs-application-sidebar" class="hs-overlay  [--auto-close:lg]
    hs-overlay-open:translate-x-0
    -translate-x-full transition-all duration-300 transform
    w-[260px] h-[100dvh]
    hidden
    fixed inset-y-0 start-0 z-[60]
    bg-white border-e border-gray-200
    lg:block lg:translate-x-0 lg:end-auto lg:bottom-0" role="dialog" tabindex="-1" aria-label="Sidebar">
    <div class="relative flex flex-col h-full max-h-full">
      <div class="px-4 pt-4">
        <!-- Logo -->
        <AppLogo />
        <!-- End Logo -->
      </div>

      <!-- Content -->
      <div
          class="h-full overflow-y-auto [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-track]:bg-gray-100 [&::-webkit-scrollbar-thumb]:bg-gray-300">
        <nav class="hs-accordion-group p-3 w-full flex flex-col flex-wrap" data-hs-accordion-always-open>
          <ul class="flex flex-col space-y-1">
            <li>
              <NuxtLink active-class="bg-gray-100" class="flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100 focus:outline-none focus:bg-gray-100"
                 to="/">
                <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="m12 5.69l5 4.5V18h-2v-6H9v6H7v-7.81zM12 3L2 12h3v8h6v-6h2v6h6v-8h3"/></svg>
                Dashboard
              </NuxtLink>
            </li>

            <li><NuxtLink
                active-class="bg-gray-100"
                class="w-full flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100"
                to="/puskesmas">
              <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M2 22V7a1 1 0 0 1 1-1h4V2h10v4h4a1 1 0 0 1 1 1v15h-8v-5h-4v5zM9 4v6h2V8h2v2h2V4h-2v2h-2V4zM4 20h4v-3H4zm0-5h4v-3H4zm12 5h4v-3h-4zm0-5h4v-3h-4zm-6 0h4v-3h-4z"/></svg>
              Puskesmas
            </NuxtLink></li>
            <li><NuxtLink
                active-class="bg-gray-100"
                class="w-full flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100"
                to="/posyandu">
              <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M19 5v14H5V5zm2-2H3v18h18zm-4 14H7v-1h10zm0-2H7v-1h10zm0-3H7V7h10z"/></svg>
              Posyandu
            </NuxtLink></li>
            <li><NuxtLink
                active-class="bg-gray-100"
                class="w-full flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100"
                to="/anak">
              <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M13 2v8h8a8 8 0 0 0-8-8m6.32 13.89A7.95 7.95 0 0 0 21 11H6.44L5.5 9H2v2h2.22s1.89 4.07 2.12 4.42C5.24 16 4.5 17.17 4.5 18.5A3.5 3.5 0 0 0 8 22c1.76 0 3.22-1.3 3.46-3h2.08c.24 1.7 1.7 3 3.46 3a3.5 3.5 0 0 0 3.5-3.5c0-1.04-.46-1.97-1.18-2.61M8 20a1.5 1.5 0 0 1-1.5-1.5A1.5 1.5 0 0 1 8 17a1.5 1.5 0 0 1 1.5 1.5A1.5 1.5 0 0 1 8 20m9 0a1.5 1.5 0 0 1-1.5-1.5A1.5 1.5 0 0 1 17 17a1.5 1.5 0 0 1 1.5 1.5A1.5 1.5 0 0 1 17 20"/></svg>
              Anak
            </NuxtLink></li>
            <li><NuxtLink
                active-class="bg-gray-100"
                class="w-full flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100"
                to="/pemeriksaan">
              <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M19 7h-2.81c-.45-.8-1.07-1.5-1.82-2L16 3.41L14.59 2l-2.17 2.17a6 6 0 0 0-2.83 0L7.41 2L6 3.41L7.62 5c-.75.5-1.36 1.21-1.81 2H3v2h2.09c-.06.33-.09.66-.09 1v1H3v2h2v1c0 .34.03.67.09 1H3v2h2.81A6 6 0 0 0 13 19.65V19c0-.57.09-1.14.25-1.69c-.66.45-1.45.69-2.25.69c-2.21 0-4-1.79-4-4v-4c0-2.21 1.79-4 4-4s4 1.79 4 4v4c0 .19 0 .39-.05.58c.59-.54 1.29-.96 2.05-1.23V13h2v-2h-2v-1c0-.34-.03-.67-.09-1H19zm2.34 9l-3.59 3.59L16.16 18L15 19.16l2.75 3l4.75-4.75zM13 9v2H9V9zm0 4v2H9v-2z"/></svg>
              Pemeriksaan
            </NuxtLink></li>
            <li><NuxtLink
                active-class="bg-gray-100"
                class="w-full flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100"
                to="/stunting">
              <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M12 .5a1.746 1.746 0 0 0-1 3.18v1.4c-.9.13-1.74.42-2.5.86L7.39 4.35c.19-.52.14-1.12-.2-1.6C6.84 2.26 6.3 2 5.75 2c-.35 0-.7.1-1 .32c-.79.55-.99 1.64-.43 2.43c.34.49.88.75 1.43.75l1.18 1.68c-.43.43-.77.91-1.06 1.44c-.2-.08-.41-.12-.62-.12c-.45 0-.9.17-1.25.5c-.67.7-.67 1.8 0 2.5c.29.27.64.42 1 .5c0 .54.07 1.06.18 1.56l-1.31.35c-.31-.26-.71-.41-1.12-.41c-.15 0-.31 0-.46.06a1.75 1.75 0 0 0-1.23 2.15C1.27 16.5 2 17 2.75 17c.15 0 .3 0 .46-.06c.57-.16 1-.58 1.18-1.1l1.51-.41c.45.79 1.05 1.49 1.75 2.07l-1.1 2c-.55.08-1.05.39-1.34.92a1.749 1.749 0 1 0 3.08 1.66c.28-.52.27-1.12.02-1.61l1.07-1.97c.81.32 1.69.5 2.62.5h.18c-.13.26-.18.56-.18.88c.08.92.84 1.62 1.75 1.62h.13c.97-.08 1.69-.92 1.62-1.88c-.04-.5-.29-.94-.65-1.23c.47-.21.92-.48 1.34-.79l2.34 2.34c-.1.56.06 1.13.47 1.56c.35.33.8.5 1.25.5s.9-.17 1.25-.5c.67-.7.67-1.8 0-2.5c-.35-.33-.8-.5-1.25-.5c-.1 0-.2 0-.31.03l-2.34-2.34c.49-.65.87-1.39 1.11-2.19h1.11A1.746 1.746 0 0 0 23 13a1.746 1.746 0 0 0-3.18-1H19c0-1.57-.5-3-1.4-4.19l1.34-1.34c.11.03.21.03.31.03c.45 0 .9-.17 1.25-.5c.67-.69.67-1.8 0-2.5c-.35-.33-.8-.5-1.25-.5s-.9.17-1.25.5c-.41.43-.57 1-.47 1.56L16.19 6.4c-.92-.69-2-1.15-3.19-1.32v-1.4A1.746 1.746 0 0 0 12 .5M12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5s5 2.24 5 5s-2.24 5-5 5m-1.5-8C9.67 9 9 9.67 9 10.5s.67 1.5 1.5 1.5s1.5-.67 1.5-1.5S11.33 9 10.5 9m3.5 4c-.55 0-1 .45-1 1s.45 1 1 1s1-.45 1-1s-.45-1-1-1"/></svg>
              Stunting
            </NuxtLink></li>
            <li><NuxtLink
                active-class="bg-gray-100"
                class="cursor-pointer w-full flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100 hidden"
                @click="handleLogout">
              <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M4 12a1 1 0 0 0 1 1h7.59l-2.3 2.29a1 1 0 0 0 0 1.42a1 1 0 0 0 1.42 0l4-4a1 1 0 0 0 .21-.33a1 1 0 0 0 0-.76a1 1 0 0 0-.21-.33l-4-4a1 1 0 1 0-1.42 1.42l2.3 2.29H5a1 1 0 0 0-1 1M17 2H7a3 3 0 0 0-3 3v3a1 1 0 0 0 2 0V5a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-3a1 1 0 0 0-2 0v3a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3"/></svg>
              Sign Out
            </NuxtLink></li>
          </ul>
        </nav>
      </div>
      <!-- End Content -->
    </div>
  </div>
</template>

<script setup lang="ts">
const {logout} = useAuth()

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