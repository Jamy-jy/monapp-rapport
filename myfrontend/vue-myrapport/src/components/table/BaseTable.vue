<template>
  <div class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
    <div class="max-w-full overflow-x-auto custom-scrollbar">
      <table class="min-w-full">
        <!-- En-tête dynamique -->
        <thead>
          <tr class="border-b border-gray-200 dark:border-gray-700">
            <th
              v-for="(col, index) in columns"
              :key="index"
              class="px-5 py-3 text-left w-3/11 sm:px-6"
              :style="{ width: col.width || 'auto' }"
            >
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">
                {{ col.label }}
              </p>
            </th>
          </tr>
        </thead>

        <!-- Corps dynamique -->
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr 
            v-for="(row, rowIndex) in rows" 
            :key="rowIndex" 
            class="border-t border-gray-100 dark:border-gray-800">
            <td 
                v-for="(col, colIndex) in columns" 
                :key="colIndex" 
                class="px-5 py-4 sm:px-6">
              <!-- Si la colonne a un slot personnalisé, utiliser la fonction -->
              <template v-if="col.render">
                <component 
                  :is="col.render" 
                  :row="row"
                  @edit="$emit('edit', $event)"
                  @toggle="$emit('toggle', $event)"
                  @delete="$emit('delete', $event)"
                  @solution="$emit('solution', $event)" 
                  @dd="$emit('add', $event)"
                  @access="$emit('access', $event)"
                  @list="$emit('list', $event)"
                />
              </template>

              <template v-else-if="col.renderFn">
                <component :is="() => col.renderFn!(row)" />
              </template>
              
              <!-- Sinon afficher la valeur de la propriété -->
              <template v-else>
                <p class="text-gray-500 text-theme-sm dark:text-gray-400">
                  {{ col.field ? row[col.field] : '' }}
                </p>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { VNode } from 'vue'

interface Column {
  label: string           // Nom affiché dans l'en-tête
  field?: string          // Clé correspondante dans les données
  width?: string          // Largeur optionnelle
  render?: any            // Optionnel : composant ou fonction de rendu pour cell
  renderFn?: (row: Record<string, any>) => VNode // fonction custom avec h()
}

interface Props {
  columns: Column[]
  rows: Record<string, any>[]
}

defineProps<Props>()

defineEmits(['edit', 'toggle', 'delete', 'solution', 'add', 'access', 'list'])
</script>