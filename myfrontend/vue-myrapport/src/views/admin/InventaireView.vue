<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle"/>
    <div class="space-y-6">
      <form @submit.prevent="submitFormGroup" class="space-y-6">
        <ComponentCard title="Groupe Materiel">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <SelectInput
                    label="site"
                    placeholder="choisissez le site"
                    :options="siteOptions"
                    v-model="formData.site"
                />
                <PlaceholderInput
                      v-model="group.nom_group"
                      label="Groupe"
                      placeholder="Entrez le nom du groupe"
                />
              <div class="flex items-end">
                <SaveBtn class="w-full"/>
              </div>
            </div>
        </ComponentCard>
      </form>
    </div>
    <div class="grid grid-cols-1 gap-12 sm:grid-cols-1 my-8">
      <ComponentCard 
        title="Liste"
        textClick="Historique"
        @clickText="openHistoriqueList"
        :icon="ListIcon"
        >
        <BaseTable
          :columns="columnsGroup" 
          :rows="Group" 
          @list="listItemInGroup"
          @edit="openEditModalGroup"
          @delete="confirmDeleteGroup"
          @add="addItemInGroup"
          @access="accessGroupe"
          />
      </ComponentCard> 
    </div>

    <!-- modal modif paf-->
    <div
      v-if="showEditModalGroup"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
          Modifier
        </h2>

        <div class="space-y-3">
          <div>
            <PlaceholderInput
              v-model="editDataGroup.nom_group"
              label="Nom Groupe"
              placeholder="Entrez nom du groupe"
            />
            <p v-if="editErrorsGroup.nom_group" class="text-red-500 text-sm mt-1">
              {{ editErrorsGroup.nom_group }}
            </p>
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="showEditModalGroup = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="submitEditGroup"
            class="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Confirmation Suppression -->
    <div
      v-if="showDeleteModalGroup"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6 text-center">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          Confirmer la suppression
        </h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Voulez-vous vraiment supprimer
          <span class="font-medium text-gray-800 dark:text-white">
            {{ selectedGroup?.nom_group }}
          </span> ?
        </p>

        <div class="flex justify-center gap-3">
          <button
            @click="showDeleteModalGroup = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="submitDeleteGroup"
            class="px-4 py-2 text-sm text-white bg-red-500 rounded-lg hover:bg-red-600"
          >
            Supprimer
          </button>
        </div>
      </div>
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

        <!-- <div class="flex justify-end mt-6">
          <button
            @click="showModalListComposantGroup = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Fermer
          </button>
        </div> -->
      </div>
    </div>

    <!-- Modal de test de fonctionnalité -->
    <div
      v-if="showModalTestComposant"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          {{ selectedComposant?.nom_materiel }}
        </h2>
        <h3 class="text-sm font-semibold text-gray-800 dark:text-white">
          les choses à vérifier
        </h3>

        <textarea
          v-model="testFonctionnaliteText"
          rows="6"
          placeholder="Ce qui à vérifier..."
          class="w-full rounded-lg border border-gray-300 dark:border-gray-700 dark:bg-gray-800 dark:text-white p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        ></textarea>

        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="closeTestModal"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Fermer
          </button>
          <button
            @click="submitTestComposant"
            :disabled="savingTest"
            class="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600 disabled:opacity-50"
          >
            {{ savingTest ? 'Enregistrement...' : 'Enregistrer' }}
          </button>
        </div>
      </div>
    </div>
</template>
<script setup lang="ts">
    import { ref, reactive, onMounted, h } from 'vue'
    import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
    import ComponentCard from '@/components/common/ComponentCard.vue';
    import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
    import SaveBtn from '@/components/buttons/SaveBtn.vue';
    import axios from 'axios';
    import { useAlertNotifStore } from '@/stores/AlertNotif';
    import ItemActions from '@/components/table/ItemActions.vue';
    import BaseTable from '@/components/table/BaseTable.vue';
    import AddItemAction from '@/components/table/AddItemAction.vue';
    import AccessItemAction from '@/components/table/AccessItemAction.vue';
    import ListAction from '@/components/table/listAction.vue';
    import router from '@/router';
    import ListIcon from '@/icons/ListIcon.vue';
    import SelectInput from '@/components/FormElement/SelectInput.vue';
    import API_CONFIG from '@/config/api';



    const currentPageTitle =ref('Inventaire')

    const alert = useAlertNotifStore()

    interface Option{
      label: string
      value: string | number
      raw: any
    }

    const siteOptions = ref<Option[]>([])

    const formData = reactive({
        site: '',
    })

    const fetchSite = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/site/`)

    siteOptions.value = res.data.map((s: any) => ({
      label: s.accronyme_site,  // ce que tu veux afficher
      value: s.id,               // ce que tu envoies au backend
      raw : s 
    }))

  } catch (err) {
    console.error(err)
  }

}

onMounted(() => {
  fetchSite()
})

    const group = reactive ({
            nom_group: '',
        })

    const showEditModalGroup = ref(false)
    const Group = ref<any[]>([])
    const editErrorsGroup = reactive<Record<string, string>>({})
    
    const showModalAddComposantGroup = ref(false)
    const selectedGroup = ref<any | null>(null)
    const selectedGroupId = ref<number | null>(null)

    const composantGroupErrors = reactive<Record<string, string>>({
      nom_materiel: '',
      marque_materiel: '',
      numero_serie: '',
      configuration: '',
    })


    const columnsGroup = [
      { label: 'Groupe', field: 'nom_group', width: '15%'},
      { label: 'Date création', field: 'group_created_at', width: '15%'},
      // { label: 'Date création', render: ItemActions, width: '15%'},
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
            h(ItemActions, {
              row,
              onEdit: (data: any ) => openEditModalGroup(data),
              onDelete: (data: any) => confirmDeleteGroup(data)
            }),
          ]),
        width: '30%' 
      },
      { label: 'Accès', render: AccessItemAction, width: '15%'}
    ]

    const editDataGroup = reactive({
      nom_group: '',
    })

    const openEditModalGroup = (row: any) => {
      console.log('row reçu :', row)
      selectedGroupId.value = row.id
      editDataGroup.nom_group = row.nom_group
      Object.keys(editErrorsGroup).forEach(k => delete editErrorsGroup[k])
      showEditModalGroup.value = true
    }

    // Modal suppression Groupe
    const showDeleteModalGroup = ref(false)
    

    const confirmDeleteGroup = (row: any) => {
      selectedGroup.value = row
      showDeleteModalGroup.value = true
    }
    
    const submitEditGroup = async () => {
      if (!selectedGroupId.value) return
      Object.keys(editErrorsGroup).forEach(k => delete editErrorsGroup[k])

      try {
        await axios.patch(`${API_CONFIG.LOCAL.BASE_URL}/inventaire/${selectedGroupId.value}/`, editDataGroup)
        showEditModalGroup.value = false
        await fetchGroup()
        alert.showAlertNotif(
          "Modification effectué avec succès!",
          "success"
        )
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.data) {
          Object.assign(editErrorsGroup, err.response.data)
        } else {
          console.error(err)
          alert.showAlertNotif(
            "Erreur lors de la modification",
            "error"
          )
        }
      }
    }

    const submitDeleteGroup = async () => {
      if (!selectedGroup.value) return

      try {
        await axios.delete(`${API_CONFIG.LOCAL.BASE_URL}/inventaire/${selectedGroup.value.id}/`)
        showDeleteModalGroup.value = false
        await fetchGroup()
        alert.showAlertNotif(
          `Le ${selectedGroup.value.nom_group} a été supprimé avec succès`,
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

    const submitFormGroup = async () => {

      const playload = {
          ... group,
          ... formData,
      }
      try {

        const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/inventaire/`, 
          playload,
          
        )

        await fetchGroup()
        console.log('groupe ajouté', res.data)
        alert.showAlertNotif(
          "Enregistrement effectué avec succès",
          "success"
        )
        Object.assign(
          group, {nom_group: '',}, 
        )
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.data) {
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

    const accessGroupe = async (row: any) => {
      try {
        await axios.patch(
          `${API_CONFIG.LOCAL.BASE_URL}/inventaire/${row.id}/access-statut/`
        )
        await fetchGroup()  // rafraîchir la liste
      } catch (err) {
        console.error(err)
      }
    }

    onMounted(() => {
      fetchGroup()
    })

    const composantGroup = reactive({
      nom_materiel: '',
      marque_materiel: '',
      numero_serie: '',
      configuration: '',
    })

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
        label: 'Test de fonctionnalité',
        width: '25%',
        renderFn: (row: any) =>
          h('div', { class: 'flex items-center gap-2' }, [
            // h('span', { class: 'text-sm text-gray-500' }, row.test_fonctionnalite || 'Non testé'),
            h(
              'button',
              {
                class: 'px-3 py-1 text-xs text-white bg-blue-500 rounded-lg hover:bg-blue-600',
                onClick: () => openTestModal(row),
              },
              'Voir'
            ),
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

    // --- État du modal de test ---
    const showModalTestComposant = ref(false)
    const selectedComposant = ref<any | null>(null)
    const testFonctionnaliteText = ref('')
    const savingTest = ref(false)

    // --- Ouverture du modal ---
    const openTestModal = (composant: any) => {
      selectedComposant.value = composant
      testFonctionnaliteText.value = composant.test_fonctionnalite || ''
      showModalTestComposant.value = true
    }

    // --- Fermeture du modal ---
    const closeTestModal = () => {
      showModalTestComposant.value = false
      selectedComposant.value = null
      testFonctionnaliteText.value = ''
    }

    // --- Enregistrement (PATCH) ---
    const submitTestComposant = async () => {
      if (!selectedComposant.value) return

      savingTest.value = true
      try {
        const response = await axios.patch(
          `${API_CONFIG.LOCAL.BASE_URL}/composant-group/${selectedComposant.value.id}/`,
          { test_fonctionnalite: testFonctionnaliteText.value }
        )

        // Mise à jour locale dans la liste affichée, sans refetch complet
        const index = composantGroupList.value.findIndex(
          (c) => c.id === selectedComposant.value.id
        )
        if (index !== -1) {
          composantGroupList.value[index] = response.data
        }

        closeTestModal()
      } catch (err) {
        console.log(err)
      } finally {
        savingTest.value = false
      }
    }


    const openHistoriqueList  = () => {
      router.push('/admin/Historique-inventaire')
    }

</script>