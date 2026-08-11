<template>
  <FullScreenLayout>
    <div class="flex items-center justify-center min-h-screen bg-white dark:bg-gray-900">

      <div class="w-full max-w-md p-8 mb-40 bg-white rounded-xl shadow-lg dark:bg-gray-900">
        <!-- Message erreur -->
        <p v-if="errorMsg" class="text-sm text-red-500 text-center">
          {{ errorMsg }}
        </p>
        <!-- Titre -->
        <div class="mb-6 text-center">
          <h1 class="mb-2 text-xl font-semibold text-gray-800 dark:text-white/90">
            Authentification
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Connectez-vous pour accéder à votre compte
          </p>
        </div>
        <!-- check status -->
        <div
          v-if="isForcedLogout"
          class="mb-4 p-3 text-sm text-center text-orange-600 bg-orange-50 rounded-lg border border-orange-200"
        >
          Votre session a expiré. Veuillez vous reconnecter.
        </div>
        <div
          v-if="isInactive"
          class="flex mb-4 p-3 text-sm text-center text-blue-600 bg-blue-50 rounded-lg border border-blue-200"
        >
         <svg class="flex-1 text-blue-500 w-5 h-5"
            xmlns="http://www.w3.org/2000/svg" 
            width="24"  height="24"   
            viewBox="0 0 24 24"  
            stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"
            >  
            <path stroke="none" d="M0 0h24v24H0z"/>  
            <circle cx="12" cy="12" r="9" />  
            <line x1="12" y1="8" x2="12" y2="12" />  
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          
            Vous avez été déconnecté après 30 minutes d'inactivité.
          
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-5">

          <!-- Email -->
          <div>
            <label
              class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400"
            >
              Email
            </label>

            <input
              v-model="email"
              type="email"
              placeholder="exemple@email.com"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90"
            />
          </div>

          <!-- Password -->
          <div>
            <label
              class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400"
            >
              Mot de passe
            </label>

            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Votre mot de passe"
                class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent py-2.5 pl-4 pr-11 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90"
              />

              <!-- icone afficher mot de passe -->
              <span
                @click="togglePassword"
                class="absolute cursor-pointer right-4 top-1/2 -translate-y-1/2 text-gray-500 dark:text-gray-400"
              >
                <!-- OEIL OUVERT -->
                <svg
                    v-if="!showPassword"
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 
                    9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 
                    0-8.268-2.943-9.542-7z"
                    />
                </svg>

                <!-- OEIL FERMÉ -->
                <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 
                    0-8.268-2.943-9.542-7a9.956 9.956 0 012.042-3.368"
                    />
                    <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6.223 6.223A9.956 9.956 0 0112 5c4.477 
                    0 8.268 2.943 9.542 7a9.956 9.956 0 
                    01-4.132 5.411"
                    />
                    <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 01-4.243 2.828M9.879 
                    9.879A3 3 0 0115 12"
                    />
                    <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 3l18 18"
                    />
                </svg>
              </span>
            </div>
          </div>

          <!-- Button -->
          <button
            type="submit"
            class="flex items-center justify-center w-full px-4 py-3 text-sm font-medium text-white transition rounded-lg bg-brand-500 shadow-theme-xs hover:bg-brand-600 transition-transform duration-100 active:scale-95 active:shadow-inner"
          >
            Se connecter
          </button>

        </form>

      </div>

    </div>
  </FullScreenLayout>
</template>

<script setup lang="ts">
import { ref } from "vue"
import FullScreenLayout from "@/components/layouts/FullScreenLayout.vue"
import { useThemeProvider } from '@/composables/useTheme'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const email = ref('')
const password = ref('')
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const showPassword = ref(false)
const errorMsg = ref('')


/* const isBlocked = ref(route.query.blocked === '1') */
const isForcedLogout = ref(route.query.blocked === '0')
const isInactive = ref(route.query.reason === 'inactivity')

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleSubmit = async () => {
  try {
    errorMsg.value = ''
    const role = await authStore.login(email.value, password.value)

    if (role === 'admin') {
      router.push('admin/')
    } else {
      router.push('tech/')
    }
  } catch (error: any)  {
    errorMsg.value = error.response?.data?.error || 'Erreur de connexion'
  }
  console.log("Authentification", {
    email: email.value,
    password: password.value
  })
}

useThemeProvider()
</script>