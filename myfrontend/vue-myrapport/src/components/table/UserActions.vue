<template>
  <div class="flex gap-2">

    <!-- Bouton Modifier -->
    <button
      @click="$emit('edit', row)"
      class="px-3 py-1 text-xs font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition"
    >
      Modifier
    </button>

    <!-- Bouton Activer/Désactiver -->
    <button
      @click="$emit('toggle', row)"
      :class="row.statut
        ? 'bg-red-500 hover:bg-red-600'
        : 'bg-green-500 hover:bg-green-600'"
      class="px-3 py-1 text-xs font-medium text-white rounded-lg transition"
    >
      {{ row.statut ? 'Désactiver' : 'Activer' }}
    </button>

  </div>
</template>

<script setup lang="ts">
defineProps<{ row: Record<string, any> }>()
defineEmits(['edit', 'toggle'])
</script>