<template>
  <button
    class="flex items-center gap-1 justify-center rounded-lg bg-brand-100 text-brand-600  py-3 text-sm font-medium hover:bg-brand-200 focus:outline-none focus:ring-2 focus:ring-brand-900 focus:ring-offset-1 dark:focus:ring-offset-dark-900 dark:bg-brand-950 dark:text-brand-400 dark:hover:bg-brand-999 transition-all duration-150 active:scale-95"
     @click="handleClick"
  >
    <!-- Icon Plus class="flex items-center gap-2 justify-center rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-600 sm:w-auto"-->
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="18"
      height="18"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      class="dark:text-white"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 4v16m8-8H4"
      />
    </svg>

    <!-- Label -->
    
      {{ label }}
  </button>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"

const props = defineProps<{
  label?: string
  redirectTo?: string  // route de destination
}>()

const emit = defineEmits<{
  (e: 'click'): void
}>()

const router = useRouter()

const handleClick = () => {
  emit('click')

if (props.redirectTo) {
    router.push(props.redirectTo)
  }
}
</script>