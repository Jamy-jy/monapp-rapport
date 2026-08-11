<template>
  <div class="fixed top-5 right-5 z-[99999] space-y-4 w-96">
    <TransitionGroup name="toast">
      <div
        v-for="alert in alertNotifStore.alerts"
        :key="alert.id"
        class="rounded-xl shadow-lg p-4 flex justify-between items-center"
        :class="alertClasses(alert.type)"
      >
        <div class="flex items-center gap-3">
          <component
            :is="icons[alert.type]"
          />
          <div class="flex flex-col">
            <span class="text-white font-medium">
              {{ alert.message }}
            </span>
            <router-link
              v-if="alert.action"
              :to="alert.action.route"
              @click="alertNotifStore.removeAlertNotif(alert.id)"
              class="underline text-brand-800 text-sm mt-1 font-semibold hover:text-brand-600"
            >
              {{ alert.action.label }}
            </router-link>

          </div>
        </div>

        <button
          @click="alertNotifStore.removeAlertNotif(alert.id)"
          class="ml-3 font-bold"
        >
          ✕
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { useAlertNotifStore } from '@/stores/AlertNotif';
import SuccesIcon from '@/icons/SuccesIcon.vue';
import ErrorIcon from '@/icons/ErrorIcon.vue';
import WarningIcon from '@/icons/WarningIcon.vue';
import InfoIcon from '@/icons/InfoIcon.vue';


const alertNotifStore = useAlertNotifStore()

const icons = {
  success: SuccesIcon,
  error: ErrorIcon,
  warning: WarningIcon,
  info: InfoIcon
}

const alertClasses = (type:string) => {
  return {
    success: "bg-green-600",
    error: "bg-red-600",
    warning: "bg-yellow-500",
    info: "bg-blue-600"
  }[type]
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all .35s ease;
}

.toast-enter-from {
  opacity:0;
  transform:translateX(50px) scale(.9);
}

.toast-leave-to {
  opacity:0;
  transform:translateX(100px);
}
</style>