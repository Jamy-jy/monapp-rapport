<template>
  <PageBreadcrumbTech :pageTitle="currentPageTitle"/>
  <div class="space-y-6">
    <ComponentCard title="Horaire">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <PlaceholderInput
          v-model="dateDebut"
          type="datetime-local"
          label="Date et heure du début du traitement"
          placeholder=""
        />
        <PlaceholderInput
          v-model="dateFin"
          type="datetime-local"
          label="Date et heure du fin du traitement"
          placeholder=""
        />
        <div class="mt-6.5 mx-12 grid grid-cols-1 sm:grid-cols-1">
          <button
            @click="fetchData"
            :disabled="!dateDebut || !dateFin || loading"
            class=" h-11 flex items-center gap-2 justify-center rounded-lg bg-brand-100 text-brand-600 px-4 py-2.5 text-sm font-medium hover:bg-brand-200 focus:outline-none focus:ring-2 focus:ring-brand-900 focus:ring-offset-1 dark:focus:ring-offset-dark-900 dark:bg-brand-950 dark:text-brand-400 dark:hover:bg-brand-999"
          >
          <RefreshIcon/>
          {{ loading ? 'Chargement...' : 'Afficher' }}
        </button>
        </div>
      </div>
    </ComponentCard>

    <!-- Résultats -->
    <ComponentCard v-if="searched" title="Résultats">

      <!-- Aucun résultat -->
      <div v-if="results.length === 0" class="text-center text-gray-500 text-sm py-4">
        Aucun résultat pour cette période.
      </div>

      <!-- Tableau résultats -->
      <table v-else class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead>
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type Visa</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantité</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr v-for="row in results" :key="row.type">
            <td class="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">{{ row.type }}</td>
            <td class="px-4 py-3 text-sm font-semibold text-gray-800 dark:text-white">{{ row.quantite }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Total -->
      <div class="flex justify-end mt-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
        Total : {{ results.reduce((sum, r) => sum + Number(r.quantite), 0) }}
      </div>
    </ComponentCard>

    <!-- Erreur -->
    <div v-if="errorMsg" class="p-4 text-sm text-red-500 bg-red-50 rounded-lg dark:bg-red-900/20">
      {{ errorMsg }}
    </div>

    <ComponentCard title="Information du vol">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <PlaceholderInput
          v-model="NVol"
          type="text"
          label="Numéro du vol"
          placeholder="Entrez le numéro du vol"
        />
        <PlaceholderInput
          :modelValue="NbPassagers"
          type="number"
          label="Nombre du passager"
          placeholder=""
          :readonly="true"
        />
        <div class="mt-6.5 mx-12 grid grid-cols-1 sm:grid-cols-1">
          <SaveBtn @click="saveData"/>
        </div>
      </div>
    </ComponentCard>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios';
import PageBreadcrumbTech from '@/components/common/PageBreadcrumbTech.vue'
import ComponentCard from '@/components/common/ComponentCard.vue';
import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
import RefreshIcon from '@/icons/RefreshIcon.vue';
import SaveBtn from '@/components/buttons/SaveBtn.vue';
import { useAlertNotifStore } from '@/stores/AlertNotif';
import API_CONFIG from '@/config/api'; 

const currentPageTitle = ref('Mouvement du vol')

const alert = useAlertNotifStore()

const dateDebut = ref('')
const dateFin = ref('')
const NVol = ref('')
const loading = ref(false)
const searched = ref(false)
const errorMsg = ref('')
const results = ref<Record<string, any>[]>([])

// Total calculé automatiquement
const NbPassagers = computed(() => 
  results.value.reduce((sum, r) => sum + Number(r.quantite), 0)
)

// Colonnes dynamiques depuis les clés du premier résultat
const resultColumns = computed(() => {
  if (results.value.length === 0 || !results.value[0] ) return []
  return Object.keys(results.value[0])
})

const fetchData = async () => {
  if (!dateDebut.value || !dateFin.value) return

  loading.value = true
  errorMsg.value = ''
  searched.value = false
  results.value = []

  try {
    const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/proxy/report-visa/`, {
        begin: dateDebut.value,  // 
        end: dateFin.value,      // 
    })

    // Gérer result [] ou objet direct
    const data = res.data?.result 
    if (data) {
      // Convertir l'objet result en tableau de lignes
      results.value = Object.entries(data).map(([key, value]) => ({
        type: key,
        quantite: value
      }))
    }

    searched.value = true

  } catch (err) {
    errorMsg.value = 'Erreur lors de la récupération des données.'
    alert.showAlertNotif(
      "récupération interrompu! Veuillez reéssayer",
      "error"
    )
    console.error(err)
  } finally {
    loading.value = false
  }
}

const saveData = async () => {
  if (!NVol.value) {
    alert.showAlertNotif(
            "Veuillez saisir le numéro du vol",
            "warning"
          )
    return
  }

  if (results.value.length === 0) {
    alert.showAlertNotif(
      "Il faut d\'abord que les données s'affichent",
      "info"
    )
    return
  }

  try {
    const payload = {
      numero_vol: NVol.value,
      date_arrivee_vol: dateDebut.value,
      date_fin_vol: dateFin.value,
      // Envoyer les mouvements depuis les résultats affichés
      mouvements: results.value.map(r => ({
        type: r.type,
        quantite: r.quantite
      }))
    }

    const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/mouvements-vol/`, payload)
    console.log('Enregistré:', res.data)
    

    if (res.data.errors?.length > 0) {
      console.warn('Catégories manquantes:', res.data.errors)
      alert.showAlertNotif(
            "Catégories manquantes",
            "warning"
          )
    }
    alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )
        Object.assign(
          payload, {numero_vol: '', date_arrivee_vol: '', date_fin_vol: ''}, 
        )

  } catch (err) {
    console.error('Erreur enregistrement:', err)
    alert.showAlertNotif(
            "une erreur s'est produit lors de l'enregistrement",
            "error"
          )
  }
}
</script>