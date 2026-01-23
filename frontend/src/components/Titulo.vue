<script setup>

const props = defineProps({
    titulo: String,
    subtitulo: {
        type: String,
        default: null,
    },
    icono: {
        type: String,
        default: "mdi-apple",
    },

    nombreBTN: {
        type: String,
        default: null,
    },
    iconoBTN: {
        type: String,
        default: null,
    },
});

const emit = defineEmits(["crear"]);

</script>

<template>
    <!-- Header Moderno -->
    <div class="modern-header">
        <div class="header-content">
            <div class="header-left">
                <div class="icon-badge">
                    <VIcon :icon="icono" size="32" />
                </div>
                <div>
                    <h1 class="page-title">{{ titulo }}</h1>
                    <p v-if="subtitulo" class="page-subtitle">{{ subtitulo }}</p>
                </div>
            </div>

            <VBtn
                v-if="nombreBTN"
                color="primary"
                size="x-large"
                :prepend-icon="iconoBTN"
                class="modern-btn"
                elevation="0"
                @click="emit('crear')"  
            >
                {{ nombreBTN }}
            </VBtn>
        </div>
    </div>
</template>

<style scoped>
.modern-header {
    margin-bottom: 2.5rem;
    animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 2rem;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 1.25rem;
}

.icon-badge {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    background: linear-gradient(135deg, #9A1413 0%, #c41d1c 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 8px 20px rgba(154, 20, 19, 0.3);
}

.page-title {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    color: #202124;
    letter-spacing: -0.5px;
    line-height: 1.2;
}

.page-subtitle {
    font-size: 0.95rem;
    color: #5f6368;
    margin: 4px 0 0 0;
    font-weight: 500;
}

.modern-btn {
    border-radius: 14px !important;
    font-weight: 700;
    letter-spacing: 0.3px;
    padding: 0 32px !important;
}

@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 1.5rem;
    }

    .icon-badge {
        width: 56px;
        height: 56px;
    }
    
    .icon-badge .v-icon {
        font-size: 28px !important;
    }

    .page-title {
        font-size: 1.5rem;
    }
    
    .modern-btn {
        width: 100%;
    }
}
</style>
