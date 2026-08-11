<template>
  <div class="file-uploader h-full flex flex-col">
    <form
      ref="dropzoneForm"
      :id="dropzoneId"
      :action="uploadUrl"
      class="h-full min-h-[5px] border-gray-300 border-dashed dropzone rounded-xl bg-gray-50 hover:border-brand-500 dark:border-gray-700 dark:bg-gray-900 dark:hover:border-brand-500"
    >
      <div class="dz-message m-0!">
        <div class="flex justify-center ">
          <div
            class="flex h-[60px] w-[200px] px-2 items-center justify-center rounded-lg bg-gray-200 text-gray-700 dark:bg-gray-800 dark:text-gray-400"
          >
            <svg 
              class="text-themeColor-500 w-5 h-5 mr-2" 
              xmlns="http://www.w3.org/2000/svg" 
              width="24" 
              height="24" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            > 
              <path 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
              /> 
            </svg> 
            Joindre un fichier ici
          </div>
        </div>

        <span
          class="mx-auto my-2 block w-full max-w-[290px] text-sm text-gray-700 dark:text-gray-400"
        >
          Images (JPEG, PNG, WEBP) + fichiers Word, Excel, TXT (max 100 Mo)
        </span>
        <!--
          <span class="font-medium underline cursor-pointer text-theme-sm text-brand-500">
            Browse File
          </span>
        -->
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Dropzone from 'dropzone'
import 'dropzone/dist/dropzone.css'

const props = defineProps({
  uploadUrl: {
    type: String,
    default: 'http://localhost:8000/upload/',
  },
})
const emit =defineEmits(['update:files'])
const files = ref<File[]>([])

const dropzoneForm = ref(null)
const dropzoneId = 'my-dropzone'  //`dropzone-${Math.random().toString(36).substring(2, 9)}`
const dropzoneInstance = ref<any>(null)


onMounted(() => {
  Dropzone.autoDiscover = false

  dropzoneInstance.value = new Dropzone(`#${dropzoneId}`, {
    url: props.uploadUrl,
    autoProcessQueue: true,
    paramName: "file", 
    uploadMultiple: false,
    thumbnailWidth: 150,
    maxFilesize: 200,
    acceptedFiles: `image/jpeg,image/png,image/gif,image/webp,image/svg+xml,.doc,.docx,.xls,.xlsx,.txt`,
    headers: { 'My-Awesome-Header': 'header value' },
    dictDefaultMessage: '',
    init: function () {
      this.on('addedfile', (file:any) => {
        files.value.push(file)
         emit('update:files', files.value)
        console.log('A file has been added', file)

        // bouton supprimer
        const removeBtn = document.createElement('button')
        removeBtn.innerHTML = '✖'
        removeBtn.className = `
          absolute top-1 right-1 
          bg-red-500 text-white 
          rounded-full w-6 h-6 
          flex items-center justify-center 
          text-xs hover:bg-red-600
        `

        // positionner le parent
        file.previewElement.style.position = 'relative'

        removeBtn.addEventListener('click', (e) => {
          e.preventDefault()
          e.stopPropagation()

          // supprime le fichier (déclenche removedfile)
          dropzoneInstance.value.removeFile(file)
        })

        file.previewElement.appendChild(removeBtn)

      })
      this.on('success', (file:any, response:any) => {
        console.log('File successfully uploaded', file, response)
        console.log(response.file_url)

        //lien téléchargeable
        file.downloadUrl = response.file_url
      })
      // telechargement marche avec un domaine pour plus tard
    //   this.on('success', (file, response) => {
    //   const link = document.createElement('a')
    //   link.href = response.file_url
    //   link.download = file.name
    //   link.innerText = "Télécharger"

    //   file.previewElement.appendChild(link)
    // })
      
      this.on('removedfile', async (file:any) => {
        console.log("Removing file...", file)

        if (!file.downloadUrl) return

        try {
          await fetch('http://localhost:8000/delete-file/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              file_url: file.downloadUrl,
            }),
          })

          console.log("File deleted from server")
        } catch (error) {
          console.error("Delete error:", error)
        }
      })
      this.on('error', (file, error) => {
        console.error('An error occurred during upload', file, error)
      })
    },
  })
})

onBeforeUnmount(() => {
  if (dropzoneInstance) {
    dropzoneInstance.value.destroy()
  }
})


</script>

<style>
.dropzone {
  border: 1px dashed #d0d5dd;
  transition: all 0.3s ease;
}

.dropzone:hover {
  border-color: #465fff;
}

.dropzone .dz-preview {
  margin: 10px;
   position: relative !important;
  overflow: visible !important; 
}

.dropzone .dz-preview button {
  z-index: 9999;
}

.dropzone .dz-preview .dz-image {
  border-radius: 8px;
}

.dropzone .dz-preview .dz-details {
  padding: 1em;
}

.dropzone .dz-preview .dz-progress {
  height: 10px;
}

.dropzone .dz-preview .dz-progress .dz-upload {
  background: #4f46e5;
}

.dark .dropzone {
  background-color: #111827;
  border-color: #374151;
}

.dark .dropzone:hover {
  border-color: #6366f1;
}
</style>
