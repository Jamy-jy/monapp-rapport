<template>
  <div
    class="rounded-2xl border border-gray-200 bg-gray-100 dark:border-gray-800 dark:bg-white/[0.03]"
  >
    <div
      class="px-5 pt-5 bg-white shadow-default rounded-2xl pb-11 dark:bg-gray-900 sm:px-6 sm:pt-6"
    >
      <div class="flex justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white/90">Ramette Papier</h3>
          <p class="mt-1 text-gray-500 text-theme-sm dark:text-gray-400">
            Pourcentange à peu près du reste du papier 
          </p>
        </div>
      </div>
      <div class="relative max-h-[195px]">
        <div id="chartTwo" class="h-full">
          <div class="radial-bar-chart">
            <VueApexCharts type="radialBar" height="330" :options="chartOptions" :series="series" />
          </div>
        </div>
      </div>
      <div class="text-center mt-2">
        <!-- <p class="text-sm text-gray-500 dark:text-gray-400">
          Stock total : 
          <span class="font-semibold" :class="couleurTexte">
            {{ pourcentageTotal.toFixed(2) }}%
          </span>
        </p> -->
        <p class="text-xs text-gray-400">
          {{ joursEcoules.toFixed(1) }} jour(s) depuis dernière entrée
        </p>
      </div>
      <p class="mx-auto mt-1.5 w-full max-w-[380px] text-center text-sm text-gray-500 sm:text-base">
        Papier A5, partagé entre plusieurs imprimentes
      </p>
    </div>

    <div class="flex items-center justify-between gap-5 px-6 py-3.5 sm:gap-8 sm:py-5">
      <div>
        <p class="flex-1 mb-1 text-center text-gray-500 text-theme-xs dark:text-gray-400 sm:text-sm">
          Entrée
        </p>
        <p
          class="flex items-center justify-center gap-1 text-base font-semibold text-gray-800 dark:text-white/90 sm:text-lg"
        >
          {{ nbr_entree_ram }}
          
            <svg 
              class="text-green-700" xmlns="http://www.w3.org/2000/svg" width="16"  height="16"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round">  
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />  
              <polyline points="10 17 15 12 10 7" />  
              <line x1="15" y1="12" x2="3" y2="12" />
            </svg>
          
        </p>
      </div>

      <div class="w-px bg-gray-200 h-7 dark:bg-gray-800"></div>

      <div>
        <p class="flex-1 mb-1 text-center text-gray-500 text-theme-xs dark:text-gray-400 sm:text-sm">
          Sortie
        </p>
        <p
          class="flex items-center justify-center gap-1 text-base font-semibold text-gray-800 dark:text-white/90 sm:text-lg"
        >
          {{ nbr_sortie_ram }}
          
            <svg class="text-red-500" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"> 
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /> <polyline points="16 17 21 12 16 7" /> <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
         
        </p>
      </div>

      <div class="w-px bg-gray-200 h-7 dark:bg-gray-800"></div>

      <div>
        <p class="flex-1 mb-1 text-center text-gray-500 text-theme-xs dark:text-gray-400 sm:text-sm">
          Reste
        </p>
        <p
          class="flex items-center justify-center gap-1 text-base font-semibold text-gray-800 dark:text-white/90 sm:text-lg"
        >
          {{ nbr_restant_ram }}
          
            <svg v-if="(nbr_restant_ram ?? 0) < 2" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M7.26816 13.6632C7.4056 13.8192 7.60686 13.9176 7.8311 13.9176C7.83148 13.9176 7.83187 13.9176 7.83226 13.9176C8.02445 13.9178 8.21671 13.8447 8.36339 13.6981L12.3635 9.70076C12.6565 9.40797 12.6567 8.9331 12.3639 8.6401C12.0711 8.34711 11.5962 8.34694 11.3032 8.63973L8.5811 11.36L8.5811 2.5C8.5811 2.08579 8.24531 1.75 7.8311 1.75C7.41688 1.75 7.0811 2.08579 7.0811 2.5L7.0811 11.3556L4.36354 8.63975C4.07055 8.34695 3.59568 8.3471 3.30288 8.64009C3.01008 8.93307 3.01023 9.40794 3.30321 9.70075L7.26816 13.6632Z" fill="#D92D20"/>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M7.60141 2.33683C7.73885 2.18084 7.9401 2.08243 8.16435 2.08243C8.16475 2.08243 8.16516 2.08243 8.16556 2.08243C8.35773 2.08219 8.54998 2.15535 8.69664 2.30191L12.6968 6.29924C12.9898 6.59203 12.9899 7.0669 12.6971 7.3599C12.4044 7.6529 11.9295 7.65306 11.6365 7.36027L8.91435 4.64004L8.91435 13.5C8.91435 13.9142 8.57856 14.25 8.16435 14.25C7.75013 14.25 7.41435 13.9142 7.41435 13.5L7.41435 4.64442L4.69679 7.36025C4.4038 7.65305 3.92893 7.6529 3.63613 7.35992C3.34333 7.06693 3.34348 6.59206 3.63646 6.29926L7.60141 2.33683Z" fill="#039855"/>
            </svg>
         
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import VueApexCharts from 'vue3-apexcharts'
import type { ApexOptions } from 'apexcharts'
import axios from 'axios'

const pourcentage = ref(0)     
const pourcentageTotal = ref(0) 
const qteRestant = ref(0)
const joursEcoules = ref(0)

// Couleur dynamique selon le pourcentage
const couleur = computed(() => {
  if (pourcentage.value <= 20) return '#D92D20'  // rouge
  if (pourcentage.value <= 50) return '#F79009'  // orange
  return '#465FFF'                                // bleu
})

// Couleur texte selon pourcentage total
const couleurTexte = computed(() => {
  if (pourcentageTotal.value <= 20) return 'text-red-500'
  if (pourcentageTotal.value <= 50) return 'text-orange-500'
  return 'text-blue-500'
})

defineProps<{
  nbr_entree_ram: number,
  nbr_sortie_ram: number,
  nbr_restant_ram: number
}>()

const series = computed(() => [pourcentage.value])

const chartOptions = computed<ApexOptions>(() => ({
  colors: [couleur.value],
  chart: {
    fontFamily: 'Outfit, sans-serif',
    sparkline: { enabled: true },
  },
  plotOptions: {
    radialBar: {
      startAngle: -90,
      endAngle: 90,
      hollow: { size: '80%' },
      track: {
        background: '#E4E7EC',
        strokeWidth: '100%',
        margin: 5,
      },
      dataLabels: {
        name: { show: false },
        value: {
          fontSize: '36px',
          fontWeight: '600',
          offsetY: 60,
          color: '#1D2939',
          formatter: (val: number) => val.toFixed(2) + '%'
        },
      },
    },
  },
  fill: {
    type: 'solid',
    colors: [couleur.value],  // ← couleur dynamique
  },
  stroke: { lineCap: 'round' },
  labels: ['Papier'],
}))

const fetchRam = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/stock/ram/')
    pourcentage.value = res.data.pourcentage
    pourcentageTotal.value = res.data.pourcentage_total  // texte réel
    qteRestant.value = res.data.qte_restant
    joursEcoules.value = res.data.jours_ecoules
  } catch (err) {
    console.error('Erreur chargement ram:', err)
  }
}

onMounted(() => {
  fetchRam()
})
</script>

<style scoped>
.radial-bar-chart {
  width: 100%;
  max-width: 330px;
  margin: 0 auto;
}
</style>
