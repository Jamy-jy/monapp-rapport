<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle"/>
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
        <SelectInput
            label="groupe"
            placeholder="choisissez le groupe"
            :options="groupOptions"
            v-model="formData.group"
        />
        <PlaceholderInput
            v-model="dateDebut"
            type="datetime-local"
            label="du"
            placeholder=""
        />
        <PlaceholderInput
            v-model="dateFin"
            type="datetime-local"
            label="à"
            placeholder=""
        />
        <button class="h-11 mt-6.5 flex gap-2 justify-center rounded-lg bg-brand-100 text-brand-600 px-4 py-2.5 text-sm font-medium hover:bg-brand-200 focus:outline-none focus:ring-2 focus:ring-brand-900 focus:ring-offset-1 dark:focus:ring-offset-dark-900 dark:bg-brand-950 dark:text-brand-400 dark:hover:bg-brand-999"
            @click="handelClick"
            >
            <ListIcon/>
                  Afficher
        </button>
    </div>
    <div v-if="loadingHistorique" class="text-center text-gray-500 py-6">
        Chargement...
    </div>
    
    <div v-else-if="hasSearched && historiqueList.length === 0" class="text-center text-gray-500 py-6">
        Aucun résultat pour cette période et ce groupe.
    </div>
    
    <ComponentCard 
        v-else-if="historiqueList.length > 0"
        :title="selectedGroupLabel" 
        class="mt-4"
        textClick="Export PDF"
        @clickText="exportPdf"
        :icon="ExportFileIcon"
    >
        <BaseTable
            :columns="columnsHistorique"
            :rows="historiqueList"
        />
    </ComponentCard>
</template>
<script setup lang="ts">
import { ref, reactive, onMounted, h, computed } from 'vue'
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
import SelectInput from '@/components/FormElement/SelectInput.vue';
import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
import ListIcon from '@/icons/ListIcon.vue';
import axios from 'axios';
import BaseTable from '@/components/table/BaseTable.vue';
import ComponentCard from '@/components/common/ComponentCard.vue';
import ExportFileIcon from '@/icons/ExportFileIcon.vue';
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import API_CONFIG from '@/config/api';

const currentPageTitle = ref('Historique inventaire')

interface Option{
  label: string
  value: string | number
  raw: any
}

const groupOptions = ref<Option[]>([])

const dateDebut = ref('')
const dateFin = ref('')

// --- Résultats du tableau ---
const historiqueList = ref<any[]>([])
const loadingHistorique = ref(false)
const hasSearched = ref(false)

const formData = reactive({
    group: '',
})

const fetchGroup = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/inventaire/`)

    groupOptions.value = res.data.map((g: any) => ({
      label: g.nom_group,  // ce que tu veux afficher
      value: g.id,               // ce que tu envoies au backend
      raw : g 
    }))

  } catch (err) {
    console.error(err)
  }

}

const selectedGroupLabel = computed(() => {
  const selected = groupOptions.value.find(
    (opt) => String(opt.value) === String(formData.group)
  )
  return selected ? selected.label : ''
})

// --- Colonnes du tableau d'historique ---
const columnsHistorique = [
  { label: 'Nom matériel', field: 'nom_materiel', width: '18%' },
  { label: 'Marque', field: 'marque_materiel', width: '15%' },
  { label: 'Numéro série', field: 'numero_serie', width: '15%' },
  { label: 'Configuration', field: 'configuration', width: '17%' },
  {
    label: 'Date',
    width: '15%',
    renderFn: (row: any) =>
      h('span', { class: 'text-sm text-gray-500' },
        new Date(row.composant_created_at).toLocaleString()
      ),
  },
  {
    label: 'État',
    width: '10%',
    renderFn: (row: any) =>
      h(
        'span',
        {
          class: row.Etat_materiel
            ? 'px-2 py-1 text-xs rounded-full bg-green-100 text-green-700'
            : 'px-2 py-1 text-xs rounded-full bg-red-100 text-red-700',
        },
        row.Etat_materiel ? 'Fonctionnel' : 'Non fonctionnel'
      ),
  },
]

// --- Recherche ---
const handelClick = async () => {
  if (!formData.group) {
    console.warn('Veuillez sélectionner un groupe.')
    return
  }

  loadingHistorique.value = true
  hasSearched.value = true

  try {
    const params: Record<string, string> = {
      group: String(formData.group),
      historique: 'true',
    }

    if (dateDebut.value) {
      params.date_debut = new Date(dateDebut.value).toISOString()
    }
    if (dateFin.value) {
      params.date_fin = new Date(dateFin.value).toISOString()
    }

    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/composant-group/`, { params })
    historiqueList.value = res.data
  } catch (err) {
    console.error(err)
    historiqueList.value = []
  } finally {
    loadingHistorique.value = false
  }
}

onMounted(() => {
  fetchGroup()
})


const exportPdf = () => {
  if (!historiqueList.value.length) return

  const doc = new jsPDF()

  //En-tête — dates sans heure
  const formatDate = (dateStr: string) => {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: '2-digit', month: '2-digit', year: 'numeric'
    })
  }

  const titre = `Inventaire du ${formatDate(dateDebut.value)} au ${formatDate(dateFin.value)}`
  const sousTitre = selectedGroupLabel.value  // ← nom du groupe affiché dans ComponentCard

  // Titre principal
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text(titre, 14, 20)

  // Sous-titre groupe
  doc.setFontSize(11)
  doc.setFont('helvetica', 'normal')
  doc.text(sousTitre, 14, 30)

  // Colonnes depuis columnsHistorique
  const colonnes = [
  { header: 'Nom matériel', dataKey: 'nom_materiel' },
  { header: 'Marque', dataKey: 'marque_materiel' },
  { header: 'Numéro série', dataKey: 'numero_serie' },
  { header: 'Configuration', dataKey: 'configuration' },
  { header: 'Date', dataKey: 'date' },
  { header: 'État', dataKey: 'etat' },
]

  // Lignes depuis historiqueList
 const lignes = historiqueList.value.map((row: any) => ({
    nom_materiel: row.nom_materiel,
    marque_materiel: row.marque_materiel,
    numero_serie: row.numero_serie,
    configuration: row.configuration,

    date: new Date(
      row.composant_created_at
    ).toLocaleDateString('fr-FR'),

    etat: row.Etat_materiel
      ? 'Fonctionnel'
      : 'Non fonctionnel',
  }))

  // Tableau
  autoTable(doc, {
    startY: 38,
    columns: colonnes,
    body: lignes,
    styles: {
      fontSize: 9,
      cellPadding: 3,

       // Bordures des cellules
      lineColor: [0, 0, 0], 
      lineWidth: 0.7,   
    },
    headStyles: {
      fillColor:  [245, 199, 126], 
      textColor: [0, 0, 0],
      fontStyle: 'bold',

      lineColor: [0, 0, 0],
      lineWidth: 0.7,
    },

     bodyStyles: {
      textColor: [0, 0, 0],
      fontStyle: 'bold',
      lineColor: [0, 0, 0],
      lineWidth: 0.7,
    },

    tableLineColor: [0, 0, 0],
    tableLineWidth: 0.7,

    alternateRowStyles: {
      fillColor: [245, 247, 255],
    },
  })

  // Télécharger
  doc.save(`inventaire_${formatDate(dateDebut.value)}_${formatDate(dateFin.value)}.pdf`)
}

</script>