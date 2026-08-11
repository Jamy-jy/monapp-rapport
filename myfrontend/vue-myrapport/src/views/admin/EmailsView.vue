<template>
  <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />
    <div>
      <form @submit.prevent="submitForm" class="space-y-6">
        <ComponentCard title="Nouvel Email">
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <PlaceholderInput
              v-model="email.nom_proprietaire"
              label="Nom du destinataire"
              placeholder="Entrez le nom du destinataire"
            />
            <div>
              <EmailInput
                label="Email destinataire"
                type="email"
                placeholder="Entrez un email"
                v-model="email.emails_destiny"
              />
              <p v-if="serverErrors.emails_destiny" class="text-red-500 text-sm mt-1">
                {{ serverErrors.emails_destiny }}
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
      <ComponentCard title="Liste email">
        <BaseTable 
          :columns="columnsEmail" 
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
        Modifier l'email
      </h2>

      <div class="space-y-3">
        <div>
          <PlaceholderInput
            v-model="editData.nom_proprietaire"
            label="Nom "
            placeholder="Nom"
          />
          <p v-if="editErrors.nom_proprietaire" class="text-red-500 text-sm mt-1">
            {{ editErrors.nom_proprietaire }}
          </p>
        </div>

        <EmailInput
          v-model="editData.emails_destiny"
          label="email destinataire"
          placeholder="example@email.com"
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
          {{ selectedEmail?.emails_destiny}}
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
import EmailInput from '@/components/FormElement/EmailInput.vue';
import SaveBtn from '@/components/buttons/SaveBtn.vue';
import BaseTable from '@/components/table/BaseTable.vue';
import axios from 'axios';
import ItemActions from '@/components/table/ItemActions.vue';
import { useAlertNotifStore } from '@/stores/AlertNotif';

const currentPageTitle = ref('Ajout Email')
const alert = useAlertNotifStore()

const email = reactive({
  nom_proprietaire: '',
  emails_destiny: '',
})

const serverErrors = reactive<Record<string, string>>({})

const submitForm = async () => {
  try {
      const res = await axios.post('http://localhost:8000/api/emails_destinataire/', email )
      email.nom_proprietaire = ''
      email.emails_destiny = ''

      await fetchEmail()
      console.log('email ajouté', res.data)
      alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )
      Object.assign(
          email, {nom_proprietaire: '', emails_destiny: '',}, 
        )
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.data) {
        Object.assign(serverErrors, err.response.data)
        console.error(err.response?.data)
      } else {
        console.error(err)
        alert.showAlertNotif(
            "Erreur lors de l'enregistrement",
            "error"
          )
      }
    }
}

const e = ref<any[]>([])

const columnsEmail = [
  { label: 'Nom', field: 'nom_proprietaire'},
  { label: 'email', field: 'emails_destiny'},
  { label: 'date de creation', field: 'email_created_at'},
  { label: 'Actions', render: ItemActions}
]

const fetchEmail = async () => {
  try {
    const resemail = await axios.get('http://localhost:8000/api/emails_destinataire/')
    e.value = resemail.data.map((ed: any) => ({
    id: ed.id,
    nom_proprietaire: ed.nom_proprietaire,
    emails_destiny: ed.emails_destiny,
    email_created_at: new Date(ed.email_created_at).toLocaleDateString()
  }))
  console.log(e.value)
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
  const selectedEmailId = ref<number | null>(null)

  const editData = reactive({
    nom_proprietaire: '',
    emails_destiny: '',
  })

  const editErrors = reactive<Record<string, string>>({})

  const openEditModal = (row: any) => {
    selectedEmailId.value = row.id
    editData.nom_proprietaire = row.nom_proprietaire,
    editData.emails_destiny = row.emails_destiny,
   
    Object.keys(editErrors).forEach(k => delete editErrors[k])
    showEditModal.value = true
  }

  const submitEdit = async () => {
    if (!selectedEmailId.value) return
    Object.keys(editErrors).forEach(k => delete editErrors[k])

    try {
      await axios.patch(`http://localhost:8000/api/emails_destinataire/${selectedEmailId.value}/`, editData)
      showEditModal.value = false
      await fetchEmail()
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
  const selectedEmail = ref<any | null>(null)

  const confirmDelete = (row: any) => {
    selectedEmail.value = row
    showDeleteModal.value = true
  }

  const submitDelete = async () => {
    if (!selectedEmail.value) return

    try {
      await axios.delete(`http://localhost:8000/api/emails_destinataire/${selectedEmail.value.id}/`)
      showDeleteModal.value = false
      await fetchEmail()
      alert.showAlertNotif(
            `Le ${selectedEmail.value.emails_destiny} a été supprimé avec succès`,
            "error"
          )
    } catch (err) {
      console.error(err)
      alert.showAlertNotif(
            "Erreur lors de la suppression",
            "error"
          )
    }
  }

onMounted(() => {
  fetchEmail()
})
</script>



