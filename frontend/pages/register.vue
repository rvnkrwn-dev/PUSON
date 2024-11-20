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

  <div class="w-full h-full lg:ps-64">
    <div class="p-4 sm:p-6 space-y-4 sm:space-y-6">
      <div class="h-full w-full flex flex-col items-center justify-center">
        <div class="w-full max-w-md mx-auto p-6">
          <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
            <div class="p-4 sm:p-7">
              <div class="text-center">
                <h1 class="block text-2xl font-bold text-gray-800">Daftar</h1>
              </div>

              <div class="mt-8">
                <!-- Form -->
                <form @submit.prevent="handleRegister">
                  <div class="grid gap-y-4">

                    <!-- Full Name -->
                    <div>
                      <label for="name" class="block text-sm mb-2">Nama Lengkap</label>
                      <input
                          type="text"
                          id="name"
                          v-model="fullName"
                          class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500"
                          placeholder="Masukkan nama lengkap"
                          required
                      />
                    </div>

                    <!-- Email -->
                    <div>
                      <label for="email" class="block text-sm mb-2">Email</label>
                      <input
                          type="email"
                          id="email"
                          v-model="email"
                          class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500"
                          placeholder="Masukkan email"
                          required
                      />
                    </div>

                    <!-- Password -->
                    <div>
                      <label for="password" class="block text-sm mb-2">Kata Sandi</label>
                      <input
                          type="password"
                          id="password"
                          v-model="password"
                          class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500"
                          placeholder="Masukkan kata sandi"
                          required
                      />
                    </div>

                    <!-- Confirm Password -->
                    <div>
                      <label for="confirm_password" class="block text-sm mb-2">Konfirmasi Kata Sandi</label>
                      <input
                          type="password"
                          id="confirm_password"
                          v-model="confirmPassword"
                          class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500"
                          placeholder="Ulangi kata sandi"
                          required
                      />
                    </div>

                    <!-- Checkbox -->
                    <div class="flex items-center">
                      <input
                          id="terms"
                          type="checkbox"
                          v-model="termsAccepted"
                          class="shrink-0 mt-0.5 border-gray-200 rounded text-blue-600 focus:ring-blue-500"
                          required
                      />
                      <label for="terms" class="text-sm ms-3">
                        Saya menerima
                        <a href="#" class="text-blue-500 font-semibold">Syarat dan Ketentuan</a>
                      </label>
                    </div>

                    <!-- Submit Button -->
                    <button
                        type="submit"
                        :disabled="!termsAccepted || loading"
                        class="w-full py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
                    >
                      {{ loading ? 'Loading...' : 'Daftar' }}
                    </button>

                    <!-- Error Message -->
                    <p v-if="errorMessage" class="text-xs text-red-600 mt-2">{{ errorMessage }}</p>
                  </div>
                </form>
                <!-- End Form -->

                <p class="mt-2 text-sm text-gray-600 text-center">
                  Sudah punya akun?
                  <a href="/login"
                     class="text-blue-600 decoration-2 hover:underline focus:outline-none focus:underline font-medium">Masuk
                    disini</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const fullName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const termsAccepted = ref(false);
const loading = ref(false);
const errorMessage = ref("");

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Kata sandi tidak cocok.";
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  try {
    const response = await useFetchApi(
        "https://unhappy-lee-chi-abiyyu-f01e137b.koyeb.app/auth/register",
        {
          method: "POST",
          body: {
            full_name: fullName.value,
            email: email.value,
            password: password.value,
            role: "user",
          },
        }
    );

    console.log(response);

    alert("Pendaftaran berhasil!");
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Tambahkan styling custom di sini jika diperlukan */
</style>
