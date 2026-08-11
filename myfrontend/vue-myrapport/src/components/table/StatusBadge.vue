<template>
  <span
    :class="[
      'rounded-full px-2 py-0.5 text-xs font-medium',
      isActive
        ? 'bg-success-50 text-success-600 dark:bg-success-500/15 dark:text-success-500'
        : 'bg-error-50 text-error-600 dark:bg-error-500/15 dark:text-error-500'
    ]"
  >
    {{ isActive  ? 'Activé' : 'Désactivé' }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{ row: any }>()

const isActive = props.row.statut === true || props.row.statut === 'Activé'
</script>