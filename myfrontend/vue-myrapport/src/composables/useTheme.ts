import { ref, provide, inject, watchEffect, type Ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

/* ------------------------------------------------------------------
 * Types
 * ------------------------------------------------------------------ */

export type Theme = 'light' | 'dark'

interface ThemeContext {
  theme: Ref<Theme>
  toggleTheme: () => void
}

/* ------------------------------------------------------------------
 * Symbol
 * ------------------------------------------------------------------ */

const ThemeSymbol = Symbol('ThemeContext')

/* ------------------------------------------------------------------
 * Provider
 * ------------------------------------------------------------------ */

export function useThemeProvider(): ThemeContext {
  const authStore = useAuthStore()
  //clé unique par utilisateur
  const themeKey = `theme_user_${authStore.user?.id}_${authStore.user?.role}`

  const theme = ref<Theme>(
    (sessionStorage.getItem(themeKey) as Theme) || 'light'
  )

  // init depuis sessionStorage
  watchEffect(() => {
    document.documentElement.classList.toggle('dark', theme.value === 'dark')
    sessionStorage.setItem(themeKey, theme.value)
  })

  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  const context: ThemeContext = {theme,toggleTheme,}
  provide(ThemeSymbol, context)
  return context
}

/* ------------------------------------------------------------------
 * Consumer
 * ------------------------------------------------------------------ */

export function useTheme(): ThemeContext {
  const context = inject<ThemeContext>(ThemeSymbol)

  if (!context) {
    throw new Error(
      'useTheme must be used within a ThemeProvider',
    )
  }

  return context
}
