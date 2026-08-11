<template>
    <div>
        <div class="relative">
            <span
              class="absolute left-0 top-1/2 inline-flex h-11 -translate-y-1/2 items-center justify-center border-r border-gray-200 py-3 pl-3.5 pr-3 text-gray-500 dark:border-gray-800 dark:text-gray-400"
            >
              {{ label }}
            </span>
            <input
              :type="type"
              :value="modelValue"
              @input="onInput"
              :placeholder="placeholder"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 pl-[90px] text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
    interface Props {
        label?: string
        type?: string
        placeholder?: string
        modelValue: string
    }

    const props = defineProps<Props>()

    const emit = defineEmits<{
        (e: 'update:modelValue', value: string): void
    }>()

    const onInput = (e: Event) => {
        emit('update:modelValue', (e.target as HTMLInputElement).value)
    }
</script>