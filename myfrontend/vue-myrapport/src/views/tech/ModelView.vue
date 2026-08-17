<template>
    <PageBreadcrumbTech :pageTitle="currentPageTitle"/>
    <div class="mb-6 col-span-12 flex items-center gap-4 xl:col-span-7">
          <p
           class="text-sm font-medium text-gray-700 cursor-pointer select-none dark:text-gray-400"
           >Modèle: 
          </p>
        <div class="flex-1">
          <SelectInput
            placeholder="Choisissez votre modèle"
            v-model="selectedModele"
            :options="modeles"/>
        </div>
    </div>
    <ComponentCard :title="cardTitle">
      <TextareaInput v-model="modelValue"/>
      <div class="flex gap-4 mt-4 justify-end">
          <SaveBtn 
            v-if="!isEditing"
            @click="saveModel"
          />
          <template v-else>
            <CanceleBtn
              @click="cancelEdit"
            />
            <UpdateBtn
              @click="updateModel"
            />
            <DeleteBtn
              @click="deleteModel"
            />
        </template>
      </div>
    </ComponentCard>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import PageBreadcrumbTech from '@/components/common/PageBreadcrumbTech.vue';
import SelectInput from '@/components/FormElement/SelectInput.vue';
import ComponentCard from '@/components/common/ComponentCard.vue';
import TextareaInput from '@/components/FormElement/TextareaInput.vue';
import SaveBtn from '@/components/buttons/SaveBtn.vue';
import axios from 'axios';
import { useAlertNotifStore } from '@/stores/AlertNotif';
import CanceleBtn from '@/components/buttons/CanceleBtn.vue';
import UpdateBtn from '@/components/buttons/UpdateBtn.vue';
import DeleteBtn from '@/components/buttons/DeleteBtn.vue';
import API_CONFIG from '@/config/api';


const currentPageTitle = ref('Modèle')

const modelValue = ref("")

const selectedModele = ref('')

const alert = useAlertNotifStore()

const isEditing = computed(() => selectedModele.value !== '')

const cardTitle = computed(() => {
  return isEditing.value
    ? 'Modification/Suppression Modèle'
    : 'Nouvel Modèle'
})

interface Option{
  label: string
  value: string | number
  text: string
}

const cancelEdit = () => {
  selectedModele.value = ''
  modelValue.value = ''
}

const saveModel = async () => {
  try {
    await axios.post(`http://127.0.0.1:8000/api/text-model/create/`, {
      text: modelValue.value,
    })
    alert.showAlertNotif(
        "Modèle bien enregistré",
        "success"
    )
    console.log("Modèle enregistré")

    modelValue.value = ""
  } catch (error) {
    console.error(error)
    alert.showAlertNotif(
      "Une erreur s'est produite lors de l'enregistrement",
      "error"
    )
  }
}

const modeles = ref<Option[]>([])

//affichage consommable dans select
const fetchModeles = async () => {
  try {
    const res = await axios.get(`${API_CONFIG.LOCAL.BASE_URL}/api/text-model/list/`)
    //Transformer en format Option { label, value }
    modeles.value = res.data.map((m: any) => ({
      label: m.text,
      value: m.id,
      text: m.text
    }))
  } catch (err) {
    console.error('Erreur chargement modèles:', err)
  }
}

//emporté dans la tesxt email
watch(selectedModele, (newVal) => {
    console.log('selected:', newVal)
    const modele = modeles.value.find(
      (m) => String(m.value) === String(newVal)
    )
    
    console.log('modele trouvé:', modele)
    if (modele) {
      modelValue.value = modele.text  // texte complet dans TextareMail
    } else {
      modelValue.value = ''
    }
  })

onMounted(() => {
  fetchModeles()
})

//Modification du texte
const updateModel = async () => {
  try {
    await axios.put(
      `http://127.0.0.1:8000/api/text-model/update/${selectedModele.value}/`,
      {
        text: modelValue.value,
      }
    )

    alert.showAlertNotif(
      "Modèle modifié avec succès",
      "success"
    )

    fetchModeles()
    modelValue.value = ""

  } catch (error) {
    console.error(error)
    alert.showAlertNotif(
          "Une erreur s'est produite lors de la modification",
          "error"
        )
  }
}

//Suppression du texte
const deleteModel = async () => {
  try {
    await axios.delete(
      `http://127.0.0.1:8000/api/text-model/delete/${selectedModele.value}/`
    )

    alert.showAlertNotif(
      "Modèle supprimé avec succès",
      "success"
    )

    cancelEdit()
    fetchModeles()
    modelValue.value = ""

  } catch (error) {
    console.error(error)
    alert.showAlertNotif(
          "Suppression interrompu",
          "error"
        )
  }
}

</script>