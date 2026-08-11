<template>
  <div class="relative" ref="dropdownRef">
    <button
      class="flex items-center text-gray-700 dark:text-gray-400"
      @click.prevent="toggleDropdown"
    >
    
      <span class="block mr-1 font-medium text-theme-sm">{{ authStore.user?.nom }} </span>

      <ChevronDownIcon :class="{ 'rotate-180': dropdownOpen }" />
    </button>

    <!-- Dropdown Start -->
    <div
      v-if="dropdownOpen"
      class="absolute right-0 mt-[17px] flex w-[260px] flex-col rounded-2xl border border-gray-200 bg-white p-3 shadow-theme-lg dark:border-gray-800 dark:bg-gray-dark"
    >
      <div>
        <span class="block font-medium text-gray-700 text-theme-sm dark:text-gray-400">
          {{ authStore.user?.nom }}
        </span>
        <span class="mt-0.5 block text-theme-xs text-gray-500 dark:text-gray-400">
          {{ authStore.user?.prenom }}
        </span>
      </div>

      <ul class="flex flex-col gap-1 pt-4 pb-3 border-b border-gray-200 dark:border-gray-800">
        <li v-for="item in menuItems" :key="item.href">
          <router-link
            :to="item.href"
            class="flex items-center gap-3 px-3 py-2 font-medium text-gray-700 rounded-lg group text-theme-sm hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
          >
            <!-- SVG icon would go here -->
            <component
              :is="item.icon"
              class="text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-300"
            />
            {{ item.text }}
          </router-link>
        </li>
      </ul>
      
      <div>
        <!-- Bouton déconnexion -->
        <button
          @click="showLogoutModal = true"
          class="flex items-center gap-3 px-3 py-2 mt-3 w-full font-medium text-gray-700 rounded-lg group text-theme-sm hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
        >
          <LogoutIcon class="text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-300" />
          Déconnexion
        </button>

        <!-- Modal confirmation -->
        <div
          v-if="showLogoutModal"
          class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
        >
          <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6 text-center">

            <!-- Icône -->
            <div class="flex items-center justify-center w-14 h-14 rounded-full bg-red-100 dark:bg-red-900/30 mx-auto mb-4">
              <LogoutIcon class="w-7 h-7 text-red-500" />
            </div>

            <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
              Confirmer la déconnexion
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
              Êtes-vous sûr de vouloir vous déconnecter ?
            </p>

            <div class="flex justify-center gap-3">
              <!-- Annuler -->
              <button
                @click="showLogoutModal = false"
                class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-800"
              >
                Annuler
              </button>

              <!-- Confirmer -->
              <button
                @click="handleLogOut"
                :disabled="loading"
                class="px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition disabled:opacity-50"
              >
                {{ loading ? 'Déconnexion...' : 'Se déconnecter' }}
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
    <!-- Dropdown End -->
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, computed } from 'vue'
import { ChevronDownIcon, LogoutIcon, UserCircleIcon, HistoriqueIcon } from '@/icons'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const dropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const route = useRoute()
const authStore = useAuthStore()
const router = useRouter()
const showLogoutModal = ref(false)
const loading = ref(false)

const profileLink = computed(() => {
  if (authStore.user?.role === 'admin') return '/admin/profile'
  if (authStore.user?.role === 'tech') return '/tech/profile'
  return '/login'
})

const menuItems = computed(() => [
  { href: profileLink.value, icon: UserCircleIcon, text: 'profile' },
  ...(authStore.user?.role === 'admin'
    ? [
        {
          href: '/admin/historique',
          icon: HistoriqueIcon,
          text: 'historique',
        },
      ]
    : []),
])

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleLogOut = async () => {
  
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 3000))
  
  try {
    //timer le deconnexion de 3 secondes
    await authStore.logout()
    showLogoutModal.value = false
    router.push('/login')
  } catch (err) {
    console.error('Erreur logout:', err)
  } finally {
    loading.value = false
  }
}

const handleClickOutside = (event: Event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
