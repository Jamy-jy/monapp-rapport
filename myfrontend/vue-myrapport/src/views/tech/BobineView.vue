<template>
    <PageBreadcrumbTech :pageTitle="currentPageTitle"/>
    <div>
      <form @submit.prevent="submitForm" class="space-y-6">
        <ComponentCard title="Vignettes">
          <BaseEditTable
            v-model="vinette"
            :columns="columns"
            row-class-key="rowClass"
          />

          <!-- Erreurs N°fin de série -->
          <!-- APRÈS — wrapper template -->
          <div class="mt-2 space-y-1">
            <template v-for="(err, i) in finSerieErrors" :key="i">
              <p v-if="err" class="text-sm text-red-500 px-4">
                Ligne {{ i + 1 }} : {{ err }}
              </p>
            </template>
          </div>
          <div class="dark:bg-dark-900 w-full flex justify-end bg-transparent px-4 text-gray-800 outline-none dark:text-white/90">
            <label for="">Total :</label>
            <p class="ml-2">{{ totalConso }}</p>
          </div>
          <div class="flex gap-4 mt-4 justify-end">
            <SaveBtn :disabled="finSerieErrors.some(e => e !== '')"/>
          </div>
        </ComponentCard>
      </form>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import PageBreadcrumbTech from '@/components/common/PageBreadcrumbTech.vue';
import ComponentCard from '@/components/common/ComponentCard.vue';
import BaseEditTable from '@/components/table/BaseEditTable.vue';
import SaveBtn from '@/components/buttons/SaveBtn.vue';
import axios from 'axios'
import { useAlertNotifStore } from '@/stores/AlertNotif';

const currentPageTitle = ref('Etiquettes')

const alert = useAlertNotifStore()

const columns = [
  { label: "Box PAF", key: "boxPaf", type: "text", readonly: true },
  { label: "N°Bobine", key: "numberBobine", type: "text", readonly: true},
  { label: "N°Vignette", key: "numberVignette", type: "text", readonly: true },
  { label: "N° debut de série", key: "numberDebutSerie", type: "text", readonly: true },
  { label: "N° fin de série", key: "numberFinSerie", type: "text" },
  { label: "Nombre consommé", key: "nbConso", type: "number", readonly: true },
  { label: "Nombre Abimé", key: "nbAbime", type: "number" },
  { label: "Cause", key: "cause", type: "text" },
]

type VignetteRow = {
  boxPaf: string
  numberBobine: string
  numberVignette: {
    debut: string
    fin: string
  }
  numberDebutSerie: number
  numberFinSerie: number
  nbConso: number
  est_terminee : boolean
  nbAbime: number
  cause: string
  vignetteDebut: number 
  vignetteFin: number   
  rowClass?: string     
  numero_bobine?: number 
}
const vinette = ref<VignetteRow[]>([])

const fetchBobines = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/bobines/')
    
    
    vinette.value = res.data
    .map((box: any) => ({
      boxPaf: box.box_paf?.numero_boxPaf || '',   // affichage depuis serializer
      numero_bobine: box.id,
      numberBobine: `Bobine ${box.numero_bobine}`,
      // affichage intervalle
      numberVignette: `
        <div class="flex flex-col items-center leading-tight dark:bg-dark-900 w-full bg-transparent px-4 py-2.5 text-sm text-gray-800 outline-none dark:text-white/75">
          <span>${box.debut_serie}</span>
          <span>${box.fin_serie}</span>
        </div>`,        
      //gerer la couleur rendu du BoxPaf terminée
      est_terminee: box.est_terminee,

      rowClass: box.est_terminee
        ? 'bg-red-100 text-red-700 dark:bg-red-900/50'
        : '',

      numberDebutSerie: Number(box.debut_serie),
      numberFinSerie: Number(box.fin_serie),

      vignetteDebut: Number(box.debut_serie),  // borne min
      vignetteFin: Number(box.fin_serie),      // borne max
      
      nbAbime: 0,
      cause: ''
      
    }))
    
  } catch (err) {
    console.error(err)
  }
}
onMounted(() => {
    fetchBobines()
})

//calcul auto du nbConso
watch(
  vinette,
  (rows) => {
    rows.forEach((row) => {
      const debut = Number(row.numberDebutSerie) || 0
      const fin = Number(row.numberFinSerie) || 0
      const abime = Number(row.nbAbime) || 0

      const total = fin - debut - abime

      if (row.nbConso !== total) {
        row.nbConso = total >= 0 ? total : 0
      }
    })
  },
  { deep: true }
)

//affichage Total conso
const totalConso = computed(() => {
  return vinette.value
    .filter(row => !row.est_terminee)
    .reduce((sum, row) => {
      return sum + (Number(row.nbConso) || 0)
    }, 0)
})

const formatPayload = () => {
  return vinette.value.map((row: any) => {

      return {
        num_bobine: row.numero_bobine,
        num_debutVignette: Number(row.numberDebutSerie),
        num_FinVignette: Number(row.numberFinSerie),
        nb_abime: Number(row.nbAbime),
        cause: row.cause
      }
      
  })
  
}

//gestion erreur de validation par ligne
const finSerieErrors = computed(() => {
  return vinette.value.map(row => {
    const debut = Number(row.numberDebutSerie) || 0
    const fin = Number(row.numberFinSerie) || 0
    const vignetteDebut = Number(row.vignetteDebut) || 0  // début vignette
    const vignetteFin = Number(row.vignetteFin) || 0 
    if (fin > 0 && fin < debut) {
      return `Le numéro de fin de série est hors plage (trop petit) — doit être supérieur à ${debut}`
    }
     // N°début et N°fin doivent être compris dans la plage vignette
    if (debut > 0 && debut < vignetteDebut) {
      return `N° début de série (${debut}) est inférieur au début vignette (${vignetteDebut})`
    }

    if (fin > 0 && fin > vignetteFin) {
      return `N° fin de série (${fin}) dépasse la fin vignette (${vignetteFin})`
    }
    return ''
  })
})

const submitForm = async () => {
   // Vérifier s'il y a des erreurs
  const hasError = finSerieErrors.value.some(e => e !== '')
  if (hasError) return
  try {
    const payload = formatPayload()
    console.log(JSON.stringify(formatPayload(), null, 2))
    const res = await axios.post('http://localhost:8000/api/vignettes/',payload)

    console.log('Données enregistrées', res.data)
     alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )
    // N°fin serie -> N°debut serie 
    vinette.value = vinette.value.map(row => ({
      ...row,
      numberDebutSerie: row.numberFinSerie,  //  fin devient début
      nbAbime: 0,                             //  reset abimé
      cause: '',                              //  reset cause
      nbConso: 0,                             // reset conso
    }))
  } catch (err) {
    if (axios.isAxiosError(err)) {
      console.error(err.response?.data)
    } else {
      console.error(err)
     alert.showAlertNotif(
            "Une erreur s'est produit lors de l'enregistrement",
            "error"
          )
    }
  }
}

</script>