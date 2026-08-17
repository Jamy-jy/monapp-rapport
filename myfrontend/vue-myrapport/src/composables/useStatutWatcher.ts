import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import API_CONFIG from '@/config/api'

export function useStatutWatcher() {
  const authStore = useAuthStore()
  const router = useRouter()
  let interval: ReturnType<typeof setInterval> | null = null

  const checkStatut = async () => {
    if (!authStore.isAuthenticated) return

    try {
      await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/check-statut/`, {
        headers: { Authorization: `Bearer ${authStore.token}` }
      })
    } catch (err: any) {
      const status = err.response?.status
      
      // Compte bloqué ou token invalide déconnexion forcée
      if (status === 403 || status === 401) {
        stopWatcher()
        await authStore.logout()
        router.push({
          path: '/',
          query: { blocked: status === 403 ? '1' : '0' }  // passer info à login
        })
      }
    }
  }

  const startWatcher = () => {
    // Vérifier toutes les 10 secondes
    interval = setInterval(checkStatut, 10000)
  }

  const stopWatcher = () => {
    if (interval) {
      clearInterval(interval)
      interval = null
    }
  }

  onMounted(() => {
    startWatcher()
  })

  onUnmounted(() => {
    stopWatcher()
  })

  return { checkStatut, startWatcher, stopWatcher }
}