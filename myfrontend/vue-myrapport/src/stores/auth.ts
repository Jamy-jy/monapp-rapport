import { defineStore } from 'pinia'
import axios from 'axios'

interface User {
  id: number
  nom: string
  prenom: string
  email: string
  role: 'admin' | 'tech'
  phone?:string
}


export const useAuthStore = defineStore('auth', {
  state: () => ({
    //sessionStorage pour distingué chaque session 
    token: sessionStorage.getItem('token') || null as string | null,
    user: JSON.parse(sessionStorage.getItem('user') || 'null') as User | null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin',
    fullName: (state) => state.user ? `${state.user.prenom} ${state.user.nom}` : '',
  },

  actions: {

    initAuth() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      }
    },
    
    async login(email: string, password: string) {
      const res = await axios.post('http://192.168.1.204/api/login/', { email, password })
      
      this.token = res.data.token
      this.user = res.data.user

      sessionStorage.setItem('token', res.data.token)
      sessionStorage.setItem('user', JSON.stringify(res.data.user))

      // Injection token dans tous les appels axios
      axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.token}`

      return res.data.user.role  // retourne le role pour la redirection
    },

    async logout() {
      try {
        await axios.post('http://localhost:8000/api/logout/', {}, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
      } catch (e) {
        //continuer même si backend échoue
      } finally {
        this.token = null
        this.user = null
        sessionStorage.removeItem('token')
        sessionStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
      }
    },

    updateUser(data: Partial<User>) {
      if (this.user) {
        this.user = { ...this.user, ...data }
        //  Mettre à jour sessionStorage aussi
        sessionStorage.setItem('user', JSON.stringify(this.user))
      }
    }
  }
})