<template>
  <button
    @click="$emit('list', row)"
    class="px-3 py-1 text-xs font-medium dark:text-white border border-gray-700 bg-dark rounded-lg hover:bg-gray-700 transition"
  >
    lister
  </button>
</template>

<script setup lang="ts">
defineProps<{ row: Record<string, any> }>()
defineEmits(['list'])
</script>