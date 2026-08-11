<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle"/>
    <ComponentCard 
        title="Ajout nouvel incident"
        textClick="Historique"
        @clickText="openListe"
        :icon="ListIcon"
        >
        <form @submit.prevent="handleSave" class="space-y-6">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
                <div class="sm:col-span-3">
                  <PlaceholderInput
                    v-model="reseau.nom_incident_reseau"
                    label="nom incident"
                    placeholder="Entrez le nom de l'incident"
                  />
                  <p v-if="serverErrors.nom_incident_reseau" class="text-red-500 text-sm mt-1">
                    {{ serverErrors.nom_incident_reseau }}
                  </p>
                </div>
                <div class="sm:col-span-1 flex items-end">
                  <SaveBtn class="w-full" @click="handleSave"/>
                </div>
            </div>
        </form>
    </ComponentCard>

    <!-- liste incident -->
    <div class="mt-6">
        <ComponentCard title="Liste des incidents">
            <BaseTable
                :columns="columns"
                :rows="reseaux"
                @solution="openSolutionModal"
            />
        </ComponentCard>
    </div>

    <!-- Modal solution à la création -->
    <div v-if="showSolutionCreateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div class="w-full max-w-lg bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
            <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
                Ajouter une solution
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
                Incident : <span class="font-medium text-gray-700 dark:text-white">{{ reseau.nom_incident_reseau }}</span>
            </p>

            <TextareaInput
                v-model="reseau.solution"
                placeholder="Décrivez la solution..."
                :rows="6"
            />

            <!-- Upload PDF -->
            <div class="mt-4">
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                    Fichier PDF <span class="text-gray-400 font-normal">(optionnel)</span>
                </label>

                <!-- Zone upload -->
                <div
                    class="relative flex flex-col items-center justify-center w-full h-24 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-brand-400 transition dark:border-gray-700"
                    @click="triggerFileInput"
                    @dragover.prevent
                    @drop.prevent="onFileDrop"
                >
                    <!-- Fichier sélectionné -->
                    <div v-if="fichierSelectionne" class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                        <svg class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                        </svg>
                        <span>{{ fichierSelectionne.name }}</span>
                        <button
                            @click.stop="fichierSelectionne = null"
                            class="text-red-400 hover:text-red-600 ml-2"
                        >✕</button>
                    </div>

                    <!-- Placeholder -->
                    <div v-else class="flex flex-col items-center text-gray-400 text-sm">
                        <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
                        </svg>
                        Cliquer ou glisser un fichier PDF
                    </div>

                    <!-- Input caché -->
                    <input
                        ref="fileInput"
                        type="file"
                        accept=".pdf"
                        class="hidden"
                        @change="onFileChange"
                    />
                </div>

                <!-- Erreur format -->
                <p v-if="fichierErreur" class="text-red-500 text-sm mt-1">{{ fichierErreur }}</p>
            </div>

            <div class="flex justify-end gap-3 mt-4">
                <button
                @click="submitForm(false)"
                class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400"
                >
                Ignorer
                </button>
                <button
                @click="submitForm(true)"
                class="px-4 py-2 text-sm text-white bg-brand-500 rounded-lg hover:bg-brand-600"
                >
                Enregistrer
                </button>
            </div>
        </div>
    </div>

    <!-- Modal voir/modifier/supprimer solution -->
    <div v-if="showDetailModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div class="w-full max-w-lg bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
            <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-1">
                {{ selectedReseau?.nom_incident_reseau }}
            </h2>
            <p class="text-xs text-gray-400 mb-4">{{ selectedReseau?.date_creation }}</p>

            <!-- Mode lecture -->
            <div v-if="!editMode">
                <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line min-h-[80px]">
                {{ selectedReseau?.solution || 'Aucune solution renseignée.' }}
                </p>

                <!-- Fichier PDF si présent -->
                <div v-if="selectedReseau?.fichier_solution" class="mt-4 border border-gray-200 dark:border-gray-700 rounded-xl p-4">
                  <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-3 uppercase tracking-wide">
                    Fichier joint
                  </p>

                  <div class="flex items-center gap-3">
                    <!-- Icône PDF -->
                    <div class="flex items-center justify-center w-9 h-9 rounded-lg bg-red-100 dark:bg-red-900/30 shrink-0">
                      <svg class="w-5 h-5 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                      </svg>
                    </div>

                    <div class="flex-1">
                      <p class="text-sm font-medium text-gray-800 dark:text-white">
                        {{ selectedReseau.fichier_solution.split('/').pop() }}
                      </p>
                      <p class="text-xs text-gray-400">PDF</p>
                    </div>

                    <!--Bouton afficher readonly -->
                    <a
                      :href="`http://localhost:8000${selectedReseau.fichier_solution}`"
                      target="_blank"
                      class="flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-brand-600 border border-brand-300 rounded-lg hover:bg-brand-50 dark:border-brand-700 dark:text-brand-400 dark:hover:bg-brand-900/20 transition"
                    >
                      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                      </svg>
                      Afficher
                    </a>
                  </div>
                </div>


                <div class="flex justify-end gap-3 mt-6">
                    <button
                        @click="showDetailModal = false"
                        class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700"
                    >
                        Fermer
                    </button>
                    <button
                        @click="editMode = true"
                        class="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
                    >
                        Modifier
                    </button>
                    <button
                        @click="deleteReseau"
                        class="px-4 py-2 text-sm text-white bg-red-500 rounded-lg hover:bg-red-600"
                    >
                        Supprimer
                    </button>
                </div>
            </div>

            <!-- Mode édition -->
            <div v-else>
                <PlaceholderInput
                    v-model="editData.nom_incident_reseau"
                    label="Titre"
                    placeholder="Titre de l'incident"
                    class="mb-3"
                />
                <p class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Solution</p>
                <TextareaInput
                    v-model="editData.solution"
                    placeholder="Solution..."
                    :rows="6"
                />
                <div class="flex justify-end gap-3 mt-4">
                    <button
                        @click="editMode = false"
                        class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700"
                    >
                        Annuler
                    </button>
                    <button
                        @click="updateReseau"
                        class="px-4 py-2 text-sm text-white bg-brand-500 rounded-lg hover:bg-brand-600"
                    >
                        Enregistrer
                    </button>
                </div>
            </div>
        </div>
    </div>        
</template>
<script setup lang="ts">
    import { ref, reactive, onMounted } from 'vue'
    import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
    import ComponentCard from '@/components/common/ComponentCard.vue';
    import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
    import SaveBtn from '@/components/buttons/SaveBtn.vue';
    import { useAlertNotifStore } from '@/stores/AlertNotif';
    import SystemeActions from '@/components/table/SystemeActions.vue';
    import BaseTable from '@/components/table/BaseTable.vue';
    import axios from 'axios';
    import TextareaInput from '@/components/FormElement/TextareaInput.vue';
    import router from '@/router';
    import ListIcon from '@/icons/ListIcon.vue';

    const currentPageTitle = ref('Incident Reseau')

    const alert = useAlertNotifStore()

    const reseau = reactive({ 
        nom_incident_reseau: '', 
        solution: '' 
    })
    const serverErrors = reactive<Record<string, string>>({})

    // Modals
    const showSolutionCreateModal = ref(false)
    const showDetailModal = ref(false)
    const editMode = ref(false)

    const reseaux = ref<any[]>([])
    const selectedReseau = ref<any | null>(null)
    const editData = reactive({ nom_incident_reseau: '', solution: '' })

    // Colonnes tableau
    const columns = [
        { label: 'Titre', field: 'nom_incident_reseau', width: '50%' },
        { label: 'Date', field: 'date_creation', width: '20%' },
        { label: 'Action', width: '15%', render: SystemeActions },
    ]

    // Étape 1 — clic SaveBtn → ouvrir modal solution
    const handleSave = () => {
    Object.keys(serverErrors).forEach(k => delete serverErrors[k])

    if (!reseau.nom_incident_reseau.trim()) {
        serverErrors.nom_incident_reseau = 'Ce champ ne peut pas être vide.'
        return
    }

    reseau.solution = ''
    showSolutionCreateModal.value = true
    }

    // * upload file
    const fileInput = ref<HTMLInputElement | null>(null)
    const fichierSelectionne = ref<File | null>(null)
    const fichierErreur = ref('')

    const triggerFileInput = () => {
        fileInput.value?.click()
    }

    const onFileChange = (e: Event) => {
        const file = (e.target as HTMLInputElement).files?.[0]
        validerFichier(file)
    }

    const onFileDrop = (e: DragEvent) => {
        const file = e.dataTransfer?.files?.[0]
        validerFichier(file)
    }

    const validerFichier = (file: File | undefined) => {
        fichierErreur.value = ''
        if (!file) return

        // Vérifier que c'est bien un PDF
        if (file.type !== 'application/pdf') {
            fichierErreur.value = 'Seuls les fichiers PDF sont acceptés.'
            return
        }

        fichierSelectionne.value = file
    }

    // Étape 2 — soumettre avec ou sans solution
    const submitForm = async (avecSolution: boolean) => {
        try {
            const formData = new FormData()
            formData.append('nom_incident_reseau',  reseau.nom_incident_reseau)

            if (avecSolution) {
                formData.append('solution', reseau.solution)
                if (fichierSelectionne.value) {
                    formData.append('fichier_solution', fichierSelectionne.value)
                }
            }

            await axios.post('http://localhost:8000/api/reseaux/create/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            })

            showSolutionCreateModal.value = false
            reseau.nom_incident_reseau = ''
            reseau.solution = ''
            alert.showAlertNotif(
                "Enregistrement effectué avec succès",
                "success"
            )
            await fetchReseaux()
        } catch (err) {
            if (axios.isAxiosError(err) && err.response?.data) {
                Object.assign(serverErrors, err.response.data)
                console.log(err.response?.data)
            }
            showSolutionCreateModal.value = false
            console.error(err)
            alert.showAlertNotif(
                "Erreur lors de l'enregistrement",
                "error"
            )
        }
    }

    // Ouvrir modal détail/solution
    const openSolutionModal = (row: any) => {
        selectedReseau.value = row
        editData.nom_incident_reseau = row.nom_incident_reseau
        editData.solution = row.solution_incident_reseau
        editMode.value = false
        showDetailModal.value = true
    }

    // Modifier
    const updateReseau = async () => {
        if (!selectedReseau.value) return
        try {
            await axios.patch(
            `http://localhost:8000/api/reseaux/${selectedReseau.value.id}/update/`,
            {
                nom_incident_reseau: editData.nom_incident_reseau,
                solution_incident_reseau: editData.solution,
            }
            )
            showDetailModal.value = false
                alert.showAlertNotif(
                "Modification effectué avec succès",
                "success"
            )
            await fetchReseaux()
        } catch (err) {
            console.error('Erreur modification:', err)
            alert.showAlertNotif(
                "une erreur s'est produite lors du Modification",
                "error"
            )
        }
    }

    // Supprimer
    const deleteReseau = async () => {
        if (!selectedReseau.value) return
        try {
            await axios.delete(
            `http://localhost:8000/api/reseaux/${selectedReseau.value.id}/delete/`
            )
            showDetailModal.value = false
            alert.showAlertNotif(
                "suppression d'un élement effectué avec succès",
                "success"
            )
            await fetchReseaux()
        } catch (err) {
            console.error('Erreur suppression:', err)
            alert.showAlertNotif(
                "suppression interrompu!",
                "error"
            )
        }
    }

    // Charger la liste
    const fetchReseaux = async () => {
    try {
        const res = await axios.get('http://localhost:8000/api/reseaux/reseau-list/')
        reseaux.value = res.data
    } catch (err) {
        console.error('Erreur chargement:', err)
    }
    }

    onMounted(() => {
        fetchReseaux()
    })

    const openListe = () => {
        router.push('/admin/Historique-incidents')
    }
</script>