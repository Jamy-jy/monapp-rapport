<template>
    <PageBreadcrumbTech :pageTitle="currentPageTitle" />
    <!-- <div class="p-6 bg-white dark:bg-gray-900 rounded-xl"></div> -->          
    <!-- Chargement -->
  <div v-if="loading" class="p-6 text-center text-gray-500 text-sm">
    Chargement...
  </div>

  <!-- Erreur -->
  <div v-else-if="!rapport" class="p-6 text-center text-gray-500 text-sm">
    Rapport introuvable.
  </div>

  <!-- Détail email -->
  <div v-else class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 space-y-6">

    <!-- Objet -->
    <h2 class="text-xl font-semibold text-gray-800 dark:text-white">
      {{ rapport.objet }}
    </h2>

    <!-- Entête expéditeur -->
    <div class="flex items-start justify-between border-b border-gray-200 dark:border-gray-700 pb-4">
      <div class="flex items-center gap-3">

        <!-- Avatar initiales -->
        <div class="flex items-center justify-center w-10 h-10 rounded-full bg-brand-500 text-white text-sm font-semibold shrink-0">
          {{ initiales }}
        </div>

        <div>
          <!-- Expéditeur -->
          <p class="text-sm font-semibold text-gray-800 dark:text-white">
            {{ rapport.user_nom }}
          </p>

          <!-- Destinataires -->
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
            <span v-if="rapport.est_expediteur">
              À : <span class="text-gray-700 dark:text-gray-300">{{ rapport.email_destiny }}</span>
            </span>
            <span v-else>
              De : <span class="text-gray-700 dark:text-gray-300">{{ rapport.user_nom }}</span>
            </span>
          </p>

          <!-- Période du service -->
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
            Service : {{ formatDateTime(rapport.date_debut) }} à {{ formatDateTime(rapport.date_fin) }}
          </p>
        </div>
      </div>

      <!-- Date envoi -->
      <span class="text-xs text-gray-500 dark:text-gray-400 shrink-0">
        {{ formatDateTime(rapport.created_at) }}
      </span>
    </div>

    <!-- Corps du message -->
    <div class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line min-h-[120px]">
      {{ rapport.message || 'Aucun message.' }}
    </div>

    <!-- Pièce jointe -->
    <div
      v-if="rapport.fichier"
      class="border border-gray-200 dark:border-gray-700 rounded-xl p-4"
    >
      <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-3 uppercase tracking-wide">
        Pièce jointe
      </p>

      <a
        :href="`http://localhost:8000${rapport.fichier}`"
        target="_blank"
        download
        class="flex items-center gap-3 w-fit px-4 py-2.5 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
      >
        <!-- Icône fichier -->
        <div class="flex items-center justify-center w-9 h-9 rounded-lg bg-green-100 dark:bg-green-900/30">
          <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>

        <div>
          <p class="text-sm font-medium text-gray-800 dark:text-white">
            {{ nomFichier }}
          </p>
          <p class="text-xs text-gray-500">Cliquer pour télécharger</p>
        </div>
      </a>
    </div>

    <!-- Bouton retour -->
    <div class="flex gap-3 pt-2">
      <button
        v-if="!rapport.est_expediteur"
        @click="repondre"
        class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600 transition"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"/>
        </svg>
        Répondre
      </button>

      <button
        @click="router.back()"
        class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        Retour
      </button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios'
import PageBreadcrumbTech from '@/components/common/PageBreadcrumbTech.vue';

const route = useRoute()
const router = useRouter()
const currentPageTitle = ref('Detail email')
const loading = ref(true)

interface Rapport {
  id: number
  user_nom: string
  email_destiny: string
  user_email: string 
  objet: string
  message: string
  fichier: string | null
  date_debut: string
  date_fin: string
  created_at: string
  est_expediteur: boolean
}

const rapport = ref<Rapport | null>(null)

//Initiales de l'expéditeur pour l'avatar
const initiales = computed(() => {
  if (!rapport.value?.user_nom) return '?'
  return rapport.value.user_nom
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

// Nom du fichier extrait du chemin
const nomFichier = computed(() => {
  if (!rapport.value?.fichier) return ''
  return rapport.value.fichier.split('/').pop() || 'fichier'
})

const formatDateTime = (dateStr: string): string => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const fetchRapport = async () => {
  try {
    const id = route.params.id
    const res = await axios.get(`http://localhost:8000/api/rapports/${id}/`)
    rapport.value = res.data
    console.log('RAPPORT DATA:', res.data)           // ← voir toutes les données
    console.log('EST EXPEDITEUR:', res.data.est_expediteur) 
  } catch (err) {
    console.error('Erreur chargement rapport:', err)
    rapport.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRapport()
})

// Répondre — redirige vers FaireRapport avec l'email de l'expéditeur pré-rempli
const repondre = () => {
  if (!rapport.value) return
  router.push({
    path: '/tech/redigeRapport',
    query: {
      replyTo: rapport.value.user_email,
      objet: `Re: ${rapport.value.objet}`,
    }
  })
}
</script>