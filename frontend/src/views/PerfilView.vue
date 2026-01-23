<script setup>
import { ref, computed , onMounted } from 'vue'
import axios from 'axios'

import Header from "@/components/Titulo.vue";

// Estado del usuario
const user = ref({
    id_usuario: null,
    nombres_apellidos: '',
    nickname: '',
    dni: '',
    tipo_usuario: ''
})

// mapa de roles
const roles = {
    1: 'Administrador',
    2: 'Organizador',
    3: 'Apoyo'
}

const loading = ref(false)
const success = ref('')
const error = ref('')

// Estado del cambio de contraseña
const passwordForm = ref({
    contraseña_actual: '',
    contraseña_nueva: '',
    contraseña_nueva_confirmation: ''
})

const passwordLoading = ref(false)
const passwordSuccess = ref('')
const passwordError = ref('')

// Traducción automática
const tipoUsuarioTexto = computed(() => {
    return roles[user.value?.tipo_usuario] || 'Desconocido'
})

// Obtener usuario desde API

const fetchUser = async () => {
    try {
        const savedUser = JSON.parse(localStorage.getItem('usuario'))
        if (!savedUser) return

        const { data } = await axios.get(`/usuario/${savedUser.id_usuario}`)

        user.value = data 
    } catch (err) {
        error.value = 'No se pudo cargar el perfil'
    }
}


// Guardar cambios del perfil
const saveUser = async () => {
    try {
        loading.value = true
        success.value = ''
        error.value = ''

        await axios.put(`/usuario/${user.value.id_usuario}`, user.value)

        success.value = 'Perfil actualizado correctamente'
    } catch (err) {
        error.value = 'No se pudo actualizar el perfil'
    } finally {
        loading.value = false
    }
}

// Cambiar contraseña
const changePassword = async () => {
    try {
        passwordLoading.value = true
        passwordSuccess.value = ''
        passwordError.value = ''

        await axios.post(`/usuarios/cambiar-password/${user.value.id_usuario}`, {
            contraseña_actual: passwordForm.value.contraseña_actual,
            contraseña_nueva: passwordForm.value.contraseña_nueva,
            contraseña_nueva_confirmation: passwordForm.value.contraseña_nueva_confirmation
        })

        passwordSuccess.value = 'Contraseña actualizada correctamente'
        passwordForm.value = {
            contraseña_actual: '',
            contraseña_nueva: '',
            contraseña_nueva_confirmation: ''
        }
    } catch (err) {
        passwordError.value =
        err.response?.data?.message || 'No se pudo cambiar la contraseña'
    } finally {
        passwordLoading.value = false
    }
}

onMounted(() => {
    fetchUser()
})
</script>

<template>
    <div class="pagina">
        <Header 
            titulo="Mi Perfil"
            subtitulo="Mostrando los tipos de eventos los cuales existen en la CSJP"
            icono="mdi-chart-bar"
        />

        <VRow>
            <!-- Columna izquierda: Datos de usuario -->
            <VCol cols="12" md="7">
                <VCard elevation="3" class="rounded-xl pa-3">
                    <VCardTitle class="font-weight-bold text-primary">
                        Mis datos
                    </VCardTitle>

                    <VCardText>
                        <VForm>
                            <v-row>
                                <v-col cols="12" sm="6">
                                    <VTextField v-model="user.nickname"                label="Usuario"                 outlined dense readonly/>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <VTextField :model-value="tipoUsuarioTexto"   label="Tipo de Usuario"     outlined dense readonly />
                                </v-col>
                            </v-row>
                            
                            <VTextField v-model="user.nombres_apellidos"      label="Nombres completos"    outlined dense />     
                        </VForm>

                        <VAlert v-if="success" type="success" dense class="mt-3">{{ success }}</VAlert>
                        <VAlert v-if="error" type="error" dense class="mt-3">{{ error }}</VAlert>
                    </VCardText>

                    <VCardActions>
                        <VBtn
                            color="success"
                            block
                            variant="flat"
                            :loading="loading"
                            @click="saveUser"
                            prepend-icon="mdi-content-save"
                        >
                            Guardar Cambios
                        </VBtn>
                    </VCardActions>
                </VCard>
            </VCol>

            <!-- Columna derecha: Cambio de contraseña -->
            <VCol cols="12" md="5">
                <VCard elevation="3" class="rounded-xl pa-3">
                    <VCardTitle class="font-weight-bold text-primary">
                        Cambiar mi contraseña
                    </VCardTitle>
                    <VCardText>
                        <VForm>
                        <VTextField
                            v-model="passwordForm.contraseña_actual"
                            label="Contraseña Actual"
                            type="password"
                            outlined
                            dense
                        />
                        <VTextField
                            v-model="passwordForm.contraseña_nueva"
                            label="Nueva Contraseña"
                            type="password"
                            outlined
                            dense
                        />
                        <VTextField
                            v-model="passwordForm.contraseña_nueva_confirmation"
                            label="Confirmar Nueva Contraseña"
                            type="password"
                            outlined
                            dense
                        />
                        </VForm>

                        <VAlert v-if="passwordSuccess" type="success" dense class="mt-3">
                            {{ passwordSuccess }}
                        </VAlert>
                        <VAlert v-if="passwordError" type="error" dense class="mt-3">
                            {{ passwordError }}
                        </VAlert>
                    </VCardText>
                    <VCardActions>
                        <VBtn
                            color="warning"
                            block
                            variant="flat"
                            :loading="passwordLoading"
                            @click="changePassword"
                            prepend-icon="mdi-lock-reset"
                        >
                            Cambiar Contraseña
                        </VBtn>
                    </VCardActions>
                </VCard>
            </VCol>
        </VRow>
    </div>
</template>
