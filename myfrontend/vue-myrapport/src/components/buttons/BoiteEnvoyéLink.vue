<template>
  <div class="flex gap-6 text-sm font-medium mb-2">
    
    <!-- Boite de réception -->
    <router-link
      :to="route1"
      class="cursor-pointer border-b-2 pb-1"
      :class="$route.path === route1
        ? 'text-blue-600 border-blue-600'
        : 'text-gray-500 border-transparent text-gray-600 hover:border-gray-500 hover:text-gray-500'"
    >
      {{ label1 }}
    </router-link>
    <span class="text-gray-500">
        /
    </span>

    <!-- Email envoyé -->
    <router-link
      :to="route2"
      class="cursor-pointer pb-1 border-b-2 transition-all duration-200"
      :class="$route.path === route2
        ? 'text-blue-600 border-blue-600 text-blue-600'
        : 'text-gray-500 border-transparent text-gray-600 hover:border-gray-500 hover:text-gray-500'"
    >
      {{ label2 }}
    </router-link>

  </div>
</template>

<script setup>
import { ref } from "vue"

const activeTab = ref("inbox")

defineProps({
  route1: {
    type: String,
    required: true
  },
  route2: {
    type: String,
    required: true
  },
  label1: {
    type: String,
    default: "Boîte de réception"
  },
  label2: {
    type: String,
    default: "Email envoyé"
  }
})
</script>