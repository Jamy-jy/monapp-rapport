<template>
  <PageBreadcrumbTech :pageTitle="currentPageTitle"/>
    <form @submit.prevent="submitForm" class="space-y-6">
      <ComponentCard title="Imprimante">
        <div class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
          <div class="max-w-full overflow-x-auto custom-scrollbar">
            <table class="min-w-full">
              <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                  
                  <!-- Ligne 1 : BoxOp -->
                  <tr class="border-b border-gray-200 dark:border-gray-700 font-medium text-gray-500 text-theme-xs dark:text-gray-400">
                    <td class="text-center py-4">Box Op</td>
                    <td 
                        v-for="box in boxOps" 
                        :key="box.id"
                        class="text-center py-4"
                    >
                        {{ box.numero_boxOp }}
                    </td>
                  </tr>
    
                  <!-- Ligne 2 : nb copie -->
                  <tr class="dark:border-gray-700 font-medium text-gray-500 text-theme-xs dark:text-gray-400">
                    <td class="text-center">Nombre copie</td>
                    <td 
                        v-for="(box, index) in boxOps" 
                        :key="box.id"
                        
                    >
                        <input
                        type="number"
                        v-model="copies[index]"
                        class="dark:bg-dark-900 w-full text-center font-medium text-gray-500 text-theme-sm dark:text-gray-400 bg-transparent px-4 py-4 text-sm text-gray-800 outline-none dark:text-white/90"
                        />
                    </td>
                  </tr>
    
              </tbody>
            </table>
    
            
          </div>  
        </div>  
        <div class="flex justify-end mt-4">
          <SaveBtn/>
        </div>
      </ComponentCard>
    </form>

    <form @submit.prevent="saveAll" class="mt-6">
      <ComponentCard title="Encre">
        <ConsoImprimante 
            v-model:products="encreProducts"
            :boxops="encreBoxops"
            :editable="true"
        />
        <div class="flex justify-end mt-4">
          <SaveBtn/>
        </div>
      </ComponentCard>
    </form>
    
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ComponentCard from '@/components/common/ComponentCard.vue'
import PageBreadcrumbTech from '@/components/common/PageBreadcrumbTech.vue'
import SaveBtn from '@/components/buttons/SaveBtn.vue'
import { useAlertNotifStore } from '@/stores/AlertNotif'
import ConsoImprimante from '@/components/dashboard/ConsoImprimante.vue'
import API_CONFIG from '@/config/api'

const currentPageTitle = ref('Imprimante')
const alert = useAlertNotifStore()

const boxOps = ref<any[]>([])
const copies = ref<number[]>([])

const encreProducts = ref<any[]>([])
const encreBoxops = ref<any[]>([])


// fetch boxOp
const fetchBoxOps = async () => {
  const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/boxop/`)
  boxOps.value = res.data

  // init copies
  copies.value = boxOps.value.map(() => 0)
}

// submit
const submitForm = async () => {
  const payload = boxOps.value.map((box, index) => ({
    boxOp: box.id,
    nb_copie: copies.value[index]
  }))

  try {
    await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/imprimante/`, payload)
     alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )
  } catch (err) {
    console.error(err)
    alert.showAlertNotif(
      "Une erreur s'est prouduit lors de l'enregistrement",
      "error"
    )
  }
}

const fetchEncre = async () => {
        try {
            const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/encre/`)

            // boxop
            encreBoxops.value = res.data.boxops

            encreProducts.value = res.data.data.map((row: any) => ({
            couleur: row.couleur,
            couleur_id: row.couleur_id,
            nbr_bouteil: row.reserve,
            status: row.status,
            // niveaux : { boxop_id: '' }
            niveaux: Object.fromEntries(
                Object.entries(row.niveaux).map(([boxId, info]: [string, any]) => [
                Number(boxId),
                info.niveau + '%'
                ])
            )
            }))

        } catch (err) {
            console.error('Erreur chargement encre:', err)
        }
    }

//Enregistrer tout en un seul clic
const saveAll = async () => {
  try {
    for (const product of encreProducts.value) {

      //Sauvegarder la réserve
      await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/encre/reserve/`, {
        couleur_id: product.couleur_id,
        reserve: Number(product.nbr_bouteil),
      })

      //Sauvegarder chaque niveau par boxop
      for (const [boxId, niveau] of Object.entries(product.niveaux)) {
        // '75%' -> 75 | 'Vide' -> 0
        const niveauInt = parseInt((niveau as string).replace('%', '')) || 0

        console.log('Envoi niveau:', {
          couleur_id: product.couleur_id,
          boxop_id: Number(boxId),
          niveau: niveauInt,
        })

        await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/api/encre/update/`, {
          couleur_id: product.couleur_id,
          boxop_id: Number(boxId),
          niveau: niveauInt,  
        })
      }
    }

    console.log('Tout enregistré')
    alert.showAlertNotif(
      "Enregistrement effectué avec succès",
      "success"
    )
    await fetchEncre()  // rafraîchir après sauvegarde

  } catch (err) {
    if (axios.isAxiosError(err)) {
      console.error('Erreur sauvegarde:', err.response?.data)
    } else {
      console.error('Erreur sauvegarde:', err)
      alert.showAlertNotif(
        "Une erreur s'est produite lors de l'enregistrement",
        "success"
      )
    }
  }
}
onMounted(() => {
  fetchEncre()
  fetchBoxOps()
})
</script>