import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import AdminLayout from '@/components/layouts/admin/AdminLayout.vue'
import TechLayout from '@/components/layouts/tech/TechLayout.vue'
import DashboardView from '@/views/admin/DashboardView.vue'
import UsersView from '@/views/admin/UsersView.vue'
import ConsommablesView from '@/views/admin/ConsommablesView.vue'
import EmailsView from '@/views/admin/EmailsView.vue'
import ListeUsersView from '@/views/admin/ListeUsersView.vue'
import DashboardTechView from '@/views/tech/DashboardTechView.vue'
import BobineView from '@/views/tech/BobineView.vue'
import TechConsultRapportView from '@/views/tech/TechConsultRapportView.vue'
import RedigerRapportView from '@/views/admin/RedigerRapportView.vue'
import ConsultRapportView from '@/views/admin/ConsultRapportView.vue'
import EmailEnvoieView from '@/views/admin/EmailEnvoieView.vue'
import FaireRapportView from '@/views/tech/FaireRapportView.vue'
import MoveVolView from '@/views/tech/MoveVolView.vue'
import ImprimanteView from '@/views/tech/ImprimanteView.vue'
import TechEmailEnvoieView from '@/views/tech/TechEmailEnvoieView.vue'
import AdminProfilView from '@/views/admin/AdminProfilView.vue'
import UserProfilView from '@/views/tech/UserProfilView.vue'
import EmailDetailAdminView from '@/views/admin/EmailDetailAdminView.vue'
import EmailDetailTechView from '@/views/tech/EmailDetailTechView.vue'
import BoxOfficeView from '@/views/admin/BoxOfficeView.vue'
import StockView from '@/views/tech/StockView.vue'
import SejourVisaView from '@/views/admin/SejourVisaView.vue'
import HistoriqueView from '@/views/admin/HistoriqueView.vue'
import ModelView from '@/views/tech/ModelView.vue'
import SystemeView from '@/views/admin/SystemeView.vue'
import MaterielView from '@/views/admin/MaterielView.vue'
import ReseauView from '@/views/admin/ReseauView.vue'
import IncidentechlView from '@/views/tech/IncidentechlView.vue'
import HistoriqueIncidentView from '@/views/admin/HistoriqueIncidentView.vue'
import MessagingAdminView from '@/views/admin/MessagingAdminView.vue'
import MessagingTechView  from '@/views/tech/MessagingTechView.vue'
import stockBureauView from '@/views/admin/stockBureauView.vue'
import InventaireView from '@/views/admin/InventaireView.vue'
import InventaireTechView from '@/views/tech/InventaireTechView.vue'
import HistoriqueinventaireView from '@/views/admin/HistoriqueinventaireView.vue'
/* import { title } from 'process' */

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left:0, top: 0 }
  },
  routes: [
    {
      path:'/',
      redirect:'/login',
    },
    {
      path: '/login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: {guestOnly: true, title: 'login'}
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { 
        requiresAuth: true, 
        role: 'admin' 
      },
      children: [
        {
          path:'',
          name: 'admin-dashboard',
          component: DashboardView,
          meta: {
            title: 'Tableau de bord',
          }
        },
        { 
          path: 'users', 
          name: 'users',
          component: UsersView,
          meta: {
            title: 'Ajout utilisateur',
          }
        },
        {
          path: 'liste_users', 
          name: 'liste_users',
          component: ListeUsersView,
          meta: {
            title: 'liste des utilisateurs',
          }
        },
        {
          path: 'box',
          name: 'Box office',
          component: BoxOfficeView,
          meta: {
            title: 'Box office',
          }
        },
        { 
          path: 'consommables',
          name: 'consommables', 
          component: ConsommablesView,
          meta: {
            title: 'Parametrage consommables',
          }
        },
        {
          path: 'inventaire',
          name:'inventaire',
          component: InventaireView,
          meta: {
            title: 'groupe inventaire',
          }

        },
        {
          path: 'stockBureau',
          name: 'stockBureau',
          component: stockBureauView,
          meta: {
            title: 'mouvement stock'
          }
        },
        { 
          path: 'emails',
          name: 'emails',
          component: EmailsView,
          meta: {
            tilte: 'Email Destinataires'
          } 
        },
        {
          path: 'sejour',
          name: 'sejour',
          component: SejourVisaView,
          meta: {
            title: 'Sejour visa'
          }
        },
        {
          path: 'systeme',
          name: 'systeme',
          component: SystemeView,
          meta: {
            title: 'système',
          }
        },
        {
          path: 'materiel',
          name: 'materiel',
          component: MaterielView,
          meta: {
            title: 'materiels',
          }
        },
        {
          path: 'reseau',
          name: 'reseau',
          component: ReseauView,
          meta: {
            title: 'reseau',
          }
        },
        { 
          path: 'rediger', 
          name: 'rediger',
          component: RedigerRapportView,
          meta: {
            title: 'Rediger'
          }
        },
        { 
          path: 'consulter', 
          name: 'consulter',
          component: ConsultRapportView,
          meta: {
            title: 'Consulter'
          }
        },
        { 
          path: 'emailEnvoie', 
          name: 'emailEnvoie',
          component: EmailEnvoieView,
          meta: {
            title: 'EmailEnvoie'
          }
        },
        {
          path: 'profile',
          name: 'admin-Profile',
          component: AdminProfilView,
          meta: {
            title: 'Profile',
          },
        },
        {
          path: 'historique',
          name: 'historique',
          component: HistoriqueView,
          meta: {
            title: 'Historique',
          }
        },
        {
          path: 'emails/:id',
          name: 'Email DetailAdmin',
          component: EmailDetailAdminView,
          meta: {
            requiresAuth: true,
            title: 'EmailDetailAdmin',
          }
        },
        {
          path: 'Historique-incidents',
          name: 'historique incidents',
          component: HistoriqueIncidentView,
          meta: {
            title: 'Historique Incidents'
          }
        },
        {
          path: 'Historique-inventaire',
          name: 'historique inventaire',
          component: HistoriqueinventaireView,
          meta: {
            title: 'Historique inventaire'
          }
        },
        {
          path: 'messaging',
          name: 'admin-messaging',
          component: MessagingAdminView,
          meta: {
            title: 'Messagerie',
          }
        },
        {
          path: 'messaging/:convId',
          name: 'admin-messaging-conv',
          component: MessagingAdminView,
          meta: {
            title: 'Messagerie',
          }
        },
      ],
    },
    {
      path: '/tech',
      component: TechLayout,
      meta: { 
        requiresAuth: true, 
        role: 'tech' 
      },
      children: [
        {
          path:'',
          name: 'tech',
          component: DashboardTechView,
          meta: {
            title : 'Tableau de bord',
          }
        },
        { 
          path: 'bobine', 
          name: 'bobine',
          component: BobineView,
          meta: {
            title: 'Mouvement du Bobine',
          }
        },
        { 
          path: 'stock', 
          name: 'Stock',
          component: StockView,
          meta: {
            title: 'Mouvement de stock',
          }
        },   
        {
          path: 'imprimante',
          name: 'imprimante',
          component: ImprimanteView,
          meta: {
            title: 'Imprimante',
          }
        },
        {
          path: 'MoveVol',
          name: 'MoveVol',
          component: MoveVolView,
          meta: {
            title: 'Mouvemeent du Vol'
          }
        },  
        {
          path: 'Incidents',
          name: 'Incidents',
          component: IncidentechlView,
          meta: {
            title: 'Incidents'
          }
        },
        {
          path: 'Inventaire-tech',
          name: 'Inventaire-tech',
          component: InventaireTechView,
          meta: {
            title: 'Inventaire-tech'
          }
        },    
        {
          path: 'redigeRapport',
          name: 'FaireRapport',
          component: FaireRapportView,
          meta: {
            title: 'Faire du Rapport',
          }
        },
        { 
          path: 'TechConsultingRapport', 
          name: 'ConsulterRapport',
          component: TechConsultRapportView,
          meta: {
            title: 'consultation du Rapport',
          } 
        },
        { 
          path: 'TechEmailEnvoie', 
          name: 'TechEmailEnvoie',
          component: TechEmailEnvoieView,
          meta: {
            title: 'TechEmailEnvoie'
          }
        },
        {
          path: 'profile',
          name: 'tech-Profile',
          component: UserProfilView,
          meta: {
            title: 'Profile',
          },
        },
        {
          path: 'emails/:id',
          name: 'Email DetailTech',
          component: EmailDetailTechView,
          meta: {
            requiresAuth: true,
            title: 'EmailDetail',
          }
        },
        {
          path: 'modele',
          name: 'modele',
          component: ModelView,
          meta: {
            requiresAuth: true,
            role: 'tech',
            title: 'Modèle'
          }
        },
        {
          path: 'messaging',
          name: 'tech-messaging',
          component: MessagingTechView,
          meta: {
            title: 'Messagerie',
          }
        },
        {
          path: 'messaging/:convId',
          name: 'tech-messaging-conv',
          component: MessagingTechView,
          meta: {
            title: 'Messagerie',
          }
        },
      ],
    },
    
  ],
})


router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuth = authStore.isAuthenticated
  const role = authStore.user?.role

  console.log('GUARD ->', {
    to: to.path,
    isAuth,
    role,
    meta: to.meta
  })
  
  // Si déjà connecté, rediriger vers son espace
  if (to.meta.guestOnly && isAuth) {
    const target = role === 'admin' ? '/admin' : '/tech'
    if (to.path === target) return next()
    return next(target)
  }

  // Page protégée → si non connecté
  if (to.meta.requiresAuth && !isAuth) {
    if (to.path === '/login') return next()
    return next('/login')
  }

  // Fix — vérifier le rôle uniquement si to.meta.role est défini
  // Les children n'ont pas de meta.role donc on ignore la vérification
  if (to.meta.requiresAuth && to.meta.role && role !== to.meta.role) {
    const target = role === 'admin' ? '/admin' : '/tech'
    if (to.path === target) return next()
    return next(target)
  }

  // Fix — vérifier le rôle via le parent pour les children
  // Un tech ne peut pas accéder aux routes /admin/... et vice versa
  if (isAuth) {
    if (to.path.startsWith('/admin') && role !== 'admin') {
      return next('/tech')
    }
    if (to.path.startsWith('/tech') && role !== 'tech') {
      return next('/admin')
    }
  }

  document.title = `Vue.js ${to.meta.title} | rapport consommable`
  next()
})

export default router