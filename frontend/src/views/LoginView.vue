<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axios'

import fondo from "@/assets/img/fondo.png";
import img_login_web from "@/assets/img/login_web.jpg";
import img_login_mobile from "@/assets/img/login_mobile.png";

// --- FORM STATE ---
const loginForm = reactive({ nickname: '', password: '' })
const loginError = ref('')
const loginLoading = ref(false)
const loginFormRef = ref(null)

const router = useRouter()

// --- VALIDATION RULES ---
const rules = {
    required: v => !!v || 'Este campo es obligatorio',
    nickname: v => (!!v && !/\s/.test(v)) || 'El nickname no debe contener espacios'
}

// --- LOGIN FUNCTION ---
const login = async () => {
    loginError.value = ''
    const { valid } = await loginFormRef.value.validate()
    if (!valid) return

    loginLoading.value = true

    try {
        const { data } = await axios.post('/login', loginForm)

        // Guardar token
        localStorage.setItem('token', data.token)

        // Guardar usuario
        localStorage.setItem('usuario', JSON.stringify(data.usuario))

        // Guardar opciones de menú
        localStorage.setItem('opciones', JSON.stringify(data.opciones))

        // Redirigir a la primera opción
        if (data.opciones.length > 0) {
        router.push(data.opciones[0].ruta)
        } else {
        router.push('/')
        }
    } catch (err) {
        loginError.value = 'Credenciales incorrectas'
    } finally {
        loginLoading.value = false
    }
}
</script>

<template>
    <v-container 
        fluid
        class="login-view d-flex align-center justify-center"
        :style="{
            height: '100vh',
            backgroundImage: `url(${fondo})`,
            backgroundRepeat: 'repeat',
            backgroundSize: '100px 100px',
            backgroundPosition: 'center'
        }"
    >
        <v-card 
            elevation="10"
            class="d-flex flex-row flex-wrap"
            style="
                max-width: 800px; 
                width: 100%; 
                height: 400px;
                border-radius: 15px; 
                overflow: hidden; 
                background-color: white;"
        >
        <!-- Imagen lateral -->
        <v-col
            cols="12"
            md="6"
            class="p-0 hidden-sm-and-down"
            :style="{
            backgroundImage: `url(${img_login_web})`,
            backgroundSize: 'cover'
            }"
        ></v-col>

        <!-- Formulario -->
        <v-col
            cols="12"
            md="6"
            class="d-flex flex-column align-center justify-center"
            style="background: white;"
        >
            <v-img 
            :src="img_login_mobile"
            max-width="350"
            alt="Logo"
            style="display: none;" 
            class="responsive-img"
            />

            <v-card-title class="text-h5 font-weight-bold text-center">
            Inicio de Sesión
            </v-card-title>
            <v-card-subtitle class="text-center mb-6">
            Ingresa tus credenciales para continuar
            </v-card-subtitle>

            <v-form ref="loginFormRef" @submit.prevent="login" style="width: 100%; max-width: 300px;">
            <v-text-field
                v-model="loginForm.nickname"
                label="Usuario"
                placeholder="Ingrese su usuario"
                prepend-inner-icon="mdi-card-account-details-outline"
                variant="outlined"
                :rules="[rules.required, rules.nickname]"
                class="mb-3"
                required
            />

            <v-text-field
                v-model="loginForm.password"
                label="Contraseña"
                type="password"
                placeholder="Ingrese su contraseña"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                :rules="[rules.required]"
                required
            />

            <v-alert
                v-if="loginError"
                type="error"
                class="my-2"
                variant="tonal"
                density="compact"
            >
                {{ loginError }}
            </v-alert>

            <v-btn
                :loading="loginLoading"
                type="submit"
                color="primary"
                size="large"
                class="mt-2"
                block
            >
                Iniciar Sesión
            </v-btn>
            </v-form>
        </v-col>
        </v-card>
    </v-container>
</template>

<style scoped>
@media (max-width: 600px) {
  .responsive-img {
    display: block !important;
  }
}
</style>
