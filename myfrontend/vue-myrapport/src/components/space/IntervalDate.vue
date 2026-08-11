<template>
    <div class="col-span-12 xl:col-span-5">
        <div class="grid mb-2 grid-cols-1 gap-4 sm:grid-cols-4">
          <SelectInput
              label="item"
              placeholder="choisissez le item"
              :options="tableOptions"
              v-model="formData.table"
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
              <ExportIcon/>
              Joindre
            </button>
        </div>
      </div>
</template>
<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import SelectInput from '../FormElement/SelectInput.vue'
import PlaceholderInput from '../FormElement/PlaceholderInput.vue'
import ExportIcon from '@/icons/ExportIcon.vue'

interface Model {
  table: string
  dateDebut: string
  dateFin: string
}

const props = defineProps<{
  modelValue: Model
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: Model): void
  (e: 'submit', value: Model): void
}>()

const dateDebut = ref(props.modelValue.dateDebut || '')
const dateFin = ref(props.modelValue.dateFin || '')

const formData = reactive({
  table: props.modelValue.table || ''
})

const tableOptions = ref([
  { label: 'stock', value: 'stock' },
  { label: 'vol', value: 'vol' }
])

watch(
  [() => formData.table, dateDebut, dateFin],
  () => {
    emit('update:modelValue', {
      table: formData.table,
      dateDebut: dateDebut.value,
      dateFin: dateFin.value
    })
  }
)

const handelClick = () => {
  emit('submit', {
    table: formData.table,
    dateDebut: dateDebut.value,
    dateFin: dateFin.value
  })
}
</script>
