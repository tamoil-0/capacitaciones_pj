<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/axios";

// Componentes
import Header from "@/components/Titulo.vue";

// Estados principales
const route = useRoute();
const idEvento = route.params.idEvento;

const evaluaciones = ref([]);
const eventoInfo = ref(null);
const loading = ref(false);

// Estado Filtros
const search = ref("");
const estadoFilter = ref(null);
const itemsPerPage = ref(10);

// Opciones de filtro
const estadosExamen = [
    { value: null, title: "Todos" },
    { value: "aprobado", title: "Aprobados" },
    { value: "desaprobado", title: "Desaprobados" },
];

// Headers de la tabla
const headers = [
    { title: "DNI", key: "inscrito.dni", sortable: true, align: "center", width: "100" },
    { title: "Nombres Completos", key: "inscrito.nombres_completos", sortable: true },
    { title: "Fecha Evaluación", key: "fecha_evaluacion", sortable: true, align: "center", width: "160" },
    { title: "Correctas", key: "resultado.correctas", sortable: true, align: "center", width: "100" },
    { title: "Puntaje", key: "resultado.puntaje", sortable: true, align: "center", width: "100" },
    { title: "Nota", key: "resultado.porcentaje", sortable: true, align: "center", width: "80" },
    { title: "Estado", key: "resultado.aprobado", sortable: true, align: "center", width: "120" },
    { title: "Acciones", key: "actions", sortable: false, align: "center", width: "200" },
];

// Computed
const evaluacionesFiltradas = computed(() => {
    if (!evaluaciones.value) return [];

    return evaluaciones.value.filter((e) => {
        // Búsqueda por DNI o nombres
        const matchesSearch =
            e.inscrito.dni.includes(search.value) ||
            e.inscrito.nombres_completos.toLowerCase().includes(search.value.toLowerCase());

        // Filtro por estado (aprobado/desaprobado)
        const matchesEstado = estadoFilter.value
            ? (estadoFilter.value === "aprobado" && e.resultado.aprobado) ||
              (estadoFilter.value === "desaprobado" && !e.resultado.aprobado)
            : true;

        return matchesSearch && matchesEstado;
    });
});

// Estadísticas
const estadisticas = computed(() => {
    const total = evaluaciones.value.length;
    const aprobados = evaluaciones.value.filter(e => e.resultado.aprobado).length;
    const desaprobados = total - aprobados;
    const promedioGeneral = total > 0
        ? (evaluaciones.value.reduce((sum, e) => sum + e.resultado.porcentaje, 0) / total).toFixed(2)
        : 0;

    return { total, aprobados, desaprobados, promedioGeneral };
});

// Métodos principales
const fetchEvaluacionesEvento = async () => {
    try {
        loading.value = true;
        const { data } = await api.get('/evaluaciones');
        
        // Filtrar solo las evaluaciones de este evento
        evaluaciones.value = data.data.filter(e => e.evento.id_evento == idEvento);
        
        console.log('Evaluaciones cargadas:', evaluaciones.value);
        console.log('PDFs encontrados:', evaluaciones.value.map(e => ({
            dni: e.inscrito.dni,
            pdf_completo: e.archivos.pdf_completo,
            pdf_evidencia: e.archivos.pdf_evidencia
        })));
        
        // Guardar info del evento
        if (evaluaciones.value.length > 0) {
            eventoInfo.value = evaluaciones.value[0].evento;
        }
        
    } catch (error) {
        console.error("Error al obtener evaluaciones del evento:", error);
    } finally {
        loading.value = false;
    }
};

// Formatear fecha
const formatearFecha = (fecha) => {
    if (!fecha) return "N/A";
    const date = new Date(fecha);
    return date.toLocaleString("es-PE", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

// Descargar PDF
const descargarPDF = async (url, tipo) => {
    console.log('Intentando descargar PDF:', { url, tipo });
    
    if (!url) {
        alert(`No hay archivo de ${tipo} disponible para este examen.`);
        return;
    }
    
    try {
        // Abrir directamente la URL pública del PDF
        const fullUrl = `http://127.0.0.1:8000${url}`;
        window.open(fullUrl, '_blank');
    } catch (error) {
        console.error('Error al abrir PDF:', error);
        alert(`Error al abrir el archivo de ${tipo}`);
    }
};

// Color del estado
const getEstadoColor = (aprobado) => {
    return aprobado ? "success" : "error";
};

const getEstadoTexto = (aprobado) => {
    return aprobado ? "Aprobado" : "Desaprobado";
};

// Color de la nota (basado en puntaje de 30)
const getNotaColor = (puntaje) => {
    if (puntaje >= 20) return "success";  // Aprobado (20/30 = 66.67%)
    if (puntaje >= 15) return "warning";  // Cerca de aprobar
    return "error";  // Desaprobado
};

// Exportar a Excel
const exportando = ref(false);
const exportarExcel = async () => {
    try {
        exportando.value = true;
        
        // Exportar solo este evento específico
        const { data } = await api.get(`/evaluaciones/exportar/${idEvento}`);
        
        if (data.success) {
            // Descargar el archivo
            const url = data.data.url;
            const link = document.createElement('a');
            link.href = url;
            link.download = data.data.nombre_archivo;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Mostrar mensaje de éxito
            alert(`Excel generado exitosamente:\n${data.data.evento}\nArchivo: ${data.data.nombre_archivo}`);
        }
    } catch (error) {
        console.error('Error al exportar Excel:', error);
        alert('Error al generar el archivo Excel. Por favor intente nuevamente.');
    } finally {
        exportando.value = false;
    }
};

onMounted(() => {
    fetchEvaluacionesEvento();
});
</script>

<template>
    <div class="pagina">
        <Header 
            :titulo="eventoInfo ? `Exámenes: ${eventoInfo.nombre}` : 'Cargando...'"
            :subtitulo="eventoInfo ? `Resultados de evaluaciones del evento` : ''"
            icono="mdi-clipboard-text"
        />

        <!-- Información del Evento -->
        <VCard class="mb-5 elevation-2 bg-primary" v-if="eventoInfo">
            <VCardText class="text-white">
                <VRow>
                    <VCol cols="12" md="6">
                        <div class="d-flex align-center">
                            <VIcon icon="mdi-calendar" size="24" class="mr-3" />
                            <div>
                                <div class="text-caption">Fecha del Evento</div>
                                <div class="text-h6">{{ formatearFecha(eventoInfo.fecha_evento) }}</div>
                            </div>
                        </div>
                    </VCol>
                    <VCol cols="12" md="6">
                        <div class="d-flex align-center">
                            <VIcon icon="mdi-tag" size="24" class="mr-3" />
                            <div>
                                <div class="text-caption">Tipo de Evento</div>
                                <div class="text-h6">Tipo {{ eventoInfo.tipo_evento }}</div>
                            </div>
                        </div>
                    </VCol>
                </VRow>
            </VCardText>
        </VCard>

        <!-- Estadísticas -->
        <VRow class="mb-5 align-center">
            <VCol cols="12" sm="6" md="2">
                <VCard class="elevation-2">
                    <VCardText class="text-center">
                        <VIcon icon="mdi-account-group" size="40" color="primary" class="mb-2" />
                        <div class="text-h4 font-weight-bold primary--text">
                            {{ estadisticas.total }}
                        </div>
                        <div class="text-caption text-grey">Total Inscritos</div>
                    </VCardText>
                </VCard>
            </VCol>

            <VCol cols="12" sm="6" md="2">
                <VCard class="elevation-2">
                    <VCardText class="text-center">
                        <VIcon icon="mdi-check-circle" size="40" color="success" class="mb-2" />
                        <div class="text-h4 font-weight-bold success--text">
                            {{ estadisticas.aprobados }}
                        </div>
                        <div class="text-caption text-grey">Aprobados</div>
                    </VCardText>
                </VCard>
            </VCol>

            <VCol cols="12" sm="6" md="2">
                <VCard class="elevation-2">
                    <VCardText class="text-center">
                        <VIcon icon="mdi-close-circle" size="40" color="error" class="mb-2" />
                        <div class="text-h4 font-weight-bold error--text">
                            {{ estadisticas.desaprobados }}
                        </div>
                        <div class="text-caption text-grey">Desaprobados</div>
                    </VCardText>
                </VCard>
            </VCol>

            <VCol cols="12" sm="6" md="2">
                <VCard class="elevation-2">
                    <VCardText class="text-center">
                        <VIcon icon="mdi-chart-line" size="40" color="info" class="mb-2" />
                        <div class="text-h4 font-weight-bold info--text">
                            {{ estadisticas.promedioGeneral }}%
                        </div>
                        <div class="text-caption text-grey">Promedio</div>
                    </VCardText>
                </VCard>
            </VCol>

            <!-- BOTÓN EXPORTAR EXCEL - DESTACADO -->
            <VCol cols="12" md="4" class="d-flex align-center justify-center">
                <VCard 
                    class="elevation-4 w-100 cursor-pointer hover-card"
                    color="success"
                    @click="exportarExcel"
                    :disabled="exportando || evaluacionesFiltradas.length === 0"
                >
                    <VCardText class="text-center pa-6">
                        <VIcon 
                            icon="mdi-microsoft-excel" 
                            size="50" 
                            color="white" 
                            class="mb-2"
                        />
                        <div class="text-h5 font-weight-bold white--text mb-1">
                            {{ exportando ? 'Generando...' : 'Exportar Excel' }}
                        </div>
                        <div class="text-caption white--text">
                            {{ evaluacionesFiltradas.length }} evaluaciones
                        </div>
                        <VProgressLinear 
                            v-if="exportando"
                            indeterminate
                            color="white"
                            class="mt-2"
                        />
                    </VCardText>
                </VCard>
            </VCol>
        </VRow>

        <!-- Filtros -->
        <VCard class="mb-5 elevation-2">
            <VCardText>
                <VRow>
                    <VCol cols="12" md="8">
                        <VTextField
                            v-model="search"
                            prepend-inner-icon="mdi-magnify"
                            label="Buscar por DNI o nombre"
                            variant="outlined"
                            density="compact"
                            clearable
                            hide-details
                        />
                    </VCol>

                    <VCol cols="12" md="4">
                        <VSelect
                            v-model="estadoFilter"
                            :items="estadosExamen"
                            item-title="title"
                            item-value="value"
                            label="Filtrar por estado"
                            variant="outlined"
                            density="compact"
                            prepend-inner-icon="mdi-filter"
                            clearable
                            hide-details
                        />
                    </VCol>
                </VRow>
            </VCardText>
        </VCard>

        <!-- Tabla de Evaluaciones -->
        <VCard class="elevation-3">
            <VCardText>
                <VDataTable
                    :headers="headers"
                    :items="evaluacionesFiltradas"
                    :loading="loading"
                    :items-per-page="itemsPerPage"
                    class="elevation-1"
                    loading-text="Cargando evaluaciones..."
                    no-data-text="No hay evaluaciones registradas para este evento"
                >
                    <!-- DNI -->
                    <template v-slot:item.inscrito.dni="{ item }">
                        <VChip size="small" color="primary" variant="tonal">
                            {{ item.inscrito.dni }}
                        </VChip>
                    </template>

                    <!-- Nombres Completos -->
                    <template v-slot:item.inscrito.nombres_completos="{ item }">
                        <div class="font-weight-medium">
                            {{ item.inscrito.nombres_completos }}
                        </div>
                    </template>

                    <!-- Fecha Evaluación -->
                    <template v-slot:item.fecha_evaluacion="{ item }">
                        <div class="text-caption">
                            {{ formatearFecha(item.fecha_evaluacion) }}
                        </div>
                    </template>

                    <!-- Correctas -->
                    <template v-slot:item.resultado.correctas="{ item }">
                        <VChip size="small" color="info" variant="tonal">
                            {{ item.resultado?.correctas || 0 }} / {{ item.resultado?.total_preguntas || 30 }}
                        </VChip>
                    </template>

                    <!-- Puntaje -->
                    <template v-slot:item.resultado.puntaje="{ item }">
                        <VChip 
                            size="small" 
                            :color="getNotaColor(Number(item.resultado?.puntaje) || 0)"
                            variant="tonal"
                        >
                            {{ Number(item.resultado?.puntaje || 0).toFixed(2) }} / {{ item.resultado?.puntaje_maximo || 30 }}
                        </VChip>
                    </template>

                    <!-- Nota (Porcentaje) -->
                    <template v-slot:item.resultado.porcentaje="{ item }">
                        <div class="text-center">
                            <div 
                                class="text-h6 font-weight-bold"
                                :class="[
                                    Number(item.resultado?.puntaje || 0) >= 20 ? 'text-success' :
                                    Number(item.resultado?.puntaje || 0) >= 15 ? 'text-warning' :
                                    'text-error'
                                ]"
                            >
                                {{ Number(item.resultado?.porcentaje || 0).toFixed(2) }}%
                            </div>
                        </div>
                    </template>

                    <!-- Estado -->
                    <template v-slot:item.resultado.aprobado="{ item }">
                        <VChip 
                            :color="getEstadoColor(item.resultado.aprobado)"
                            size="small"
                            variant="flat"
                        >
                            {{ getEstadoTexto(item.resultado.aprobado) }}
                        </VChip>
                    </template>

                    <!-- Acciones -->
                    <template v-slot:item.actions="{ item }">
                        <div class="d-flex gap-2 justify-center">
                            <!-- Botón Ver Reporte -->
                            <VTooltip text="Ver Reporte Completo" location="top">
                                <template v-slot:activator="{ props }">
                                    <VBtn
                                        v-bind="props"
                                        icon="mdi-file-document"
                                        size="small"
                                        color="primary"
                                        variant="tonal"
                                        :disabled="!item.archivos.pdf_completo"
                                        @click="descargarPDF(item.archivos.pdf_completo, 'reporte')"
                                    />
                                </template>
                            </VTooltip>

                            <!-- Botón Ver Evidencias -->
                            <VTooltip text="Ver Evidencia (Hoja Escaneada)" location="top">
                                <template v-slot:activator="{ props }">
                                    <VBtn
                                        v-bind="props"
                                        icon="mdi-image"
                                        size="small"
                                        color="secondary"
                                        variant="tonal"
                                        :disabled="!item.archivos.pdf_evidencia"
                                        @click="descargarPDF(item.archivos.pdf_evidencia, 'evidencia')"
                                    />
                                </template>
                            </VTooltip>
                        </div>
                    </template>
                </VDataTable>
            </VCardText>
        </VCard>
    </div>
</template>

<style scoped>
.pagina {
    padding: 20px;
}

.text-success {
    color: #4caf50 !important;
}

.text-warning {
    color: #fb8c00 !important;
}

.text-error {
    color: #f44336 !important;
}

.success--text {
    color: #4caf50 !important;
}

.error--text {
    color: #f44336 !important;
}

.info--text {
    color: #2196f3 !important;
}

.primary--text {
    color: #1565C0 !important;
}

.bg-primary {
    background-color: #1565C0 !important;
}

/* Botón de exportar Excel - efecto hover */
.hover-card {
    transition: all 0.3s ease;
    cursor: pointer;
}

.hover-card:hover:not([disabled]) {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(76, 175, 80, 0.4) !important;
}

.hover-card[disabled] {
    opacity: 0.6;
    cursor: not-allowed;
}
</style>
