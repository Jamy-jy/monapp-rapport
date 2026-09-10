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
            {{ selectedIncident?.nom_incident }}
        </h2>
        <span class="text-xs px-2 py-0.5 rounded-full bg-brand-50 text-brand-600 dark:bg-brand-500/15">
            {{ selectedIncident?.type }}
        </span>

        <div class="mt-4 min-h-[80px]">
            <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line">
            {{ selectedIncident?.description_incident || 'Aucune description renseignée.' }}
            </p>
        </div>
        <div class="mt-4 min-h-[80px]">
            <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line">
            {{ selectedIncident?.solutionPrise || 'Aucune solution ajouté renseignée.' }}
            </p>
        </div>
        <span class="text-xs px-2 py-0.5 rounded-full bg-brand-50 text-brand-600 dark:bg-brand-500/15">
            {{ selectedIncident?.user }}
        </span>

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
    import API_CONFIG from '@/config/api';


    const currentPageTitle = ref('Incidents')
    const alert = useAlertNotifStore()

    // Recherche et filtre
    const search = ref('')
    const filtre = ref('')
    const recherche = ref<string>('') 

    interface User {
        id: number
        nom: string
        prenom: string
    }

    interface IncidentSurvenu {
        id: number
        nom_incident: string
        type: string
        description_incident: string
        solution: string
        solutionPrise: string
        user: User | null
        date_creation: string
    }

    interface IncidentsRow extends Omit<IncidentSurvenu, 'user'> {
        user: string
    }

    const incidents = ref<IncidentSurvenu[]>([])
    const showModal = ref(false)
    const showAddModal = ref(false)
    const selectedIncident = ref<IncidentSurvenu | null>(null)

    

    // Formulaire ajout
    const newIncident = reactive({ titre: '', type: '', description: '',  solution: ''})
    const addErrors = reactive<Record<string, string>>({})

    const columns = [
        { label: 'Incidents', field: 'nom_incident', width: '45%' },
        { label: 'Type', field: 'type', width: '30%' },
        { label: 'solution', field: 'solutionPrise', width: '30%' },
        { label: 'technicien', field: 'user', width: '30%' },
    ]


    const fetchIncident = async () => {
      try {
        const token = sessionStorage.getItem('token')
        const response = await axios.get<IncidentSurvenu[]>(`${API_CONFIG.LOCAL.BASE_URL}/incidents-survenus/list-create/`,  {
          headers: { Authorization: `Bearer ${token}` }
        })
        incidents.value = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des solutions :', error)
      }
    }

    // Remplace l'objet user par "nom prenom" directement dans le champ "user"
    const solutionsFormatees = computed<IncidentsRow[]>(() => {
      return incidents.value.map((s) => ({
        ...s,
        user: s.user ? `${s.user.nom} ${s.user.prenom}` : 'Inconnu',
      }))
    })

    // Filtre selon la recherche, sur tous les champs affichés
    const SolutionFiltres = computed<IncidentsRow[]>(() => {
      const terme = recherche.value.toLowerCase().trim()
      if (!terme) return solutionsFormatees.value

      return solutionsFormatees.value.filter((s) =>
        Object.values(s).some((val) =>
          String(val ?? '').toLowerCase().includes(terme)
        )
      )
    })

    onMounted(() => {
      fetchIncident()
    })

    // Incidents filtrés par recherche + type
    const incidentsFiltres = computed(() => {
        return incidents.value.filter(i => {
            const matchSearchnom = i.nom_incident.toLowerCase().includes(search.value.toLowerCase())
            const matchSearchtype = i.type.toLowerCase().includes(search.value.toLowerCase())
            return matchSearchnom && matchSearchtype
        })
    })

    const openSolutionModal = (row: IncidentSurvenu) => {
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
            await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/incidents-survenus/create/`, {
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
            const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/incidents/`)
            incidents.value = res.data
        } catch (err) {
            console.error('Erreur chargement incidents:', err)
        }
    }

    onMounted(() => {
        fetchIncidents()
    })

</script>