<template>
    <DestinataireInput
        :modelValue="destinataire"
        @update:modelValue="val => emit('update:destinataire', val)"
        @update:cc="val => emit('update:cc', val)"
        @update:cci="val => emit('update:cci', val)"
    />
    <Inputgroup 
        :modelValue="objet"
        @update:modelValue="val => emit('update:objet', val)"
        label="Objet :"
        type="text"
        placeholder="Entrez l'objet du rapport"
    />
</template>

<script setup lang="ts">

import Inputgroup from '../FormElement/Inputgroup.vue';
import DestinataireInput from './DestinataireInput.vue';

const props = withDefaults(defineProps<{
    destinataire?: string[]
    cc?: string
    cci?: string
    objet?: string
}>(), {
    destinataire: () => [],
    cc: "",
    cci: "",
    objet: ""
})

const emit = defineEmits([
    "update:destinataire",
    "update:cc",
    "update:cci",
    "update:objet"
])


</script>