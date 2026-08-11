<template>
  <button
    @click="$emit('add', row)"
    class="px-3 py-1 text-xs font-medium text-white bg-brand-900 rounded-lg hover:bg-brand-800 transition"
  >
    Ajouter item
  </button>
</template>

<script setup lang="ts">
defineProps<{ row: Record<string, any> }>()
defineEmits(['add'])
</script>