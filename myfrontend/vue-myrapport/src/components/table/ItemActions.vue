<template>
  <div class="flex gap-2">

    <button
      @click="$emit('edit', row)"
      class="px-3 py-1 text-xs font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition"
    >
      Modifier
    </button>

    <button
      @click="$emit('delete', row)"
      class="px-3 py-1 text-xs font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition"
    >
      Supprimer
    </button>

  </div>
</template>

<script setup lang="ts">
defineProps<{ row: Record<string, any> }>()
defineEmits(['edit', 'delete'])
</script>