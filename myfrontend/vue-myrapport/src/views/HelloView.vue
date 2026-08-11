<script setup>
    import {ref, onMounted} from 'vue'
    import api from '../services/api'

    const message = ref('chargement...')

    onMounted(async () => {
        try{
            const response = await api.get('/api/hello/')
            message.value = response.data.message
        } catch (error) {
            message.value = 'Erreur de connexion au backend'
            console.error(error)
        }
    })
</script>

<template>
    <div>
        <h1> Vue -> django (Axios) </h1>
        <p> {{ message }} </p>
    </div>
</template>