<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>Nouvelle conversation</h2>

      <!-- Type -->
      <div class="tabs">
        <button :class="{ active: mode === 'private' }" @click="mode = 'private'">Privée</button>
        <button :class="{ active: mode === 'group' }"   @click="mode = 'group'">Groupe</button>
      </div>

      <!-- Nom du groupe -->
      <input v-if="mode === 'group'" v-model="groupName"
             placeholder="Nom du groupe" class="input" />

      <!-- Sélection multiple des techs -->
      <div class="tech-list">
        <label v-for="tech in techList" :key="tech.id" class="tech-item">
          <input type="checkbox" :value="tech.id" v-model="selectedTechs" />
          <span class="avatar">{{ tech.username[0].toUpperCase() }}</span>
          <span>{{ tech.username }}</span>
        </label>
      </div>

      <div class="modal-actions">
        <button class="btn btn-secondary" @click="$emit('close')">Annuler</button>
        <button class="btn btn-primary" :disabled="!canCreate" @click="create">
          Créer
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMessagingStore } from '@/stores/messaging'
import axios from 'axios'

const emit  = defineEmits(['close', 'created'])
const store = useMessagingStore()

const mode          = ref('private')
const groupName     = ref('')
const selectedTechs = ref([])
const techList      = ref([])

onMounted(async () => {
  const { data } = await axios.get('/api/users/?role=tech')
  techList.value = data
})

const canCreate = computed(() => {
  if (!selectedTechs.value.length) return false
  if (mode.value === 'group' && !groupName.value.trim()) return false
  return true
})

async function create() {
  if (mode.value === 'private') {
    await store.createPrivateConv(selectedTechs.value)
  } else {
    await store.createGroup(groupName.value, selectedTechs.value)
  }
  emit('created')
}
</script>