<template>
    <div class="grid grid-cols-1 sm:grid-cols-4 flex items-center ">
      <div class="relative sm:col-span-3 z-20 bg-transparent mr-4">
        <select
          :value="modelValue"
          @change="onChange"
          class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 pr-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90"
          :class="{ 'text-gray-800 dark:text-white/90': modelValue }"
        >
          <option value="" disabled>
              {{ placeholder }}
          </option>

          <option
            v-for="option in options"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
        <span
          class="absolute z-30 text-gray-500 -translate-y-1/2 pointer-events-none right-4 top-1/2 dark:text-gray-400"
        >
          <svg
            class="stroke-current"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396"
              stroke=""
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </span>
      </div>
      <div class="sm:col-span-1 flex items-end">
        <!-- Bouton ajout -->
        <PlusBtn
          label="Ajouter un modèle"
          redirectTo="/tech/modele"
          class="w-full"
        />
      </div>
    </div>
  
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"
import PlusBtn from "../buttons/PlusBtn.vue"

interface Option {
  label: string
  value: string | number
}

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: "",
  },

  options: {
    type: Array as () => Option[],
    default: () => [],
  },

  placeholder: {
    type: String,
    default: "Choisissez votre modèle",
  },

  redirectTo: {
    type: String,
    required: true,
  },
})

const emit = defineEmits([
  "update:modelValue",
])

const router = useRouter()

const onChange = (event: Event) => {
  const target = event.target as HTMLSelectElement

  emit("update:modelValue", target.value)
}

const goToLink = () => {
  router.push(props.redirectTo)
}
</script>