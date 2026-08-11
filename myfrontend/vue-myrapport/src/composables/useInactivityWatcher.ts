import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export function useInactivityWatcher(timeoutMinutes = 30) {
  const authStore = useAuthStore()
  const router = useRouter()
  let inactivityTimer: ReturnType<typeof setTimeout> | null = null

  const TIMEOUT_MS = timeoutMinutes * 30 * 1000  // 30 minutes -> ms

  // Réinitialiser le timer à chaque activité
  const resetTimer = () => {
    if (inactivityTimer) clearTimeout(inactivityTimer)

    inactivityTimer = setTimeout(async () => {
      await authStore.logout()
      router.push({
        path: '/login',
        query: { reason: 'inactivity' }  // <- info pour LoginView
      })
    }, TIMEOUT_MS)
  }

  // Événements à surveiller
  const events = [
    'mousemove',
    'mousedown',
    'keydown',
    'scroll',
    'touchstart',
    'click'
  ]

  const startWatcher = () => {
    events.forEach(event => {
      window.addEventListener(event, resetTimer)
    })
    resetTimer()  // démarrer le timer dès le montage
  }

  const stopWatcher = () => {
    if (inactivityTimer) {
      clearTimeout(inactivityTimer)
      inactivityTimer = null
    }
    events.forEach(event => {
      window.removeEventListener(event, resetTimer)
    })
  }

  onMounted(() => startWatcher())
  onUnmounted(() => stopWatcher())

  return { resetTimer, startWatcher, stopWatcher }
}