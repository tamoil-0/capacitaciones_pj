<script setup>
import { ref, computed, onMounted } from "vue";
import api from "@/axios";

// Componentes
import Header from "@/components/Titulo.vue";
import Filtros from "@/components/cruds/Filtros.vue";
import Tabla from "@/components/cruds/Tabla.vue";
import Formulario from "@/components/forms/Formulario.vue";
import DeleteForm from "@/components/forms/Delete.vue";

// Estados principales
const personas = ref([]);
const loading = ref(false);
// Estado Dialogs
const selectedPersona = ref(null);
const deleteDialog = ref(false);
// Estado Formulario
const dialog = ref(false);
const editMode = ref(false);
// Estado Filtros y búsqueda
const search = ref("");
const itemsPerPage = ref(10);

// Formulario principal
const form = ref({
    dni: "",
    nombres: "",
    apPaterno: "",
    apMaterno: "",
});

// Validaciones
const formValid = ref(false);
const errors = ref({});

// Headers de la tabla
const headers = [
    { title: "DNI",   key: "dni",    sortable: true, align: "center" },
    { title: "Nombres",          key: "nombres",       sortable: true },
    { title: "Apellido Paterno",           key: "apPaterno", sortable: true, align: "center" },
    { title: "Apellido Materno",          key: "apMaterno",       sortable: true, align: "center" },
    { title: "Acciones",        key: "actions",      sortable: false },
];

// Computed
const personasFiltrados = computed(() => {
    if (!personas.value) return [];

    return personas.value.filter((p) => {
        const matchesSearch =
            p.dni.includes(search.value) ||
            p.nombres.toLowerCase().includes(search.value.toLowerCase()) ||
            p.apPaterno.toLowerCase().includes(search.value.toLowerCase()) ||
            p.apMaterno.toLowerCase().includes(search.value.toLowerCase());

        return matchesSearch;
    });
});

// Métodos principales
const fetchPersonas = async () => {
    try {
        loading.value = true;
        const { data } = await api.get(`/personas`);
        personas.value = data;
    } catch (error) {
        console.error("Error al obtener eventos:", error);
    } finally {
        loading.value = false;
    }
};

// Definimos los campos para el formulario
const fields = ref([
    { key: "dni", label: "DNI", type: "text", rules: ["required", "dni"] },
    { key: "nombres", label: "Nombres", type: "text", rules: ["required"] },
    { key: "apPaterno", label: "Apellido Paterno", type: "text", rules: ["required"] },
    { key: "apMaterno", label: "Apellido Materno", type: "text", rules: ["required"] },
]);

const openCreateDialog = () => {
    editMode.value = false;
    Object.keys(form.value).forEach(k => (form.value[k] = "")); // limpiar
    dialog.value = true;
};

const openEditDialog = (persona) => {
    editMode.value = true;
    selectedPersona.value = persona;
    form.value = { ...persona };
    dialog.value = true;
};

const openDeleteDialog = (persona) => {
    selectedPersona.value = persona;
    deleteDialog.value = true;
};

// Guardar evento
const savePersona = async () => {
    try {
        loading.value = true;
        errors.value = {};

        if (editMode.value) {
            await api.put(`/personas/${selectedPersona.value.id_persona}`, form.value);
        } else {
            await api.post(`/personas`, form.value);
        }

        dialog.value = false;
        fetchPersonas();
    } catch (err) {
        errors.value = err.response?.data?.errors || {};
    } finally {
        loading.value = false;
    }
};

const deletePersona = async () => {
    try {
        loading.value = true;
        await api.delete(`/personas/${selectedPersona.value.id_persona}`);

        showAlert("Persona eliminado correctamente", "success");
        deleteDialog.value = false;
        selectedPersona.value = null;
        await fetchEventos();
    } catch (error) {
        console.error("Error al eliminar persona:", error);
        showAlert("Error al eliminar persona", "error");
    } finally {
        loading.value = false;
    }
};

const showAlert = (message, type) => {
    console.log(`${type.toUpperCase()}: ${message}`);
};

// Lifecycle
onMounted(() => {
    fetchPersonas();
});
</script>

<template>
    <div class="pagina">
        <!-- Header -->
        <Header
            titulo      = "Personas"
            subtitulo   = "Gestión de eventos asociados al tipo seleccionado"
            icono       = "mdi-account-group"
            nombreBTN   = "Nueva Persona"
            iconoBTN    = "mdi-person"
            @crear="openCreateDialog" 
        />

        <!-- Filtros -->
        <Filtros
            v-model:search="search"
            v-model:tipoFilter="estadoFilter"
            v-model:itemsPerPage="itemsPerPage"
            search-label="Buscar personas"
            search-placeholder="Ingrese DNI, nombres o apellidos"
            tipo-label="Sin filtro"
        />

        <!-- Tabla -->
        <Tabla
            :headers="headers"
            :items="personasFiltrados"
            :items-per-page="itemsPerPage"
            :loading="loading"
            search
        >
            <!-- Slot para acciones -->
            <template #item.actions="{ item }">
                <div class="actions-buttons">
                    <VBtn
                        icon="mdi-pencil"
                        size="small"
                        variant="text"
                        color="warning"
                        @click="openEditDialog(item)"
                    />
                    <VBtn
                        icon="mdi-delete"
                        size="small"
                        variant="text"
                        color="error"
                        @click="openDeleteDialog(item)"
                    />
                </div>
            </template>
        </Tabla>

        <Formulario
            v-model="dialog"
            :editMode="editMode"
            title="Persona"
            icon="mdi-shield-star"
            :fields="fields"
            :formData="form"
            :loading="loading"
            :errors="errors"
            @save="savePersona"
        />
        
        <DeleteForm
            v-model="deleteDialog"
            :title="'Confirmar Eliminación'"
            :message="'¿Estás seguro de que deseas eliminar el evento:'"
            :itemInfo="`${selectedPersona?.nombres} ${selectedPersona?.apPaterno} ${selectedPersona?.apMaterno}`"
            :loading="loading"
            @deleteSelection="deletePersona"
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

