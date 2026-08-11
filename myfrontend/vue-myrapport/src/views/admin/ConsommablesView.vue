<template>
  <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />
  <div>
    <form @submit.prevent="submitForm" class="space-y-6">
      <ComponentCard title="Nouveau Consommable">
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
          
          <div>
            <PlaceholderInput
              v-model="consommable.nom_consommable"
              label="Nom Consommable"
              placeholder="Entrez le nom du consommable"
            />
            <p v-if="serverErrors.nom_consommable" class="text-red-500 text-sm mt-1">
              {{ serverErrors.nom_consommable }}
            </p>
          </div>
          <PlaceholderInput
            v-model="consommable.type_consommable"
            label="Type"
            placeholder="Ex: papier A5 pour imprimante"
          />

          <SelectInput
            v-model="consommable.mode_consommation"
            label="Mode de consommation"
            placeholder="Choisissez un mode"
            :options="modeOptions"
          />

        </div>

        <div class="flex gap-4 mt-4 justify-end">
          <SaveBtn/>
        </div>
      </ComponentCard>
    </form>
  </div>
  <div class="my-6">
    <ComponentCard title="Liste consommable">
      <BaseTable 
        :columns="columnsConso" 
        :rows="conso" 
        @edit="openEditModal"
        @delete="confirmDelete"
      />
    </ComponentCard>
  </div>

  <!-- modal modif-->
  <div
    v-if="showEditModal"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
  >
    <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
      <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
        Modifier le consommable
      </h2>

      <div class="space-y-3">
        <div>
          <PlaceholderInput
            v-model="editData.nom_consommable"
            label="Nom consommable"
            placeholder="Nom"
          />
          <p v-if="editErrors.nom_consommable" class="text-red-500 text-sm mt-1">
            {{ editErrors.nom_consommable }}
          </p>
        </div>

        <PlaceholderInput
          v-model="editData.type_consommable"
          label="Type consommable"
          placeholder="Type"
        />

        <SelectInput
          label="Mode consommation"
          :options="modeOptions"
          v-model="editData.mode_consommation"
        />
      </div>

      <div class="flex justify-end gap-3 mt-6">
        <button
          @click="showEditModal = false"
          class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          Annuler
        </button>
        <button
          @click="submitEdit"
          class="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
        >
          Enregistrer
        </button>
      </div>
    </div>
  </div>

  <!-- Modal Confirmation Suppression -->
  <div
    v-if="showDeleteModal"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
  >
    <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6 text-center">
      <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
        Confirmer la suppression
      </h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
        Voulez-vous vraiment supprimer
        <span class="font-medium text-gray-800 dark:text-white">
          {{ selectedConso?.nom_consommable }}
        </span> ?
      </p>

      <div class="flex justify-center gap-3">
        <button
          @click="showDeleteModal = false"
          class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          Annuler
        </button>
        <button
          @click="submitDelete"
          class="px-4 py-2 text-sm text-white bg-red-500 rounded-lg hover:bg-red-600"
        >
          Supprimer
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted, reactive, ref } from 'vue'
  import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue'
  import ComponentCard from '@/components/common/ComponentCard.vue'
  import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue'
  import SelectInput from '@/components/FormElement/SelectInput.vue'
  import SaveBtn from '@/components/buttons/SaveBtn.vue'
  import BaseTable from '@/components/table/BaseTable.vue'
  import ItemActions from '@/components/table/ItemActions.vue'
  import axios from 'axios'
import { useAlertNotifStore } from '@/stores/AlertNotif'

  const currentPageTitle = ref('Nouveau Consommable')

  const alert = useAlertNotifStore()

  const consommable = reactive ({
    nom_consommable: '',
    type_consommable: '',
    mode_consommation: '',
  })

  const serverErrors = reactive<Record<string, string>>({})

  interface Option{
    label: string
    value: string | number
  }

  const modeOptions: Option[] = [
    {label: "en carton", value: "carton"},
    {label: "par piéce", value: "pièce"},
    {label: "en rouleau", value: "rouleau"},
    {label: "en bouteille", value: "bouteille"}
  ]

  const submitForm = async () => {
    try {
      const res = await axios.post('http://localhost:8000/api/consommables/', consommable)
      consommable.nom_consommable = ''
      consommable.type_consommable = ''
      consommable.mode_consommation = ''

      await fetchConso()
      console.log('consommable ajouté', res.data)
      alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )
      Object.assign(
          consommable, {nom_consommable: '', type_consommable: '', mode_consommation: '',}, 
        )
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.data) {
        Object.assign(serverErrors, err.response.data)
        console.error(err.response?.data)
      } else {
        console.error(err)
        alert.showAlertNotif(
            "erreur lors de l'enregistrement",
            "error"
          )
      }
    }
  }

  const conso = ref<any[]>([])

  const columnsConso = [
    { label: 'Nom consommable', field: 'nom_consommable'},
    { label: 'Type consommable', field: 'type_consommable'},
    { label: 'mode consommation', field: 'mode_consommation'},
    { label: 'date de creation', field: 'created_at_consommation'},
    { label: 'Actions', render: ItemActions },
  ]
  
  const fetchConso = async () => {
    try {
      const resconso = await axios.get('http://localhost:8000/api/consommables/')
      conso.value = resconso.data.map((c: any) => ({
        id: c.id,
        nom_consommable: c.nom_consommable,
        type_consommable: c.type_consommable,
        mode_consommation: c.mode_consommation,
        created_at_consommation: new Date(c.created_at_consommation).toLocaleDateString()
      }))
      console.log(conso.value)
    } catch (err){
      console.log(err)
      alert.showAlertNotif(
            "Erreur lors de l'affichage",
            "error"
          )
    }
  }

  // Modal modifier
  const showEditModal = ref(false)
  const selectedConsoId = ref<number | null>(null)

  const editData = reactive({
    nom_consommable: '',
    type_consommable: '',
    mode_consommation: '',
  })

  const editErrors = reactive<Record<string, string>>({})

  const openEditModal = (row: any) => {
    selectedConsoId.value = row.id
    editData.nom_consommable = row.nom_consommable
    editData.type_consommable = row.type_consommable
    editData.mode_consommation = row.mode_consommation
    Object.keys(editErrors).forEach(k => delete editErrors[k])
    showEditModal.value = true
  }

  const submitEdit = async () => {
    if (!selectedConsoId.value) return
    Object.keys(editErrors).forEach(k => delete editErrors[k])

    try {
      await axios.patch(`http://localhost:8000/api/consommables/${selectedConsoId.value}/`, editData)
      showEditModal.value = false
      await fetchConso()
      alert.showAlertNotif(
            "Modification effectué avec succès",
            "success"
          )
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.data) {
        Object.assign(editErrors, err.response.data)
      } else {
        alert.showAlertNotif(
            "Erreur lors de la modification",
            "error"
          )
      }
    }
  }

  // Modal suppression
  const showDeleteModal = ref(false)
  const selectedConso = ref<any | null>(null)

  const confirmDelete = (row: any) => {
    selectedConso.value = row
    showDeleteModal.value = true
  }

  const submitDelete = async () => {
    if (!selectedConso.value) return

    try {
      await axios.delete(
        `http://localhost:8000/api/consommables/${selectedConso.value.id}/`
      )
      showDeleteModal.value = false
      await fetchConso()
      alert.showAlertNotif(
            `Le ${selectedConso.value.nom_consommable} a été supprimé avec succès`,
            "success"
          )
    } catch (err) {
      console.error(err)
      alert.showAlertNotif(
            "Erreur lors de la suppression",
            "error"
          )
    }
  }

  onMounted (() => {
    fetchConso()
  })

</script>



