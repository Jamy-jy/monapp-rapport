<template>
    <button
        class="h-11 px-5 flex items-center gap-2 justify-center rounded-lg bg-red-600 text-white text-sm font-medium shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1 dark:focus:ring-offset-dark-900"
        @click="deleteItem"
    >
         <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width="24"  height="24"  
            viewBox="0 0 24 24"  
            fill="none"  
            stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"
        >  
            <path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z" />  
            <line x1="18" y1="9" x2="12" y2="15" />  
            <line x1="12" y1="9" x2="18" y2="15" />
        </svg>
        Supprimer
    </button>
</template>

<script setup lang="ts">
import { ref } from 'vue'

function deleteItem() {
  console.log('update clicked')
}
</script>