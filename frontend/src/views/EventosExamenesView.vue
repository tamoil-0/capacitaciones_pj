<script setup>
import { ref, computed, onMounted } from "vue";
import api from "@/axios";

// Componentes
import Header from "@/components/Titulo.vue";

// Estados principales
const eventos = ref([]);
const loading = ref(false);
const search = ref("");

// Computed - Eventos filtrados
const eventosFiltrados = computed(() => {
    if (!eventos.value) return [];

    return eventos.value.filter((e) => {
        const matchesSearch = e.nombre.toLowerCase().includes(search.value.toLowerCase());
        return matchesSearch;
    });
});

// Métodos principales
const fetchEventosConExamenes = async () => {
    try {
        loading.value = true;
        const { data } = await api.get('/evaluaciones');
        
        // Agrupar evaluaciones por evento
        const eventosMap = new Map();
        
        data.data.forEach(evaluacion => {
            const eventoId = evaluacion.evento.id_evento;
            
            if (!eventosMap.has(eventoId)) {
                eventosMap.set(eventoId, {
                    id_evento: evaluacion.evento.id_evento,
                    nombre: evaluacion.evento.nombre,
                    fecha_evento: evaluacion.evento.fecha_evento,
                    tipo_evento: evaluacion.evento.tipo_evento,
                    total_examenes: 0,
                    aprobados: 0,
                    desaprobados: 0
                });
            }
            
            const evento = eventosMap.get(eventoId);
            evento.total_examenes++;
            
            if (evaluacion.resultado.aprobado) {
                evento.aprobados++;
            } else {
                evento.desaprobados++;
            }
        });
        
        eventos.value = Array.from(eventosMap.values());
        
    } catch (error) {
        console.error("Error al obtener eventos con exámenes:", error);
    } finally {
        loading.value = false;
    }
};

// Formatear fecha
const formatearFecha = (fecha) => {
    if (!fecha) return "N/A";
    const date = new Date(fecha);
    return date.toLocaleDateString("es-PE", {
        day: "2-digit",
        month: "long",
        year: "numeric",
    });
};

onMounted(() => {
    fetchEventosConExamenes();
});
</script>

<template>
    <div class="pagina">
        <Header 
            titulo="CONVOCATORIAS - Eventos con Exámenes Procesados"
            subtitulo="Eventos con evaluaciones de exámenes calificadas"
            icono="mdi-clipboard-text"
        />

        <!-- Alerta informativa -->
        <VAlert
            type="success"
            variant="tonal"
            class="mb-4"
            prominent
            border="start"
        >
            <template #prepend>
                <VIcon icon="mdi-file-document-check" size="large"></VIcon>
            </template>
            <strong>Sistema de Evaluación de Exámenes</strong>
            <div class="text-body-2 mt-1">
                Estos eventos tienen exámenes procesados y calificados. 
                Solo eventos tipo CONVOCATORIAS pueden tener evaluaciones de exámenes.
            </div>
        </VAlert>

        <!-- Búsqueda -->
        <VCard class="mb-5 elevation-2">
            <VCardText>
                <VTextField
                    v-model="search"
                    prepend-inner-icon="mdi-magnify"
                    label="Buscar evento por nombre"
                    variant="outlined"
                    density="compact"
                    clearable
                    hide-details
                />
            </VCardText>
        </VCard>

        <!-- Lista de Eventos -->
        <VRow v-if="!loading && eventosFiltrados.length > 0">
            <VCol 
                v-for="evento in eventosFiltrados" 
                :key="evento.id_evento"
                cols="12" 
                md="6" 
                lg="4"
            >
                <VCard 
                    class="evento-card elevation-3"
                    hover
                    @click="$router.push(`/examenes/eventos/${evento.id_evento}`)"
                >
                    <VCardTitle class="bg-primary text-white d-flex align-center">
                        <VIcon icon="mdi-calendar-check" size="24" class="mr-2" />
                        {{ evento.nombre }}
                    </VCardTitle>

                    <VCardText>
                        <div class="mb-3">
                            <VIcon icon="mdi-calendar" size="18" class="mr-2" />
                            <span class="text-caption">{{ formatearFecha(evento.fecha_evento) }}</span>
                        </div>

                        <VDivider class="my-3" />

                        <!-- Estadísticas -->
                        <VRow dense>
                            <VCol cols="4" class="text-center">
                                <div class="text-h5 font-weight-bold primary--text">
                                    {{ evento.total_examenes }}
                                </div>
                                <div class="text-caption text-grey">Total</div>
                            </VCol>

                            <VCol cols="4" class="text-center">
                                <div class="text-h5 font-weight-bold text-success">
                                    {{ evento.aprobados }}
                                </div>
                                <div class="text-caption text-grey">Aprobados</div>
                            </VCol>

                            <VCol cols="4" class="text-center">
                                <div class="text-h5 font-weight-bold text-error">
                                    {{ evento.desaprobados }}
                                </div>
                                <div class="text-caption text-grey">Desaprobados</div>
                            </VCol>
                        </VRow>
                    </VCardText>

                    <VCardActions class="justify-center pb-4">
                        <VBtn 
                            color="primary" 
                            variant="tonal"
                            prepend-icon="mdi-account-group"
                        >
                            Ver Inscritos
                        </VBtn>
                    </VCardActions>
                </VCard>
            </VCol>
        </VRow>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-10">
            <VProgressCircular indeterminate color="primary" size="64" />
            <div class="mt-4 text-h6">Cargando eventos...</div>
        </div>

        <!-- Sin datos -->
        <VCard v-if="!loading && eventosFiltrados.length === 0" class="elevation-2">
            <VCardText class="text-center py-10">
                <VIcon icon="mdi-folder-open" size="64" color="grey" class="mb-4" />
                <div class="text-h6 text-grey">No hay eventos con exámenes procesados</div>
            </VCardText>
        </VCard>
    </div>
</template>

<style scoped>
.pagina {
    padding: 20px;
}

.evento-card {
    cursor: pointer;
    transition: transform 0.2s;
}

.evento-card:hover {
    transform: translateY(-4px);
}

.text-success {
    color: #4caf50 !important;
}

.text-error {
    color: #f44336 !important;
}

.primary--text {
    color: #9A1413 !important;
}

.bg-primary {
    background-color: #9A1413 !important;
}
</style>
