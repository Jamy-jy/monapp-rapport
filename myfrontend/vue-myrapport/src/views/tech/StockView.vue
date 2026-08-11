<template>
    <PageBreadcrumbTech :pageTitle ="currentPageTitle"/>
    <!-- Bandeau envois en attente -->
    <div v-if="envoisEnAttente.length > 0" class="space-y-3 mb-6">
      <div
        v-for="envoi in envoisEnAttente"
        :key="envoi.id"
        class="flex items-center justify-between p-4 rounded-xl border border-orange-200 bg-orange-50 dark:border-orange-700 dark:bg-orange-900/20"
      >
        <div class="flex items-center gap-3">
          <div class="flex items-center justify-center w-9 h-9 rounded-full bg-orange-100 dark:bg-orange-900/40 shrink-0">
            <svg class="w-5 h-5 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-orange-800 dark:text-orange-200">
              On vous a envoyé
              <span class="font-bold ml-2">{{ envoi.qte_envoye }}</span>
              <span class="font-bold ml-2">{{ envoi.nom_consommable }}</span>
            </p>
            <p class="text-xs text-orange-600 dark:text-orange-400 mt-0.5">
              De : {{ envoi.envoye_par }} - {{ envoi.date }}
            </p>
          </div>
        </div>

        <div class="flex gap-2 shrink-0">
          <!-- <button
            @click="traiterEnvoi(envoi.id, 'refuse')"
            class="px-3 py-1.5 text-xs font-medium text-red-600 border border-red-300 rounded-lg hover:bg-red-50 dark:border-red-700 dark:hover:bg-red-900/20 transition"
          >
            Refuser
          </button> -->
          <button
            @click="traiterEnvoi(envoi.id, 'valide')"
            class="px-6 py-1.5 text-xs font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 transition"
          >
            reçu
          </button>
        </div>
      </div>
    </div>
    <div>
      <form @submit.prevent="submitForm" class="space-y-6">
        <ComponentCard title="Stock">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-5">
            <SelectInput
              label="consommable"
              placeholder="choisissez le consommable"
              :options="stockOptions"
              v-model="formData.consommable"
            />
            
            <PlaceholderInput
              v-model="stock.qte_entree"
              type="number"
              label="Entrée :"
              placeholder=""
            />
            <PlaceholderInput
              v-model="stock.qte_sortie"
              type="number"
              label="Sortie :"
              placeholder=""
            />
            <PlaceholderInput
              v-model="stock.qte_restant"
              type="number"
              label="Reste :"
              placeholder=""
            />
            <ValideBtn class="mt-6.5"/>
          </div>
          <span v-if="loadingStock" class="text-sm text-gray-500">
              Chargement...
          </span>
        </ComponentCard>
      </form>
    </div>
    <div v-if="showBobineModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="relative bg-white dark:bg-gray-900 p-6 rounded-xl w-[800px] shadow-2xl border dark:border-gray-dark">

        <button
          @click="closeModal"
          class="absolute top-3 right-3 text-gray-500 hover:text-gray-800 dark:hover:text-white text-xl"
        >
          &times;
        </button>
        <h2 class="text-base font-medium text-gray-800 dark:text-white/90 mb-4">
          Ajout de {{ nbBobinesToCreate }} bobine(s)
        </h2>

        <div v-for="(b, i) in bobines" :key="i" class="grid grid-cols-1 gap-4 sm:grid-cols-4">
          <PlaceholderInput v-model="b.numero_bobine" placeholder="Numéro bobine" label="Numéro bobine" />
          <PlaceholderInput v-model="b.debut_serie" placeholder="Début série" label="N° debut Vignette"/>
          <PlaceholderInput v-model="b.fin_serie" placeholder="Fin série" label="N° fin vignette"/>
          <SelectInput 
            label="Box Paf"
            placeholder="choississez le Box Paf" 
            :options="boxPafOptions" 
            v-model="b.box_paf" 
          />
        </div>
        <div @click="submitBobines" class="flex justify-end mt-2 ">
          <SaveBtn />
        </div>
      </div>
    </div>
</template>
<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue';
import ComponentCard from '@/components/common/ComponentCard.vue';
import PageBreadcrumbTech from '@/components/common/PageBreadcrumbTech.vue';
import ValideBtn from '@/components/buttons/ValideBtn.vue';
import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
import SelectInput from '@/components/FormElement/SelectInput.vue';
import axios from 'axios';
import SaveBtn from '@/components/buttons/SaveBtn.vue';
import { useAlertNotifStore } from '@/stores/AlertNotif';

const currentPageTitle = ref('Stock')
const alert = useAlertNotifStore()

interface Option{
  label: string
  value: string | number
  raw: any
}

const stockOptions = ref<Option[]>([])

//affichage consommable dans select
const fetchConsommable = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/consommables/')

    stockOptions.value = res.data.map((c: any) => ({
      label: c.nom_consommable,  // ce que tu veux afficher
      value: c.id,               // ce que tu envoies au backend
      raw : c 
    }))

  } catch (err) {
    console.error(err)
  }

}
onMounted(() => {
  fetchConsommable()
})

const stock = reactive({
  qte_entree: 0,
  qte_sortie: 0,
  qte_restant: 0
})

const formData = reactive({
    consommable: '',
})

const loadingStock = ref(false)

const qteInitial = ref(0)

//affichage stock dans le champs avec entre et sortie initialisé
watch(() => formData.consommable, async (newVal) => {
  if (!newVal) return

  loadingStock.value = true

  try {
    const [res] = await Promise.all([
      axios.get(`http://localhost:8000/api/stock/last/${newVal}/`),

      // delai
      new Promise(resolve => setTimeout(resolve, 1000))
    ])

    // reset inputs
    stock.qte_entree = 0
    stock.qte_sortie = 0

    qteInitial.value = res.data.qte_restant
    stock.qte_restant = qteInitial.value

  } catch (err) {
    console.error(err)
  } finally {
    loadingStock.value = false
  }
})
//déclanchement modal
const showBobineModal = ref(false)
const nbBobinesToCreate = ref(0)

const initialized = ref(false)

onMounted(async () => {
  await fetchConsommable()
  initialized.value = true
})

//choix etiquette consommable + valeur sortie
const lastSortie = ref(0)
watch(
  () => [formData.consommable, stock.qte_sortie],
  ([consommableId, sortie]) => {

    if (!formData.consommable) return

    const found = stockOptions.value.find(
      o => Number(o.value) === Number(consommableId)
    )
    
    if (!found) return

    const qty = Number(sortie)
    
    console.log('CHECK:', {
    type: found.raw.type_consommable,
    sortie,
    condition: found.raw.type_consommable === 'Bobine' && Number(sortie) > 0
  })

   if (
      found.raw.type_consommable === 'Bobine' &&
      qty > 0 &&
      !showBobineModal.value
    ) {
      nbBobinesToCreate.value = qty
      showBobineModal.value = true
    }

    if (!initialized.value) return
  }
)


interface BobineForm {
  numero_bobine: string
  debut_serie: string
  fin_serie: string
  box_paf: number 
}

watch(nbBobinesToCreate, (n) => {
  bobines.value = Array.from({ length: n }, () => ({
    numero_bobine: '',
    debut_serie: '',
    fin_serie: '',
    box_paf: 0
  }))
})
//fetch box paf select option 
const boxPafOptions = ref<Option[]>([])

const fetchBoxPaf = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/boxpaf/')

    boxPafOptions.value = res.data.map((b: any) => ({
      label: b.numero_boxPaf,
      value: b.id,
      raw: b
    }))
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  fetchConsommable()
  fetchBoxPaf()
})

//auto calcule de numéro de serie
const generateSeries = (numero: number) => {
  const base = 261001623501 ;
  const bobineReference = 2248;
  const nbrVignette = 500;

  const start = base + ((numero - bobineReference) * nbrVignette)
  const end = start + (nbrVignette -1)

  return {
    debut: start.toString(),
    fin: end.toString()
  }
}

const bobines = ref<BobineForm[]>([])

watch(
  bobines,
  (list) => {
    list.forEach((b) => {
      if (b.numero_bobine.length === 4) {
        const num = Number(b.numero_bobine)
        const { debut, fin } = generateSeries(num)

        b.debut_serie = debut
        b.fin_serie = fin
      }
    })
  },
  { deep: true }
)
//auto calcule restant sortie
watch(
  () => [stock.qte_entree, stock.qte_sortie],
  ([entree, sortie]) => {
    stock.qte_restant =
      qteInitial.value + (Number(entree) - Number(sortie))
  }
)

const submitForm = async () => {

    const playload = {
    ... stock,
    ... formData,
}
    try {
      const res = await axios.post('http://localhost:8000/api/stock/', playload )
      console.log('stock enregistré', res.data)
      Object.assign(
      stock, {qte_entree: 0, qte_sortie: 0, qte_restant: 0},
      formData, {consommable: '',}
    )
     alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )
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

  const submitBobines = async () => {
  try {
    await axios.post('http://localhost:8000/api/bobines/createBobine/', {
        bobines: bobines.value.map(b => ({
          consommable: formData.consommable,
          numero_bobine: b.numero_bobine,
          debut_serie: Number(b.debut_serie),
          fin_serie: Number(b.fin_serie),
          box_paf_id: b.box_paf
        }))
      }
    )
    
    alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )

    showBobineModal.value = false

  } catch (err) {
    if (axios.isAxiosError(err)) {
    console.log('STATUS:', err.response?.status)
    console.log('DATA:', err.response?.data)
    } else {
      alert.showAlertNotif(
              "Une erreur s'est produit lors de l'enregistrement",
              "error"
            )

      console.log('PAYLOAD:', bobines.value)
    } 
  }
}

const closeModal = () => {
  showBobineModal.value = false
  stock.qte_sortie = 0
}

// Validation ou refus de consommable envoyé
interface EnvoiAttente {
  id:              number
  nom_consommable: string
  qte_envoye:      number
  envoye_par:      string
  date:            string
}
const envoisEnAttente = ref<EnvoiAttente[]>([])

const traiterEnvoi = async (id: number, action: 'valide' | 'refuse') => {
  try {
    const url = action === 'valide'
      ? `http://localhost:8000/api/transfert-stock/${id}/valider/`
      : `http://localhost:8000/api/transfert-stock/${id}/refuser/`

    const res = await axios.post(url)  
    console.log(res.data.message)

    // Retirer de la liste après traitement
    envoisEnAttente.value = envoisEnAttente.value.filter(e => e.id !== id)

    // Notification selon l'action
    if (action === 'valide') {
      alert.showAlertNotif(
        "Validation avec succès, consommable bien reçu", 
        "success"
      )
    } else {
      alert.showAlertNotif(
        "Le consommable a été refusé", 
        "error"
      )
    }

  } catch (err) {
    if (axios.isAxiosError(err)) {
      console.error('Erreur:', err.response?.data)
    }
  }
}

const fetchEnvoisEnAttente = async () => {
  try {
    // Adapter selon ton endpoint réel
    const res = await axios.get('http://localhost:8000/api/transfert-stock/en-attente/')
    envoisEnAttente.value = res.data.map((t: any) => ({
      id:              t.id,
      nom_consommable: t.consommable_nom,           
      qte_envoye:      t.quantite,                  
      envoye_par:      'Admin',               
      date:            new Date(t.date_envoi).toLocaleString('fr-FR', {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
      }),
    }))
  } catch (err) {
    console.error('Erreur chargement transferts:', err)
  }
}

onMounted(() => {
  fetchEnvoisEnAttente()
})
</script>