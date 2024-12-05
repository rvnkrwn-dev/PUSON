<template>
  <div>
    <NuxtLayout>
      <NuxtLoadingIndicator color="blue"/>
      <div class="mt-2 fixed top-6 right-4 z-50 bg-yellow-100 border border-yellow-200 text-sm text-yellow-800 rounded-lg p-4 dark:bg-yellow-800/10 dark:border-yellow-900 dark:text-yellow-500" role="alert" tabindex="-1" aria-labelledby="hs-soft-color-warning-label">
        <span id="hs-soft-color-warning-label" class="font-bold">Warning</span> website under maintenance
      </div>
      <NuxtPage/>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
const {initAuth} = useAuth()

onBeforeMount(async () => {
  await initAuth()
})
</script>