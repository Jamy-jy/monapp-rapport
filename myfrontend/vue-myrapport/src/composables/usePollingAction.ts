import { onMounted, onUnmounted } from 'vue'

export function usePollingAction(
  actionFn: () => Promise<void> | void,
  intervalMs: number = 3000,
  pauseOnHidden: boolean = true
) {
  let timer: ReturnType<typeof setInterval> | null = null

  const start = (): void => {
    if (timer) return
    actionFn()
    timer = setInterval(actionFn, intervalMs)
  }

  const stop = (): void => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  const handleVisibilityChange = (): void => {
    if (document.hidden) stop()
    else start()
  }

  onMounted(() => {
    start()
    if (pauseOnHidden) {
      document.addEventListener('visibilitychange', handleVisibilityChange)
    }
  })

  onUnmounted(() => {
    stop()
    if (pauseOnHidden) {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  })

  return { start, stop }
}