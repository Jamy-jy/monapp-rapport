<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />
        <div class="space-y-5 sm:space-y-6">
            <ComponentCard title="utilisateurs">
                <BaseTable 
                    :columns="columns" 
                    :rows="users" 
                    @edit="openEditModal"
                    @toggle="toggleStatut"
                />
            </ComponentCard>
        </div>

        <div
            v-if="showModal"
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
        >
            <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
                <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
                    Modifier l'utilisateur
                </h2>

                <div class="space-y-3">
                    <PlaceholderInput v-model="editData.nom" label="Nom" placeholder="Nom" />
                    <PlaceholderInput v-model="editData.prenom" label="Prénom" placeholder="Prénom" />

                    <div>
                        <EmailInput v-model="editData.email" label="Email" placeholder="Email" />
                        <p v-if="editErrors.email" class="text-red-500 text-sm mt-1">{{ editErrors.email }}</p>
                    </div>

                    <div>
                        <PlaceholderInput v-model="editData.phone" label="Téléphone" placeholder="phone" />
                        <p v-if="editErrors.phone" class="text-red-500 text-sm mt-1">{{ editErrors.phone }}</p>
                    </div>

                    <SelectInput
                        label="Rôle"
                        :options="roleOptions"
                        v-model="editData.role"
                    />

                    <div>
                        <PasswordInput v-model="editData.password" label="Nouveau mot de passe (optionnel)" />
                        <p v-if="editErrors.password" class="text-red-500 text-sm mt-1">{{ editErrors.password }}</p>
                    </div>
                </div>

                <div class="flex justify-end gap-3 mt-6">
                    <button
                        @click="showModal = false"
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
</template>
<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
import ComponentCard from '@/components/common/ComponentCard.vue';
import BaseTable from '@/components/table/BaseTable.vue';
import StatusBadge from '@/components/table/StatusBadge.vue';
import UserActions from '@/components/table/UserActions.vue';
import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
import EmailInput from '@/components/FormElement/EmailInput.vue';
import SelectInput from '@/components/FormElement/SelectInput.vue';
import PasswordInput from '@/components/FormElement/PasswordInput.vue';
import axios from 'axios';
import { useAlertNotifStore } from '@/stores/AlertNotif';
import API_CONFIG from '@/config/api';

const users = ref([])
const alert = useAlertNotifStore()

const currentPageTitle = ref('Liste utilisateur')
const showModal = ref(false)
const selectedUserId = ref<number | null>(null)

const editData = reactive({
    nom: '',
    prenom: '',
    email: '',
    phone: '',
    role: '',
    password: '',
})

const editErrors = reactive<Record<string, string>>({})

interface Option {
    label: string
    value: string | number
}

const roleOptions: Option[] = [
    { label: "Administrateur", value: "admin"},
    { label: "Technicien", value: "tech" }
]

const columns = [
    { label: 'Utilisateur', field: 'nom', width: '20%' },
    { label: 'Email', field: 'email', width: '20%' },
    { label: 'Rôle', field: 'role', width: '15%' },
    { label: 'Statut', field: 'statut', width: '15%', render: StatusBadge },
    { label: 'Date de création', field: 'created_at', width:'15%'},
    { label: 'Action', width: '15%', render: UserActions}
]

//recuperation de donnée depuis API
const fetchUsers = async () => {
    try {
        const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/users/`)
        //assignation au colonne
        users.value = res.data.map((u: any) => ({
            id: u.id,
            nom: `${u.prenom} ${u.nom}`,
            email: u.email,
            phone: u.phone,
            role: u.role === 'tech' ? 'Technicien' : 'Administrateur',
            role_raw: u.role,
            statut: u.statut,
            created_at: new Date(u.created_at).toLocaleDateString(),
        }))
        console.log(users.value)
    } catch (err) {
        console.error(err)
        alert.showAlertNotif(
            "une s'est produit lors de l'affichage",
            "error"
          )
    }
} 

// Ouvrir modal modification
const openEditModal = (row: any) => {
  selectedUserId.value = row.id
  editData.nom = row.nom.split(' ')[1] || ''
  editData.prenom = row.nom.split(' ')[0] || ''
  editData.email = row.email
  editData.phone = row.phone || ''
  editData.role = row.role_raw,
  editData.password = ''
  Object.keys(editErrors).forEach(k => delete editErrors[k])
  showModal.value = true
}

// Soumettre modification
const submitEdit = async () => {
  if (!selectedUserId.value) return
  Object.keys(editErrors).forEach(k => delete editErrors[k])

  try {
    await axios.patch(
      `${API_CONFIG.LOCAL.BASE_URL}/users/${selectedUserId.value}/`,
      editData
    )
    showModal.value = false
    await fetchUsers()  // rafraîchir la liste
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

// Toggle statut activer/désactiver
const toggleStatut = async (row: any) => {
  try {
    await axios.patch(
      `${API_CONFIG.LOCAL.BASE_URL}/users/${row.id}/toggle-statut/`
    )
    await fetchUsers()  // rafraîchir la liste
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
    fetchUsers()
})
</script>

