<template>
  <button
    @click="$emit('solution', row)"
    class="px-3 py-1 text-xs font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600 transition"
  >
    Solution
  </button>
</template>

<script setup lang="ts">
defineProps<{ row: Record<string, any> }>()
defineEmits(['solution'])
</script>