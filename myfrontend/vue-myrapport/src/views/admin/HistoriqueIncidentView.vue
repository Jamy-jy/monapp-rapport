<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle"/>
    <ComponentCard title="filtre">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
            <SelectInput
              label="technicien"
              placeholder="choisissez le technicien"
              :options="techOptions"
              v-model="formData.tech" 
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
                <searchIcon/>
                Recherche
            </button>
        </div>
    </ComponentCard>

    <!-- liste incident -->
    <div class="mt-6">
        <ComponentCard title="Liste des incidents">
            <BaseTable
                v-if="incidents.length > 0"
                :columns="columns"
                :rows="incidents"
            />
            <p
                v-else-if="noResult"
                class="text-center text-gray-500 py-4"
            >
                Aucun résultat trouvé
            </p>
        </ComponentCard>
    </div>
</template>
<script setup lang="ts">
    import { ref, reactive, onMounted, computed } from 'vue'
    import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
    import ComponentCard from '@/components/common/ComponentCard.vue';
    import SelectInput from '@/components/FormElement/SelectInput.vue';
    import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
    import axios from 'axios';
    import BaseTable from '@/components/table/BaseTable.vue';
    import searchIcon from '@/icons/searchIcon.vue';
    import API_CONFIG from '@/config/api';

    const currentPageTitle = ref('Historique Incident')

    interface Model {
        tech: string
        dateDebut: string
        dateFin: string
    }

    interface Incident {
        id: number
        source: 'systeme' | 'materiel' | 'reseau'
        nom: string
        premon: string
        type: string
        date_creation: string
    }


    const incidents = ref<Incident[]>([])
    const noResult = ref(false)

    const props = defineProps<{
        modelValue?: Model
    }>()

    const formData = reactive({
        tech: props.modelValue?.tech || ''
    })

    const techOptions = ref([])

    const dateDebut = ref(props.modelValue?.dateDebut || '')
    const dateFin = ref(props.modelValue?.dateFin || '')

    const loadTechs = async () => {
        try {
            const response = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/tech/`)

            techOptions.value = response.data
        } catch (error) {
            console.error(error)
        }
    }

    onMounted(() => {
        loadTechs()
    })
    
    interface Incident {
        id: number
        source: 'systeme' | 'materiel' | 'reseau'
        titre: string
        type: string
        date_creation: string
    }

    // Colonnes tableau
    const columns = [
        { label: 'Incident', field: 'nom_incident', width: '40%' },
        { label: 'type', field: 'type', width: '35%' },
        {label: 'Date', field: 'date_creation', width: '35%' },
        {label: 'Technicien', field: 'user_prenom', width: '35%' },
    ]

    const fetchIncidents = async () => {
        try {
            const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/incidents-survenus/list/`)
            incidents.value = res.data
        } catch (err) {
            console.error('Erreur chargement incidents:', err)
        }
    }
   

    const fetchSearchIncidents = async (tech = '', debut = '', fin = '') => {
        try {
            const params: Record<string, string> = {}
            // Ajouter les filtres seulement si renseignés
            if (tech) params.tech = tech
            if (debut) params.dateDebut = debut
            if (fin) params.dateFin = fin
    
            const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/incidents-survenus/serchTechlist/`, {
                params
            })
            incidents.value = res.data

            noResult.value = res.data.length === 0

        } catch (err) {
            console.error('Erreur chargement incidents:', err)
        }
    }

    // Bouton recherche
    const handelClick = () => {
        fetchSearchIncidents(
            formData.tech,    // tech sélectionné ou vide
            dateDebut.value,  // date début ou vide
            dateFin.value     // date fin ou vide
        )
    }

    // Au chargement — afficher tout
    onMounted(() => {
        loadTechs()
        fetchIncidents()  // sans paramètres = tout afficher
    })
</script>