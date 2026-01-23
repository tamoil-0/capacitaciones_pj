<script setup>
import { defineModel } from "vue"

// 🔹 Modelos reactivos que se conectan al padre con v-model
const search = defineModel("search")
const tipoFilter = defineModel("tipoFilter")
const itemsPerPage = defineModel("itemsPerPage")

// 🔹 Props personalizables
defineProps({
    searchLabel: { type: String, default: "Buscar" },
    searchPlaceholder: { type: String, default: "" },
    tipoLabel: { type: String, default: "Filtrar por tipo" },
    tipos: { type: Array, default: () => [] },
    itemsLabel: { type: String, default: "Items por página" }
})
</script>

<template>
    <VCard class="filters-card" elevation="2">
        <VCardText>
            <VRow align="center">
                <!-- Search -->
                <VCol cols="12" md="6">
                    <VTextField
                        v-model="search"
                        prepend-inner-icon="mdi-magnify"
                        :label="searchLabel"
                        :placeholder="searchPlaceholder"
                        variant="outlined"
                        density="comfortable"
                        hide-details
                        clearable
                    />
                </VCol>

                <!-- Filtro por tipo -->
                <VCol cols="12" md="3">
                    <VSelect
                        v-model="tipoFilter"
                        :items="tipos"
                        :label="tipoLabel"
                        variant="outlined"
                        density="comfortable"
                        hide-details
                        clearable
                    />
                </VCol>

                <!-- Items por página -->
                <VCol cols="12" md="3">
                    <VSelect
                        v-model="itemsPerPage"
                        :items="[5, 10, 25, 50, 100]"
                        :label="itemsLabel"
                        variant="outlined"
                        density="comfortable"
                        hide-details
                    />
                </VCol>
            </VRow>
        </VCardText>
    </VCard>
</template>

<style scoped>

.filters-card {
    margin-bottom: 1.5rem;
}

/* Tema oscuro */
.dark-theme .filters-card {
    background: rgb(var(--v-theme-surface));
}
</style>
