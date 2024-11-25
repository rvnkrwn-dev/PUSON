<template>
  <div>
    <NuxtLoadingIndicator/>
    <NuxtLayout>
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