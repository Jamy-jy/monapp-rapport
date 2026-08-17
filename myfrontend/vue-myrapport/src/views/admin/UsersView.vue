<template>
  <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />
    <div>
      <form @submit.prevent="submitForm" class="space-y-6">
        <ComponentCard title="Nouvel utilisateur">
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <!--
              <PlaceholderInput
              v-model="userID"
              label="ID"
              placeholder="Entrez l'ID"
            />
            -->
            <div>
              <PlaceholderInput
                v-model="user.nom"
                label="Nom"
                placeholder="Entrez le nom"
              />
              <p v-if="serverErrors.nom" class="text-red-500 text-sm mt-1">
                {{ serverErrors.nom }}
              </p>
            </div>
            <div>
              <PlaceholderInput
                v-model="user.prenom"
                label="Prenom"
                placeholder="Entrez le prenom"
              />
              <p v-if="serverErrors.prenom" class="text-red-500 text-sm mt-1">
                {{ serverErrors.prenom }}
              </p>
            </div>
            <div>
              <EmailInput
              v-model="user.email"  
              label="Email"
              placeholder="ExempleEmail@gmail.com"
              type="email"
              />
              <p v-if="serverErrors.email" class="text-red-500 text-sm mt-1">
                {{ serverErrors.email }}
              </p>
            </div>
            <div>
              <PlaceholderInput
              v-model="user.phone"
              label="Téléphone"
              placeholder="03X XXX XX XX"
              />
              <p v-if="phoneError" class="text-red-500 text-sm mt-1">
                {{ phoneError }}
              </p>
              <p v-if="serverErrors.phone" class="text-red-500 text-sm mt-1">
                {{ serverErrors.phone }}
              </p>
            </div>
            <div>
              <PasswordInput
              v-model="formData.password"
              />
              <p v-if="passwordError" class="text-red-500 text-sm mt-1">
                {{ passwordError }}
              </p>
              <p v-if="serverErrors.password" class="text-red-500 text-sm mt-1">
                {{ serverErrors.password }}
              </p>
            </div>
            <PasswordInput
            label="Confirmer votre mot de passe"
            v-model="formData.confirmPassword"
            placeholder="Entrez une même mot de passe"
            />
            <SelectInput
              label="Role"
              placeholder="choisissez un role"
              :options="roleOptions"
              v-model="formData.role"
            />
          </div>
           <div class="flex gap-4 mt-4 justify-end">
              <SaveBtn/>
          </div>
        </ComponentCard>
      </form>
    </div>
</template>
    
<script setup lang="ts">
import { ref,reactive, computed } from 'vue'
import axios from 'axios'
import ComponentCard from '@/components/common/ComponentCard.vue';
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
import PlaceholderInput from '@/components/FormElement/PlaceholderInput.vue';
import SelectInput from '@/components/FormElement/SelectInput.vue';
import PasswordInput from '@/components/FormElement/PasswordInput.vue';
import EmailInput from '@/components/FormElement/EmailInput.vue';
import SaveBtn from '@/components/buttons/SaveBtn.vue';
import { useAlertNotifStore } from '@/stores/AlertNotif';
import API_CONFIG from '@/config/api';

const currentPageTitle = ref('Ajout utilisateur')

const alert = useAlertNotifStore()

const user = reactive({
  nom: '',
  prenom: '',
  phone: '',
  email: '',
})


interface Option{
  label: string
  value: string | number
}

const roleOptions: Option[] = [
  {label: "Administrateur", value: "admin"},
  {label: "Techinicien", value: "tech"}
]

const formData = reactive({
  role: '',
  password: '',
  confirmPassword: '',
})

const serverErrors = reactive<Record<string, string>>({})

//validation password
const passwordError = computed(() => {
  if (!formData.confirmPassword) return ''
  if (formData.password.length <6) return 'Le mot de passe est trop court, au moins 6 caractères'
  if (formData.password !== formData.confirmPassword) {
    return 'Les mots de passe ne correspondent pas'
  }

  return ''
})

//Validation phone
const phoneError = computed(() => {
  if (!user.phone) return ''
  const digits = user.phone.replace(/\s/g, '')
  if (!/^\d+$/.test(digits)) return 'Le numéro doit contenir uniquement des chiffres'
  if (digits.length !== 10) return `${digits.length}/10 chiffres - exactement 10 requis`
  return ''
})

const submitForm = async () => {
  if (passwordError.value || phoneError.value) return

  const { confirmPassword, ... restForm} = formData

  const payload = {
    ... user,
    ... restForm,
  }

  //Nettoyer les erreurs serveur
  Object.keys(serverErrors).forEach(k => delete serverErrors[k])

  try {
    const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/users/`, payload )
    console.log('Utilisateur ajouté', res.data)

    //reset formulaire
    Object.assign(
      user, {nom: '', prenom: '', phone: '', email: ''}, 
      formData, {role: '', password: '', confirmPassword: '',}
    )
     alert.showAlertNotif(
            "Enregistrement effectué avec succès",
            "success"
          )

  } catch (err) {
    if (axios.isAxiosError(err) && err.response?.data) {

      Object.assign(serverErrors, err.response.data)
      alert.showAlertNotif(
            "Attention! certain champs sont vide, faut bien les remplir",
            "warning"
          )

      console.error(err.response?.data)
    } else {
      console.error(err)
       alert.showAlertNotif(
            "une erreur s'est produit lors de la suppression",
            "error"
          )
    }
  }
}
</script>
