<template>
    <PageBreadcrumbTech :pageTitle="currentPageTitle"/>

    <!-- Bandeau d'alerte -->
    <div
      v-if="showBandeau"
      class="bg-red-50 border border-red-200 text-red-800 rounded-lg px-4 py-3 mb-4 flex items-start justify-between dark:bg-red-900/20 dark:border-red-800 dark:text-red-300"
    >
      <div>
        <p class="font-medium mb-1">
          N'oublier pas de mettre dans le rapport que 
          "{{ alertesMateriel.length }}  matériel(s)" est siganlé non fonctionnel, cela nécessitent un remplacement
        </p>
        <ul class="text-sm space-y-1">
          <li v-for="a in alertesMateriel" :key="a.id">
            <span>
              <strong>{{ a.nom_materiel }}</strong> (N/S: {{ a.numero_serie }}) — groupe
              <strong>{{ a.nom_group }}</strong>
              — constaté le {{ new Date(a.date_constat).toLocaleDateString() }}
            </span>
            <button
              @click="openRemplacementModal(a)"
              class="px-3 py-1 ml-2 text-xs text-white bg-orange-500 rounded-lg hover:bg-orange-600 whitespace-nowrap"
            >
              Remplacer
            </button>
          </li>
        </ul>
      </div>
      <button
        @click="showBandeau = false"
        class="text-red-400 hover:text-red-600 text-lg leading-none"
      >
        &times;
      </button>
    </div>

    <div class="grid grid-cols-12 gap-4 md:gap-6">
      <div class="col-span-12 space-y-6 xl:col-span-7">
        <IntervalDate 
          v-model="intervalData"
          @submit="handleSubmit"
        />
        <Entete
          v-model:destinataire="destinataire"
          v-model:cc="cc"
          v-model:cci="cci"
          v-model:objet="objet"
        />
      </div>
      <div class="col-span-12 xl:col-span-5">
        <Jointzone @update:files="files = $event"/>
      </div>
      <div class="col-span-12 flex items-center gap-4 xl:col-span-7">
          <p
           class="text-sm font-medium text-gray-700 cursor-pointer select-none dark:text-gray-400"
           >Modèle: 
          </p>
        <div class="flex-1">
          <InputgroupSelect
              v-model="selectedModele"
              :options="modeles"
              redirectTo="/modeles/create"
           />
        </div>
      </div>
      <div class="col-span-12">
        <TextareMail v-model="message"/>
      </div>
    </div>
    <div class="my-2 flex justify-end">
      <SendBtn @click="sendEmail"/>
    </div>


    <!-- Modal de remplacement  -->
    <div v-if="showModalRemplacement" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/50">
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
          nouveau : {{ materielARemplacer?.nom_materiel }}
        </h2>
         <div class="space-y-3">
          <PlaceholderInput v-model="nouveauMateriel.nom_materiel" label="Nom nouveau matériel" placeholder="Nom" />
          <PlaceholderInput v-model="nouveauMateriel.marque_materiel" label="Marque" placeholder="Marque" />
          <PlaceholderInput v-model="nouveauMateriel.numero_serie" label="Numéro série" placeholder="Numéro de série" />
          <PlaceholderInput v-model="nouveauMateriel.configuration" label="Configuration" placeholder="Configuration" />
          <div>
            <label class="text-sm text-gray-500 block mb-1">Date de remplacement</label>
            <input
              type="date"
              v-model="nouveauMateriel.date_remplacement"
              class="w-full rounded-lg border border-gray-300 dark:border-gray-700 dark:bg-gray-800 dark:text-white p-2 text-sm"
            />
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button @click="showModalRemplacement = false" class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50">
            Annuler
          </button>
          <button @click="submitRemplacement" class="px-4 py-2 text-sm text-white bg-orange-500 rounded-lg hover:bg-orange-600">
            Confirmer le remplacement
          </button>
        </div>
      </div>
    </div>
</template>
<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue';
import SendBtn from '@/components/buttons/SendBtn.vue';
import PageBreadcrumbTech from '@/components/common/PageBreadcrumbTech.vue';
import Jointzone from '@/components/FormElement/Jointzone.vue';
import Entete from '@/components/space/Entete.vue';
import TextareMail from '@/components/space/TextareMail.vue';
import IntervalDate from '@/components/space/IntervalDate.vue';
import InputgroupSelect from '@/components/FormElement/InputgroupSelect.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useAlertNotifStore } from '@/stores/AlertNotif';
import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
import API_CONFIG from '@/config/api';

const currentPageTitle = ref('Rapport')
const message = ref('')           // contenu textarea
const files = ref<File[]>([])     //piece joint

const alert = useAlertNotifStore()
const destinataire = ref<string[]>([])
const cc = ref('')
const cci = ref('')
const objet = ref('')

const intervalData = ref({
  table: '',
  dateDebut: '',
  dateFin: ''
})

const handleSubmit = async (data: {
  table: string,
  dateDebut: string,
  dateFin: string
}) => {
  console.log('RECEIVED DATA:', data)
  //pour l'export de consommable
  if (data.table === 'stock') {
    await exportStock(data)
  }
  // pour l'export de mouvement de vol
  if (data.table === 'vol') {
    await exportVol(data)
  }

}

interface Option{
  label: string
  value: string | number
  text: string
  raw: any
}

const selectedModele = ref('')

//stockage des données brute complète séparement pour l'afficher dans le texte email
/* const modelesRaw = ref<any[]>([]) */
//stockage de modèl partiel pour l'affichage option select
const modeles = ref<Option[]>([])

//affichage consommable dans select
const fetchModeles = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/text-model/list/`)
    //Transformer en format Option { label, value }
    modeles.value = res.data.map((m: any) => ({
      label: m.text,
      value: m.id,
      text: m.text
    }))
  } catch (err) {
    console.error('Erreur chargement modèles:', err)
  }
}


//emporté dans la tesxt email   -> suivi de la chargement d'incident
watch(selectedModele, async (newVal) => {
    console.log('selected:', newVal)
    const modele = modeles.value.find(
      (m) => String(m.value) === String(newVal)
    )
    
    console.log('modele trouvé:', modele)
    if (modele) {
      message.value = modele.text  // texte complet dans TextareMail
      await fetchDernierIncident() // puis incident en dessous
      await fetchAlertesRapport()  //texte alerte consommable

    } else {
      message.value = ''
      dernierIncidentId.value = []
    }
  })

onMounted(() => {
  fetchModeles()
})

const exportStock = async (data: {
  dateDebut: string,
  dateFin: string
}) => {
  try {

    // Récupérer le token depuis sessionStorage
    const token = sessionStorage.getItem('token')

    const response = await fetch(
      `${API_CONFIG.LOCAL.BASE_URL}/api/export/vol/?dateDebut=${data.dateDebut}&dateFin=${data.dateFin}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`  // ajout de token
        }
      }
    )

    //verification que la reponse envoi bien un fichier ecxel
    const contentType = response.headers.get('content-type')
    if (!response.ok || !contentType?.includes('spreadsheetml')) {
      console.error('Réponse invalide:', response.status, contentType)
      return
    }
    
    const blob = await response.blob()

    const url = window.URL.createObjectURL(blob)

    const a = document.createElement('a')
    a.href = url
    a.download = 'export_stock.xlsx'
    a.click()

    

    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error(error)
  }
  
}

const exportVol = async (data: {
  dateDebut: string,
  dateFin: string
}) => {
  try {
    const token = sessionStorage.getItem('token')
    const response = await fetch(
      `${API_CONFIG.LOCAL.BASE_URL}/api/export/vol/?dateDebut=${data.dateDebut}&dateFin=${data.dateFin}&table=vol`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )

    const contentType = response.headers.get('content-type')
    if (!response.ok || !contentType?.includes('spreadsheetml')) {
      console.error('Réponse invalide:', response.status, contentType)
      return
    }

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'export_vol.xlsx'
    a.click()
    window.URL.revokeObjectURL(url)

  } catch (error) {
    console.error(error)
  }
}

const loadDefaultEmail = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/emails_destinataire/`)

    if (res.data.length > 0) {
      destinataire.value = res.data.map((item: any) => item.emails_destiny)
    }
  } catch (err) {
    console.error("erreur chargement email:", err)
  }
}
const route = useRoute()
//pré- remplire le champ email
onMounted(() => {
  loadDefaultEmail()

  if (route.query.replyTo) {
    // Remplacer les destinataires par l'expéditeur de l'email original
    destinataire.value = [route.query.replyTo as string]
  }

  if (route.query.objet) {
    objet.value = route.query.objet as string
  }
})

//recuperation incident aujourd'hui
const dernierIncidentId = ref<number[]>([])

const fetchDernierIncident = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/incidents-survenus/dernier/`)
    const incident = res.data.incident

    if (!incident || incident.length === 0) return

    // Ne pas afficher si déjà affiché/envoyé
    //if (dernierIncidentId.value === incident.id) return

    // Filtrer ceux déjà affichés
    const nouveaux = incident.filter(
      (i: any) => !dernierIncidentId.value.includes(i.id)
    )

    if (nouveaux.length === 0) return

    // Construire le texte incident — 2 lignes en dessous du modèle
    const lignes = nouveaux.map((i: any) => [
      `Incident : ${i.nom_incident} (${i.type})`,
      `Description : ${i.description_incident || 'Pas de description'}`,
      `Solution : ${i.solutionPrise || 'Non renseignée'}`,
    ].join('\n'))

    // Ajouter en dessous du texte modèle existant
    message.value = (message.value || '') + '\n\n' + lignes.join('\n\n')

    // Mémoriser les IDs affichés
    dernierIncidentId.value = [
      ...dernierIncidentId.value,
      ...nouveaux.map((i: any) => i.id)
    ]

  } catch (err) {
    console.error('Erreur dernier incident:', err)
  }
}

//affichage text d'alert consommable
const fetchAlertesRapport = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/stock/alertes-rapport/`)
    const alertes = res.data.alertes

    if (!alertes || alertes.length === 0) return

    // Construire le bloc alertes
    const lignesAlertes = alertes.map((a: any) => a.message)

    // Ajouter après les incidents
    message.value = (message.value || '') + '\n\n' + lignesAlertes.join('\n')

  } catch (err) {
    console.error('Erreur alertes stock:', err)
  }
}


const sendEmail = async () => {
  try {
    const formData = new FormData()

    // champs texte
    formData.append('objet', objet.value)
    formData.append('message', message.value)

    //récupéré la date_debut et fin pour un traçabilité de rapportJournallier
    formData.append('date_debut', intervalData.value.dateDebut)
    formData.append('date_fin', intervalData.value.dateFin)

    // tableaux emails
    destinataire.value.forEach(email => {
      formData.append('destinataire[]', email)
    })

    if (cc.value) formData.append('cc', cc.value)
    if (cci.value) formData.append('cci', cci.value)

    // fichiers
    files.value.forEach(file => {
      formData.append('files', file)
    })

    //re-fetch chaque fichier depuis son dowloadUrl
    for (const file of files.value) {
      const downloadUrl = (file as any).downloadUrl

      if (downloadUrl) {
        const response = await fetch(downloadUrl)
        const blob = await response.blob()
        const realFile = new File([blob], file.name, {type: file.type})
        formData.append('file', realFile)
      } else {
        //fichier pas encore uploadé par Dropzone
        formData.append('files', file)
      }
    }
    const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/send-email/`,formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    console.log('Email envoyé ', res.data)
    Object.assign(
      formData, {objet: '', message: '', intervalData: '', destinataire: '', files: '',}
    )
     alert.showAlertNotif(
            "Email bien envoyé",
            "success"
          )

  } catch (error) {
    console.error('Erreur envoi ', error)
    alert.showAlertNotif(
            "Erreur! Email non envoyé",
            "error"
          )
  }
  console.log(files.value)
}

// --- État du bandeau ---
const alertesMateriel = ref<any[]>([])
const showBandeau = ref(false)

const fetchAlertesMateriel = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/composant-group/alertes/`)
    alertesMateriel.value = res.data
    showBandeau.value = alertesMateriel.value.length > 0
  } catch (err) {
    console.log(err)
  }
}

// --------- remplacement modal -------------------
const showModalRemplacement = ref(false)
const materielARemplacer = ref<any | null>(null)
const nouveauMateriel = reactive({
  nom_materiel: '',
  marque_materiel: '',
  numero_serie: '',
  configuration: '',
  date_remplacement: new Date().toISOString().slice(0, 10),
})

// const remplacementErrors = reactive<Record<string, string>>({
//   marque_materiel: '',
//   numero_serie: '',
//   configuration: '',
// })



const openRemplacementModal = (materiel: any) => {
  materielARemplacer.value = materiel
  nouveauMateriel.nom_materiel = materiel.nom_materiel
  nouveauMateriel.marque_materiel = ''
  nouveauMateriel.numero_serie = ''
  nouveauMateriel.configuration = ''
  nouveauMateriel.date_remplacement = new Date().toISOString().slice(0, 10)
  showModalRemplacement.value = true
}

const submitRemplacement = async () => {
  if (!materielARemplacer.value) return

  try {
    await axios.post(
      `${API_CONFIG.LOCAL.BASE_URL}/api/composant-group/${materielARemplacer.value.id}/remplacer/`,
      {
        ...nouveauMateriel,
        date_remplacement: new Date(nouveauMateriel.date_remplacement).toISOString(),
      }
    )

    showModalRemplacement.value = false
    materielARemplacer.value = null

    // Rafraîchir le bandeau (le matériel remplacé disparaît automatiquement)
    await fetchAlertesMateriel()
  } catch (err) {
    console.log(err)
  }
}

onMounted(() => {
  fetchAlertesMateriel()
})
</script>
