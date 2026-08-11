<template>
  <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />
  <BoiteEnvoyéLink
    route1="/admin/consulter"
    route2="/admin/emailEnvoie"
    label1="Boîte de réception"
    label2="Email envoyé"
  />

  <div v-if="loading" class="p-6 text-center text-gray-500 text-sm">
    Chargement...
  </div>

  <div v-else-if="emails.length === 0" class="p-6 text-center text-gray-500 text-sm">
    Aucun email reçu.
  </div>

  <div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
    <div
      v-for="email in emails"
      :key="email.id"
      @click="goToEmail(email.id)"
      class="flex items-center justify-between px-5 py-4 border-b border-gray-200 dark:border-gray-800 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800"
      :class="!email.read ? 'font-semibold bg-gray-50 dark:bg-gray-800/40' : ''"
    >

      <!-- nouveau implémentation -->
      <div 
        class="flex items-center gap-3 w-full cursor-pointer"
        @click="goToEmail(email.id)"
      >

        <!-- Indicateur point non lu -->
        <span v-if="!email.read" class="block w-2 h-2 rounded-full bg-brand-500 shrink-0"></span>
          
        <span v-else class="block w-2 h-2 shrink-0"></span>
        
        <!-- Avatar initiales expéditeur -->
        <div class="flex items-center justify-center w-9 h-9 rounded-full bg-brand-500 text-white text-xs font-semibold shrink-0">
          {{ email.initiales }}
        </div>

        <div class="flex flex-col w-full">
          <div class="flex justify-between items-center">
            <span class="text-sm font-semibold text-gray-800 dark:text-white">
                {{ email.sender }}
            </span>
            <span class="text-xs text-gray-500">
              {{ email.date }}
            </span>
          </div>
          <span class="text-sm text-gray-700 dark:text-gray-300">
            {{ email.subject }}
          </span>
          <span class="text-xs text-gray-500 truncate">
            {{ email.preview }}
          </span>
        </div>

      </div>
      
       <!-- Bouton supprimer -->
      <button
        @click.stop="supprimerEmail(email.id)"
        class="ml-3 shrink-0 p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition"
        title="Supprimer"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue'
import BoiteEnvoyéLink from '@/components/buttons/BoiteEnvoyéLink.vue'
import { useAlertNotifStore } from '@/stores/AlertNotif'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const currentPageTitle = ref('Boite de réception')
const loading = ref(true)
const alert = useAlertNotifStore()

const authStore = useAuthStore()

interface Email {
  id: number
  sender: string
  initiales: string
  subject: string
  preview: string
  date: string
  read: boolean
}

const emails = ref<Email[]>([])

const getInitiales = (nom: string): string => {
  return nom.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr)
  const now = new Date()
  const dayDiff = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))

  if (dayDiff === 0) return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  if (dayDiff === 1) return 'Hier'
  if (dayDiff < 7) return date.toLocaleDateString('fr-FR', { weekday: 'short' })
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}

const fetchRecus = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/rapports/recus/')
    emails.value = res.data.map((r: any) => ({
      id: r.id,
      sender: r.user_nom,
      initiales: getInitiales(r.user_nom),
      subject: r.objet,
      preview: r.message?.substring(0, 80) || '',
      date: formatDate(r.created_at),
      read: r.is_read,
    }))
  } catch (err) {
    console.error('Erreur chargement réception:', err)
    alert.showAlertNotif(
            "Une erreur chargement",
            "error"
          )
  } finally {
    loading.value = false
  }
}

const goToEmail = (id: number) => {
  const role = authStore.user?.role
  router.push(`/${role}/emails/${id}`)
}

onMounted(() => {
  fetchRecus()
})

// Supprimer email — marque is_delete = true côté backend
const supprimerEmail = async (id: number) => {
  try {
    await axios.patch(`http://localhost:8000/api/rapports/recus/${id}/delete/`)
    // Retirer immédiatement de la liste sans refetch
    emails.value = emails.value.filter(e => e.id !== id)
    alert.showAlertNotif(
            "suppression effectué avec succès",
            "success"
          )
  } catch (err) {
    console.error('Erreur suppression:', err)
    alert.showAlertNotif(
            "Une erreur s'est produit lors de la suppression",
            "error"
          )
  }
}
</script>