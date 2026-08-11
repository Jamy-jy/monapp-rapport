<template>
        <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />
          <div class="p-6 bg-white dark:bg-gray-900 rounded-xl">

            <h1 class="text-lg text-gray-700 dark:text-gray-300 font-semibold mb-2">
              Rapport de service reçu
            </h1>

            <p class="text-sm text-gray-500 mb-4">
              Support IT • 10:45
            </p>

            <div class="text-gray-700 dark:text-gray-300">
              Votre rapport a été enregistré avec succès.
            </div>

          </div>

</template>

<script setup lang="ts">
import { ref } from 'vue'
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';


const currentPageTitle = ref('Detail email')

</script>