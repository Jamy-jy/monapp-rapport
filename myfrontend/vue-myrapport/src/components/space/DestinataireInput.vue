<template>
  <div class="space-y-3">

    <!-- Champ A -->
    <div class="relative">
      <span
        class="absolute left-0 top-1/2 inline-flex h-11 -translate-y-1/2 items-center justify-center border-r border-gray-200 py-3 pl-3.5 pr-3 text-gray-500 dark:border-gray-800 dark:text-gray-400"
      >
        À :
      </span>

      <div
        class="flex flex-wrap items-center gap-2 min-h-[30px] w-full rounded-lg border border-gray-200 pl-[90px] dark:border-gray-700"
      >
        <!-- Chips -->
        <span
          v-for="(email, index) in modelValue"
          :key="index"
          class="flex items-center gap-1 bg-brand-100 text-brand-700 px-2 py-1 rounded-md text-sm"
        >
          {{ email }}

          <button @click="removeEmail(index)">
            ✕
          </button>
        </span>

        <!-- Input -->
        <input
          v-model="inputValue"
          @keydown.enter.prevent="addEmail"
          @keydown.tab.prevent="addEmail"
          @keydown="handleKeydown"
          @blur="addEmail"
          type="email"
          placeholder="Entrez un autre email"
          class="flex-1 min-w-[120px] h-11 w-full text-sm text-gray-800 placeholder:text-gray-400 dark:text-white/90 dark:placeholder:text-white/30 focus:border-none focus:outline-none"
        />
      </div>



      <!-- Boutons Cc / Cci -->
      <div
        class="absolute right-3 top-1/2 -translate-y-1/2 flex gap-2 text-sm"
      >
        <button
          class="text-gray-500 hover:text-brand-500"
          @click="showCc = true"
        >
          Cc
        </button>

        <button
          class="text-gray-500 hover:text-brand-500"
          @click="showCci = true"
        >
          Cci
        </button>
      </div>
    </div>

    <!-- Champ CC -->
    <div v-if="showCc" class="relative">
      <span
        class="absolute left-0 top-1/2 inline-flex h-11 -translate-y-1/2 items-center justify-center border-r border-gray-200 py-3 pl-3.5 pr-3 text-gray-500 dark:border-gray-800 dark:text-gray-400"
      >
        Cc
      </span>

      <input
        v-model="cc"
        @input="emit('update:cc', cc)"
        type="email"
        placeholder="copie@madaozi.mg"
        class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 pl-[90px] text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
      />

      <!-- Trash Cc-->
      <button
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-red-500"
        @click="showCc = false"
        >
        <svg
            class="w-5 h-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <!-- couvercle -->
            <path d="M3 6h18"/>
            
            <!-- poubelle -->
            <path d="M8 6V4h8v2"/>
            <rect x="5" y="6" width="14" height="14" rx="2"/>

            <!-- lignes internes -->
            <path d="M10 11v6"/>
            <path d="M14 11v6"/>
        </svg>
      </button>
    </div>

    <!-- Champ Cci -->
    <div v-if="showCci" class="relative">
      <span
        class="absolute left-0 top-1/2 inline-flex h-11 -translate-y-1/2 items-center justify-center border-r border-gray-200 py-3 pl-3.5 pr-3 text-gray-500 dark:border-gray-800 dark:text-gray-400"
      >
        Cci
      </span>

      <input
        v-model="cci"
        @input="emit('update:cci', cci)"
        type="email"
        placeholder="copie cachée@madaozi.mg"
        class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 pl-[90px] text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
      />

      <!-- Trash -->
      <button
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-red-700"
        @click="showCci = false"
        >
        <svg
            class="w-5 h-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <!-- couvercle -->
            <path d="M3 6h18"/>
            
            <!-- poubelle -->
            <path d="M8 6V4h8v2"/>
            <rect x="5" y="6" width="14" height="14" rx="2"/>

            <!-- lignes internes -->
            <path d="M10 11v6"/>
            <path d="M14 11v6"/>
        </svg>
      </button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"

interface Props {
        label?: string
        type?: string
        placeholder?: string
        modelValue: string[]
    }
  
const props = defineProps<Props>()

const emit = defineEmits<{
        (e: 'update:modelValue', value: string[]): void
        (e: 'update:cc', value: string): void
        (e: 'update:cci', value: string): void
    }>()

const cc = ref("")
const cci = ref("")
    
const showCc = ref(false)
const showCci = ref(false)

const inputValue = ref("")

const addEmail = () => {
  const value = inputValue.value.trim()

  if (!value) return

  // split si plusieurs emails collés
  const emails = value.split(/[,;\s]+/)

  const validEmails = emails.filter(e =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)
  )

  emit("update:modelValue", [...props.modelValue, ...validEmails])

  inputValue.value = ""

  const uniqueEmails = validEmails.filter(
    e => !props.modelValue.includes(e)
  )
}

const removeEmail = (index: number) => {
  const updated = [...props.modelValue]
  updated.splice(index, 1)
  emit("update:modelValue", updated)
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === "," || e.key === "Enter" || e.key === "Tab") {
    e.preventDefault()
    addEmail()
  }
}
</script>