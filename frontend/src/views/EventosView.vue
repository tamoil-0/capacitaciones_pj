<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/axios";

// Componentes
import Header from "@/components/Titulo.vue";
import Filtros from "@/components/cruds/Filtros.vue";
import Tabla from "@/components/cruds/Tabla.vue";
import Formulario from "@/components/forms/Formulario.vue";
import DeleteForm from "@/components/forms/Delete.vue";

// Estados principales
const route = useRoute();
const idTipoEvento = route.params.idTipoEvento;
const eventos = ref([]);
const loading = ref(false);
// Estado Dialogs
const selectedEvento = ref(null);
const deleteDialog = ref(false);
// Estado Formulario
const dialog = ref(false);
const editMode = ref(false);
// Estado Filtros y búsqueda
const search = ref("");
const estadoFilter = ref(null);
const itemsPerPage = ref(5);

const usuario = ref(null);
const tipoEventoInfo = ref({
    nombre: '',
    icono: 'mdi-calendar',
    descripcion: '',
    botonLabel: 'Ver Inscritos'
});

const estados = [
    { value: 0, title: "Pendiente", color: "success" },
    { value: 1, title: "Finalizado", color: "error" },
];

// Formulario principal
const form = ref({
    nombre: "",
    fecha_evento: "",
    estado: 0,
});

// Estado del archivo Excel
const excelFile = ref(null);
// Validaciones
const formValid = ref(false);
const errors = ref({});

// Headers de la tabla
const headers = [
    { title: "Identificador",   key: "id_evento",    sortable: true, align: "center" },
    { title: "Nombre",          key: "nombre",       sortable: true },
    { title: "Fecha",           key: "fecha_evento", sortable: true, align: "center" },
    { title: "Estado",          key: "estado",       sortable: true, align: "center" },
    { title: "Acciones",        key: "actions",      sortable: false },
];

// Computed
const eventosFiltrados = computed(() => {
    if (!eventos.value) return [];

    return eventos.value.filter((e) => {
        const matchesSearch =
            e.nombre.toLowerCase().includes(search.value.toLowerCase());

        const matchesEstado = estadoFilter.value !== null
            ? e.estado === estadoFilter.value
            : true;

        return matchesSearch && matchesEstado;
    });
});

// Métodos principales
const fetchEventos = async () => {
    try {
        loading.value = true;
        const { data } = await api.get(`/eventos/${idTipoEvento}`);
        eventos.value = data;
    } catch (error) {
        console.error("Error al obtener eventos:", error);
    } finally {
        loading.value = false;
    }
};

// Definimos los campos para el formulario
const fields = ref([
    { key: "nombre",        label: "Nombre",                   type: "text",            rules: ["required"] },
    { key: "fecha_evento",  label: "Fecha y hora del evento",  type: "datetime-local",  rules: ["required"] },
    {
        key: "estado", 
        label: "Estado", 
        type: "select",              // 👈 importante, tipo select
        options: estados,            // 👈 aquí pasas el array que ya tienes
        itemTitle: "title",          // qué mostrar en el select
        itemValue: "value",          // qué guardar en el modelo
    },
]);

const openCreateDialog = () => {
    editMode.value = false;
    Object.keys(form.value).forEach(k => (form.value[k] = "")); // limpiar
    dialog.value = true;
};

const openEditDialog = (evento) => {
    editMode.value = true;
    selectedEvento.value = evento;
    form.value = { ...evento };
    console.log('🔍 Estado del evento al abrir diálogo:', evento.estado);
    console.log('🔍 Estado en form después de copiar:', form.value.estado);
    dialog.value = true;
};

const openDeleteDialog = (evento) => {
    selectedEvento.value = evento;
    deleteDialog.value = true;
};

// Guardar evento
const saveEvento = async () => {
    try {
        loading.value = true;
        errors.value = {};

        console.log('💾 Guardando evento con estado:', form.value.estado);
        console.log('💾 Datos completos del form:', JSON.stringify(form.value, null, 2));

        if (editMode.value) {
            await api.put(`/eventos/${selectedEvento.value.id_evento}`, form.value);
        } else {
            await api.post(`/eventos/${idTipoEvento}`, form.value);
        }

        dialog.value = false;
        fetchEventos();
    } catch (err) {
        errors.value = err.response?.data?.errors || {};
    } finally {
        loading.value = false;
    }
};

const deleteEvento = async () => {
    try {
        loading.value = true;
        await api.delete(`/eventos/${selectedEvento.value.id_evento}`);

        showAlert("Evento eliminado correctamente", "success");
        deleteDialog.value = false;
        selectedUser.value = null;
        await fetchEventos();
    } catch (error) {
        console.error("Error al eliminar evento:", error);
        showAlert("Error al eliminar evento", "error");
    } finally {
        loading.value = false;
    }
};

const subirExcel = async () => {
    if (!excelFile.value) {
        alert("Selecciona un archivo primero");
        return;
    }

    try {
        const formData = new FormData();
        formData.append("file", excelFile.value);

        await api.post(`/eventos/importar-event-person/${idTipoEvento}`,formData);
        alert("Personas importadas con éxito");
        await fetchEventos();
    } catch (error) {
        console.error(error);
        alert("Error al importar el Excel");
    }
};

const showAlert = (message, type) => {
    console.log(`${type.toUpperCase()}: ${message}`);
};

const getEstadoColor = (estado) =>
  estados.find((t) => t.value === estado)?.color || "default";

const getEstadoName = (estado) =>
  estados.find((t) => t.value === estado)?.title || "N/A";

// Formatear hora y fecha 
function formatDate(value) {
    if (!value) return "";
    const date = new Date(value);
    const day = date.getDate().toString().padStart(2, "0");
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

// Lifecycle
onMounted(() => {
    usuario.value = JSON.parse(localStorage.getItem("usuario"));
    
    // Configurar información según tipo de evento
    if (idTipoEvento == 1) {
        tipoEventoInfo.value = {
            nombre: 'CONVOCATORIAS - Control de Asistencias',
            icono: 'mdi-clipboard-text',
            descripcion: 'Control de asistencias para eventos de convocatorias y exámenes',
            botonLabel: 'Ver Inscritos',
            botonIcono: 'mdi-account-group'
        };
    } else if (idTipoEvento == 2) {
        tipoEventoInfo.value = {
            nombre: 'CURSOS - Control de Asistencias',
            icono: 'mdi-school',
            descripcion: 'Eventos con registro de entrada y salida de participantes',
            botonLabel: 'Ver Asistencias',
            botonIcono: 'mdi-clipboard-check'
        };
    } else if (idTipoEvento == 3) {
        tipoEventoInfo.value = {
            nombre: 'OTROS EVENTOS - Control de Asistencias',
            icono: 'mdi-calendar-star',
            descripcion: 'Eventos diversos con registro de asistencias',
            botonLabel: 'Ver Asistencias',
            botonIcono: 'mdi-clipboard-check'
        };
    }
    
    fetchEventos();
});
</script>

<template>
    <div class="pagina">
        <!-- Header -->
        <Header
            :titulo="tipoEventoInfo.nombre"
            :icono="tipoEventoInfo.icono"
            nombreBTN   = "Nuevo Evento"
            iconoBTN    = "mdi-calendar-plus"
            @crear="openCreateDialog" 
        />

        <!-- Alerta informativa -->
        <VAlert
            v-if="tipoEventoInfo.descripcion"
            type="info"
            variant="tonal"
            class="mb-4"
            prominent
            border="start"
        >
            <template #prepend>
                <VIcon :icon="tipoEventoInfo.icono" size="large"></VIcon>
            </template>
            <strong>{{ tipoEventoInfo.nombre }}</strong>
            <div class="text-body-2 mt-1">{{ tipoEventoInfo.descripcion }}</div>
        </VAlert>

        <VRow align="center" dense>
            <!-- Filtros -->
            <VCol cols="12" md="7">
                <!-- Filtros -->
                <Filtros
                    v-model:search="search"
                    v-model:tipoFilter="estadoFilter"
                    v-model:itemsPerPage="itemsPerPage"
                    search-label="Buscar eventos"
                    search-placeholder="Nombre o descripción"
                    tipo-label="Filtrar por estado"
                    :tipos="estados"
                />
            </VCol>

            
            <!-- Métodos importar y asistencia -->
            <VCol cols="12" md="5">
                <VCard class="mb-6" elevation="2">
                    <VCardText>
                        <VRow align="center" dense>
                            <!-- Subir Excel SOLO si admin <template v-if="usuario && usuario.id_usuario < 3">-->
                            <VCol cols="12" md="8">
                                <VFileInput
                                    v-model="excelFile"
                                    label="Seleccionar archivo Excel"
                                    prepend-icon="mdi-file-excel"
                                    accept=".xlsx,.xls,.csv"
                                    variant="outlined"
                                    density="comfortable"
                                    hide-details
                                />
                            </VCol>

                            <VCol cols="12" md="4">
                                <VBtn color="success" block size="large" @click="subirExcel">
                                    <v-icon start>mdi-upload</v-icon>
                                    Importar
                                </VBtn>
                            </VCol>
                        </VRow>
                    </VCardText>
                </VCard>
            </VCol>
        </VRow>


        


        <!-- Tabla -->
        <Tabla
            :headers="headers"
            :items="eventosFiltrados"
            :items-per-page="itemsPerPage"
            :loading="loading"
            search
        >
            <template #item.fecha_evento="{ item }">
                {{ formatDate(item.fecha_evento) }}
            </template>
            <!-- Slot para estado -->
            <template #item.estado="{ item }">
                <VChip
                    :color="getEstadoColor(item.estado)"
                    size="small"
                    variant="tonal"
                >
                    {{ getEstadoName(item.estado) }}
                </VChip>
            </template>

            <!-- Slot para acciones -->
            <template #item.actions="{ item }">
                <div class="actions-buttons">
                    <RouterLink :to="`/asistentes/${item.id_evento}`">
                        <VTooltip location="top">
                            <template #activator="{ props }">
                                <VBtn
                                    :icon="tipoEventoInfo.botonIcono || 'mdi-clipboard-check'"
                                    size="small"
                                    variant="tonal"
                                    color="info"
                                    v-bind="props"
                                />
                            </template>
                            <span>{{ tipoEventoInfo.botonLabel }}</span>
                        </VTooltip>
                    </RouterLink>
                    <VTooltip location="top">
                        <template #activator="{ props }">
                            <VBtn
                                icon="mdi-pencil"
                                size="small"
                                variant="tonal"
                                color="warning"
                                v-bind="props"
                                @click="openEditDialog(item)"
                            />
                        </template>
                        <span>Editar evento</span>
                    </VTooltip>
                    <VTooltip location="top">
                        <template #activator="{ props }">
                            <VBtn
                                icon="mdi-delete"
                                size="small"
                                variant="tonal"
                                color="error"
                                v-bind="props"
                                @click="openDeleteDialog(item)"
                            />
                        </template>
                        <span>Eliminar evento</span>
                    </VTooltip>
                </div>
            </template>
        </Tabla>

        <Formulario
            v-model="dialog"
            :editMode="editMode"
            title="Evento"
            icon="mdi-shield-star"
            :fields="fields"
            :formData="form"
            :loading="loading"
            :errors="errors"
            @save="saveEvento"
        />
        
        <DeleteForm
            v-model="deleteDialog"
            :title="'Confirmar Eliminación'"
            :message="'¿Estás seguro de que deseas eliminar el evento:'"
            :itemInfo="`${selectedEvento?.nombre}`"
            :loading="loading"
            @deleteSelection="deleteEvento"
        />
    </div>
</template>

<style scoped>

.actions-buttons {
    display: flex;
    gap: 0.25rem;
}

.dialog-title {
    background: rgb(var(--v-theme-primary));
    color: rgb(var(--v-theme-on-primary));
    font-weight: 600;
    display: flex;
    align-items: center;
    border-radius: 4px 4px 0 0;
    padding: 12px 16px;
}

.user-info {
    padding: 1rem;
    background: rgb(var(--v-theme-surface-variant));
    border-radius: 8px;
    margin: 0.5rem 0;
}

@media (max-width: 768px) {

    .actions-buttons {
        flex-direction: column;
        gap: 0.5rem;
    }
}
</style>

