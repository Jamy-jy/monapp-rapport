<template>
  <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />
    <div>
      <form @submit.prevent="submitForm" class="space-y-6">
        <ComponentCard title="Nouvel sejour ou spécification particulière">
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div>
                <PlaceholderInput
                  v-model="visa.libelle"
                  label="libelle"
                  placeholder="Entrez l'apellation complet"
                />
                <p v-if="serverErrors.libelle" class="text-red-500 text-sm mt-1">
                    {{ serverErrors.libelle }}
                </p>
            </div>
            <div>
              <PlaceholderInput
                v-model="visa.typeVisa"
                label="type visa"
                placeholder="Entrez le jour ou une abreviation"
              />
              <p v-if="serverErrors.typeVisa" class="text-red-500 text-sm mt-1">
                {{ serverErrors.typeVisa }}
              </p>
            </div>
          </div>
           <div class="flex gap-4 mt-4 justify-end">
              <SaveBtn/>
            </div>
        </ComponentCard>
      </form>
    </div>
    <div class="my-6">
      <ComponentCard title="Liste visa">
        <BaseTable 
          :columns="columnsVisa" 
          :rows="e" 
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
        Modification
      </h2>

      <div class="space-y-3">
        <div>
          <PlaceholderInput
            v-model="editData.libelle"
            label="libelle "
            placeholder="libelle"
          />
          <p v-if="editErrors.libelle" class="text-red-500 text-sm mt-1">
            {{ editErrors.libelle }}
          </p>
        </div>

        <PlaceholderInput
            v-model="editData.typeVisa"
            label="type visa"
            placeholder="visa"
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
          {{ selectedVisa?.libelle}}
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
import { ref, reactive, onMounted } from 'vue'
import ComponentCard from '@/components/common/ComponentCard.vue';
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
import SaveBtn from '@/components/buttons/SaveBtn.vue';
import BaseTable from '@/components/table/BaseTable.vue';
import axios from 'axios';
import ItemActions from '@/components/table/ItemActions.vue';
import { useAlertNotifStore } from '@/stores/AlertNotif';
import API_CONFIG from '@/config/api';

const currentPageTitle = ref('Ajout de Categorie')
const alert = useAlertNotifStore()

const visa = reactive({
  libelle: '',
  typeVisa: '',
})

const serverErrors = reactive<Record<string, string>>({})

const submitForm = async () => {
  try {
      const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/sejour_visa/`, visa )
      visa.libelle = ''
      visa.typeVisa = ''

      await fetchVisa()
      console.log('visa ajouté', res.data)
      alert.showAlertNotif(
            "Enregistrement effectué avec success",
            "success"
          )
      Object.assign(
      visa, {libelle: '',typeVisa: '',}, 
    )
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.data) {
        Object.assign(serverErrors, err.response.data)
        console.error(err.response?.data)
      } else {
        console.error(err)
        alert.showAlertNotif(
            "une s'est produit lors de l'affichage",
            "error"
          )
      }
    }
}

const e = ref<any[]>([])

const columnsVisa = [
  { label: 'libelle', field: 'libelle'},
  { label: 'visa', field: 'visa'},
  { label: 'Actions', render: ItemActions}
]

const fetchVisa = async () => {
  try {
    const resvisa = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/sejour_visa/`)
    e.value = resvisa.data.map((v: any) => ({
    id: v.id,
    libelle: v.libelle,
    visa: v.typeVisa,
  }))
  console.log(e.value)
  } catch (err){
    console.log(err)
    alert.showAlertNotif(
            "une s'est produit lors de l'affichage",
            "error"
          )
  }

}

// Modal modifier
  const showEditModal = ref(false)
  const selectedVisaId = ref<number | null>(null)

  const editData = reactive({
    libelle: '',
    typeVisa: '',
  })

  const editErrors = reactive<Record<string, string>>({})

  const openEditModal = (row: any) => {
    selectedVisaId.value = row.id
    editData.libelle = row.libelle,
    editData.typeVisa = row.visa,
   
    Object.keys(editErrors).forEach(k => delete editErrors[k])
    showEditModal.value = true
  }

  const submitEdit = async () => {
    if (!selectedVisaId.value) return
    Object.keys(editErrors).forEach(k => delete editErrors[k])

    try {
      await axios.patch(`${API_CONFIG.LOCAL.BASE_URL}/sejour_visa/${selectedVisaId.value}/`, editData)
      showEditModal.value = false
      await fetchVisa()
      alert.showAlertNotif(
            "Modification effectué avec succès",
            "success"
          )
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.data) {
        Object.assign(editErrors, err.response.data)
      } else {
        alert.showAlertNotif(
            "une s'est produit lors de la modification",
            "error"
          )
      }
    }
  }

  // Modal suppression
  const showDeleteModal = ref(false)
  const selectedVisa = ref<any | null>(null)

  const confirmDelete = (row: any) => {
    selectedVisa.value = row
    showDeleteModal.value = true
  }

  const submitDelete = async () => {
    if (!selectedVisa.value) return

    try {
      await axios.delete(`${API_CONFIG.LOCAL.BASE_URL}/sejour_visa/${selectedVisa.value.id}/`)
      showDeleteModal.value = false
      await fetchVisa()
      alert.showAlertNotif(
            ` le ${selectedVisa.value.libelle} a été supprimé`,
            "success"
          )
    } catch (err) {
      console.error(err)
      alert.showAlertNotif(
            "une erreur s'est produit lors de la suppression",
            "error"
          )
    }
  }

onMounted(() => {
  fetchVisa()
})
</script>



