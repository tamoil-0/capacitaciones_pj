<script setup>
import { ref, computed, onMounted } from "vue";
import api from "@/axios";

// Componentes
import Header from "@/components/Titulo.vue";

// Estado para exportación
const exportando = ref(false);

// Estados principales
const evaluaciones = ref([]);
const loading = ref(false);

// Estado Filtros y búsqueda
const search = ref("");
const eventoFilter = ref(null);
const estadoFilter = ref(null);
const itemsPerPage = ref(10);

// Opciones de filtro
const eventos = ref([]);
const estadosExamen = [
    { value: null, title: "Todos" },
    { value: "aprobado", title: "Aprobados" },
    { value: "desaprobado", title: "Desaprobados" },
];

// Headers de la tabla
const headers = [
    { title: "DNssI", key: "inscrito.dni", sortable: true, align: "center", width: "100" },
    { title: "Nombres Completos", key: "inscrito.nombres_completos", sortable: true },
    { title: "Evento", key: "evento.nombre", sortable: true },
    { title: "Fecha Evaluación", key: "fecha_evaluacion", sortable: true, align: "center", width: "160" },
    { title: "Correctas", key: "resultado.correctas", sortable: true, align: "center", width: "100" },
    { title: "Puntssssaje", key: "resultado.puntaje", sortable: true, align: "center", width: "100" },
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
            e.inscrito.nombres_completos.toLowerCase().includes(search.value.toLowerCase()) ||
            e.evento.nombre.toLowerCase().includes(search.value.toLowerCase());

        // Filtro por evento
        const matchesEvento = eventoFilter.value
            ? e.evento.id_evento === eventoFilter.value
            : true;

        // Filtro por estado (aprobado/desaprobado)
        const matchesEstado = estadoFilter.value
            ? (estadoFilter.value === "aprobado" && e.resultado.aprobado) ||
              (estadoFilter.value === "desaprobado" && !e.resultado.aprobado)
            : true;

        return matchesSearch && matchesEvento && matchesEstado;
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
const fetchEvaluaciones = async () => {
    try {
        loading.value = true;
        const { data } = await api.get('/evaluaciones');
        evaluaciones.value = data.data;
        
        // Extraer eventos únicos para el filtro
        const eventosUnicos = new Map();
        data.data.forEach(e => {
            if (e.evento.id_evento && !eventosUnicos.has(e.evento.id_evento)) {
                eventosUnicos.set(e.evento.id_evento, {
                    value: e.evento.id_evento,
                    title: e.evento.nombre
                });
            }
        });
        eventos.value = [
            { value: null, title: "Todos los eventos" },
            ...Array.from(eventosUnicos.values())
        ];
    } catch (error) {
        console.error("Error al obtener evaluaciones:", error);
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
const exportarExcel = async () => {
    try {
        exportando.value = true;
        
        // Preparar el ID del evento (si hay filtro aplicado)
        const eventoId = eventoFilter.value || '';
        
        // Llamar al endpoint
        const { data } = await api.get(`/evaluaciones/exportar/${eventoId}`);
        
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
    fetchEvaluaciones();
});
</script>

<template>
    <div class="pagina">
        <Header 
            titulo="CONVOCATORIAS - Resultados de Exámenes"
            subtitulo="Sistema de calificación de exámenes - Solo para eventos tipo CONVOCATORIAS"
            icono="mdi-clipboard-text"
        />

        <!-- Alerta informativa -->
        <VAlert
            type="info"
            variant="tonal"
            class="mb-4"
            prominent
            border="start"
        >
            <template #prepend>
                <VIcon icon="mdi-file-document-check" size="large"></VIcon>
            </template>
            <strong>Sistema de Evaluación - Criterios de Aprobación</strong>
            <div class="text-body-2 mt-1">
                Los exámenes son procesados automáticamente. 
                <strong>Puntaje mínimo aprobatorio: 20/30 puntos.</strong> 
                Los resultados mostrados corresponden únicamente a eventos tipo CONVOCATORIAS.
            </div>
        </VAlert>

        <!-- ═══════════════════════════════════════════════════════ -->
        <!-- ESTADÍSTICAS Y BOTÓN EXPORTAR -->
        <!-- ═══════════════════════════════════════════════════════ -->
        <VRow class="mb-5 align-center">
            <VCol cols="12" sm="6" md="2">
                <VCard class="elevation-2">
                    <VCardText class="text-center">
                        <VIcon icon="mdi-clipboard-list" size="40" color="primary" class="mb-2" />
                        <div class="text-h4 font-weight-bold primary--text">
                            {{ estadisticas.total }}
                        </div>
                        <div class="text-caption text-grey">Total Exámenes</div>
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
                        <div class="text-caption text-grey">Promedio General</div>
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

        <!-- ═══════════════════════════════════════════════════════ -->
        <!-- FILTROS -->
        <!-- ═══════════════════════════════════════════════════════ -->
        <VCard class="mb-5 elevation-2">
            <VCardText>
                <VRow>
                    <VCol cols="12" md="4">
                        <VTextField
                            v-model="search"
                            prepend-inner-icon="mdi-magnify"
                            label="Buscar por DNI, nombre o evento"
                            variant="outlined"
                            density="compact"
                            clearable
                            hide-details
                        />
                    </VCol>

                    <VCol cols="12" md="4">
                        <VSelect
                            v-model="eventoFilter"
                            :items="eventos"
                            item-title="title"
                            item-value="value"
                            label="Filtrar por evento"
                            variant="outlined"
                            density="compact"
                            prepend-inner-icon="mdi-calendar"
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

        <!-- ═══════════════════════════════════════════════════════ -->
        <!-- TABLA DE EVALUACIONES -->
        <!-- ═══════════════════════════════════════════════════════ -->
        <VCard class="elevation-3">
            <VCardText>
                <VDataTable
                    :headers="headers"
                    :items="evaluacionesFiltradas"
                    :loading="loading"
                    :items-per-page="itemsPerPage"
                    class="elevation-1"
                    loading-text="Cargando evaluaciones..."
                    no-data-text="No hay evaluaciones registradas"
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

                    <!-- Evento -->
                    <template v-slot:item.evento.nombre="{ item }">
                        <div class="text-caption">
                            {{ item.evento.nombre }}
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
    color: #9A1413 !important;
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

