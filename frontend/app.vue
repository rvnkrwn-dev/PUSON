<template>
  <div>
    <NuxtLayout>
      <NuxtLoadingIndicator color="blue"/>
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