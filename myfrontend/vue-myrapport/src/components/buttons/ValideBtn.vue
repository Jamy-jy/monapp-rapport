<template>
    <button
        class=" h-11 flex items-center gap-2 justify-center rounded-lg bg-green-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-1 dark:focus:ring-offset-dark-900"
        @click="valided"
    >
    <svg 
        xmlns="http://www.w3.org/2000/svg" 
        width="24" 
        height="24" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
    > 
        <path 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        stroke-width="2" 
        d="M5 13l4 4L19 7"
        /> 
    </svg>
        Valider   
    </button>
</template>
<script setup lang="ts">
import { ref } from 'vue'

function valided() {
  console.log('update clicked')
}
</script>