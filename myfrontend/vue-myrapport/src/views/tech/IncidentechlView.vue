<template>
    <PageBreadcrumbTech :pageTitle="currentPageTitle"/>
    <ComponentCard title="Incidents">

        <!-- Barre recherche + filtre + bouton ajout -->
        <div class="flex items-center gap-3 mb-4">
    
          <!-- Recherche -->
          <div class="relative flex-1">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
              </svg>
            </span>
            <input
              v-model="search"
              type="text"
              placeholder="Recherche..."
              class="w-full pl-9 pr-4 h-10 text-sm border border-gray-300 rounded-lg bg-transparent dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 focus:border-brand-300 focus:outline-none focus:ring-2 focus:ring-brand-500/10"
            />
          </div>
    
          <!-- Filtre -->
          <select
            v-model="filtre"
            class="h-10 px-3 text-sm border border-gray-300 rounded-lg bg-transparent dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 focus:border-brand-300 focus:outline-none"
          >
            <option value="">Tous</option>
            <option value="systeme">Système</option>
            <option value="materiel">Matériel</option>
            <option value="reseau">Réseau</option>
          </select>
    
          <!-- Bouton ajout -->
          <button
            @click="showAddModal = true"
            class="flex items-center gap-2 h-10 px-4 text-sm font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600 transition active:scale-95 shrink-0"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Ajout nouvel incident
          </button>
        </div>
    
        <BaseTable
            :columns="columns"
            :rows="incidentsFiltres"
            @solution="openSolutionModal"
        />
    </ComponentCard>

     <!-- Modal ajout nouvel incident -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div class="w-full max-w-lg bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
            <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
                Nouvel incident
            </h2>

            <div class="space-y-4">

                <!-- Nom incident -->
                <div>
                    <PlaceholderInput
                        v-model="newIncident.titre"
                        label="Nom de l'incident"
                        placeholder="Entrez le nom de l'incident"
                    />
                    <p v-if="addErrors.titre" class="text-red-500 text-sm mt-1">{{ addErrors.titre }}</p>
                </div>

                <!-- Type -->
                <div>
                    <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Type</label>
                    <select
                        v-model="newIncident.type"
                        class="h-11 w-full px-4 text-sm border border-gray-300 rounded-lg bg-transparent dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 focus:border-brand-300 focus:outline-none"
                    >
                        <option value="" disabled>Choisissez un type</option>
                        <option value="systeme">Système</option>
                        <option value="materiel">Matériel</option>
                        <option value="reseau">Réseau</option>
                    </select>
                    <p v-if="addErrors.type" class="text-red-500 text-sm mt-1">{{ addErrors.type }}</p>
                </div>

                <!-- Description / solution -->
                <div>
                    <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                        Description de l'incident (optionnel) <span class="text-gray-400 font-normal">(optionnel)</span>
                    </label>
                    <TextareaInput
                        v-model="newIncident.description"
                        placeholder="Décrivez l'incident"
                        :rows="5"
                    />
                </div>
                <div>
                    <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                        Solution <span class="text-gray-400 font-normal">(optionnel)</span>
                    </label>
                    <TextareaInput
                        v-model="newIncident.solution"
                        placeholder="Décrivez la solution si connue..."
                        :rows="5"
                    />
                </div>

            </div>
            <div class="flex justify-end gap-3 mt-6">
                <button
                    @click="closeAddModal"
                    class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400"
                >
                    Annuler
                </button>
                <button
                    @click="submitNewIncident"
                    class="px-4 py-2 text-sm text-white bg-brand-500 rounded-lg hover:bg-brand-600 transition"
                >
                    Enregistrer
                </button>
            </div>
        </div>
    </div>

    <!-- Modal solution -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div class="w-full max-w-lg bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">

        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-1">
            {{ selectedIncident?.titre }}
        </h2>
        <span class="text-xs px-2 py-0.5 rounded-full bg-brand-50 text-brand-600 dark:bg-brand-500/15">
            {{ selectedIncident?.type }}
        </span>

        <div class="mt-4 min-h-[80px]">
            <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line">
            {{ selectedIncident?.solution || 'Aucune solution renseignée.' }}
            </p>
        </div>

        <!-- Fichier PDF si présent -->
        <div v-if="selectedIncident?.fichier_solution" class="mt-4 border border-gray-200 dark:border-gray-700 rounded-xl p-4">
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
                        {{ selectedIncident.fichier_solution.split('/').pop() }}
                    </p>
                    <p class="text-xs text-gray-400">PDF</p>
                </div>

                <!--Bouton afficher readonly -->
                <a
                    :href="`http://localhost:8000${selectedIncident.fichier_solution}`"
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

        <div class="flex justify-end mt-6">
            <button
            @click="showModal = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:border-gray-700"
            >
            Fermer
            </button>
        </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted, reactive, computed } from 'vue';
    import PageBreadcrumbTech from '@/components/common/PageBreadcrumbTech.vue';
    import BaseTable from '@/components/table/BaseTable.vue';
    import SolutionActions from '@/components/table/SolutionActions.vue';
    import axios from 'axios';
    import ComponentCard from '@/components/common/ComponentCard.vue';
    import TextareaInput from '@/components/FormElement/TextareaInput.vue';
    import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
    import { useAlertNotifStore } from '@/stores/AlertNotif';


    const currentPageTitle = ref('Incidents')
    const alert = useAlertNotifStore()

    // Recherche et filtre
    const search = ref('')
    const filtre = ref('')

    interface Incident {
        id: number
        source: 'systeme' | 'materiel' | 'reseau'
        titre: string
        type: string
        description: string
        solution: string
        fichier_solution: string
        date_creation: string
    }

    const incidents = ref<Incident[]>([])
    const showModal = ref(false)
    const showAddModal = ref(false)
    const selectedIncident = ref<Incident | null>(null)

    // Formulaire ajout
    const newIncident = reactive({ titre: '', type: '', description: '',  solution: ''})
    const addErrors = reactive<Record<string, string>>({})

    const columns = [
        { label: 'Incidents', field: 'titre', width: '45%' },
        { label: 'Type', field: 'type', width: '30%' },
        { label: 'Action', width: '15%', render: SolutionActions },
    ]

    // Incidents filtrés par recherche + type
    const incidentsFiltres = computed(() => {
        return incidents.value.filter(i => {
            const matchSearch = i.titre.toLowerCase().includes(search.value.toLowerCase())
            const matchFiltre = filtre.value === '' || i.source === filtre.value
            return matchSearch && matchFiltre
        })
    })

    const openSolutionModal = (row: Incident) => {
        selectedIncident.value = row
        showModal.value = true
    }

    const closeAddModal = () => {
        showAddModal.value = false
        newIncident.titre = ''
        newIncident.type = ''
        newIncident.solution = ''
        newIncident.description = ''
        Object.keys(addErrors).forEach(k => delete addErrors[k])
    }

    const submitNewIncident = async () => {
        Object.keys(addErrors).forEach(k => delete addErrors[k])

        if (!newIncident.titre.trim()) {
            addErrors.titre = 'Ce champ ne peut pas être vide.'
            return
        }
        if (!newIncident.type) {
            addErrors.type = 'Veuillez choisir un type.'
            return
        }

        try {
            // Un seul endpoint — tout va dans IncidentSurvenu
            await axios.post('http://localhost:8000/api/incidents-survenus/create/', {
            nom_incident: newIncident.titre,
            type: newIncident.type,
            solutionPrise: newIncident.solution || null,
            description_incident: newIncident.description || null,
            })

            closeAddModal()
            alert.showAlertNotif(
                "Enregistrement effectué avec succès",
                "success"
            )
            await fetchIncidents()

        } catch (err) {
            if (axios.isAxiosError(err) && err.response?.data) {
            Object.assign(addErrors, err.response.data)
            }
            alert.showAlertNotif(
                "Une erreur s'est produite lors de l'enregistrement",
                "error"
            )
        }
    }

    const fetchIncidents = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/incidents/')
            incidents.value = res.data
        } catch (err) {
            console.error('Erreur chargement incidents:', err)
        }
    }

    onMounted(() => {
        fetchIncidents()
    })

</script>