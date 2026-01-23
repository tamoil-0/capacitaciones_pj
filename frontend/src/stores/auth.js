import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: localStorage.getItem('token') || null,
        isAuthCheckComplete: false,
    }),

    actions: {
        async login(credentials) {
        try {
            const response = await axios.post('/api/login', credentials)
            const token = response.data.token

            this.token = token
            localStorage.setItem('token', token)
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

            this.user = response.data.user
            return this.user
        } catch (error) {
            throw error.response?.data?.message || 'Error al iniciar sesión'
        }
        },

        async getPerfil() {
        try {
            const response = await axios.get('/api/perfil')
            this.user = response.data.user
        } catch (e) {
            this.logout()
            console.error('Error obteniendo perfil:', e)
            throw e
        }
        },

        async checkAuth() {
        if (this.isAuthCheckComplete) return
            const token = localStorage.getItem('token')

        if (!token) {
            this.isAuthCheckComplete = true
            return
        }

        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
            try {
                await this.getPerfil()
            } catch (e) {
                // logout ya está dentro de getPerfil
            } finally {
                this.isAuthCheckComplete = true
            }
        },

        logout() {
            this.token = null
            this.user = null
            this.isAuthCheckComplete = true
            localStorage.removeItem('token')
            delete axios.defaults.headers.common['Authorization']
        }
    }
})
