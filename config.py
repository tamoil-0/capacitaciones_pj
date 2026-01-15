"""
════════════════════════════════════════════════════════════════
CONFIGURACIÓN - API LARAVEL
════════════════════════════════════════════════════════════════
Configuración de conexión entre el sistema OMR (Python)
y el backend Laravel.
"""

# ============================================================
# CONFIGURACIÓN DE LA API
# ============================================================

# URL base de la API Laravel
API_BASE_URL = "http://127.0.0.1:8000/api"

# Token de autenticación (si es necesario)
API_TOKEN = None  # O tu token si usas autenticación

# Timeout para requests HTTP (segundos)
REQUEST_TIMEOUT = 10

# Reintentos en caso de error
MAX_RETRIES = 3
RETRY_DELAY = 1  # segundos

# ============================================================
# ENDPOINTS DE LA API
# ============================================================

ENDPOINTS = {
    "eventos": "/omr/eventos",
    "inscritos": "/omr/eventos/{id_evento}/inscritos",
    "crear_evaluacion": "/omr/evaluaciones",
    "guardar_resultado": "/omr/resultados",
    "guardar_respuestas": "/omr/respuestas",
}

# ============================================================
# CONFIGURACIÓN DE CACHÉ
# ============================================================

# Tiempo de vida del caché (minutos)
CACHE_TTL = 5
CACHE_DURATION = 300  # segundos (5 minutos)

# Habilitar caché local
CACHE_ENABLED = True

# ============================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================

# Habilitar logs detallados
DEBUG_MODE = True

# Mostrar requests HTTP en consola
LOG_REQUESTS = False

# Archivo de log para api_client
LOG_FILE = "api_client.log"
 