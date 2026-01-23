<script setup>
import { ref, onMounted } from "vue";
import api from "@/axios";
import { selectedTipoEvento, selectedEvento } from "@/stores/appState";

// Componentes
import Header from "@/components/Titulo.vue";
import Carta from "@/components/Carta.vue"; 

const tipos_eventos = ref([]);

const fetchTiposEventos = async () => {
    try {
        const { data } = await api.get("/tipos_eventos");
        tipos_eventos.value = data;
    } catch (error) {
        console.error("Error al obtener estándares:", error);
    }
};

onMounted(() => {
    selectedTipoEvento.value    = null;
    selectedEvento.value        = null;

    fetchTiposEventos();
});
</script>

<template>
    <div class="pagina">
        <Header 
            titulo="Sistema de Gestión de Eventos"
            subtitulo="Gestione eficientemente convocatorias, cursos y exámenes desde un solo lugar"
            icono="mdi-view-dashboard"
        />

        <VRow>
            <VCol cols="12" sm="6" md="3">
                <Carta
                    nombre="Convocatorias"
                    ruta="/eventos/1"
                    icono="mdi-briefcase-account"
                    height="200"
                    font-size="1.25rem"
                />
            </VCol>

            <VCol cols="12" sm="6" md="3">
                <Carta
                    nombre="Cursos"
                    ruta="/eventos/2"
                    icono="mdi-school-outline"
                    height="200"
                    font-size="1.25rem"
                />
            </VCol>

            <VCol cols="12" sm="6" md="3">
                <Carta
                    nombre="Otros Eventos"
                    ruta="/eventos/3"
                    icono="mdi-calendar-star"
                    height="200"
                    font-size="1.25rem"
                />
            </VCol>

            <VCol cols="12" sm="6" md="3">
                <Carta
                    nombre="Ver Exámenes"
                    ruta="/examenes/eventos"
                    icono="mdi-file-document-check"
                    height="200"
                    font-size="1.25rem"
                />
            </VCol>
        </VRow>

    </div>
</template>
