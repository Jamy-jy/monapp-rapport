<template>
  <div
    :class="[
      'rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]',
      className,
    ]"
  >
    <!-- Card Header -->
    <div class="flex items-center justify-between px-6 py-5">
      <div>
        <h3 class="text-base font-medium text-gray-800 dark:text-white/90">
          {{ title }}
        </h3>
        <p v-if="desc" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {{ desc }}
        </p>
      </div>

      <button
        v-if="textClick"
        type="button"
        @click="$emit('clickText')"
        class="flex items-center gap-2 text-sm font-medium transition text-brand-500 hover:text-brand-600 dark:text-brand-400"
      >
        <Component
          :is="icon"
          v-if="icon"
          class="w-5 h-5"
        />
        <span>{{ textClick }}</span>
      </button>
    </div>

    <!-- Card Body -->
    <div class="p-4 border-t border-gray-100 dark:border-gray-800 sm:p-6">
      <div class="space-y-5">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  title: string
  className?: string
  desc?: string
  textClick?: string
  icon?: Component
}>()

defineEmits<{
  (e: 'clickText'): void
}>()


</script>
