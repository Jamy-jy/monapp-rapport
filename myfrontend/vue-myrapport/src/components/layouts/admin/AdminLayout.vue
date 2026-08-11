<template>
  <div class="min-h-screen xl:flex bg-gray-50 dark:bg-gray-900 
            transition-colors duration-300">
    <AdminSidebar /> <!--app-sidebar nomination-->
    <Backdrop />
    <div
      class="flex-1 transition-all duration-300 ease-in-out"
      :class="[isExpanded || isHovered ? 'lg:ml-[290px]' : 'lg:ml-[90px]']"
    >
      <Navbar />  <!--app-header nomination-->
      <div class="p-4 mx-auto max-w-(--breakpoint-2xl)"> <!--<div class="p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6 min-h-screen xl:flex 
            bg-gray-50 dark:bg-gray-900 
            transition-colors duration-300">-->
        <router-view />
        <slot></slot>
      </div>
      <!-- Footer -->
      <footer class="p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6 pt-0">
        <p class="text-sm text-center text-gray-500 dark:text-gray-400">
          Developpé par  
          <a 
            href="https://madaozi.mg/webmail/" 
            target="_blank" 
            rel="noopener noreferrer"
            class="text-brand-500 hover:text-brand-600 transition-colors duration-200 font-medium"
          >
          MadaOzi
          </a>
          ~ Rapport de service  
          <a 
            href="" 
            target="_blank" 
            rel="noopener noreferrer"
            class="text-brand-500 hover:text-brand-600 transition-colors duration-200 font-medium"
          >
          Aeroport
          </a>
          .
        </p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import AdminSidebar from './AdminSidebar.vue'
import Navbar from '../Navbar.vue'
import Backdrop from '../Backdrop.vue'
import { useStatutWatcher } from '@/composables/useStatutWatcher'
import { useSidebarProvider} from '@/composables/useSidebar'
import { useThemeProvider } from '@/composables/useTheme'
import { useInactivityWatcher } from '@/composables/useInactivityWatcher'

const sidebar = useSidebarProvider()

const { isExpanded, isHovered } = sidebar

useStatutWatcher()
useThemeProvider()
useInactivityWatcher()

</script>
