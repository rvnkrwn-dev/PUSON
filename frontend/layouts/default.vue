<template>
  <AppHeader/>
  <AppSidebar/>
  <slot />
</template>

<script setup lang="ts">

import AppHeader from "~/components/AppHeader.vue";
import AppSidebar from "~/components/AppSidebar.vue";
</script>

<style scoped>

</style>