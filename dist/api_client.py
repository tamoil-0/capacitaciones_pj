"""
════════════════════════════════════════════════════════════════
API CLIENT - INTEGRACIÓN OMR + LARAVEL
════════════════════════════════════════════════════════════════
Cliente HTTP para comunicación entre el sistema OMR (Python)
y el backend Laravel.

RESPONSABILIDADES:
- Gestionar requests HTTP hacia la API Laravel
- Manejo de errores y reintentos
- Caché local de datos (eventos e inscritos)
- Logging de operaciones

ARQUITECTURA:
Este módulo actúa como CAPA DE INTEGRACIÓN entre el OMR
y el backend, sin modificar la lógica OMR existente.
"""

import requests
import json
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

# Importar configuración
from config import (
    API_BASE_URL,
    API_TOKEN,
    ENDPOINTS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    CACHE_ENABLED,
    CACHE_DURATION,
    DEBUG_MODE,
    LOG_FILE
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLASE PRINCIPAL: API CLIENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class OMRApiClient:
    """Cliente para comunicación con API Laravel"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = API_TOKEN
        self.timeout = REQUEST_TIMEOUT
        self.max_retries = MAX_RETRIES
        
        # Cache interno
        self._cache = {}
        self._cache_time = {}
        
        # Headers por defecto
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        # Si hay token, agregarlo
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'
        
        self._log("OMRApiClient inicializado", "INFO")
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # UTILIDADES INTERNAS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _log(self, message: str, level: str = "INFO"):
        """Log interno con timestamp"""
        if DEBUG_MODE:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_msg = f"[{timestamp}] [{level}] {message}"
            print(log_msg)
            
            # Guardar en archivo
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(log_msg + '\n')
            except:
                pass
    
    def _get_cache(self, key: str) -> Optional[any]:
        """Obtener datos del cache si están vigentes"""
        if not CACHE_ENABLED:
            return None
        
        if key not in self._cache:
            return None
        
        # Verificar si el cache expiró
        cache_time = self._cache_time.get(key)
        if cache_time:
            elapsed = (datetime.now() - cache_time).total_seconds()
            if elapsed < CACHE_DURATION:
                self._log(f"Cache HIT: {key}", "DEBUG")
                return self._cache[key]
        
        # Cache expirado
        self._log(f"Cache EXPIRED: {key}", "DEBUG")
        del self._cache[key]
        del self._cache_time[key]
        return None
    
    def _set_cache(self, key: str, data: any):
        """Guardar datos en cache"""
        if CACHE_ENABLED:
            self._cache[key] = data
            self._cache_time[key] = datetime.now()
            self._log(f"Cache SET: {key}", "DEBUG")
    
    def _make_request(self, method: str, endpoint: str, 
                      data: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> Tuple[bool, any]:
        """
        Realiza una petición HTTP con reintentos automáticos
        
        Returns:
            Tuple[bool, any]: (success, response_data_or_error)
        """
        url = f"{self.base_url}{endpoint}"
        
        # ⚠️ IMPORTANTE: Desactivar proxy para conexiones locales
        proxies = {
            'http': None,
            'https': None
        }
        
        for attempt in range(1, self.max_retries + 1):
            try:
                self._log(f"{method} {url} (intento {attempt}/{self.max_retries})", "INFO")
                
                if method.upper() == 'GET':
                    response = requests.get(
                        url, 
                        headers=self.headers, 
                        params=params,
                        timeout=self.timeout,
                        proxies=proxies
                    )
                elif method.upper() == 'POST':
                    response = requests.post(
                        url, 
                        headers=self.headers, 
                        json=data,
                        timeout=self.timeout,
                        proxies=proxies
                    )
                else:
                    return False, f"Método HTTP no soportado: {method}"
                
                # Verificar status code
                if response.status_code in [200, 201]:
                    result = response.json()
                    self._log(f"✓ Request exitoso: {response.status_code}", "SUCCESS")
                    return True, result
                
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self._log(f"✗ Error en request: {error_msg}", "WARNING")
                    
                    # Si es un error 4xx (client error), no reintentar
                    if 400 <= response.status_code < 500:
                        return False, error_msg
                    
                    # Si es 5xx, reintentar
                    if attempt < self.max_retries:
                        time.sleep(2 ** attempt)  # backoff exponencial
                        continue
                    
                    return False, error_msg
            
            except requests.exceptions.Timeout:
                self._log(f"✗ Timeout en intento {attempt}", "ERROR")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                return False, "Timeout: el servidor no respondió a tiempo"
            
            except requests.exceptions.ConnectionError:
                self._log(f"✗ Error de conexión en intento {attempt}", "ERROR")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                return False, "Error de conexión: no se pudo conectar al servidor"
            
            except Exception as e:
                self._log(f"✗ Error inesperado: {str(e)}", "ERROR")
                return False, f"Error inesperado: {str(e)}"
        
        return False, "Máximo de reintentos alcanzado"
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODOS PÚBLICOS - API ENDPOINTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def obtener_eventos(self) -> Tuple[bool, List[Dict]]:
        """
        GET /api/omr/eventos
        Obtiene la lista de eventos activos
        
        Returns:
            Tuple[bool, List[Dict]]: (success, eventos_list)
        """
        # Intentar cache
        cached = self._get_cache('eventos')
        if cached:
            return True, cached
        
        # Request
        success, response = self._make_request('GET', ENDPOINTS['eventos'])
        
        if success and response.get('success'):
            eventos = response.get('data', [])
            self._set_cache('eventos', eventos)
            return True, eventos
        
        return False, []
    
    def obtener_inscritos(self, id_evento: int) -> Tuple[bool, Dict[str, Dict]]:
        """
        GET /api/omr/eventos/{id}/inscritos
        Obtiene los inscritos de un evento con información completa
        
        Returns:
            Tuple[bool, Dict[str, Dict]]: (success, {dni: {id_inscripcion, nombres, apellidos}})
        """
        # Intentar cache
        cache_key = f'inscritos_{id_evento}'
        cached = self._get_cache(cache_key)
        if cached:
            return True, cached
        
        # Request
        endpoint = ENDPOINTS['inscritos'].format(id_evento=id_evento)
        success, response = self._make_request('GET', endpoint)
        
        if success and response.get('success'):
            inscritos_list = response.get('data', [])
            
            # Crear diccionario DNI → información completa
            inscritos_dict = {}
            for inscrito in inscritos_list:
                dni = inscrito.get('dni')
                id_inscripcion = inscrito.get('id_inscripcion')
                nombres = inscrito.get('nombres', '')
                ap_paterno = inscrito.get('apPaterno', '')
                ap_materno = inscrito.get('apMaterno', '')
                
                if dni and id_inscripcion:
                    inscritos_dict[dni] = {
                        'id_inscripcion': id_inscripcion,
                        'nombres': nombres,
                        'apellido_paterno': ap_paterno,
                        'apellido_materno': ap_materno,
                        'nombre_completo': f"{nombres} {ap_paterno} {ap_materno}".strip()
                    }
            
            self._set_cache(cache_key, inscritos_dict)
            self._log(f"Inscritos obtenidos: {len(inscritos_dict)}", "INFO")
            return True, inscritos_dict
        
        return False, {}
    
    def crear_evaluacion(self, id_inscripcion: int, 
                        tipo_examen: str = 'regular',
                        observaciones: Optional[str] = None) -> Tuple[bool, Optional[int]]:
        """
        POST /api/omr/evaluaciones
        Crea una nueva evaluación
        
        Returns:
            Tuple[bool, Optional[int]]: (success, id_evaluacion)
        """
        data = {
            'id_inscripcion': id_inscripcion,
            'tipo_examen': tipo_examen,
        }
        
        if observaciones:
            data['observaciones'] = observaciones
        
        success, response = self._make_request('POST', ENDPOINTS['crear_evaluacion'], data=data)
        
        if success and response.get('success'):
            id_evaluacion = response.get('data', {}).get('id_evaluacion')
            self._log(f"Evaluación creada: ID {id_evaluacion}", "SUCCESS")
            return True, id_evaluacion
        
        error_msg = response if isinstance(response, str) else response.get('message', 'Error desconocido')
        self._log(f"Error al crear evaluación: {error_msg}", "ERROR")
        return False, None
    
    def guardar_resultado(self, id_evaluacion: int, puntaje: float,
                         total_preguntas: int, aprobado: bool,
                         archivo_pdf: Optional[str] = None) -> Tuple[bool, str]:
        """
        POST /api/omr/resultados
        Guarda el resultado de una evaluación
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        data = {
            'id_evaluacion': id_evaluacion,
            'puntaje': puntaje,
            'total_preguntas': total_preguntas,
            'aprobado': aprobado,
        }
        
        if archivo_pdf:
            data['archivo_pdf'] = archivo_pdf
        
        success, response = self._make_request('POST', ENDPOINTS['guardar_resultado'], data=data)
        
        if success and response.get('success'):
            self._log(f"Resultado guardado para evaluación {id_evaluacion}", "SUCCESS")
            return True, "Resultado guardado exitosamente"
        
        error_msg = response if isinstance(response, str) else response.get('message', 'Error desconocido')
        self._log(f"Error al guardar resultado: {error_msg}", "ERROR")
        return False, error_msg
    
    def guardar_respuestas_omr(self, id_evaluacion: int,
                               respuestas: List[Dict]) -> Tuple[bool, str]:
        """
        POST /api/omr/respuestas
        Guarda las respuestas OMR detalladas
        
        Args:
            respuestas: Lista de diccionarios con formato:
                {
                    'numero_pregunta': int,
                    'respuesta_marcada': str | None,
                    'confianza': float | None
                }
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        data = {
            'id_evaluacion': id_evaluacion,
            'respuestas': respuestas
        }
        
        success, response = self._make_request('POST', ENDPOINTS['guardar_respuestas'], data=data)
        
        if success and response.get('success'):
            total = response.get('data', {}).get('total_respuestas', 0)
            self._log(f"Respuestas guardadas: {total} preguntas", "SUCCESS")
            return True, f"{total} respuestas guardadas"
        
        error_msg = response if isinstance(response, str) else response.get('message', 'Error desconocido')
        self._log(f"Error al guardar respuestas: {error_msg}", "ERROR")
        return False, error_msg
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MÉTODO HELPER DE ALTO NIVEL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def guardar_evaluacion_completa(self, id_inscripcion: int, puntaje: float,
                                    total_preguntas: int, aprobado: bool,
                                    respuestas: List[Dict],
                                    archivo_pdf: Optional[str] = None) -> Tuple[bool, str]:
        """
        Guarda una evaluación COMPLETA (evaluación + resultado + respuestas)
        en una sola operación lógica.
        
        Este es el método recomendado para usar desde completo.py
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # 1. Crear evaluación
        success, id_evaluacion = self.crear_evaluacion(id_inscripcion)
        if not success:
            return False, "No se pudo crear la evaluación"
        
        # 2. Guardar resultado
        success, msg = self.guardar_resultado(
            id_evaluacion, puntaje, total_preguntas, aprobado, archivo_pdf
        )
        if not success:
            return False, f"Evaluación creada pero error en resultado: {msg}"
        
        # 3. Guardar respuestas
        success, msg = self.guardar_respuestas_omr(id_evaluacion, respuestas)
        if not success:
            return False, f"Resultado guardado pero error en respuestas: {msg}"
        
        return True, f"Evaluación completa guardada (ID: {id_evaluacion})"
    
    def test_conexion(self) -> Tuple[bool, str]:
        """
        Prueba la conexión con la API
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            self._log("Probando conexión con API...", "INFO")
            success, eventos = self.obtener_eventos()
            
            if success:
                return True, f"✓ Conexión exitosa. {len(eventos)} eventos disponibles."
            else:
                return False, "✗ No se pudo conectar con la API"
        
        except Exception as e:
            return False, f"✗ Error al probar conexión: {str(e)}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INSTANCIA GLOBAL (Singleton)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

api_client = OMRApiClient()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNCIONES DE UTILIDAD (API SIMPLIFICADA)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_api_connection() -> Tuple[bool, str]:
    """Prueba la conexión con la API"""
    return api_client.test_conexion()

def get_eventos() -> List[Dict]:
    """Obtiene eventos activos"""
    success, eventos = api_client.obtener_eventos()
    return eventos if success else []

def get_inscritos(id_evento: int) -> Dict[str, int]:
    """Obtiene inscritos de un evento (DNI → id_inscripcion)"""
    success, inscritos = api_client.obtener_inscritos(id_evento)
    return inscritos if success else {}

def validar_dni_inscrito(dni: str, inscritos_dict: Dict[str, Dict]) -> Optional[Dict]:
    """
    Valida si un DNI está inscrito en el evento
    
    Returns:
        Optional[Dict]: Información completa del inscrito si está inscrito, None si no
                       {id_inscripcion, nombres, apellido_paterno, apellido_materno, nombre_completo}
    """
    return inscritos_dict.get(dni)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TESTING (ejecutar directamente este archivo)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("="*60)
    print("PROBANDO API CLIENT - OMR + LARAVEL")
    print("="*60)
    
    # Test 1: Conexión
    print("\n1. Probando conexión...")
    success, msg = test_api_connection()
    print(msg)
    
    if success:
        # Test 2: Obtener eventos
        print("\n2. Obteniendo eventos...")
        eventos = get_eventos()
        print(f"   → {len(eventos)} eventos encontrados")
        for evento in eventos[:3]:  # Mostrar primeros 3
            print(f"      - {evento.get('nombre')} (ID: {evento.get('id_evento')})")
        
        # Test 3: Obtener inscritos (si hay eventos)
        if eventos:
            id_evento = eventos[0].get('id_evento')
            print(f"\n3. Obteniendo inscritos del evento {id_evento}...")
            inscritos = get_inscritos(id_evento)
            print(f"   → {len(inscritos)} inscritos encontrados")
            
            # Mostrar algunos DNIs
            for dni in list(inscritos.keys())[:5]:
                print(f"      - DNI: {dni} → Inscripción: {inscritos[dni]}")
    
    print("\n" + "="*60)
    print("FIN DE PRUEBAS")
    print("="*60)
