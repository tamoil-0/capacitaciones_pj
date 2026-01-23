<script setup>
import {defineEmits } from "vue";

const dialog = defineModel("modelValue");

const props = defineProps({
    title: { type: String, default: "Confirmar Eliminación" },
    message: { type: String, default: "¿Estás seguro de que deseas eliminar este registro?" },
    itemInfo: { type: String, default: "" },
    loading: { type: Boolean, default: false }
});

const emit = defineEmits(["deleteSelection"]);
</script>

<template>
    <VDialog v-model="dialog" max-width="480" transition="dialog-bottom-transition" persistent>
        <VCard class="rounded-xl elevation-10" style="overflow: hidden;">
            <!-- 🔹 Encabezado -->
            <VCardTitle
                class="d-flex align-center font-weight-bold px-6 py-4 text-error"
                style="background-color: #ffebee; border-bottom: 2px solid #d32f2f;"
            >
                <VIcon icon="mdi-alert-circle" color="error" size="26" class="mr-3" />
                {{ title }}
            </VCardTitle>

            <!-- 🔹 Contenido principal -->
            <VCardText class="pt-6 pb-4 px-6 text-center">
                <div class="d-flex justify-center mb-3">
                    <VAvatar color="error" size="72" class="elevation-3">
                        <VIcon icon="mdi-delete-alert" size="40" color="white" />
                    </VAvatar>
                </div>

                <p class="text-body-1 font-weight-medium text-grey-darken-3 mb-2">
                    {{ message }}
                </p>

                <div v-if="itemInfo" class="item-box mb-3">
                    <strong>{{ itemInfo }}</strong>
                </div>

                <p class="text-error text-caption">
                    ⚠️ Esta acción no se puede deshacer.
                </p>
            </VCardText>

            <!-- 🔹 Botones de acción -->
            <VCardActions class="pb-5 px-6 d-flex justify-end">
                <VBtn
                    variant="outlined"
                    color="grey-darken-1"
                    class="rounded-pill px-5"
                    @click="dialog = false"
                    :disabled="loading"
                >
                    Cancelar
                </VBtn>

                <VBtn
                    color="error"
                    class="rounded-pill px-5 ml-3 text-white"
                    elevation="2"
                    @click="$emit('deleteSelection')"
                    :loading="loading"
                >
                    <VIcon left size="18">mdi-trash-can-outline</VIcon>
                    Eliminar
                </VBtn>
            </VCardActions>
        </VCard>
    </VDialog>
</template>

<style scoped>
.item-box {
    display: inline-flex;
    align-items: center;
    background-color: #ffebee;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 0.95rem;
    color: #b71c1c;
}

/* 💅 Animación sutil de entrada */
.v-dialog__content {
    animation: fadeIn 0.25s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
