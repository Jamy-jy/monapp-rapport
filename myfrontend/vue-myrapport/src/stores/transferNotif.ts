import { defineStore } from 'pinia'
import axios from 'axios'
import { useAlertNotifStore } from '@/stores/AlertNotif'
import API_CONFIG from '@/config/api'

export const useTransfertNotifStore = defineStore('transfertNotif', {
    state: () => ({
        transfertsEnAttente: [] as any[],
        pollingId: null as number | null,
        isPolling: false,
    }),

    actions: {
        async fetchTransferts() {
            try {
                const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/transfert-stock/en-attente/`)
                this.transfertsEnAttente = res.data

                const alert = useAlertNotifStore()
                res.data.forEach((t: any) => {
                    alert.showAlertNotif(
                        `Nouvel envoi : "${t.consommable_nom}" (nombre : ${t.quantite}) par ${t.admin_nom} — à valider`,
                        "warning",
                        10000,
                        {
                            label: "Cliquez ici pour la validation",
                            route: "/tech/stock"
                        }
                    )
                })
            } catch (err) {
                console.error(err)
            }
        },

        startPolling() {
            if (this.isPolling) return // évite les doublons si appelé plusieurs fois
            this.isPolling = true
            this.fetchTransferts() // premier appel immédiat
            this.pollingId = window.setInterval(() => {
                this.fetchTransferts()
            }, 15000)
        },

        stopPolling() {
            if (this.pollingId) {
                clearInterval(this.pollingId)
                this.pollingId = null
            }
            this.isPolling = false
        },
    },
})