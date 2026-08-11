<template>
    <button
        class="h-11 px-5 flex items-center gap-2 justify-center rounded-lg bg-brand-500 py-2.5 text-sm font-medium text-white hover:bg-brand-600 sm:w-auto"
        @click="update"
    >
        <svg  
            width="24"  height="24"  viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"  
            fill="none"  
            stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"
        >  
            <path d="M12 20h9" />  
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
        </svg>
        Modifier
    </button>
</template>
<script setup lang="ts">
import { ref } from 'vue'

function update() {
  console.log('update clicked')
}
</script>