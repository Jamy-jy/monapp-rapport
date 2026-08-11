<template>
    <button
        class="h-11 px-6 flex items-center gap-2 justify-center rounded-lg bg-green-600 text-white text-sm font-medium shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-1 dark:focus:ring-offset-dark-900 transition-transform duration-100 active:scale-95 active:shadow-inner"
        @click="save"
    >
        <svg
            xmlns="http://www.w3.org/2000/svg" 
            width="24"  
            height="24"  
            viewBox="0 0 24 24"  
            fill="none"  
            stroke="currentColor"  
            stroke-width="2"  
            stroke-linecap="round"  
            stroke-linejoin="round"
        >  
            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />  <polyline points="17 21 17 13 7 13 7 21" />  
            <polyline points="7 3 7 8 15 8" />
        </svg>
        Enregistrer
    </button>
</template>

<script setup lang="ts">
import { ref } from 'vue'

function save() {
  console.log('Save clicked')
}
</script>