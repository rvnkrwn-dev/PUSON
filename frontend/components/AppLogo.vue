<template>
  <NuxtLink to="/"
            aria-label="Puson">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="20 5 260 90" width="220" height="80">
      <!-- Background Circle for the Symbol -->
      <circle cx="50" cy="45" r="20" fill="#007BFF" stroke="white" stroke-width="4" />

      <!-- Symbol: Hands forming a Heart -->
      <path d="M40,40 Q50,30 60,40 Q70,50 50,70 Q30,50 40,40"
            fill="white" />

      <!-- Text: PUSON -->
      <text x="80" y="45" font-family="Arial, sans-serif" font-size="24" fill="#007BFF" font-weight="bold">
        PUSON
      </text>

      <!-- Tagline: Posyandu Untuk Stunting Online -->
      <text x="80" y="70" font-family="Arial, sans-serif" font-size="11" fill="#333" font-weight="normal">
        Posyandu Untuk Stunting Online
      </text>
    </svg>
  </NuxtLink>

</template>

<script setup lang="ts">

</script>

<style lang="css" scoped>
@import url('https://fonts.googleapis.com/css2?family=Gloria+Hallelujah&display=swap');

.gloria-hallelujah-regular {
  font-family: "Gloria Hallelujah", cursive;
  font-weight: 600;
  font-style: normal;
}
</style>