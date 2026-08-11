<template>
  <div class="space-y-6">
    <div class="rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]">
            
          <!-- En-tête -->
          <div class="flex items-center gap-2 mb-3">
            <!-- Icône enveloppe -->
            <svg
                class="w-5 h-5 text-gray-700 dark:text-white/80"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
            >
                <rect x="3" y="5" width="18" height="14" rx="2"/>
                <path d="M3 7l9 6 9-6"/>
            </svg>

            <h3 class="text-sm font-semibold text-gray-800 dark:text-white">
                Message
            </h3>
            </div>
            <TextareaInput v-model="modelValue"/>

        </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TextareaInput from '../FormElement/TextareaInput.vue';

const normalDescription = ref('')
const modelValue = defineModel<string>()
</script>