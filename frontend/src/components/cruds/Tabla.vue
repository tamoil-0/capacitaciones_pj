<script setup>
import { ref, watch } from "vue";

const props = defineProps({
    headers: { type: Array, required: true },
    items: { type: Array, required: true },
    loading: { type: Boolean, default: false },
    search: { type: String, default: "" },
    itemsPerPage: { type: Number, default: 5 },
    noDataText: { type: String, default: "No hay datos disponibles" },
    loadingText: { type: String, default: "Cargando..." },
});

// Estado interno para que sea reactivo
const itemsPerPageInternal = ref(props.itemsPerPage);

// Si el padre cambia itemsPerPage, actualizamos el interno
watch(
    () => props.itemsPerPage,
    (newVal) => {
        itemsPerPageInternal.value = newVal;
    }
);


</script>


<template>
    <VCard class="table-card" elevation="2">
        <VDataTable
            v-model:items-per-page="itemsPerPageInternal"
            :headers="props.headers"
            :items="props.items"
            :search="props.search"
            :loading="props.loading"  
            :loading-text="props.loadingText"
            :no-data-text="props.noDataText"
            class="custom-table"
        >
            <!-- Slot para sobrescribir columnas -->
            <template v-for="(_, name) in $slots" v-slot:[name]="slotProps">
                <slot :name="name" v-bind="slotProps" />
            </template>

        </VDataTable>
    </VCard>
</template>

<style scoped>
.custom-table :deep(.v-data-table__wrapper) {
    border-radius: 8px;
}

.table-card {
    margin-bottom: 1.5rem;
}

/* Tema oscuro */
.dark-theme .table-card {
    background: rgb(var(--v-theme-surface));
}
</style>