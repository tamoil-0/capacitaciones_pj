<script setup>
import { ref, computed, onMounted, watch, reactive} from "vue";
import api from "@/axios";

// Componentes reutilizables
import Header from "@/components/Titulo.vue";
import Filtros from "@/components/cruds/Filtros.vue";
import Tabla from "@/components/cruds/Tabla.vue";
import Formulario from "@/components/forms/Formulario.vue";
import DeleteForm from "@/components/forms/Delete.vue";

// Estados principales
const usuarios = ref([]);
const loading = ref(false);
// Dialogs
const selectedUser = ref(null);
const passwordDialog = ref(false);
const showPassword = ref(false)
const deleteDialog = ref(false);
// Formulario
const dialog = ref(false);
const editMode = ref(false);
// Estado Filtros y búsqueda
const search = ref("");
const tipoFilter = ref(null);
const itemsPerPage = ref(10);

const tiposUsuario = [
    { value: 2, title: "Organizador", color: "warning" },
    { value: 3, title: "Apoyo", color: "info" },
];

const tiposEvento = [
    { value: 1, title: "Convocatorias", color: "success" },
    { value: 2, title: "Cursos",        color: "info" },
    { value: 3, title: "Otros",         color: "warning" },
];

const estadosUsuario = [
    { value: 0, title: "Inhabilitado", color: "error" },
    { value: 1, title: "Habilitado", color: "success" },
];

// Formulario principal
const form = ref({
    nombres_apellidos: "",
    contrasena: "",
    confirmarContrasena: "",
    tipo_usuario: null,
    asignado: null,
    habilitado: 1,
});

// Formulario de reestablecer de contraseña
const passwordForm = reactive({
    contrasena_nueva: ""
})

// Validaciones
const passwordValid = ref(false)
const errors = ref({});

// Headers de la tabla
const headers = [
    { title: "N°", key: "contador", align: "center" },
    { title: "Nombre del Encargado",        key: "nombres_apellidos",  sortable: true },
    { title: "Usuario",                     key: "nickname",           sortable: true },
    { title: "Tipo",                        key: "tipo_usuario",       sortable: true,     align: "center" },
    { title: "Tipo de Evento Asignado",     key: "asignado",           sortable: true,     align: "center" },
    { title: "Habilitado",                  key: "habilitado",         sortable: true,     align: "center" },
    { title: "Acciones",                    key: "actions",            sortable: false },
];
// Reglas
const rules = {
    required: (value) => !!value || "Este campo es obligatorio",
    password: (value) => value && value.length >= 6 || "La contraseña debe tener al menos 6 caracteres"
}

// Computed
const filteredUsers = computed(() => {
    if (!usuarios.value) return [];
    
    return usuarios.value
        .filter((usuario) => {
            const matchesSearch =
                usuario.nombres_apellidos.includes(search.value) ||
                usuario.nickname.toLowerCase().includes(search.value.toLowerCase());

            const matchesTipo = tipoFilter.value !== null
                ? usuario.tipo_usuario === tipoFilter.value
                : true

            return matchesSearch && matchesTipo;
        }) 
});

// Métodos principales
const fetchUsuarios = async () => {
    try {
        loading.value = true;
        const { data } = await api.get("/usuarios");
        usuarios.value = data;
    } catch (error) {
        console.error("Error al obtener usuarios:", error);
        showAlert("Error al cargar usuarios", "error");
    } finally {
        loading.value = false;
    }
};

// Definimos los campos para el formulario
const baseFields = [
    { key: "nickname",          label: "Usuario",           type: "text", rules: ["required"] },
    { key: "nombres_apellidos", label: "Nombres Completos", type: "text", rules: ["required"] },
    {
        key: "tipo_usuario",
        label: "Tipo de usuario",
        type: "select",
        options: tiposUsuario,
        itemTitle: "title",
        itemValue: "value",
        rules: ["required"]
    },
    {
        key: "habilitado",
        label: "Estado del usuario",
        type: "select",
        options: estadosUsuario,
        itemTitle: "title",
        itemValue: "value"
    },
    {
        key: "asignado",
        label: "Tipo de Evento asignado",
        type: "select",
        options: tiposEvento,
        itemTitle: "title",
        itemValue: "value"
    },
];

const passwordFields = [
    { key: "contraseña", label: "Contraseña", type: "password", rules: ["required","password"] },
    { key: "confirmarContraseña", label: "Confirmar Contraseña", type: "password", rules: ["required"] }
];

const fields = ref(
    editMode.value ? [...baseFields] : [...baseFields, ...passwordFields]
);

// Campos de contraseña solo si es creación
watch(editMode, (isEdit) => {
    if (isEdit) {
        fields.value = [...baseFields]; // edición → sin password
    } else {
        fields.value = [...baseFields, ...passwordFields]; // creación → con password
    }
});

// Abrir el dialog para crear
const openCreateDialog = () => {
    editMode.value = false;
    Object.keys(form.value).forEach(k => (form.value[k] = "")); // limpiar
    dialog.value = true;
};
// Abrir el dialog para editar
const openEditDialog = (user) => {
    editMode.value = true;
    selectedUser.value = user;
    form.value = { ...user};
    dialog.value = true;
};
// Abrir dialog para eliminar
const openDeleteDialog = (user) => {
    selectedUser.value = user;
    deleteDialog.value = true;
};
//
const openResetPasswordDialog = (user) => {
    selectedUser.value = user
    passwordForm.contraseña_nueva = "" // limpiar form
    showPassword.value = false
    passwordDialog.value = true
}

const saveUser = async () => {
    try {
        loading.value = true;
        errors.value = {};

        const userData = {
            nombres_apellidos: form.value.nombres_apellidos,
            nickname: form.value.nickname,
            tipo_usuario: form.value.tipo_usuario,
            asignado: form.value.asignado,
            habilitado: form.value.habilitado,
        };

        if (!editMode.value) {
            userData.contrasena = form.value.contraseña;
        }

        if (editMode.value) {
            await api.put(`/usuario/${selectedUser.value.id_usuario}`, userData);
            showAlert("Usuario actualizado correctamente", "success");
        } else {
            await api.post("/usuarios", userData);
            showAlert("Usuario creado correctamente", "success");
        }

        dialog.value = false;
        fetchUsuarios();
    } catch (error) {
        if (error.response?.status === 422) {
            errors.value = error.response.data.errors || {};
            showAlert("Por favor corrige los errores", "error");
        } else {
            console.error("Error al guardar usuario:", error);
            showAlert("Error al guardar usuario", "error");
        }
    } finally {
        loading.value = false;
    }
};

const deleteUser = async () => {
    try {
        loading.value = true;
        await api.delete(`/usuarios/${selectedUser.value.id_usuario}`);

        showAlert("Usuario eliminado correctamente", "success");
        deleteDialog.value = false;
        selectedUser.value = null;
        await fetchUsuarios();
    } catch (error) {
        console.error("Error al eliminar usuario:", error);
        showAlert("Error al eliminar usuario", "error");
    } finally {
        loading.value = false;
    }
};

const changePassword = async () => {
    try {
        loading.value = true
        await api.post(`/usuarios/restablecer-password/${selectedUser.value.id_usuario}`, {
        contraseña_nueva: passwordForm.contraseña_nueva,
        })
        passwordDialog.value = false
        // notificación opcional
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
}

const showAlert = (message, type) => {
    // Implementar con tu sistema de notificaciones preferido
    console.log(`${type.toUpperCase()}: ${message}`);
};

const getTipoColor = (tipo) => {
    return tiposUsuario.find((t) => t.value === tipo)?.color || "default";
};

const getTipoName = (tipo) => {
    switch (tipo) {
        case 2: return "Organizador";
        case 3: return "Apoyo";
        default: return "N/A";
    }
};

const getTipoColor2 = (tipo) => {
    return estadosUsuario.find((t) => t.value === tipo)?.color || "default";
};

const getTipoName2 = (tipo) => {
    switch (tipo) {
        case 0: return "Inhabilitado";
        case 1: return "Habilitado";
        default: return "N/A";
    }
};

const getTipoColor3 = (tipo) => {
    return tiposEvento.find((t) => t.value === tipo)?.color || "default";
};

const getTipoName3 = (tipo) => {
    switch (tipo) {
        case 1: return "Convocatoria";
        case 2: return "Cursos";
        case 3: return "Otros";
        default: return "N/A";
    }
};

onMounted(() => {
    fetchUsuarios();
});
</script>

<template>
    <div class="pagina" >
        <!-- Header -->
        <Header
            titulo      = "Gestión de Usuarios"
            subtitulo   = "Administra usuarios del sistema con roles y permisos"
            icono       = "mdi-account-group"
            nombreBTN   = "Nuevo Usuario"
            iconoBTN    = "mdi-account-plus"
            @crear="openCreateDialog" 
        />

        <!-- Filtros -->
        <Filtros
            v-model:search="search"
            v-model:tipoFilter="tipoFilter"
            v-model:itemsPerPage="itemsPerPage"
            search-label="Buscar usuarios"
            search-placeholder="DNI, nombre, apellido o correo"
            tipo-label="Filtrar por tipo de usuario"
            :tipos="tiposUsuario"
        />

        <!-- Tabla -->
        <Tabla
            :headers="headers"
            :items="filteredUsers"
            :items-per-page="itemsPerPage"
            :loading="loading"
            :search="search"
        >
            <template #item.contador="{ index }">
                {{ index + 1 }}
            </template>

            <!-- Slot para tipo de usuario estadosUsuario-->
            <template #[`item.tipo_usuario`]="{ item }">
                <VChip
                    :color="getTipoColor(item.tipo_usuario)"
                    size="small"
                    variant="tonal"
                >
                    {{ getTipoName(item.tipo_usuario) }}
                </VChip>
            </template>

            <!-- Slot para tipo de evento -->
            <template #[`item.asignado`]="{ item }">
                <VChip
                    :color="getTipoColor2(item.asignado)"
                    size="small"
                    variant="tonal"
                >
                    {{ getTipoName3(item.asignado) }}
                </VChip>
            </template>

            <!-- Slot para tipo de usuario -->
            <template #[`item.habilitado`]="{ item }">
                <VChip
                    :color="getTipoColor2(item.habilitado)"
                    size="small"
                    variant="tonal"
                >
                    {{ getTipoName2(item.habilitado) }}
                </VChip>
            </template>


            <!-- Slot para acciones -->
            <template #item.actions="{ item }">
                <div class="actions-buttons">
                    <VBtn
                        icon="mdi-pencil"
                        size="small"
                        variant="text"
                        color="primary"
                        @click="openEditDialog(item)"
                    />
                    <VBtn
                        v-bind="props"
                        icon="mdi-lock-reset"
                        size="small"
                        variant="text"
                        color="warning"
                        @click="openResetPasswordDialog(item)"
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

        <!-- Dialog Crear/Editar Usuario -->
        <Formulario
            v-model="dialog"
            :editMode="editMode"
            title="Usuario"
            icon="mdi-account-plus"
            :fields="fields"
            :formData="form"
            :loading="loading"
            :errors="errors"
            @save="saveUser"
        />

        <!-- Dialog Eliminar -->
        <DeleteForm
            v-model="deleteDialog"
            :title="'Confirmar Eliminación'"
            :message="'¿Estás seguro de que deseas eliminar al usuario:'"
            :itemInfo="`${selectedUser?.nombres_apellidos}`"
            :loading="loading"
            @deleteSelection="deleteUser"
        />

        <!-- Dialog Resetear Contraseña -->
        <VDialog v-model="passwordDialog" max-width="500" persistent>
            <VCard>
                <VCardTitle class="dialog-title">
                    <VIcon icon="mdi-lock-reset" class="mr-2" />
                    Resetear Contraseña
                </VCardTitle>

                <VForm v-model="passwordValid" @submit.prevent="changePassword">
                    <VCardText>
                        <div class="user-info mb-4">
                            <strong>
                                {{ selectedUser?.nombres_apellidos }}
                            </strong>
                        </div>

                        <!-- Campo único de nueva contraseña con ojito -->
                        <VTextField
                            v-model="passwordForm.contraseña_nueva"
                            :rules="[rules.required, rules.password]"
                            label="Nueva Contraseña"
                            variant="outlined"
                            :type="showPassword ? 'text' : 'password'"
                            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                            @click:append-inner="showPassword = !showPassword"
                        />
                    </VCardText>

                    <VCardActions>
                        <VSpacer />
                        <VBtn
                            variant="text"
                            @click="passwordDialog = false"
                            :disabled="loading"
                        >
                            Cancelar
                        </VBtn>
                        <VBtn
                            color="primary"
                            type="submit"
                            :loading="loading"
                            :disabled="!passwordValid"
                        >
                            Guardar
                        </VBtn>
                    </VCardActions>
                </VForm>
            </VCard>
        </VDialog>

    </div>
</template>


