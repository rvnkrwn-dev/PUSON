<template>
  <AppHeader/>
  <AppSidebar/>
  <div class="bg-gray-50 min-h-screen overflow-y-scroll overflow-x-hidden">
    <slot/>
  </div>
</template>

<script setup lang="ts">

import AppHeader from "~/components/AppHeader.vue";
import AppSidebar from "~/components/AppSidebar.vue";
</script>

<style scoped>

</style>