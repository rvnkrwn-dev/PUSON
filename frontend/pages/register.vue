<template>
  <div class="h-[100dvh] w-[100dvw] flex flex-col items-center justify-center overflow-hidden">
    <div class="w-full max-w-md mx-auto p-6">
      <div class="bg-white sm:border border-gray-200 rounded-xl sm:shadow-sm">
        <div class="p-4 sm:p-7">
          <div class="text-center flex gap-2 items-center justify-around">
            <AppLogo/>
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
                      :class="!passwordIsSame ? 'border-red-500' : ''"
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
                      :class="!passwordIsSame ? 'border-red-500' : ''"
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
                    :disabled="!termsAccepted || loading || !passwordIsSame"
                    class="w-full py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
                >
                  {{ loading ? 'Loading...' : 'Daftar' }}
                </button>
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
</template>

<script setup lang="ts">
import Swal from 'sweetalert2'

definePageMeta({
  layout: false
})
const fullName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const termsAccepted = ref(false);
const loading = ref(false);
const passwordIsSame = ref(true)

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    passwordIsSame.value = false
    return;
  } else {
    passwordIsSame.value = true
  }

  loading.value = true;

  try {
    const response = await useFetchApi(
        "https://puso-be.vercel.app/auth/register",
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


    await Swal.fire({
      position: "top-end",
      icon: "success",
      title: "Berhasil mendaftar!",
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });

    return navigateTo('/')
  } catch (error) {
    await Swal.fire({
      position: "top-end",
      icon: "error",
      title: "Gagal untuk mendaftar!",
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  } finally {
    loading.value = false;
  }
};
</script>