<template>
  <div class="flex gap-2">
    <!-- Bouton Activer/Désactiver -->
    <button
      @click="$emit('access', row)"
      :class="row.access_group
        ? 'bg-red-500 hover:bg-red-600'
        : 'bg-green-500 hover:bg-green-600'"
      class="px-3 py-1 text-xs font-medium text-white rounded-lg transition"
    >
      {{ row.access_group ? 'Déverouiller' : 'Verouiller' }}
    </button>

  </div>
</template>

<script setup lang="ts">
defineProps<{ row: Record<string, any> }>()
defineEmits(['access'])
</script>