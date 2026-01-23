// main.js
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'
import './assets/personalice.css'   // 👈 Importación global

import { useAuthStore } from '@/stores/auth' // ✅ Importar store

// ✅ Cargar token desde localStorage
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// 1. Colores - Paleta Poder Judicial (Rojo y Plomo)
const myCustomThemes = {
  light: {
    colors: {
      background: '#F8F9FA',
      surface: '#FFFFFF',
      primary: '#9A1413',
      secondary: '#2c3e50',
      error: '#c41d1c',
      info: '#34495e',
      success: '#27ae60',
      warning: '#f39c12',
    }
  }
}

// 2. Config Vuetify
const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: myCustomThemes,
  }
})

// 3. Crear app
const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

// ✅ Ejecutar checkAuth antes de montar
const auth = useAuthStore()
auth.checkAuth().then(() => {
  app.mount('#app')
})
