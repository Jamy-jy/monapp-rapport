import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Réinjecter le token dès le démarrage
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
authStore.initAuth() 

app.mount('#app')
