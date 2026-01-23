<script setup>

const props = defineProps({
  // Filtros
  searchLabel: { type: String, default: "Buscar" },
  searchPlaceholder: { type: String, default: "Escribe para buscar..." },
  searchModel: { type: String, required: true },
  selects: { type: Array, default: () => [] },
  itemsPerPage: { type: Number, required: true },

  // Tabla
  headers: { type: Array, required: true },
  items: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  noDataText: { type: String, default: "No hay datos disponibles" },
  loadingText: { type: String, default: "Cargando..." },
});
</script>

<template>
  <div>
    <!-- Filtros -->
    <VCard class="filters" elevation="2">
      <VCardText>
        <VRow align="center">
          <!-- Campo de búsqueda -->
          <VCol cols="12" md="6">
            <VTextField
              v-model="props.searchModel"
              prepend-inner-icon="mdi-magnify"
              :label="props.searchLabel"
              :placeholder="props.searchPlaceholder"
              variant="outlined"
              density="comfortable"
              hide-details
              clearable
            />
          </VCol>

          <!-- Selects dinámicos -->
          <VCol
            v-for="(select, index) in props.selects"
            :key="index"
            cols="12"
            md="3"
          >
            <VSelect
              v-model="select.model"
              :items="select.items"
              :label="select.label"
              variant="outlined"
              density="comfortable"
              hide-details
              clearable
            />
          </VCol>

          <!-- Items por página -->
          <VCol cols="12" md="3">
            <VSelect
              v-model="props.itemsPerPage"
              :items="[10, 25, 50, 100]"
              label="Items por página"
              variant="outlined"
              density="comfortable"
              hide-details
            />
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Tabla -->
    <VDataTable
      v-model:items-per-page="props.itemsPerPage"
      :headers="props.headers"
      :items="props.items"
      :search="props.searchModel"
      :loading="props.loading"
      :loading-text="props.loadingText"
      :no-data-text="props.noDataText"
      class="custom-table"
    >
      <!-- Slots para columnas personalizadas -->
      <template v-for="(_, name) in $slots" v-slot:[name]="slotProps">
        <slot :name="name" v-bind="slotProps" />
      </template>
    </VDataTable>
  </div>
</template>

<style scoped>
.filters {
  margin-bottom: 1.5rem;
}

.custom-table :deep(.v-data-table__wrapper) {
  border-radius: 8px;
}

.actions-buttons {
  display: flex;
  gap: 0.25rem;
}
</style>
