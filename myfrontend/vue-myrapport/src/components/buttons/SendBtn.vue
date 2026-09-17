<template>
    <button
        class="flex items-center gap-2 justify-center rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-600 sm:w-auto"
        :disabled="loading"
        @click="send"
    >
        {{ loading ? 'Envoi...' : 'Envoyer' }}
        <svg 
            v-if="!loading"
            class="text-themeColor-500 w-5 h-5" 
            xmlns="http://www.w3.org/2000/svg" 
            width="8" 
            height="8" 
            viewBox="0 0 24 24" 
            stroke-width="2" 
            stroke="currentColor" 
            fill="none" 
            stroke-linecap="round" 
            stroke-linejoin="round"
        > 
            <path 
                stroke="none" 
                d="M0 0h24v24H0z"
            /> 
            <line x1="10" y1="14" x2="21" y2="3" /> 
            <path d="M21 3L14.5 21a.55 .55 0 0 1 -1 0L10 14L3 10.5a.55 .55 0 0 1 0 -1L21 3" />
        </svg>

        <!-- Spinner pendant le chargement -->
        <svg
            v-else
            class="w-5 h-5 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
        >
            <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
            />

            <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
        </svg>
        
       
    </button>
</template>
<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
    loading?: boolean
}>()

const emit = defineEmits<{
    (e: 'click'): void
}>()

function send() {
    if (props.loading) return

    emit('click')
    console.log('update clicked')
}
</script>