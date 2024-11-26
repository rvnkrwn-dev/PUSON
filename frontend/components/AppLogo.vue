<template>
  <NuxtLink to="/"
            aria-label="Puson">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="10 10 300 80" width="180" height="60">
      <!-- Background Circle for the Symbol -->
      <circle cx="50" cy="50" r="35" fill="#007BFF" stroke="white" stroke-width="2" />

      <!-- Symbol: Hands forming a Heart -->
      <path d="M40,45 Q50,35 60,45 Q70,55 50,75 Q30,55 46,44"
            fill="white" />

      <!-- Text: PUSON -->
      <text x="100" y="52" font-family="'Gloria Hallelujah', cursive" font-size="30" fill="#007BFF" font-weight="bold">
        PUSON
      </text>

      <!-- Tagline: Posyandu Untuk Stunting Online -->
      <text x="100" y="72" font-family="Arial, sans-serif" font-size="14" fill="#333" font-weight="normal">
        Posyandu Untuk Stunting Online
      </text>
    </svg>
  </NuxtLink>

</template>

<script setup lang="ts">

</script>

<style lang="css" scoped>
@import url('https://fonts.googleapis.com/css2?family=Gloria+Hallelujah&display=swap');
</style>