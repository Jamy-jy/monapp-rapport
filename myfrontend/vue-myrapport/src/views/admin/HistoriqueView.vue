<template>
  <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />

  <ComponentCard title="Historique de mouvement de stock">

    <!-- Header avec bouton effacer -->
    <div class="flex items-center justify-between mb-4">
      <p class="text-sm text-gray-500 dark:text-gray-400">
        {{ historique.length }} mouvement(s)
      </p>
      <button
        @click="showDeleteModal = true"
        class="text-sm text-red-500 hover:text-red-600 hover:underline transition"
      >
        Effacer les historiques
      </button>
    </div>

    <!-- Liste des mouvements -->
    <div v-if="loading" class="text-center text-gray-500 text-sm py-6">
      Chargement...
    </div>

    <div v-else-if="historique.length === 0" class="text-center text-gray-500 text-sm py-6">
      Aucun historique disponible.
    </div>

    <ul v-else class="space-y-3">
      <li
        v-for="item in historique"
        :key="item.id"
        class="flex items-start gap-3 p-3 rounded-lg border border-gray-100 dark:border-gray-800"
      >
        <!-- Icône type mouvement -->
        <div
          class="flex items-center justify-center w-8 h-8 rounded-full shrink-0 mt-0.5"
          :class="item.type === 'entree'
            ? 'bg-green-100 dark:bg-green-900/30'
            : 'bg-orange-100 dark:bg-orange-900/30'"
        >
          <!-- Flèche haut = entrée -->
          <svg v-if="item.type === 'entree'" class="w-4 h-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
          </svg>
          <!-- Flèche bas = sortie -->
          <svg v-else class="w-4 h-4 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
          </svg>
        </div>

        <!-- Message -->
        <div class="flex-1">
          <p class="text-sm text-gray-700 dark:text-gray-300">
            {{ item.message }}
          </p>
          <p class="text-xs text-gray-400 mt-0.5">{{ item.date }}</p>
        </div>

        <!-- Badge type -->
        <span
          class="text-xs px-2 py-0.5 rounded-full font-medium shrink-0"
          :class="item.type === 'entree'
            ? 'bg-green-50 text-green-600 dark:bg-green-500/15'
            : 'bg-orange-50 text-orange-600 dark:bg-orange-500/15'"
        >
          {{ item.type === 'entree' ? 'Entrée' : 'Sortie' }}
        </span>
      </li>
    </ul>

  </ComponentCard>

  <!-- Modal suppression -->
  <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
      <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
        Effacer l'historique
      </h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
        Choisissez la période à supprimer :
      </p>

      <div class="space-y-2">
        <button
          v-for="option in deleteOptions"
          :key="option.value"
          @click="confirmDelete(option.value)"
          class="w-full text-left px-4 py-2.5 text-sm rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-red-50 hover:border-red-300 hover:text-red-600 dark:hover:bg-red-900/20 transition"
        >
          {{ option.label }}
        </button>
      </div>

      <div class="flex justify-end mt-4">
        <button
          @click="showDeleteModal = false"
          class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400"
        >
          Annuler
        </button>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'
import API_CONFIG from '@/config/api'

const currentPageTitle = ref('Historique')
const loading = ref(true)
const showDeleteModal = ref(false)

interface HistoriqueItem {
  id: number
  message: string
  date: string
  type: 'entree' | 'sortie'
}

const historique = ref<HistoriqueItem[]>([])

const deleteOptions = [
  { label: "Aujourd'hui", value: 'aujourd_hui' },
  { label: 'Semaine dernière', value: 'semaine' },
  { label: 'Mois dernier', value: 'mois' },
  { label: 'Tout supprimer', value: 'tout' },
]

const fetchHistorique = async () => {
  try {
    loading.value = true
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/historique/`)
    historique.value = res.data
  } catch (err) {
    console.error('Erreur historique:', err)
  } finally {
    loading.value = false
  }
}

const confirmDelete = async (intervalle: string) => {
  try {
    await axios.delete(`${API_CONFIG.LOCAL.BASE_URL}/historique/delete/`, {
      data: { intervalle }
    })
    showDeleteModal.value = false
    await fetchHistorique()
  } catch (err) {
    console.error('Erreur suppression:', err)
  }
}

onMounted(() => {
  fetchHistorique()
})
</script>