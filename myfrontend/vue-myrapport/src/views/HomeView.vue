<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
</script>
  async mounted() {
    const res = await fetch("http://127.0.0.1:8000/hello/");
    const data = await res.json();
    console.log(data)
  }
<template>
  <main>
    <TheWelcome />
  </main>
</template>
