<template>
  <div
    class="overflow-hidden rounded-2xl border border-gray-200 bg-white px-5 pt-5 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6 sm:pt-6"
  >
    <div class="flex flex-col gap-2 mb-4 sm:flex-row sm:items-center sm:justify-between">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-white/90">
        Vol hier
      </h3>
      <div class="flex items-center gap-3 text-lg font-semibold text-gray-800 dark:text-white/90">
        {{ nbr_vol }} vol{{ nbr_vol > 1 ? 's' : '' }} 
      </div>

    </div>
    <div class="max-w-full overflow-x-auto custom-scrollbar">
      <table class="min-w-full">
        <thead>
          <tr class="border-t border-gray-100 dark:border-gray-800">
            <th class="py-3 text-center">
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">Numéro de vol</p>
            </th>
            <th class="py-3 text-center">
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">Nombre passagers</p>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="vols.length === 0">
            <td colspan="2" class="py-4 text-center text-sm text-gray-400">
              Aucun vol enregistré hier.
            </td>
          </tr>
          <tr
            v-for="vol in vols"
            :key="vol.numero_vol"
            class="border-t border-gray-100 dark:border-gray-800"
          >
            <td class="py-3 text-center whitespace-nowrap">
              <p class="text-gray-500 text-theme-sm dark:text-gray-400">{{ vol.numero_vol }}</p>
            </td>
            <td class="py-3 text-center whitespace-nowrap">
              <p class="text-gray-500 text-theme-sm dark:text-gray-400">{{ vol.total_passagers }}</p>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- <table class="min-w-full">
        <thead>
          <tr class="border-t border-gray-100 dark:border-gray-800">
            <th class="py-3 text-center">
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">Numero de vol</p>
            </th>
            <th class="py-3 text-center">
              <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">Nombre passagers</p>
            </th>
          </tr>
        </thead>
        <tbody>
           <tr
            v-for="(product, index) in products"
            :key="index"
            class="border-t border-gray-100 dark:border-gray-800"
          > 
          <tr
            class="border-t border-gray-100 dark:border-gray-800"
          >
            <td class="py-3 whitespace-nowrap">
              <p class="text-gray-500 text-theme-sm dark:text-gray-400">{{ product.box1 }} </p>
            </td>
            <td class="py-3 whitespace-nowrap">
              <p class="text-gray-500 text-theme-sm dark:text-gray-400"> {{ product.box2 }} </p>
            </td>
          </tr>
        </tbody>
      </table> -->
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import API_CONFIG from '@/config/api'

interface Vol {
  numero_vol: string
  total_passagers: number
  date_arrivee: string
}

const nbr_vol = ref(0)
const vols = ref<Vol[]>([])

const fetchRecap = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/recap-hier/`)
    nbr_vol.value = res.data.nbr_vol
    vols.value = res.data.vols
  } catch (err) {
    console.error('Erreur recap hier:', err)
  }
}

// Exposer les données tech pour le parent
const emit = defineEmits<{
  (e: 'tech', value: { prenom: string, nom: string, email: string } | null): void
}>()

onMounted(async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/recap-hier/`)
    nbr_vol.value = res.data.nbr_vol
    vols.value = res.data.vols
    emit('tech', res.data.tech)  // ← envoyer info tech au parent
  } catch (err) {
    console.error('Erreur recap hier:', err)
  }
})
</script>