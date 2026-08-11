import { defineStore } from "pinia"
import { ref } from "vue"

export type AlertNotifType = "success" | "error" | "warning" | "info"

export interface AlertNotifAction {
  label: string
  route: string
}

interface AlertNotifItem {
  id: number
  type: AlertNotifType
  message: string
  action?: AlertNotifAction
}

export const useAlertNotifStore = defineStore("alert", () => {
  const alerts = ref<AlertNotifItem[]>([])

  const showAlertNotif = (
    message: string,
    type: AlertNotifType = "success",
    duration = 5000,
    action?: AlertNotifAction
  ) => {
    const id = Date.now()

    alerts.value.push({
      id,
      message,
      type,
      action
    })

    setTimeout(() => {
      removeAlertNotif(id)
    }, duration)
  }

  const removeAlertNotif = (id: number) => {
    alerts.value = alerts.value.filter(
      alert => alert.id !== id
    )
  }

  return {
    alerts,
    showAlertNotif,
    removeAlertNotif
  }
})