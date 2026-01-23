import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import BlankLayout from '../layouts/BlankLayout.vue'

const routes = [
  {
    path: '/',
    component: BlankLayout,
    children: [
      { path: '', name: 'Login', component: () => import('@/views/LoginView.vue') }
    ]
  },


  /* -------------------------------- PERFIL -------------------------------- */
  {
    path: '/perfil',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '', // La ruta hija vacía para /dashboard
        name: 'Perfil',
        component: () => import('@/views/PerfilView.vue'),
      },
    ]
  },

  /* -------------------------------- TIPO DE EVENTOS -------------------------------- */
  {
    path: '/tipos_eventos',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '', // 
        name: 'Home',
        component: () => import('@/views/HomeView.vue'),
      },
    ]
  },

  /* -------------------------------- EVENTOS -------------------------------- */
  {
    path: '/eventos',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: ':idTipoEvento', // La ruta hija vacía para /dashboard
        name: 'Eventos',
        component: () => import('@/views/EventosView.vue'),
        props: true,
      },
    ]
  },

  /* -------------------------------- ASISTENTES -------------------------------- */
  {
    path: '/asistentes',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: ':idEvento', // La ruta hija vacía para /dashboard
        name: 'Asistentes',
        component: () => import('@/views/AsistentesView.vue'),
        props: true,
      },
    ]
  },

  /* -------------------------------- EVENTOS -------------------------------- */
  {
    path: '/usuarios',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '', // La ruta hija vacía para /dashboard
        name: 'Useff',
        component: () => import('@/views/UsuariosView.vue'),
      },
    ]
  },

  /* -------------------------------- EVENTOS -------------------------------- */
  {
    path: '/personas',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '', // La ruta hija vacía para /dashboard
        name: 'Perosnas',
        component: () => import('@/views/PersonasView.vue'),
      },
    ]
  },

  /* -------------------------------- EXAMENES -------------------------------- */
  {
    path: '/examenes',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Examenes',
        component: () => import('@/views/ExamenesView.vue'),
      },
    ]
  },

  /* -------------------------------- EXAMENES - EVENTOS -------------------------------- */
  {
    path: '/examenes/eventos',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'EventosExamenes',
        component: () => import('@/views/EventosExamenesView.vue'),
      },
    ]
  },

  /* -------------------------------- EXAMENES - INSCRITOS POR EVENTO -------------------------------- */
  {
    path: '/examenes/eventos/:idEvento',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'InscritosExamenes',
        component: () => import('@/views/InscritosExamenesView.vue'),
        props: true,
      },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = !!localStorage.getItem('token')

  if (requiresAuth && !isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router