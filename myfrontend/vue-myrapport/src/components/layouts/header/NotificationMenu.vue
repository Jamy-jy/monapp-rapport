<template>
  <div class="relative" ref="dropdownRef">
    <button
      class="relative flex items-center justify-center text-gray-500 transition-colors bg-white border border-gray-200 rounded-full hover:text-dark-900 h-11 w-11 hover:bg-gray-100 hover:text-gray-700 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-white"
      @click="toggleDropdown"
    >
      <!-- <span
        :class="{ hidden: !notifying, flex: notifying }"
        class="absolute right-0 top-0.5 z-1 h-2 w-2 rounded-full bg-orange-400"
      >
        <span
          class="absolute inline-flex w-full h-full bg-orange-400 rounded-full opacity-75 -z-1 animate-ping"
        ></span>
      </span> -->
      <span
        v-if="hasUnread"
        class="absolute right-0 top-0.5 z-1 h-2 w-2 rounded-full bg-orange-400 flex"
      >
        <span class="absolute inline-flex w-full h-full bg-orange-400 rounded-full opacity-75 -z-1 animate-ping"></span>
      </span>
      <svg
        class="fill-current"
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M10.75 2.29248C10.75 1.87827 10.4143 1.54248 10 1.54248C9.58583 1.54248 9.25004 1.87827 9.25004 2.29248V2.83613C6.08266 3.20733 3.62504 5.9004 3.62504 9.16748V14.4591H3.33337C2.91916 14.4591 2.58337 14.7949 2.58337 15.2091C2.58337 15.6234 2.91916 15.9591 3.33337 15.9591H4.37504H15.625H16.6667C17.0809 15.9591 17.4167 15.6234 17.4167 15.2091C17.4167 14.7949 17.0809 14.4591 16.6667 14.4591H16.375V9.16748C16.375 5.9004 13.9174 3.20733 10.75 2.83613V2.29248ZM14.875 14.4591V9.16748C14.875 6.47509 12.6924 4.29248 10 4.29248C7.30765 4.29248 5.12504 6.47509 5.12504 9.16748V14.4591H14.875ZM8.00004 17.7085C8.00004 18.1228 8.33583 18.4585 8.75004 18.4585H11.25C11.6643 18.4585 12 18.1228 12 17.7085C12 17.2943 11.6643 16.9585 11.25 16.9585H8.75004C8.33583 16.9585 8.00004 17.2943 8.00004 17.7085Z"
          fill=""
        />
      </svg>
    </button>

    <!-- Dropdown Start -->
    <div
      v-if="dropdownOpen"
      class="absolute -right-[240px] mt-[17px] flex h-[480px] w-[350px] flex-col rounded-2xl border border-gray-200 bg-white p-3 shadow-theme-lg dark:border-gray-800 dark:bg-gray-dark sm:w-[361px] lg:right-0"
    >
      <div
        class="flex items-center justify-between pb-3 mb-3 border-b border-gray-100 dark:border-gray-800"
      >
        <h5 class="text-lg font-semibold text-gray-800 dark:text-white/90">Notification
          <span v-if="visibleNotifications.length > 0" class="ml-2 text-sm font-normal text-gray-500">
            ({{ visibleNotifications.length }})
          </span>
        </h5>

        <button @click="closeDropdown" class="text-gray-500 dark:text-gray-400">
          <svg
            class="fill-current"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M6.21967 7.28131C5.92678 6.98841 5.92678 6.51354 6.21967 6.22065C6.51256 5.92775 6.98744 5.92775 7.28033 6.22065L11.999 10.9393L16.7176 6.22078C17.0105 5.92789 17.4854 5.92788 17.7782 6.22078C18.0711 6.51367 18.0711 6.98855 17.7782 7.28144L13.0597 12L17.7782 16.7186C18.0711 17.0115 18.0711 17.4863 17.7782 17.7792C17.4854 18.0721 17.0105 18.0721 16.7176 17.7792L11.999 13.0607L7.28033 17.7794C6.98744 18.0722 6.51256 18.0722 6.21967 17.7794C5.92678 17.4865 5.92678 17.0116 6.21967 16.7187L10.9384 12L6.21967 7.28131Z"
              fill=""
            />
          </svg>
        </button>
      </div>

<!--       liste notifications  --> 
      <ul v-if="visibleNotifications.length > 0" class="flex flex-col h-auto overflow-y-auto custom-scrollbar">
        <li 
          v-for="notif in visibleNotifications"
          :key="notif.consommable_id + notif.type"
          >
          <div
            class="flex gap-3 rounded-lg border-b border-gray-100 p-3 px-4.5 py-3 cursor-pointer hover:bg-gray-100 dark:border-gray-800 dark:hover:bg-white/5"
            :class="notif.type === 'urgent' ? 'border-l-2 border-l-red-400' : 'border-l-2 border-l-orange-400'"
          >
            <!-- Icône type -->
            <div
              class="flex items-center justify-center w-8 h-8 rounded-full shrink-0"
              :class="notif.type === 'urgent' ? 'bg-red-100 dark:bg-red-900/30' : 'bg-orange-100 dark:bg-orange-900/30'"
            >
              <svg class="w-4 h-4" :class="notif.type === 'urgent' ? 'text-red-500' : 'text-orange-500'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              </svg>
            </div>

            <span class="block flex-1">
              <span class="mb-1 block text-theme-sm text-gray-500 dark:text-gray-400">
                {{ notif.message }} —
                <span class="font-medium text-gray-800 dark:text-white/90">
                   reste {{ notif.qte_restant }}
                </span>
              </span>
              <span class="flex items-center gap-2 text-theme-xs">
                <span 
                  class="font-medium px-2 py-0.5 rounded-full text-xs"
                  :class="notif.type === 'urgent' ? 'bg-red-100 text-red-600' : 'bg-orange-100 text-orange-600'"
                >
                  {{ notif.type === 'urgent' ? 'Urgent' : 'Alerte' }}
                </span>
                <span class="text-gray-400">{{ notif.timeLabel }}</span>
              </span>
            </span>
          </div>
        </li>
      </ul>
      <!-- Aucune notification -->
      <div v-else class="flex flex-col items-center justify-center flex-1 text-gray-400 text-sm">
        <svg class="w-10 h-10 mb-2 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
        </svg>
        Aucune notification
      </div>
      <!-- <router-link
        to="#"
        class="mt-3 flex justify-center rounded-lg border border-gray-300 bg-white p-3 text-theme-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
        @click="handleViewAllClick"
      >
        View All Notification
      </router-link> -->
    </div>
    <!-- Dropdown End -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const dropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

interface Notification {
  consommable_id: number
  nom_consommable: string
  qte_restant: number
  type: 'urgent' | 'alerte'
  message: string
  intervalle_minutes: number
  timeLabel?: string
  lu_at?: number  // timestamp de quand lu
}
 
const allNotifications = ref<Notification[]>([])

// Clé localStorage par type pour tracker quand la notif a été lue
const getLuKey = (notif: Notification) =>
  `notif_lu_${notif.consommable_id}_${notif.type}`

// Notifications visibles — filtre selon intervalle de réapparition
const visibleNotifications = computed(() => {
  const now = Date.now()
  return allNotifications.value.filter(notif => {
    const key = getLuKey(notif)
    const luAt = sessionStorage.getItem(key)
    if (!luAt) return true  // jamais lu → visible

    const elapsed = (now - parseInt(luAt)) / 60000  // en minutes
    return elapsed >= notif.intervalle_minutes  // réapparaît selon intervalle
  }).map(notif => ({
    ...notif,
    timeLabel: notif.type === 'urgent' ?  'besoin d\' une approvisionnement rapide' : 'approvisionnement le plut tôt possible'
  }))
})

// Badge orange si au moins une notification visible
const hasUnread = computed(() => visibleNotifications.value.length > 0)

const fetchNotifications = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/notifications/')
    allNotifications.value = res.data
  } catch (err) {
    console.error('Erreur notifications:', err)
  }
}

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value

  //Marquer toutes les notifications visibles comme lues
  if (dropdownOpen.value) {
    const now = Date.now()
    visibleNotifications.value.forEach(notif => {
      sessionStorage.setItem(getLuKey(notif), now.toString())
    })
  }
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    closeDropdown()
  }
}

// Rafraîchir les notifications toutes les 30 minutes
let refreshInterval: ReturnType<typeof setInterval>

onMounted(() => {
  fetchNotifications()
  document.addEventListener('click', handleClickOutside)
  refreshInterval = setInterval(fetchNotifications, 30 * 60 * 1000)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  clearInterval(refreshInterval)
})
</script>
