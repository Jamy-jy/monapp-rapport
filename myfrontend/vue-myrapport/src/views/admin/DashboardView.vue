<template>
  
  <div class="grid grid-cols-12 gap-4 md:gap-6">
      <div class="col-span-12 space-y-6 xl:col-span-7">
        <CardBobineRuban
          :nbr_bobine="nbr_bobine"
          :nbr_ruban="nbr_ruban"
          />
        <ConsoMensuel 
          title="Consommation mensuelle"
          :data="consoData"
          :series-name="`Consommation ${anneeSelectionnee}`"
        />
      </div>
      <div class="col-span-12 xl:col-span-5">
        <ConsoPapier
          :nbr_entree_ram="nbr_entree_ram"
          :nbr_sortie_ram="nbr_sortie_ram"
          :nbr_restant_ram="nbr_restant_ram"
          />
      </div>

      <div class="col-span-12">
        <ConsoImprimante 
            :products="encreProducts"
            :boxops="encreBoxops"
        />
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CardBobineRuban from '@/components/dashboard/CardBobineRuban.vue'
import ConsoMensuel from '@/components/dashboard/ConsoMensuel.vue'
import ConsoPapier from '@/components/dashboard/ConsoPapier.vue'
import ConsoImprimante from '@/components/dashboard/ConsoImprimante.vue'
import { useAuthStore } from '@/stores/auth'
import { useAlertNotifStore } from '@/stores/AlertNotif'
import API_CONFIG from '@/config/api'

const auth = useAuthStore()
const message = ref('Chargement...')
const alert = useAlertNotifStore()

const nbr_bobine = ref(0)
const nbr_ruban = ref(0)
const nbr_entree_ram = ref(0)
const nbr_sortie_ram = ref(0)
const nbr_restant_ram = ref(0)

const encreProducts = ref<any[]>([])
const encreBoxops = ref<any[]>([])

//donnée conso Mensuel
const anneeActuelle = new Date().getFullYear()
const anneeSelectionnee = ref(anneeActuelle)
const annees = Array.from({ length: 5 }, (_, i) => anneeActuelle - i)
const consoData = ref<number[]>([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

const fetchConsoBobine = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/stock/dernier/`, {
      params: { nom: 'etiquette' }  // insensible à la casse côté backend
    })
    nbr_bobine.value = res.data.qte_restant
    console.log('Bobine:', nbr_bobine.value)
  } catch (err) {
    console.error(err)
  }
}

const fetchConsoRuban = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/stock/dernier/`, {
      params: { nom: 'ruban' }
    })
    nbr_ruban.value = res.data.qte_restant
    console.log('Ruban:', nbr_ruban.value)
  } catch (err) {
    console.error(err)
    alert.showAlertNotif(
            "Erreur lors de l'affichage",
            "error"
          )
  }
}

const fetchConsoRam = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/stock/dernier/`, {
      params: { nom: 'ram papier' }
    })
    nbr_entree_ram.value = res.data.qte_entree
    nbr_restant_ram.value = res.data.qte_restant
    nbr_sortie_ram.value = res.data.qte_sortie
    console.log('Ram:', nbr_ruban.value)
  } catch (err) {
    console.error(err)
    alert.showAlertNotif(
            "Erreur lors de l'affichage",
            "error"
          )
  }
}

const fetchConsoMensuel = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/stock/conso-mensuelle/`, {
      params: { annee: anneeSelectionnee.value }
    })
    consoData.value = res.data.data
    console.log('CONSO DATA:', res.data)        
    console.log('DATA ARRAY:', res.data.data)   
    consoData.value = res.data.data
  } catch (err) {
    console.error('Erreur conso mensuelle:', err)
    alert.showAlertNotif(
            "Erreur lors de l'affichage",
            "error"
          )
  }
}

const fetchEncre = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/encre/`)

    // Construire la structure attendue par le composant
    encreBoxops.value = res.data.boxops

    encreProducts.value = res.data.data.map((row: any) => ({
      couleur: row.couleur,
      nbr_bouteil: row.reserve,
      status: row.status,
      // niveaux : { boxop_id: '75%' }
      niveaux: Object.fromEntries(
        Object.entries(row.niveaux).map(([boxId, info]: [string, any]) => [
          Number(boxId),
          info.niveau + '%'
        ])
      )
    }))

  } catch (err) {
    console.error('Erreur chargement encre:', err)
  }
}

onMounted(() => {
  fetchConsoBobine()
  fetchConsoRuban()
  fetchConsoRam()
  fetchConsoMensuel()
  fetchEncre()
})

/* onMounted(async () => {
  const res = await api.get('/api/hello/')
  message.value = res.data.message
}) */
</script>

