<template>
    <!-- <div class="mb-2 flex justify-end" v-if="!props.readonly">
      <button
        class=" h-11 flex items-center gap-2 justify-center bg-brand-100 text-brand-600 rounded-lg mx-2 px-4 py-2.5 text-sm font-medium hover:bg-brand-200 focus:outline-none focus:ring-2 focus:ring-brand-900 focus:ring-offset-1 dark:focus:ring-offset-dark-900 dark:bg-brand-950 dark:text-brand-400 dark:hover:bg-brand-999"
        @click="showTable"
      >
       <AperçuIcon/>
       Aperçu
      </button>
      <button
        class=" h-11 flex items-center gap-2 justify-center rounded-lg bg-brand-100 text-brand-600 px-4 py-2.5 text-sm font-medium hover:bg-brand-200 focus:outline-none focus:ring-2 focus:ring-brand-900 focus:ring-offset-1 dark:focus:ring-offset-dark-900 dark:bg-brand-950 dark:text-brand-400 dark:hover:bg-brand-999"
        @click="addRow"
      >
       <AddIcon/>
       Ajouter ligne
      </button>
    </div> -->
    <div class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
        
        <div class="max-w-full overflow-x-auto custom-scrollbar">
            
            <table class="min-w-full">
              
              <!-- Header -->
              <thead>
                <tr class="border-b border-gray-200 dark:border-gray-700">
                  <th
                    v-for="col in columns"
                    :key="col.key"
                    class="px-5 py-3 text-left w-3/11 sm:px-6"
                    :style="{ width: col.width || 'auto' }"
                  >
                    <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">
                        {{ col.label }}
                    </p>
                  </th>
                </tr>
              </thead>
          
              <!-- Body -->
              <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                <tr 
                  v-for="(row, index) in localData" 
                  :key="index"
                  :class="[
                    'border-t border-gray-100 dark:border-gray-800',
                    props.rowClassKey ? row[props.rowClassKey] : ''
                  ]"
                >
          
                  <td
                    v-for="col in columns"
                    :key="col.key"
                    class=" py-4 "
                  >
                    <span
                      v-if="col.key === 'numberVignette'"
                      v-html="row[col.key]"
                    ></span>
                    <input
                       v-else-if="!col.readonly "
                      :type="col.type || 'text'"
                      v-model="localData[index][col.key]"
                      class="dark:bg-dark-900 w-full bg-transparent px-4 py-2.5 text-sm text-gray-800 outline-none dark:text-white/90"
                    />
                    <span v-else class="px-4 py-2.5 text-sm text-gray-800 dark:text-white/90">
                      {{ row[col.key] }}
                    </span>
                  </td>

                  <!-- bouton supprimer -->
                  <!-- <td v-if="!props.readonly" class="border border-none text-center text-sm">
                    <button
                      class="text-gray-500 hover:text-red-700 px-2"
                      @click="removeRow(index)"
                    >
                      <TrashIcon class="w-5"/>
                    </button>
                  </td> -->
          
                </tr>
              </tbody>
          
            </table>
        </div>
    </div>
</template>

<script setup>
import { computed } from "vue"
import AddIcon from "@/icons/AddIcon.vue"
import TrashIcon from "@/icons/TrashIcon.vue"
import AperçuIcon from "@/icons/AperçuIcon.vue"

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  columns: Array,
  readonly: {
    type: Boolean,
    default: false
  },
  rowClassKey: {   
    type: String,
    default: null
  },
})

const emit = defineEmits(["update:modelValue"])

/**
 * PROXY v-model (solution officielle Vue 3)
 */
/* const localData = ref([]) */

const localData = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val)
})

const createEmptyRow = () => {
  const row = {}
  props.columns.forEach(col => {
    row[col.key] = ""
  })
  return row
}

/* const addRow = () => {
  localData.value = [
    ...localData.value,
    createEmptyRow()
  ]
}

const removeRow = (index) => {
  localData.value = localData.value.filter((_, i) => i !== index)
} */

</script>