<template>
    <PageBreadcrumbAdmin :pageTitle='currentPageTitle'/>
    <div>
      <form @submit.prevent="submitFormPaf" class="space-y-6">
        <ComponentCard title="Box PAF">
          <div class="grid grid-cols-1 gap-12 sm:grid-cols-4">
            <div class="sm:col-span-3">
              <PlaceholderInput
                v-model="boxPaf.numero_boxPaf"
                label="Numéro Box PAF"
                placeholder="Entrez le numéro du box"
              />
              <p v-if="serverErrorsPaf.numero_boxPaf" class="text-red-500 text-sm mt-1">
                {{ serverErrorsPaf.numero_boxPaf }}
              </p>
            </div>
            <div class="sm:col-span-1 flex items-end">
              <SaveBtn class="w-full"/>
            </div>
          </div>
        </ComponentCard>
      </form>

      <form @submit.prevent="submitFormOp" class="mt-8">
        <ComponentCard title="Box Opérateur">
          <div class="grid grid-cols-1 gap-12 sm:grid-cols-4">
            <div class="sm:col-span-3">
              <PlaceholderInput
                v-model="boxOp.numero_boxOp"
                label="Numméro Box Opérateur"
                placeholder="Entrez le nom du box"
              />
              <p v-if="serverErrorsOp.numero_boxOp" class="text-red-500 text-sm mt-1">
                {{ serverErrorsOp.numero_boxOp }}
              </p>
            </div>
            <div class="sm:col-span-1 flex items-end">
              <SaveBtn class="w-full"/>
            </div>
          </div>
        </ComponentCard>
      </form>
    </div>

      
    <div class="grid grid-cols-12 gap-2 sm:grid-cols-2 my-8">
      <ComponentCard title="Boxe Operateure">
        <BaseTable 
          :columns="columnsOp" 
          :rows="BoxOp" 
          @edit="openEditModalOp"
          @delete="confirmDeleteOp"
          />
      </ComponentCard>
      
      <ComponentCard title="Boxe Paf">
        <BaseTable 
          :columns="columnsPaf" 
          :rows="BoxPaf" 
          @edit="openEditModalPaf"
          @delete="confirmDeletePaf"
          />
      </ComponentCard> 
    </div>

    <!-- modal modif paf-->
    <div
      v-if="showEditModalPaf"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
          Modifier le boxe paf
        </h2>

        <div class="space-y-3">
          <div>
            <PlaceholderInput
              v-model="editDataPaf.numero_boxPaf"
              label="Nom consommable"
              placeholder="Nom"
            />
            <p v-if="editErrorsPaf.numero_boxPaf" class="text-red-500 text-sm mt-1">
              {{ editErrorsPaf.numero_boxPaf }}
            </p>
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="showEditModalPaf = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="submitEditPaf"
            class="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Confirmation Suppression -->
    <div
      v-if="showDeleteModalPaf"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6 text-center">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          Confirmer la suppression
        </h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Voulez-vous vraiment supprimer
          <span class="font-medium text-gray-800 dark:text-white">
            {{ selectedPaf?.numero_boxPaf }}
          </span> ?
        </p>

        <div class="flex justify-center gap-3">
          <button
            @click="showDeleteModalPaf = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="submitDeletePaf"
            class="px-4 py-2 text-sm text-white bg-red-500 rounded-lg hover:bg-red-600"
          >
            Supprimer
          </button>
        </div>
      </div>
    </div>

    <!-- modal modif op-->
    <div
      v-if="showEditModalOp"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
          Modifier le boxe operateur
        </h2>

        <div class="space-y-3">
          <div>
            <PlaceholderInput
              v-model="editDataOp.numero_boxOp"
              label="Nom consommable"
              placeholder="Nom"
            />
            <p v-if="editErrorsOp.numero_boxOp" class="text-red-500 text-sm mt-1">
              {{ editErrorsOp.numero_boxOp }}
            </p>
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="showEditModalOp = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="submitEditOp"
            class="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Confirmation Suppression op-->
    <div
      v-if="showDeleteModalOp"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6 text-center">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          Confirmer la suppression
        </h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Voulez-vous vraiment supprimer
          <span class="font-medium text-gray-800 dark:text-white">
            {{ selectedOp?.numero_boxOp }}
          </span> ?
        </p>

        <div class="flex justify-center gap-3">
          <button
            @click="showDeleteModalOp = false"
            class="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            @click="submitDeleteOp"
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
    import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
    import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
    import SaveBtn from '@/components/buttons/SaveBtn.vue';
    import ComponentCard from '@/components/common/ComponentCard.vue';
    import BaseTable from '@/components/table/BaseTable.vue';
    import axios from 'axios';
    import ItemActions from '@/components/table/ItemActions.vue';
    import { useAlertNotifStore } from '@/stores/AlertNotif';
    import API_CONFIG from '@/config/api';
    

    const currentPageTitle = ref('Box office')

    const alert = useAlertNotifStore()

    /* boxe paf */
    const boxPaf = reactive ({
        numero_boxPaf: '',
    })

    const serverErrorsPaf = reactive<Record<string, string>>({})
   
    const submitFormPaf = async () => {
      try {
        const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/boxpaf/`, boxPaf)
        boxPaf.numero_boxPaf = ''
        await fetchPaf()
        console.log('Box PAF ajouté ', res.data)
        alert.showAlertNotif(
          "Enregistrement effectué avec succès",
          "success"
        )
        Object.assign(
          boxPaf, {numero_boxPaf: '',}, 
        )
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.data) {
          Object.assign(serverErrorsPaf, err.response.data)
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

    const BoxPaf = ref<any[]>([])

    const columnsPaf = [
      { label: 'id', field: 'id'},
      { label: 'numéro boxPaf', field: 'numero_boxPaf'},
      { label: 'Actions', render: ItemActions },
    ]

    const fetchPaf = async () => {
      try {
        const respaf = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/boxpaf/`)
        BoxPaf.value = respaf.data.map((p: any) => ({
          id: p.id,
          numero_boxPaf: p.numero_boxPaf
        }))
        console.log(BoxPaf.value)
      } catch (err){
        console.log(err)
      }
    }

    //modal modif paf
    const showEditModalPaf = ref(false)
    const selectedPafId = ref<number | null>(null)

    const editDataPaf = reactive({
      numero_boxPaf: '',
    })

    const editErrorsPaf = reactive<Record<string, string>>({})

    const openEditModalPaf = (row: any) => {
      selectedPafId.value = row.id
      editDataPaf.numero_boxPaf = row.numero_boxPaf
      Object.keys(editErrorsPaf).forEach(k => delete editErrorsPaf[k])
      showEditModalPaf.value = true
    }

    const submitEditPaf = async () => {
      if (!selectedPafId.value) return
      Object.keys(editErrorsPaf).forEach(k => delete editErrorsPaf[k])

      try {
        await axios.patch(`${API_CONFIG.LOCAL.BASE_URL}/api/boxpaf/${selectedPafId.value}/`, editDataPaf)
        showEditModalPaf.value = false
        await fetchPaf()
        alert.showAlertNotif(
          "Modification effectué avec succès!",
          "success"
        )
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.data) {
          Object.assign(editErrorsPaf, err.response.data)
        } else {
          console.error(err)
          alert.showAlertNotif(
            "Erreur lors de la modification",
            "error"
          )
        }
      }
    }

    // Modal suppression Paf
    const showDeleteModalPaf = ref(false)
    const selectedPaf = ref<any | null>(null)

    const confirmDeletePaf = (row: any) => {
      selectedPaf.value = row
      showDeleteModalPaf.value = true
    }

    const submitDeletePaf = async () => {
      if (!selectedPaf.value) return

      try {
        await axios.delete(`${API_CONFIG.LOCAL.BASE_URL}/api/boxpaf/${selectedPaf.value.id}/`)
        showDeleteModalPaf.value = false
        await fetchPaf()
        alert.showAlertNotif(
          `Le ${selectedPaf.value.numero_boxPaf} a été supprimé avec succès`,
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

    /* Boxe op */
    const boxOp = reactive ({
        numero_boxOp: '',
    })

    const serverErrorsOp = reactive<Record<string, string>>({})

    const submitFormOp = async () => {
      try {
        const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/boxop/`, boxOp )
        boxOp.numero_boxOp = ''
        await fetchOp()
        alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )
        Object.assign(
          boxOp, {numero_boxOp: '',}, 
        )
        console.log('Box opérateur ajouté ', res.data)
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.data) {
          Object.assign(serverErrorsOp, err.response.data)
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

    const BoxOp = ref<any[]>([])
  
    const columnsOp = [
      { label: 'id', field: 'id'},
      { label: 'numéro boxOp', field: 'numero_boxOp'},
      { label: 'Action', render: ItemActions}
    ]

    const fetchOp = async () => {
      try {
        const resop = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/boxop/`)
        BoxOp.value = resop.data.map((o: any) => ({
          id: o.id,
          numero_boxOp: o.numero_boxOp
        }))
        console.log(BoxOp.value)
      } catch (err){
        console.log(err)
      }
    }

    //modal modif Op
    const showEditModalOp = ref(false)
    const selectedOpId = ref<number | null>(null)

    const editDataOp = reactive({
      numero_boxOp: '',
    })

    const editErrorsOp = reactive<Record<string, string>>({})

    const openEditModalOp = (row: any) => {
      selectedOpId.value = row.id
      editDataOp.numero_boxOp = row.numero_boxOp
      Object.keys(editErrorsOp).forEach(k => delete editErrorsOp[k])
      showEditModalOp.value = true
    }

    const submitEditOp = async () => {
      if (!selectedOpId.value) return
      Object.keys(editErrorsOp).forEach(k => delete editErrorsOp[k])

      try {
        await axios.patch(`${API_CONFIG.LOCAL.BASE_URL}/api/boxop/${selectedOpId.value}/`, editDataOp)
        showEditModalOp.value = false
        await fetchOp()
        alert.showAlertNotif(
            "Modification effectué avec succès",
            "success"
          )
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.data) {
          Object.assign(editErrorsOp, err.response.data)
        } else {
          console.error(err)
          alert.showAlertNotif(
            "Erreur lors de la modification",
            "error"
          )
        }
      }
    }

    // Modal suppression Op
    const showDeleteModalOp = ref(false)
    const selectedOp = ref<any | null>(null)

    const confirmDeleteOp = (row: any) => {
      selectedOp.value = row
      showDeleteModalOp.value = true
    }

    const submitDeleteOp = async () => {
      if (!selectedOp.value) return

      try {
        await axios.delete(`${API_CONFIG.LOCAL.BASE_URL}/api/boxop/${selectedOp.value.id}/`)
        showDeleteModalOp.value = false
        await fetchOp()
        alert.showAlertNotif(
            `Le ${selectedOp.value.numero_boxOp} a été supprimé avec succès`,
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

    onMounted(() => {
      fetchPaf(),
      fetchOp()
    })
</script>