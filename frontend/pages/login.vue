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

  <!-- Login Form -->
  <div class="w-full h-full lg:ps-64">
    <div class="p-4 sm:p-6 space-y-4 sm:space-y-6">
      <div class="flex flex-col items-center justify-center">
        <div class="w-full max-w-md mx-auto p-6">
          <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
            <div class="p-4 sm:p-7">
              <div class="text-center">
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
                        <p v-if="emailError" class="text-xs text-red-600 mt-2" id="email-error">{{ emailError }}</p>
                      </div>
                    </div>

                    <!-- Password Input -->
                    <div>
                      <div class="flex justify-between items-center">
                        <label for="password" class="block text-sm mb-2">Kata sandi</label>
                        <a class="inline-flex items-center gap-x-1 text-sm text-blue-600 decoration-2 hover:underline focus:outline-none focus:underline font-medium"
                           href="/forget-password">Lupa kata sandi?</a>
                      </div>
                      <div class="relative">
                        <input v-model="password" type="password" id="password" name="password"
                               class="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                               required aria-describedby="password-error" :class="{'border-red-500': passwordError}">
                        <p v-if="passwordError" class="text-xs text-red-600 mt-2" id="password-error">{{ passwordError }}</p>
                      </div>
                    </div>

                    <!-- Remember Me Checkbox -->
                    <div class="flex items-center">
                      <input id="remember-me" name="remember-me" type="checkbox"
                             class="shrink-0 mt-0.5 border-gray-200 rounded text-blue-600 focus:ring-blue-500" v-model="rememberMe">
                      <label for="remember-me" class="text-sm ms-3">Ingat saya</label>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit"
                            class="w-full py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
                            :disabled="isSubmitting">
                      Masuk
                    </button>
                  </div>
                </form>

                <!-- Sign Up Link -->
                <p class="mt-2 text-sm text-gray-600 text-center">
                  Belum punya akun?
                  <NuxtLink
                      class="text-blue-600 decoration-2 hover:underline focus:outline-none focus:underline font-medium"
                      href="/register">
                    Daftar disini
                  </NuxtLink>
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

const email = ref<string | null>(null)
const password = ref<string | null>(null)
const rememberMe = ref<boolean>(false)
const emailError = ref<string | null>(null)
const passwordError = ref<string | null>(null)
const isSubmitting = ref<boolean>(false)

const { login } = useAuth()

const handleSubmit = async () => {
  // Reset errors
  emailError.value = null
  passwordError.value = null

  // Validate fields
  if (!email.value || !/\S+@\S+\.\S+/.test(email.value)) {
    emailError.value = "Please enter a valid email address."
    return
  }

  if (!password.value || password.value.length < 8) {
    passwordError.value = "Password must be at least 8 characters."
    return
  }

  isSubmitting.value = true

  try {
    await login({ email: email.value, password: password.value })
    return navigateTo('/')
  } catch (error) {
    console.log(error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
/* You can add additional styling here if necessary */
</style>
