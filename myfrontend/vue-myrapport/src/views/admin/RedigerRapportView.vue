<template>
    <PageBreadcrumbAdmin :pageTitle="currentPageTitle" />
    <div class="grid grid-cols-12 gap-4 md:gap-6">
      <div class="col-span-12 space-y-6 xl:col-span-7">
        <Entete
          v-model:destinataire="destinataire"
          v-model:cc="cc"
          v-model:cci="cci"
          v-model:objet="objet"
        />
      </div>
      <div class="col-span-12 xl:col-span-5">
        <Jointzone @update:files="files = $event"/>
      </div>
      <div class="col-span-12">
        <TextareMail v-model="message"/>
      </div>
    </div>
    <div class="my-2 flex justify-end">
      <SendBtn @click="sendEmail"/>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageBreadcrumbAdmin from '@/components/common/PageBreadcrumbAdmin.vue';
import Jointzone from '@/components/FormElement/Jointzone.vue';
import Entete from '@/components/space/Entete.vue';
import TextareMail from '@/components/space/TextareMail.vue';
import SendBtn from '@/components/buttons/SendBtn.vue';
import { useRoute } from 'vue-router';
import { useAlertNotifStore } from '@/stores/AlertNotif';
import axios from 'axios';
import API_CONFIG from '@/config/api';

const currentPageTitle = ref('Rapport')
const message = ref('')           // contenu textarea
const files = ref<File[]>([])     //piece joint

const alert = useAlertNotifStore()
const destinataire = ref<string[]>([])
const cc = ref('')
const cci = ref('')
const objet = ref('')

const route = useRoute()

const sendEmail = async () => {
  try {
    const formData = new FormData()

    // champs texte
    formData.append('objet', objet.value)
    formData.append('message', message.value)

    // tableaux emails
    destinataire.value.forEach(email => {
      formData.append('destinataire[]', email)
    })

    if (cc.value) formData.append('cc', cc.value)
    if (cci.value) formData.append('cci', cci.value)

    // fichiers
    files.value.forEach(file => {
      formData.append('files', file)
    })

    //re-fetch chaque fichier depuis son dowloadUrl
    for (const file of files.value) {
      const downloadUrl = (file as any).downloadUrl

      if (downloadUrl) {
        const response = await fetch(downloadUrl)
        const blob = await response.blob()
        const realFile = new File([blob], file.name, {type: file.type})
        formData.append('file', realFile)
      } else {
        //fichier pas encore uploadé par Dropzone
        formData.append('files', file)
      }
    }
    const res = await axios.post(`${API_CONFIG.LOCAL.BASE_URL}/send-email/`,formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    console.log('Email envoyé ', res.data)
    Object.assign(
      formData, {objet: '', message: '', destinataire: '', files: '',}
    )
     alert.showAlertNotif(
            "Email bien envoyé",
            "success"
          )

  } catch (error) {
    console.error('Erreur envoi ', error)
    alert.showAlertNotif(
            "Erreur! Email non envoyé",
            "error"
          )
  }
  console.log(files.value)
}
</script>