<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle"/>
    <div class="grid grid-cols-1 gap-12 sm:grid-cols-1 my-8">
      <ComponentCard title="Liste">
        <BaseTable
          :columns="columnsGroup" 
          :rows="Group" 
          @list="listItemInGroup"
          @add="addItemInGroup"
        />
      </ComponentCard> 
    </div>

    <!-- Modal d'ajout de composant de groupe -->
    <div
      v-if="showModalAddComposantGroup"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
          groupe {{ selectedGroup?.nom_group }}
        </h2>

        <div class="space-y-3">
          <div>
            <PlaceholderInput
              v-model="composantGroup.nom_materiel"
              label="Nom materiel"
              placeholder="Entrez nom materiel"
            />
            <p v-if="composantGroupErrors.nom_materiel" class="text-red-500 text-sm mt-1">
              {{ composantGroupErrors.nom_materiel }}
            </p>
          </div>
          <div>
            <PlaceholderInput
              v-model="composantGroup.marque_materiel"
              label="Marque materiel"
              placeholder="Entrez marque materiel"
            />
            <p v-if="composantGroupErrors.marque_materiel" class="text-red-500 text-sm mt-1">
              {{ composantGroupErrors.marque_materiel }}
            </p>
          </div>
          <div>
            <PlaceholderInput
              v-model="composantGroup.numero_serie"
              label="Numéro série"
              placeholder="Entrez numéro série"
            />
            <p v-if="composantGroupErrors.numero_serie" class="text-red-500 text-sm mt-1">
              {{ composantGroupErrors.numero_serie }}
            </p>
          </div>
          <div>
            <PlaceholderInput
              v-model="composantGroup.configuration"
              label="Configuration"
              placeholder="Entrez configuration"
            />
            <p v-if="composantGroupErrors.nomconfiguration_group" class="text-red-500 text-sm mt-1">
              {{ composantGroupErrors.configuration }}
            </p>
          </div>
          
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="showModalAddComposantGroup = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="submitAddComposanttGroup"
            class="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>

    <!-- Modal liste des composants du groupe -->
    <div
      v-if="showModalListComposantGroup"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-4xl bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-800 dark:text-white">
            Groupe {{ selectedGroupForList?.nom_group }}
          </h2>
          <button
            @click="showModalListComposantGroup = false"
            class="text-gray-400 hover:text-gray-600 text-xl leading-none"
          >
            &times;
          </button>
        </div>

        <div v-if="loadingComposantList" class="text-center text-gray-500 py-6">
          Chargement...
        </div>

        <div v-else-if="composantGroupList.length === 0" class="text-center text-gray-500 py-6">
          Aucun composant enregistré pour ce groupe.
        </div>

        <BaseTable
          v-else
          :columns="columnsComposant"
          :rows="composantGroupList"
        />

        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="showModalListComposantGroup = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="submitAddEtatMateriel"
            class="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmation avant validation "Oui" -->
    <div
      v-if="showModalConfirmTest"
      class="fixed inset-0 z-[60] flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          {{ composantToConfirm?.nom_materiel }}
        </h2>
        <p class="text-sm text-gray-500 mb-3">
          Avez-vous bien vérifié tout ce qui suit ?
        </p>
        <div class="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 rounded-lg p-3 max-h-48 overflow-y-auto">
          {{ composantToConfirm?.test_fonctionnalite || 'Aucun test renseigné.' }}
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="cancelConfirmTest"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="confirmEtatMateriel"
            class="px-4 py-2 text-sm text-white bg-green-500 rounded-lg hover:bg-green-600"
          >
            C'est fait
          </button>
        </div>
      </div>
    </div>
</template>
<script setup lang="ts">
    import { ref, onMounted, h, reactive } from 'vue';
    import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
    import ComponentCard from '@/components/common/ComponentCard.vue';
    import BaseTable from '@/components/table/BaseTable.vue';
    import AddItemAction from '@/components/table/AddItemAction.vue';
    import axios from 'axios';
    import ListAction from '@/components/table/listAction.vue';
    import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
import API_CONFIG from '@/config/api';

    const currentPageTitle = ref('Inventaire')
    const Group = ref<any[]>([])

    const columnsGroup = [
      { label: 'Groupe', field: 'nom_group', width: '15%'},
      { label: 'Date création', field: 'group_created_at', width: '15%'},
      { label: 'Actions', 
        renderFn: (row: any) =>
            h('div', {class: 'flex gap-2'}, [
                h(ListAction, {
                    row,
                    onList: (data : any) => listItemInGroup(data),
                }),
                
                !row.access_group
                ? h(AddItemAction, {
                    row,
                    onAdd: (data: any) => addItemInGroup(data),
                })
                : null,
               
            ]),  
         width: '15%'},
    ]

    const fetchGroup = async () => {
      try {
        const resg = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/inventaire/`)
        Group.value = resg.data.map((g: any) => ({
          id: g.id,
          nom_group: g.nom_group,
          access_group: g.access_group,
          group_created_at: new Date(g.group_created_at).toLocaleDateString()
        }))
        console.log(Group.value)
      } catch (err){
        console.log(err)
      }
    }

    const composantGroup = reactive({
      nom_materiel: '',
      marque_materiel: '',
      numero_serie: '',
      configuration: '',
    })

    const composantGroupErrors = reactive<Record<string, string>>({
      nom_materiel: '',
      marque_materiel: '',
      numero_serie: '',
      configuration: '',
    })

    const showModalAddComposantGroup = ref(false)
    const selectedGroupId = ref<number | null>(null)
    const selectedGroup = ref<any | null>(null)

    const addItemInGroup = async (row: any) => {
      selectedGroupId.value = row.id
      selectedGroup.value = row 
      resetComposantGroupForm()
      showModalAddComposantGroup.value = true
    }

    const resetComposantGroupForm = () => {
      composantGroup.nom_materiel = ''
      composantGroup.marque_materiel = ''
      composantGroup.numero_serie = ''
      composantGroup.configuration = ''

      composantGroupErrors.nom_materiel = ''
      composantGroupErrors.marque_materiel = ''
      composantGroupErrors.numero_serie = ''
      composantGroupErrors.configuration = ''
    }

    // --- Validation simple côté client ---
    const validateComposantGroup = (): boolean => {
      let isValid = true

      composantGroupErrors.nom_materiel = ''
      composantGroupErrors.marque_materiel = ''
      composantGroupErrors.numero_serie = ''
      composantGroupErrors.configuration = ''

      if (!composantGroup.nom_materiel.trim()) {
        composantGroupErrors.nom_materiel = 'Le nom du matériel est requis.'
        isValid = false
      }
      if (!composantGroup.marque_materiel.trim()) {
        composantGroupErrors.marque_materiel = 'La marque est requise.'
        isValid = false
      }
      if (!composantGroup.numero_serie.trim()) {
        composantGroupErrors.numero_serie = 'Le numéro de série est requis.'
        isValid = false
      }
      if (!composantGroup.configuration.trim()) {
        composantGroupErrors.configuration = 'La configuration est requise.'
        isValid = false
      }

      return isValid
    }

    const submitAddComposanttGroup = async () => {
      if (!validateComposantGroup()) return
      if (!selectedGroupId.value) return

      try {
        const payload = {
          group: selectedGroupId.value,
          nom_materiel: composantGroup.nom_materiel,
          marque_materiel: composantGroup.marque_materiel,
          numero_serie: composantGroup.numero_serie,
          configuration: composantGroup.configuration,
          Etat_materiel: null,
          test_fonctionnalite: null,
        }

        const response = await axios.post(
          `${API_CONFIG.LOCAL.BASE_URL}/composant-group/`,
          payload
        )

        console.log('Composant ajouté :', response.data)

        showModalAddComposantGroup.value = false
        resetComposantGroupForm()

        // Rafraîchir la liste des groupes/composants si nécessaire
        await fetchGroup()

      } catch (err: any) {
        console.log(err)

        // Si le backend renvoie des erreurs de validation DRF (400)
        if (err.response?.status === 400 && err.response.data) {
          const backendErrors = err.response.data
          for (const key in backendErrors) {
            if (key in composantGroupErrors) {
              composantGroupErrors[key] = Array.isArray(backendErrors[key])
                ? backendErrors[key][0]
                : backendErrors[key]
            }
          }
        }
      }
    }

    // --- État du modal liste ---
    const showModalListComposantGroup = ref(false)
    const selectedGroupForList = ref<any | null>(null)
    const composantGroupList = ref<any[]>([])
    const loadingComposantList = ref(false)

    // --- Colonnes du tableau de composants ---
    const columnsComposant = [
      { label: 'Nom matériel', field: 'nom_materiel', width: '20%' },
      { label: 'Marque matériel', field: 'marque_materiel', width: '20%' },
      { label: 'Numéro série', field: 'numero_serie', width: '15%' },
      { label: 'Configuration', field: 'configuration', width: '30%' },
      {
        label: 'Fonctionnel',
        width: '17%',
        renderFn: (row: any) =>
          h('div', { class: 'flex items-center gap-4' }, [
            h('label', { class: 'flex items-center gap-1 cursor-pointer' }, [
              h('input', {
                type: 'radio',
                name: `etat-${row.id}`,
                checked: getEtatMaterielValue(row) === true,
                class: 'accent-green-500 w-4 h-4',
                onChange: () => handleOuiClick(row),
              }),
              h('span', { class: 'text-green-600 text-sm' }, 'Oui'),
            ]),
            h('label', { class: 'flex items-center gap-1 cursor-pointer' }, [
              h('input', {
                type: 'radio',
                name: `etat-${row.id}`,
                checked: getEtatMaterielValue(row) === false,
                class: 'accent-red-500 w-4 h-4',
                onChange: () => handleNonClick(row),
              }),
              h('span', { class: 'text-red-600 text-sm' }, 'Non'),
            ]),
          ]),
      },
    ]

    // --- Ouverture du modal liste ---
    const listItemInGroup = async (row: any) => {
      selectedGroupForList.value = row
      loadingComposantList.value = true
      showModalListComposantGroup.value = true

      try {
        const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/composant-group/`, {
          params: { group: row.id, pending: 'true' },
        })
        composantGroupList.value = res.data
      } catch (err) {
        console.log(err)
        composantGroupList.value = []
      } finally {
        loadingComposantList.value = false
      }
    }

    onMounted(() => {
      fetchGroup()
    })


    // --- Suivi des changements en attente (avant enregistrement) ---
    const etatMaterielPending = reactive<Record<number, boolean>>({})

    // --- Modal de confirmation "Oui" ---
    const showModalConfirmTest = ref(false)
    const composantToConfirm = ref<any | null>(null)

    // --- Valeur affichée (pending si modifié, sinon valeur d'origine) ---
    const getEtatMaterielValue = (row: any) => {
      return row.id in etatMaterielPending ? etatMaterielPending[row.id] : row.Etat_materiel
    }

    // --- Clic "Non" : direct, pas de confirmation ---
    const handleNonClick = (row: any) => {
      etatMaterielPending[row.id] = false
    }

    // --- Clic "Oui" : ouvre le modal de confirmation ---
    const handleOuiClick = (row: any) => {
      composantToConfirm.value = row
      showModalConfirmTest.value = true
    }

    const confirmEtatMateriel = () => {
      if (composantToConfirm.value) {
        etatMaterielPending[composantToConfirm.value.id] = true
      }
      showModalConfirmTest.value = false
      composantToConfirm.value = null
    }

    const cancelConfirmTest = () => {
      showModalConfirmTest.value = false
      composantToConfirm.value = null
    }

    const submitAddEtatMateriel = async () => {
      const idsToSave = Object.keys(etatMaterielPending)

      if (idsToSave.length === 0) {
        showModalListComposantGroup.value = false
        return
      }

      try {
        const requests = idsToSave.map((idStr) => {
          const id = Number(idStr)
          const original = composantGroupList.value.find((c) => c.id === id)
          if (!original) return null

          const payload = {
            group: original.group,
            nom_materiel: original.nom_materiel,
            marque_materiel: original.marque_materiel,
            numero_serie: original.numero_serie,
            configuration: original.configuration,
            test_fonctionnalite: original.test_fonctionnalite,
            Etat_materiel: etatMaterielPending[id],
            // composant_created_at n'est pas envoyé -> le backend applique default=timezone.now
          }

          return axios.post(`${API_CONFIG.LOCAL.BASE_URL}/composant-group/`, payload)
        })

        const responses = await Promise.all(requests.filter(Boolean))
        console.log('Nouvelles lignes créées :', responses.map(r => r?.data))

        // Réinitialiser l'état pending
        Object.keys(etatMaterielPending).forEach((k) => delete etatMaterielPending[Number(k)])

        showModalListComposantGroup.value = false

      } catch (err) {
        console.log(err)
      }
    }
</script>