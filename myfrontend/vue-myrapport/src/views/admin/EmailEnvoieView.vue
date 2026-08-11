<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle"/>
    <BoiteEnvoyéLink
        route1="/admin/consulter"
        route2="/admin/emailEnvoie"
        label1="Boîte de réception"
        label2="Email envoyé"
    />

    <!-- Chargement -->
    <div v-if="loading" class="p-6 text-center text-gray-500 text-sm">
        Chargement...
    </div>

    <!-- Liste vide -->
    <div v-else-if="emails.length === 0" class="p-6 text-center text-gray-500 text-sm">
        Aucun email envoyé.
    </div>

    <!-- Liste emails -->
  <div v-else class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
    <div
      v-for="email in emails"
      :key="email.id"
      @click="goToEmail(email.id)"
      class="flex items-center justify-between px-5 py-4 border-b border-gray-200 dark:border-gray-800 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800"
    >
      <div class="flex flex-col w-full">
        <div class="flex justify-between items-center">
          <span class="text-sm text-gray-700 dark:text-gray-300">
            {{ email.sender }}
          </span>
          <span class="text-xs text-gray-500">
            {{ email.date }}
          </span>
        </div>
        <span class="text-sm mt-1 text-gray-800 dark:text-gray-200">
          {{ email.subject }}
        </span>
        <span class="text-xs text-gray-500 truncate">
          {{ email.preview }}
        </span>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios';
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
import BoiteEnvoyéLink from '@/components/buttons/BoiteEnvoyéLink.vue';
import { useAuthStore } from '@/stores/auth';

const router = useRouter()
const currentPageTitle = ref('Email envoyé')
const loading = ref(true)

interface Email {
  id: number
  sender: string
  subject: string
  preview: string
  date: string
}

const emails = ref<Email[]>([])
const authStore = useAuthStore()

const fetchRapports = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/rapports/')

    emails.value = res.data.map((r: any) => ({
      id: r.id,
      sender: r.user_nom,                                          // expéditeur
      subject: r.objet,                                            // objet email
      preview: r.message?.substring(0, 80) || '',                  // aperçu message
      date: formatDate(r.created_at),                              // date envoi
    }))

  } catch (err) {
    console.error('Erreur chargement rapports:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const dayDiff = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (dayDiff === 0) {
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  } else if (dayDiff === 1) {
    return 'Hier'
  } else if (dayDiff < 7) {
    return date.toLocaleDateString('fr-FR', { weekday: 'short' })
  } else {
    return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
  }
}

const goToEmail = (id: number) => {
  const role = authStore.user?.role
  router.push(`/${role}/emails/${id}`)
}

onMounted(() => {
  fetchRapports()
})

</script>