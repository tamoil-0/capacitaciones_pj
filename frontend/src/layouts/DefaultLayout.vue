<script setup>
import { ref, onMounted, vModelCheckbox } from "vue";
import { RouterView, useRouter } from 'vue-router'
import { useDisplay } from "vuetify";
import { useAuthStore } from '@/stores/auth'

import icono_navbar from "@/assets/img/user.png";
import sidebar from "@/assets/img/frontis.jpg";
import fondo from "@/assets/img/fondo.png";

const { smAndDown } = useDisplay();

const authStore = useAuthStore()
const router = useRouter()

// Estado sidebar
const drawer = ref(false);

// Usuario
const usuario = ref(null);
// Opciones de menú
const opciones = ref([]);

onMounted(() => {
    const savedUser = localStorage.getItem("usuario");
    if (savedUser) {
        usuario.value = JSON.parse(savedUser);
    }

    const savedOpciones = localStorage.getItem("opciones");
    if (savedOpciones) {
        opciones.value = JSON.parse(savedOpciones);
    }
});

function logout() {
  authStore.logout()
  router.push({ name: 'Login' })
}
</script>

<template>
    <v-app>
        <!-- NAVBAR -->
        <v-app-bar app color="primary" elevation="4" class="app-navbar">
            <v-container fluid class="d-flex align-center justify-space-between">
                <v-btn
                    icon="mdi-arrow-left"
                    color="white"
                    size="small"
                    @click="router.back()"
                />
                <v-img
                    :src="icono_navbar"
                    alt="Logo Sistema"
                    max-width="40"
                    max-height="40"
                    contain
                    class="ml-3 mr-3"
                />
                <!-- Título -->
                <v-app-bar-title 
                    class="text-white font-weight-bold"
                    :class="smAndDown ? 'text-h6' : 'text-h5'"
                >
                    {{
                        smAndDown
                            ? "SACE"
                            : "Sistema de Asistencia y Calificación de Exámenes"
                    }}
                </v-app-bar-title>

                <v-spacer/>

                <!-- Botones -->
                <div class="d-flex align-center gap-2">
                    <v-btn
                        icon="mdi-menu"
                        color="white"
                        size="small"
                        @click="drawer = !drawer"
                    />
                </div>
            </v-container>
        </v-app-bar>

        <!-- SIDEBAR DERECHO -->
        <v-navigation-drawer
            v-model="drawer"
            location="right"
            :temporary="$vuetify.display.smAndDown"
            app
            color="background"
        >
            <!-- Imagen + Nombre -->
            <div class="sidebar-header">
                <VImg :src="sidebar" cover class="sidebar-bg" />
                <!-- Overlay oscuro + blur -->
                <div class="sidebar-overlay"></div>

                <!-- Nombre del usuario (no afectado por el blur) -->
                <div class="sidebar-username">
                    <span>
                        {{ usuario?.nombres_apellidos }}
                    </span>
                </div>
            </div>

            <!-- Opciones -->
            <div class="flex flex-col gap-5 pa-3">
                <VBtn
                    to="/perfil"
                    block
                    variant="text"
                    class="sidebar-btn justify-start mb-2 py-5"
                >
                    <!-- Ícono circular suave -->
                    <template v-slot:prepend>
                        <div class="icon-wrapper bg-primary">
                            <VIcon icon="mdi-account" size="22" />
                        </div>
                    </template>

                    <h3 class="text-left w-full text-lg font-bold tracking-wide text-grey-darken-3">
                        Mi Perfil
                    </h3>
                </VBtn>

                <VDivider class="my-3" />

                <VBtn
                    v-for="op in opciones"
                    :key="op.id_op"
                    :to="op.ruta"
                    block
                    variant="text"
                    class="sidebar-btn justify-start mb-2 py-5"
                >
                    <template v-slot:prepend>
                        <div class="icon-wrapper bg-primary">
                            <VIcon :icon="op.icono" size="22" />
                        </div>
                    </template>

                    <span
                        class="text-left w-full text-lg font-bold tracking-wide text-grey-darken-3"
                    >
                        {{ op.nombre }}
                    </span>
                </VBtn>
            </div>

            <template #append>
                <div class="pa-3">
                    <VBtn
                        block
                        color="error"
                        variant="flat"
                        prepend-icon="mdi-logout"
                        @click="logout"
                    >
                        Cerrar Sesión
                    </VBtn>
                </div>
            </template>
        </v-navigation-drawer>

        <!-- Contenido principal (con margen para no ser tapado por el navbar fijo) -->
        <VMain class="pt-15 main-content-wrapper">
            <v-container 
                fluid
                class="login-view"
            >
                <RouterView />
            </v-container>
        </VMain>

        <VFooter app class="modern-footer" elevation="2">
            <v-container class="text-center">
                <span class="footer-text">&copy; {{ new Date().getFullYear() }} Sistema de Asistencia y Calificación de Exámenes - Todos los derechos reservados</span>
            </v-container>
        </VFooter>
    </v-app>
</template>


<style scoped>
/* ════════════════════════════════════════════════════════════════════════════════
   🎨 NAVBAR - PALETA AZUL CORPORATIVA
   ════════════════════════════════════════════════════════════════════════════════ */
.app-navbar {
    background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%) !important;
}

/* ════════════════════════════════════════════════════════════════════════════════
   📱 SIDEBAR
   ════════════════════════════════════════════════════════════════════════════════ */
.v-navigation-drawer {
    width: 280px;
    border-left: 1px solid rgba(0, 0, 0, 0.08) !important;
    background: #f8f9fa !important;
}

.sidebar-header {
    position: relative;
    width: 100%;
    height: 140px;
    overflow: hidden;
}

.sidebar-bg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.sidebar-overlay {
    position: absolute;
    inset: 0;
    backdrop-filter: blur(3px);
    background: linear-gradient(135deg, rgba(13, 71, 161, 0.85) 0%, rgba(30, 136, 229, 0.75) 100%);
    z-index: 1;
}

.sidebar-username {
    position: relative;
    z-index: 2;
    height: 100%;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar-username span {
    color: white;
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    letter-spacing: 0.3px;
}

/* Íconos modernos */
.icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    color: white;
    background: linear-gradient(135deg, #0D47A1 0%, #1E88E5 100%);
    box-shadow: 0 4px 8px rgba(13, 71, 161, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.icon-wrapper:hover {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 6px 12px rgba(13, 71, 161, 0.4);
}

/* Botones del sidebar */
.sidebar-btn {
    border-radius: 12px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 16px 20px !important;
}

.sidebar-btn:hover {
    background: rgba(13, 71, 161, 0.08) !important;
    transform: translateX(4px);
}

.custom-btn {
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    display: flex;
    gap: 12px;
    margin-bottom: 8px !important;
    padding: 16px 20px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.custom-btn:hover {
    background: rgba(13, 71, 161, 0.08) !important;
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
}

.custom-btn span {
    color: #ecf0f1 !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px;
}

/* Fondo minimalista */
.main-content-wrapper {
    min-height: calc(100vh - 64px);
    background: #f8f9fa;
}

.login-view {
    min-height: 100%;
}

/* Footer moderno - Centrado con color plomo claro */
.modern-footer {
    background: #f5f5f5 !important;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    padding: 20px 0;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
}

.footer-text {
    color: #5f6368;
    font-size: 0.875rem;
    font-weight: 500;
    text-align: center;
}
</style>
