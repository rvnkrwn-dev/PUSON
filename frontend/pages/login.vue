<template>
  <div class="h-[100dvh] w-[100dvw] flex flex-col items-center justify-center overflow-hidden">
    <div class="w-full max-w-md mx-auto p-6">
      <div class="bg-white sm:border border-gray-200 rounded-xl sm:shadow-sm">
        <div class="p-4 sm:p-7">
          <div class="text-center flex gap-2 items-center justify-around">
            <AppLogo/>
            <h1 class="block text-2xl font-bold text-gray-800">Masuk</h1>
          </div>
          <div class="mt-8">
            <!-- Form -->
            <form @submit.prevent="handleSubmit">
              <div class="grid gap-y-4">
                <!-- Email Input -->
                <div>
                  <label for="email" class="block text-sm mb-2">Email</label>
                  <div class="relative">
                    <input v-model="email" type="email" id="email" name="email"
                           class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                           required aria-describedby="email-error" :class="{'border-red-500': emailError}">
                  </div>
                </div>

                <!-- Password Input -->
                <div>
                  <div class="flex justify-between items-center">
                    <label for="password" class="block text-sm mb-2">Kata sandi</label>
                    <NuxtLink
                        class="inline-flex items-center gap-x-1 text-sm text-blue-600 decoration-2 hover:underline focus:outline-none focus:underline font-medium"
                        to="/forget-password">Lupa kata sandi?
                    </NuxtLink>
                  </div>
                  <div class="relative">
                    <input v-model="password" type="password" id="password" name="password"
                           class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                           required aria-describedby="password-error" :class="{'border-red-500': passwordError}">
                  </div>
                </div>

                <!-- Remember Me Checkbox -->
                <div class="flex items-center">
                  <input id="remember-me" name="remember-me" type="checkbox"
                         class="shrink-0 mt-0.5 border-gray-200 rounded text-blue-600 focus:ring-blue-500"
                         v-model="rememberMe">
                  <label for="remember-me" class="text-sm ms-3">Ingat saya</label>
                </div>

                <!-- Submit Button -->
                <button type="submit"
                        class="w-full py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
                        :disabled="isSubmitting">
                  {{ isLoading ? 'Tunggu...' : 'Masuk' }}
                </button>
              </div>
            </form>

            <!-- Sign Up Link -->
            <p class="mt-2 text-sm text-gray-600 text-center">
              Belum punya akun?
              <NuxtLink
                  class="text-blue-600 decoration-2 hover:underline focus:outline-none focus:underline font-medium"
                  to="/register">
                Daftar disini
              </NuxtLink>
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
const email = ref<string | null>(null)
const password = ref<string | null>(null)
const rememberMe = ref<boolean>(false)
const emailError = ref<string | null>(null)
const passwordError = ref<string | null>(null)
const isSubmitting = ref<boolean>(false)
const isLoading = ref<boolean>(false)

const {login} = useAuth()

const handleSubmit = async () => {
  // Reset errors
  emailError.value = null
  passwordError.value = null
  isLoading.value = true

  // Validate fields
  if (!email.value || !/\S+@\S+\.\S+/.test(email.value)) {
    emailError.value = "Please enter a valid email address."
    return await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: emailError.value,
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  }

  if (!password.value || password.value.length < 8) {
    passwordError.value = "Password must be at least 8 characters."
    return await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: passwordError.value,
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  }

  isSubmitting.value = true

  try {
    await login({email: email.value, password: password.value})
    if (rememberMe.value) {
      localStorage.setItem('rememberMe', JSON.stringify({
        user: email.value,
      }))
    } else {
      localStorage.setItem('rememberMe', null)
    }
    return navigateTo('/')
  } catch (error) {
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Failed to login",
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  } finally {
    isSubmitting.value = false
    isLoading.value = false
  }
}


const getUserRememberMe = () => {
  const data = JSON.parse(localStorage.getItem('rememberMe'));
  if (data !== null) {
    email.value = data?.user
    rememberMe.value = !!data?.user
  }
}

onMounted(() => {
  getUserRememberMe()
})
</script>

<style scoped>

</style>