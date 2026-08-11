<template>
    <textarea
        :value="modelValue"
        @input="updateValue"
        :rows="rows"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        class="w-full rounded-lg border border-gray-300 bg-transparent px-4 py-3 text-sm text-gray-800 shadow-sm placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-gray-500 dark:focus:border-brand-800"
        >
    </textarea>
</template>

<script setup lang="ts">
defineProps({
  placeholder: {
    type: String,
    default: "Écrivez votre message ici..."
  },
  rows: {
    type: Number,
    default: 20
  },
  modelValue: {
    type: String,
    default: ""
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(["update:modelValue"])

const updateValue = (event: Event) => {
  const target = event.target as HTMLTextAreaElement
  emit("update:modelValue", target.value)
}
</script>
