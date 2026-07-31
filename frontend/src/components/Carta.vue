<script setup>

const props = defineProps({
    nombre: String,
    ruta: String,
    color: {
        type: String,
        default: "#1976D2",
    },
    icono: {
        type: String,
        default: "mdi-apple",
    },
    height: {
        type: String,
        default: "180", // valor por defecto
    },
    fontSize: {
        type: String,
        default: "1.1rem", // valor por defecto
    },
});
</script>

<template>
    <VCard
        class="modern-card"
        :height="height" 
        elevation="0"
        :to="ruta"
    >
        <!-- Contenido principal -->
        <div class="card-content">
            <div class="icon-container">
                <VIcon
                    :icon="icono"
                    size="48"
                    class="card-icon"
                />
            </div>
            <div class="card-text-content">
                <h3 class="card-title" :style="{ fontSize: fontSize }">
                    {{ nombre }}
                </h3>
                <VIcon icon="mdi-arrow-right" size="24" class="arrow-icon" />
            </div>
        </div>
    </VCard>
</template>

<style scoped>
/* Tarjeta minimalista moderna */
.modern-card {
    position: relative;
    border-radius: 20px !important;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    background: white !important;
    border: 2px solid rgba(21, 101, 192, 0.12);
}

.modern-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 16px 40px rgba(21, 101, 192, 0.22) !important;
    border-color: #1565C0;
}

/* Contenido en columna */
.card-content {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 24px;
    gap: 20px;
}

/* Contenedor del ícono */
.icon-container {
    width: 90px;
    height: 90px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0D47A1 0%, #1E88E5 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 20px rgba(13, 71, 161, 0.3);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.modern-card:hover .icon-container {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 12px 28px rgba(13, 71, 161, 0.4);
}

.card-icon {
    color: white !important;
}

/* Contenido de texto */
.card-text-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

/* Título del card */
.card-title {
    font-weight: 700;
    line-height: 1.3;
    color: #202124;
    text-align: center;
    letter-spacing: -0.3px;
    margin: 0;
}

/* Flecha de acción */
.arrow-icon {
    color: #1565C0 !important;
    opacity: 0;
    transform: translateX(-10px);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.modern-card:hover .arrow-icon {
    opacity: 1;
    transform: translateX(0);
}

@media (max-width: 768px) {
    .icon-container {
        width: 70px;
        height: 70px;
    }
    
    .card-icon {
        font-size: 36px !important;
    }
    
    .card-content {
        padding: 24px 16px;
        gap: 16px;
    }
}
</style>
