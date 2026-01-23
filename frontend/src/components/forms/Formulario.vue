<!-- components/CrudDialog.vue -->
<script setup>
import { ref, watch, onMounted } from "vue";

const props = defineProps({
    modelValue: { type: Boolean, required: true }, // controla abrir/cerrar dialog
    editMode: { type: Boolean, default: false },
    title: { type: String, default: "Crear / Editar" },
    icon: { type: String, default: "mdi-plus" },
    fields: { type: Array, required: true }, 

    formData: { type: Object, required: true },
    loading: { type: Boolean, default: false },
    errors: { type: Object, default: () => ({}) }
});

const emit = defineEmits(["update:modelValue", "save"]);

const dialog = ref(props.modelValue);
watch(() => props.modelValue, val => dialog.value = val);
watch(dialog, val => emit("update:modelValue", val));

const formValid = ref(false);

const rules = {
    required: v => (v !== null && v !== undefined && v !== '') || "Campo requerido",
    email: v => /.+@.+\..+/.test(v) || "Correo inválido",
    dni: v => /^\d{8}$/.test(v) || "DNI inválido",
    password: v => v?.length >= 6 || "Mínimo 6 caracteres",
};

// Formatear fecha para inputs datetime-local
function formatDateTimeLocal(value) {
    if (!value) return "";
    try {
        // Si el valor viene en formato ISO con zona horaria
        return new Date(value).toISOString().slice(0, 16);
    } catch (e) {
        return value;
    }
}


</script>

<template>
    <VDialog v-model="dialog" max-width="600" persistent>
        <VCard>
            <VCardTitle class="dialog-title">
                <VIcon :icon="editMode ? 'mdi-pencil' : icon" class="mr-2" />
                {{ editMode ? `Editar ${title}` : `Crear ${title}` }}
            </VCardTitle>

            <VForm v-model="formValid" @submit.prevent="emit('save')">
                <VCardText>
                    <VRow>
                        <template v-for="field in fields" :key="field.key">
                            <VCol cols="12" md="6" v-if="field.type !== 'textarea'">
                                <VTextField
                                    v-if="field.type !== 'select'"
                                    v-model="formData[field.key]"
                                    :label="field.label"
                                    :rules="field.rules?.map(r => rules[r])"
                                    :type="field.type"
                                    variant="outlined"
                                    :error-messages="errors[field.key]"
                                    @focus="field.type === 'datetime-local' && (formData[field.key] = formatDateTimeLocal(formData[field.key]))"
                                />
                                <VSelect
                                    v-else
                                    v-model="formData[field.key]"
                                    :label="field.label"
                                    :items="field.options || []"
                                    :item-title="field.itemTitle || 'title'"
                                    :item-value="field.itemValue || 'value'"
                                    :rules="field.rules?.map(r => rules[r])"
                                    variant="outlined"
                                    :error-messages="errors[field.key]"
                                />
                            </VCol>
                            <VCol cols="12" v-else>
                                <VTextarea
                                    v-model="formData[field.key]"
                                    :label="field.label"
                                    variant="outlined"
                                />
                            </VCol>
                        </template>
                    </VRow>
                </VCardText>

                <VCardActions>
                    <VSpacer />
                    <VBtn variant="text" @click="dialog = false" :disabled="loading">
                        Cancelar
                    </VBtn>
                    <VBtn color="primary" type="submit" :loading="loading" :disabled="!formValid">
                        {{ editMode ? "Actualizar" : "Crear" }}
                    </VBtn>
                </VCardActions>
            </VForm>
        </VCard>
    </VDialog>
</template>

<style scoped>

.dialog-title {
    background: rgb(var(--v-theme-primary));
    color: rgb(var(--v-theme-on-primary));
    font-weight: 600;
    display: flex;
    align-items: center;
    border-radius: 4px 4px 0 0;
    padding: 12px 16px;
}

</style>
