<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from "vue";
import { useRoute } from "vue-router";
import api from "@/axios";

// Componentes reutilizables
import Header from "@/components/Titulo.vue";
import Filtros from "@/components/cruds/Filtros.vue";
import Tabla from "@/components/cruds/Tabla.vue";
import Formulario from "@/components/forms/Formulario.vue";
import DeleteForm from "@/components/forms/Delete.vue";

// Estados principales
const route = useRoute();
const idEvento = route.params.idEvento;
const inscritos = ref([]);
const loading = ref(false);
// Estado del archivo Excel
const excelFile = ref(null);
// Estados de la asistencia
// Estado Dialogs
const selectedInscrito = ref(null);
const deleteDialog = ref(false);
// Formulario
const dialog = ref(false);
const editMode = ref(false);
// Estado Filtros y búsqueda
const search = ref("");
const estadoFilter = ref(null);
const itemsPerPage = ref(10);

const usuario = ref(null);


// Formulario principal
const formData = ref({
    dni: "",
    nombres: "",
    apPaterno: "",
    apMaterno: "",
    asistio: 0, // Por defecto "No asistio"
});

// Validaciones
const errors = ref({});

// Headers de la tabla (acciones solo si id_usuario <= 2)
const headers = computed(() => {
    let base = [
        { title: "N°", key: "contador", align: "center" },
        { title: "DNI", key: "dni", sortable: true },
        { title: "Nombres", key: "nombre", sortable: true },
        { title: "Apellido Paterno", key: "apPaterno", sortable: true },
        { title: "Apellido Materno", key: "apMaterno", sortable: true },

       // { title: "Entradas", key: "entradas", align:"center" },
       // { title: "Salidas", key: "salidas", align:"center" }
    ];


    if (usuario.value && usuario.value.id_usuario < 3) {
        base.push({ title: "Acciones", key: "actions", sortable: false, align: "center" });
    }

    return base;
});


// Computed
const inscritosFiltrados = computed(() => {
    if (!inscritos.value) return [];

    return inscritos.value.filter((e) => {
        const matchesSearch =
            e.dni.includes(search.value) ||
            e.nombre.toLowerCase().includes(search.value.toLowerCase()) ||
            e.apPaterno.toLowerCase().includes(search.value.toLowerCase()) ||
            e.apMaterno.toLowerCase().includes(search.value.toLowerCase());

        const matchesEstado = estadoFilter.value !== null
            ? e.estado === estadoFilter.value
            : true;

        return matchesSearch && matchesEstado;
    });
});

// ════════════════════════════════════════════════════════════
// 📊 ESTADÍSTICAS DE ASISTENCIAS
// ════════════════════════════════════════════════════════════
const estadisticas = computed(() => {
    const totalInscritos = inscritos.value.length;
    const conEntradas = inscritos.value.filter(i => i.entradas > 0).length;
    const conSalidas = inscritos.value.filter(i => i.salidas > 0).length;
    const sinRegistros = inscritos.value.filter(i => i.entradas === 0 && i.salidas === 0).length;
    
    const porcentajeAsistencia = totalInscritos > 0 
        ? ((conEntradas / totalInscritos) * 100).toFixed(1) 
        : 0;
    
    return {
        totalInscritos,
        conEntradas,
        conSalidas,
        sinRegistros,
        porcentajeAsistencia
    };
});

// Métodos principales
const fetchInscritos = async () => {
    try {
        loading.value = true;
        const { data } = await api.get(`/inscritos/${idEvento}`);

        // Mapeamos los datos de la API a lo que la tabla necesita
        inscritos.value = data.map((i, index) => ({
            contador: index + 1,
            id: i.id_inscripcion,
            id_evento: i.evento,
            dni: i.persona.dni,
            nombre: i.persona.nombres,
            apPaterno: i.persona.apPaterno,
            apMaterno: i.persona.apMaterno,

            entradas: i.entradas,
            salidas: i.salidas
        }));


    } catch (error) {
        console.error("Error al obtener las personas del evento:", error);
    } finally {
        loading.value = false;
    }
};

// Definimos los campos para el formulario
const fields = ref([
    { key: "dni",           label: "DNI",               type: "text", rules: ["required"] },
    { key: "nombres",       label: "Nombre",            type: "text", rules: ["required"] },
    { key: "apPaterno",     label: "Apellido Paterno",  type: "text", rules: ["required"] },
    { key: "apMaterno",     label: "Apellido Materno",  type: "text", rules: ["required"] },
]);

// Abrir el dialog para crear
const openCreateDialog = () => {
    editMode.value = false;
    Object.keys(formData.value).forEach(k => (formData.value[k] = "")); // limpiar
    dialog.value = true;
};

const openAsistenciaDialog = () => {
    asistenciaDialog.value = true
};

// Eliminar inscrito
const deleteInscrito = async () => {
    try {
        loading.value = true;
        await api.delete(`/inscritos/${selectedInscrito.value.id}`);
        
        // Eliminar del array local
        inscritos.value = inscritos.value.filter(i => i.id !== selectedInscrito.value.id);
        
        showSnackbar("Inscrito eliminado correctamente", "success");
        deleteDialog.value = false;
        selectedInscrito.value = null;
    } catch (error) {
        console.error("Error al eliminar inscrito:", error);
        showSnackbar("Error al eliminar inscrito", "error");
    } finally {
        loading.value = false;
    }
};

// Abrir el diálogo de eliminación
const openDeleteDialog = (item) => {
    selectedInscrito.value = item;
    deleteDialog.value = true;
};

// Guardar evento
const saveInscrito = async () => {
    try {
        loading.value = true;
        errors.value = {};

        const { data } = await api.post(`/inscritos/${idEvento}`, formData.value);
        
        // Agregar nuevo inscrito al inicio de la lista
        inscritos.value.unshift(data);

        dialog.value = false;
    } catch (err) {
        errors.value = err.response?.data?.errors || {};
    } finally {
        loading.value = false;
    }
};

const showAlert = (message, type) => {
    console.log(`${type.toUpperCase()}: ${message}`);
};

// MODAL de registros
const registrosDialog = ref(false);
const registros = ref([]);
const seleccionado = ref(null);
const loadingRegistros = ref(false);

// Snackbar (alert)
const snackbar = ref({
    visible: false,
    color: "success",
    text: "",
    timeout: 10000,
});

// Estados para filtros
const estados = [
    { value: 0, title: "Todos" },
];

// Headers para el modal de registros
const registrosHeaders = [
    { title: "Fecha/Hora", key: "fecha_registro", sortable: true },
    { title: "Tipo", key: "tipo", sortable: true },
    { title: "Estado", key: "estado", sortable: true },
];

// Computed para los datos de registros
const registrosData = computed(() => {
    if (!registros.value || !Array.isArray(registros.value)) return [];
    return registros.value.map(reg => ({
        ...reg,
        fecha_registro: formatDateTime(reg.created_at)
    }));
});

// Formatear fecha y hora
const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
};

// Abrir modal de registros por persona
const openRegistrosDialog = async (item) => {
    try {
        loadingRegistros.value = true;
        selectedInscrito.value = item;
        registrosDialog.value = true;

        const { data } = await api.get(`/registros/${item.id}`);
        registros.value = data.registros || [];

        showSnackbar(`Se cargaron ${registros.value.length} registros de asistencia.`, "success");
    } catch (error) {
        console.error(error);
        showSnackbar("Error al cargar los registros.", "error");
    } finally {
        loadingRegistros.value = false;
    }
};

// Mostrar alerta tipo snackbar
const showSnackbar = (message, type = "success") => {
  snackbar.value.text = message;
  snackbar.value.color = type === "error" ? "red-darken-1" : "green-darken-1";
  snackbar.value.visible = true;
};

// Función para subir Excel
const uploadExcel = async () => {
  if (!excelFile.value) {
    showSnackbar("Selecciona un archivo primero", "error");
    return;
  }

  try {
    const formData = new FormData();
    formData.append("file", excelFile.value);

    await api.post(`/inscritos/importar-personas/${idEvento}`, formData);

    showSnackbar("Personas importadas con éxito", "success");
    await fetchInscritos();
  } catch (error) {
    console.error(error);
    showSnackbar("Error al importar el archivo Excel", "error");
  }
};

// ════════════════════════════════════════════════════════════
// 📊 EXPORTAR ASISTENCIAS A EXCEL
// ════════════════════════════════════════════════════════════
const exportando = ref(false);
const exportarAsistencias = async () => {
    try {
        exportando.value = true;
        
        // Exportar asistencias del evento específico
        const { data } = await api.get(`/registros/exportar/${idEvento}`);
        
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
            showSnackbar(`Excel generado: ${data.data.nombre_archivo}`, "success");
        }
    } catch (error) {
        console.error('Error al exportar asistencias:', error);
        showSnackbar('Error al generar el archivo Excel', "error");
    } finally {
        exportando.value = false;
    }
};

// Asistencia
const dniAsistencia = ref("");
const tipoSeleccionado = ref("Entrada");
const tipoPersonalizado = ref("");
const bloqueado = ref(false);
const loadingAsistencia = ref(false);

const botones = ["Entrada", "Salida"];

const seleccionarTipo = (tipo) => {
    tipoSeleccionado.value = tipo;
    if (tipo !== "Otro") {
        tipoPersonalizado.value = "";
        bloqueado.value = false;
    }
};

// Estados para modales informativos
const errorDialog = ref(false);
const errorMessage = ref("");
const errorTitle = ref("");
const errorPersona = ref(null);

// Registrar asistencia con validación
const registrarAsistencia = async () => {
  if (dniAsistencia.value.length !== 8) {
    showSnackbar("Ingrese un DNI válido (8 dígitos)", "error");
    return;
  }

  let tipo =
    tipoSeleccionado.value === "Otro" && tipoPersonalizado.value
      ? tipoPersonalizado.value
      : tipoSeleccionado.value;

  try {
    loadingAsistencia.value = true;

    await api.post(`/registrar/${idEvento}/${dniAsistencia.value}`, {
      tipo: tipo,
    });

    showSnackbar(`Asistencia (${tipo}) registrada con éxito`, "success");

    dniAsistencia.value = "";
    tipoPersonalizado.value = "";
    bloqueado.value = false;

    await fetchInscritos();
  } catch (error) {
    console.error(error);
    
    // Manejar errores específicos
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;
      
      if (status === 404) {
        // Persona no inscrita
        errorTitle.value = "⚠️ Persona No Inscrita";
        errorMessage.value = data.message || "Esta persona no está inscrita en el evento.";
        errorPersona.value = null;
        errorDialog.value = true;
      } else if (status === 409) {
        // Manejar diferentes tipos de error 409
        errorPersona.value = data.persona;
        errorDialog.value = true;
        
        switch(data.error) {
          case 'DUPLICADO':
            errorTitle.value = "🚫 Registro Duplicado";
            errorMessage.value = data.message;
            break;
          case 'YA_TIENE_ENTRADA':
            errorTitle.value = "✋ Entrada Ya Registrada";
            errorMessage.value = data.message;
            break;
          case 'YA_TIENE_SALIDA':
            errorTitle.value = "✋ Salida Ya Registrada";
            errorMessage.value = data.message;
            break;
          case 'SIN_ENTRADA_PREVIA':
            errorTitle.value = "⚠️ Sin Entrada Previa";
            errorMessage.value = data.message;
            break;
          default:
            errorTitle.value = "❌ Error";
            errorMessage.value = data.message;
        }
      } else {
        showSnackbar(data.message || "Error al registrar asistencia", "error");
      }
    } else {
      showSnackbar("Error de conexión al servidor", "error");
    }
    
    // Limpiar DNI en caso de error
    dniAsistencia.value = "";
  } finally {
    loadingAsistencia.value = false;
  }
};

watch(dniAsistencia, (nuevo) => {
    if (nuevo && nuevo.length === 8 && !loadingAsistencia.value) {
        registrarAsistencia();   // Registro automático
    }
});


// Auto-actualización cada 5 segundos
let autoRefreshInterval = null;

// Lifecycle
onMounted(() => {
    usuario.value = JSON.parse(localStorage.getItem("usuario"));
    fetchInscritos();
    
    // Iniciar auto-actualización cada 5 segundos
    autoRefreshInterval = setInterval(() => {
        fetchInscritos();
    }, 5000);
});

// Limpiar interval al desmontar
onBeforeUnmount(() => {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});
</script>

<template>
    <div class="pagina">
        <!-- Header -->
        <Header
            titulo="Asistentes"
            subtitulo="Gestión de asistentes al evento"
            icono="mdi-account-group"
            v-if="usuario && usuario.id_usuario < 3"
            nombreBTN="Nuevo Asistente"
            iconoBTN="mdi-account-plus"
            @crear="openCreateDialog" 
        />
        <Header
            v-else
            titulo="Asistentes"
            subtitulo="Gestión de asistentes al evento"
            icono="mdi-calendar"
        />

        <VRow align="center" dense>
            <!-- Filtros -->
            <VCol cols="12" md="5">
                <Filtros
                    v-model:search="search"
                    v-model:tipoFilter="estadoFilter"
                    v-model:itemsPerPage="itemsPerPage"
                    search-label="Buscar persona"
                    search-placeholder="Nombre o Apellidos"
                    tipo-label="Filtrar por estado"
                    :tipos="estados"
                />
            </VCol>

            <!-- Botón Exportar Excel -->
            <VCol cols="12" md="2">
                <VCard 
                    elevation="4" 
                    class="export-card" 
                    @click="exportarAsistencias"
                    :disabled="exportando"
                    :loading="exportando"
                    style="cursor: pointer; transition: all 0.3s ease;"
                    hover
                >
                    <VCardText class="text-center pa-3">
                        <VIcon 
                            size="40" 
                            color="success" 
                            class="mb-2"
                        >
                            mdi-file-excel-box
                        </VIcon>
                        <div class="text-subtitle-2 font-weight-bold text-success">
                            Exportar Excel
                        </div>
                        <div class="text-caption text-grey">
                            {{ inscritos.length }} registros
                        </div>
                    </VCardText>
                </VCard>
            </VCol>
            
            <!-- Métodos importar  -->
            <VCol cols="12" md="5">
                <VCard class="mb-6" elevation="2">
                    <VCardText>
                        <VRow align="center" dense>
                            <!-- Subir Excel SOLO si admin -->
                            
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
                                <VBtn color="success" block size="large" @click="uploadExcel">
                                    <v-icon start>mdi-upload</v-icon>
                                    Importar
                                </VBtn>
                            </VCol>
                        </VRow>
                    </VCardText>
                </VCard>
            </VCol>
        </VRow>

        <!-- ════════════════════════════════════════════════════════════ -->
        <!-- 📊 ESTADÍSTICAS DE ASISTENCIAS -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <VCard elevation="3" class="mb-6">
            <VCardTitle class="bg-gradient-primary text-white pa-4">
                <VIcon icon="mdi-chart-box" size="24" class="mr-2"></VIcon>
                Estadísticas de Asistencias
            </VCardTitle>
            <VCardText class="pa-6">
                <VRow>
                    <VCol cols="6" md="3">
                        <VCard elevation="1" class="stat-card text-center pa-4" style="border-top: 4px solid #2196f3;">
                            <VIcon icon="mdi-account-group" size="48" color="primary" class="mb-2"></VIcon>
                            <div class="text-h4 font-weight-bold text-primary">{{ estadisticas.totalInscritos }}</div>
                            <div class="text-caption text-grey-darken-1">Total Inscritos</div>
                        </VCard>
                    </VCol>
                    <VCol cols="6" md="3">
                        <VCard elevation="1" class="stat-card text-center pa-4" style="border-top: 4px solid #4caf50;">
                            <VIcon icon="mdi-login" size="48" color="success" class="mb-2"></VIcon>
                            <div class="text-h4 font-weight-bold text-success">{{ estadisticas.conEntradas }}</div>
                            <div class="text-caption text-grey-darken-1">Con Entradas</div>
                        </VCard>
                    </VCol>
                    <VCol cols="6" md="3">
                        <VCard elevation="1" class="stat-card text-center pa-4" style="border-top: 4px solid #ff9800;">
                            <VIcon icon="mdi-logout" size="48" color="warning" class="mb-2"></VIcon>
                            <div class="text-h4 font-weight-bold text-warning">{{ estadisticas.conSalidas }}</div>
                            <div class="text-caption text-grey-darken-1">Con Salidas</div>
                        </VCard>
                    </VCol>
                    <VCol cols="6" md="3">
                        <VCard elevation="1" class="stat-card text-center pa-4" style="border-top: 4px solid #9e9e9e;">
                            <VIcon icon="mdi-account-off" size="48" color="grey" class="mb-2"></VIcon>
                            <div class="text-h4 font-weight-bold text-grey">{{ estadisticas.sinRegistros }}</div>
                            <div class="text-caption text-grey-darken-1">Sin Registros</div>
                        </VCard>
                    </VCol>
                </VRow>
                
                <!-- Barra de progreso de asistencia -->
                <VRow class="mt-4">
                    <VCol cols="12">
                        <div class="text-subtitle-1 font-weight-bold mb-2">
                            Porcentaje de Asistencia: {{ estadisticas.porcentajeAsistencia }}%
                        </div>
                        <VProgressLinear
                            :model-value="estadisticas.porcentajeAsistencia"
                            height="25"
                            :color="estadisticas.porcentajeAsistencia >= 70 ? 'success' : (estadisticas.porcentajeAsistencia >= 40 ? 'warning' : 'error')"
                            rounded
                        >
                            <template v-slot:default>
                                <strong class="text-white">{{ estadisticas.porcentajeAsistencia }}%</strong>
                            </template>
                        </VProgressLinear>
                    </VCol>
                </VRow>
            </VCardText>
        </VCard>

        <VRow>
            <!-- Tabla de inscritos -->
            <VCol cols="12" md="8">
                <Tabla
                    :headers="headers"
                    :items="inscritosFiltrados"
                    :items-per-page="itemsPerPage"
                    :loading="loading"
                    search
                >
                    <template #item="{ item }">
                        <tr
                            :style="{
                            backgroundColor:
                                tipoSeleccionado === 'Entrada'
                                ? (item.entradas > 0 ? '#c8facd' : 'white')
                                : (item.salidas > 0 ? '#ffe0b2' : 'white')
                            }"
                        >
                            <td>{{ item.contador }}</td>
                            <td>{{ item.dni }}</td>
                            <td>{{ item.nombre }}</td>
                            <td>{{ item.apPaterno }}</td>
                            <td>{{ item.apMaterno }}</td>
                            <!-- <td class="text-center">{{ item.entradas }}</td> -->
                            <!-- <td class="text-center">{{ item.salidas }}</td> -->

                            <!-- Acciones intuitivas -->
                            <td v-if="usuario && usuario.id_usuario < 3" class="text-center">
                                <!-- Botón Ver Registros -->
                                <VTooltip text="Ver historial de asistencias">
                                    <template #activator="{ props }">
                                        <VBtn
                                            v-bind="props"
                                            icon="mdi-clipboard-text-clock"
                                            size="small"
                                            variant="tonal"
                                            color="primary"
                                            @click="openRegistrosDialog(item)"
                                            class="mr-1"
                                        />
                                    </template>
                                </VTooltip>
                                
                                <!-- Botón Eliminar -->
                                <VTooltip text="Eliminar inscrito">
                                    <template #activator="{ props }">
                                        <VBtn
                                            v-bind="props"
                                            icon="mdi-delete-outline"
                                            size="small"
                                            variant="tonal"
                                            color="error"
                                            @click="openDeleteDialog(item)"
                                        />
                                    </template>
                                </VTooltip>
                            </td>
                        </tr>
                        </template>

                </Tabla>
            </VCol>

            <!-- Panel lateral de asistencia -->
            <VCol cols="12" md="4">
            <VCard elevation="2" class="pa-4">
                <VCardTitle class="text-h6 text-center">Tomar asistencia</VCardTitle>
                <VCardText>

                <!-- ✅ GRUPO DE BOTONES -->
                <VBtnGroup
                    divided
                    class="mb-4 w-90 d-flex justify-center"
                >
                    <VBtn
                        v-for="b in botones"
                        :key="b"
                        :color="tipoSeleccionado === b ? 'primary' : 'grey-lighten-2'"
                        variant="flat"
                        class="flex-1"
                        @click="seleccionarTipo(b)"
                    >
                        {{ b }}
                    </VBtn>
                </VBtnGroup>

                <!-- Campo “Otro” -->
                <VTextField
                    v-if="tipoSeleccionado === 'Otro'"
                    v-model="tipoPersonalizado"
                    label="Especificar tipo"
                    prepend-inner-icon="mdi-pencil"
                    :readonly="bloqueado"
                    append-inner-icon="mdi-check"
                    @click:append-inner="bloqueado = !bloqueado"
                    density="comfortable"
                />

                <!-- DNI -->
                <VTextField
                    v-model="dniAsistencia"
                    label="Ingrese DNI"
                    prepend-icon="mdi-card-account-details"
                    maxlength="8"
                    variant="outlined"
                    autofocus
                    class="mt-4"
                    :loading="loadingAsistencia"
                    @keyup.enter="registrarAsistencia"
                />

                <!-- Botón Registrar -->
                <VBtn
                    block
                    color="success"
                    size="large"
                    class="mt-3"
                    :loading="loadingAsistencia"
                    @click="registrarAsistencia"
                >
                    <v-icon start>mdi-check-decagram</v-icon>
                    Registrar
                </VBtn>

                </VCardText>
            </VCard>
            </VCol>
        </VRow>

        <Formulario
            v-model="dialog"
            :editMode="editMode"
            title="Incrito"
            icon="mdi-shield-star"
            :fields="fields"
            :formData="formData"
            :loading="loading"
            :errors="errors"
            @save="saveInscrito"
        />

        <DeleteForm
            v-model="deleteDialog"
            :title="'Confirmar Eliminación'"
            :message="'¿Estás seguro de que deseas eliminar al inscrito:'"
            :itemInfo="`${selectedInscrito?.nombre} ${selectedInscrito?.apPaterno}`"
            :loading="loading"
            @deleteSelection="deleteInscrito"
        />

        <VDialog v-model="registrosDialog" max-width="900">
            <VCard>
                <VCardTitle class="bg-primary text-white">
                    <VIcon icon="mdi-clipboard-text-clock" class="mr-2"></VIcon>
                    Historial de Asistencias
                </VCardTitle>
                <VCardText class="pa-6">
                    <div v-if="loadingRegistros" class="text-center py-8">
                        <VProgressCircular indeterminate color="primary"></VProgressCircular>
                    </div>
                    <div v-else>
                        <div class="mb-4">
                            <strong>Persona:</strong> {{ selectedInscrito?.nombre }} {{ selectedInscrito?.apPaterno }} {{ selectedInscrito?.apMaterno }}<br>
                            <strong>DNI:</strong> {{ selectedInscrito?.dni }}<br>
                            <strong>Total Registros:</strong> {{ registrosData.length }}
                        </div>
                        <VDataTable
                            :headers="registrosHeaders"
                            :items="registrosData"
                            :items-per-page="5"
                            density="comfortable"
                        >
                            <template #item.tipo="{ item }">
                                <VChip
                                    :color="item.tipo === 'entrada' ? 'success' : (item.tipo === 'salida' ? 'warning' : 'grey')"
                                    size="small"
                                >
                                    {{ item.tipo.toUpperCase() }}
                                </VChip>
                            </template>
                            <template #item.estado="{ item }">
                                <VChip
                                    :color="item.estado === 'A TIEMPO' ? 'success' : 'warning'"
                                    size="small"
                                >
                                    {{ item.estado }}
                                </VChip>
                            </template>
                        </VDataTable>
                    </div>
                </VCardText>
                <VCardActions>
                    <VSpacer></VSpacer>
                    <VBtn color="primary" @click="registrosDialog = false">Cerrar</VBtn>
                </VCardActions>
            </VCard>
        </VDialog>

        <!-- Modal de errores informativos -->
        <VDialog v-model="errorDialog" max-width="500">
            <VCard>
                <VCardTitle class="bg-error text-white d-flex align-center">
                    <VIcon icon="mdi-alert-circle" class="mr-2"></VIcon>
                    {{ errorTitle }}
                </VCardTitle>
                <VCardText class="pa-6">
                    <VAlert
                        type="error"
                        variant="tonal"
                        prominent
                        class="mb-4"
                    >
                        {{ errorMessage }}
                    </VAlert>
                    
                    <div v-if="errorPersona" class="persona-info">
                        <strong>Persona:</strong> {{ errorPersona.nombres }} {{ errorPersona.apPaterno }} {{ errorPersona.apMaterno }}<br>
                        <strong>DNI:</strong> {{ errorPersona.dni }}
                    </div>
                </VCardText>
                <VCardActions>
                    <VSpacer></VSpacer>
                    <VBtn color="primary" @click="errorDialog = false">Entendido</VBtn>
                </VCardActions>
            </VCard>
        </VDialog>

        <VSnackbar
            v-model="snackbar.visible"
            :color="snackbar.color"
            timeout="10000"
            top
            right
        >
            {{ snackbar.text }}
            <template #actions>
                <VBtn icon="mdi-close" variant="text" @click="snackbar.visible = false" />
            </template>
        </VSnackbar>
    </div>
</template>

<style scoped>
.export-card {
    background: linear-gradient(145deg, #f5f5f5 0%, #ffffff 100%);
    border: 2px solid #e0e0e0;
}

.export-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(154, 20, 19, 0.3) !important;
    border-color: #9A1413;
}

.export-card:active {
    transform: translateY(-2px);
}

.stat-card {
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
}

.bg-gradient-primary {
    background: linear-gradient(135deg, #9A1413 0%, #c41d1c 100%);
}
</style>
