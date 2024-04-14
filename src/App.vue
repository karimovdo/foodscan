<template>
  <div class="flex flex-col min-h-screen">
    <div class="flex-1">
      <router-view />
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Footer from "./components/Footer.vue";
</script>
