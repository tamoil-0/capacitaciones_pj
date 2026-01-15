# 🎯 SISTEMA OMR + LARAVEL - GUÍA RÁPIDA

## 📋 RESUMEN

Sistema integrado de **lectura óptica de marcas (OMR)** con validación de inscritos y almacenamiento en base de datos Laravel.

**Componentes:**
- 🐍 **Python Desktop**: Aplicación OMR con CustomTkinter
- 🎯 **Laravel API**: Backend REST con MySQL
- 🎨 **Vue Frontend**: Interfaz web de gestión

---

## ⚡ INSTALACIÓN RÁPIDA

### 1️⃣ Backend Laravel

```bash
cd backend/

# Instalar dependencias
composer install

# Configurar .env (base de datos)
cp .env.example .env
php artisan key:generate

# Ejecutar migraciones (incluye nuevas tablas)
php artisan migrate

# Ejecutar seeders (opcional - datos de prueba)
php artisan db:seed

# Iniciar servidor
php artisan serve
# URL: http://127.0.0.1:8000
```

### 2️⃣ Python OMR

```bash
# Instalar dependencias
pip install opencv-python numpy pillow pdf2image customtkinter reportlab requests

# Configurar API (editar config.py)
# Línea 20: API_BASE_URL = "http://localhost/capacitaciones_pj/backend/public/api"

# Ejecutar aplicación
python completo.py
```

### 3️⃣ Frontend Vue (opcional)

```bash
cd frontend/
npm install
npm run dev
# URL: http://localhost:5173
```

---

## 🚀 USO DEL SISTEMA

### **Flujo de trabajo:**

1. **Crear evento en Laravel** (vía frontend web)
2. **Inscribir personas** al evento
3. **Abrir OMR** (`python completo.py`)
4. **Seleccionar evento** en el ComboBox
5. **Cargar PDF/JPG** con hojas de respuestas
6. **Procesar** → Sistema valida DNIs y guarda en BD
7. **Ver resultados** hoja por hoja

### **Capturas del flujo:**

```
┌─────────────────────────────────────────┐
│  🎯 EVENTO: [1 - Capacitación OMR ▼]   │
│  Inscritos: 150                         │
├─────────────────────────────────────────┤
│  📁 Cargar   ⚙️ Procesar  📂 Carpeta    │
│  Archivo: examenes_lote_01.pdf         │
├─────────────────────────────────────────┤
│  Procesando... ████████████░░  80%      │
├─────────────────────────────────────────┤
│  Página: 12/15                          │
│  DNI: 12345678 ✓ INSCRITO | API ✓      │
│  PDF: 12345678_resultado.pdf            │
├─────────────────────────────────────────┤
│  P1: A    P11: B    P21: C              │
│  P2: B    P12: C    P22: A              │
│  ...                                    │
└─────────────────────────────────────────┘
```

---

## 📂 ESTRUCTURA DE ARCHIVOS

```
capacitaciones_pj/
│
├── completo.py              ← Aplicación OMR principal (MODIFICADO)
├── config.py                ← Configuración API (NUEVO)
├── api_client.py            ← Cliente HTTP Laravel (NUEVO)
├── DOCUMENTACION_INTEGRACION.md  ← Documentación técnica completa
│
├── backend/                 ← Laravel API
│   ├── app/
│   │   ├── Models/
│   │   │   ├── Evaluacion.php     (NUEVO)
│   │   │   ├── Resultado.php      (NUEVO)
│   │   │   └── RespuestaOmr.php   (NUEVO)
│   │   └── Http/Controllers/
│   │       └── EvaluacionController.php  (MODIFICADO)
│   ├── database/migrations/
│   │   └── 2026_01_04_000001_create_evaluaciones_table.php  (NUEVO)
│   └── routes/api.php       (MODIFICADO)
│
├── frontend/                ← Vue.js (sin cambios)
│
└── resultados_omr/          ← PDFs generados localmente
```

---

## 🔧 CONFIGURACIÓN

### **config.py** - Configuración principal

```python
# URL de la API Laravel
API_BASE_URL = "http://localhost/capacitaciones_pj/backend/public/api"

# Token de autenticación (opcional - producción)
API_TOKEN = None  # Ejemplo: "1|abc123xyz456..."

# Timeouts
REQUEST_TIMEOUT = 30  # segundos
MAX_RETRIES = 3

# Nota aprobatoria
NOTA_APROBATORIA = 60.0  # %
```

### **backend/.env** - Variables Laravel

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=capacitaciones_pj
DB_USERNAME=root
DB_PASSWORD=
```

---

## 🛠️ ENDPOINTS API

Base URL: `http://localhost/capacitaciones_pj/backend/public/api`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/omr/eventos` | Lista eventos activos |
| `GET` | `/omr/eventos/{id}/inscritos` | Lista inscritos de un evento |
| `POST` | `/omr/evaluaciones` | Crea una evaluación |
| `POST` | `/omr/resultados` | Guarda resultado de evaluación |
| `POST` | `/omr/respuestas` | Guarda respuestas detalladas |

### Ejemplo: Listar eventos

```bash
curl http://localhost/capacitaciones_pj/backend/public/api/omr/eventos
```

Respuesta:
```json
{
  "success": true,
  "data": [
    {
      "id_evento": 1,
      "nombre": "Capacitación OMR 2026",
      "fecha_evento": "2026-01-15 09:00:00",
      "tipo_evento": 1
    }
  ]
}
```

---

## 🗄️ BASE DE DATOS

### Tablas nuevas:

**`evaluaciones`**
- `id_evaluacion` (PK)
- `inscripcion` (FK → inscripciones)
- `fecha_evaluacion`
- `tipo_examen` (regular, recuperación, etc.)
- `estado` (valida, invalida, anulada)

**`resultados`**
- `id_resultado` (PK)
- `evaluacion` (FK → evaluaciones)
- `puntaje` (0-100)
- `total_preguntas` (30)
- `aprobado` (bool)
- `archivo_pdf` (ruta)
- `fecha_calificacion`

**`respuestas_omr`**
- `id_respuesta_omr` (PK)
- `evaluacion` (FK → evaluaciones)
- `numero_pregunta` (1-30)
- `respuesta_marcada` (A/B/C/D/E/null)
- `confianza` (% - futuro)

### Relaciones:

```
eventos → inscripciones → evaluaciones → resultados
                                     → respuestas_omr (x30)
```

---

## ✅ CARACTERÍSTICAS PRINCIPALES

### Integración Laravel:
- ✅ Validación automática de DNI contra inscritos
- ✅ Guardado centralizado en MySQL
- ✅ Historial completo de evaluaciones
- ✅ Respuestas detalladas por pregunta

### Sistema OMR:
- ✅ Procesamiento por lotes (PDF multipágina)
- ✅ Detección automática de DNI
- ✅ Lectura de 30 preguntas (A/B/C/D/E)
- ✅ Generación de PDF por persona
- ✅ Interfaz gráfica profesional

### Modo de operación:
- ✅ **Modo ONLINE**: Con integración Laravel (validación + BD)
- ✅ **Modo OFFLINE**: Sin API (solo genera PDFs locales)
- ✅ Fallback automático si API no disponible

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "No se pudo conectar con la API"

**Causa**: Laravel no está corriendo o URL incorrecta

**Solución**:
```bash
# Verificar Laravel
cd backend/
php artisan serve

# Probar endpoint manualmente
curl http://localhost:8000/api/omr/eventos
```

### Error: "Ningún evento disponible"

**Causa**: No hay eventos con `estado = 1` en BD

**Solución**:
```sql
-- Ver eventos existentes
SELECT * FROM eventos;

-- Activar un evento
UPDATE eventos SET estado = 1 WHERE id_evento = 1;
```

### Error: "DNI no inscrito" (pero sí está)

**Causa**: Evento incorrecto seleccionado o cache desactualizado

**Solución**:
- Presionar botón "🔄" en la app para recargar
- Verificar en BD:
```sql
SELECT p.dni, i.id_inscripcion, e.nombre
FROM personas p
JOIN inscripciones i ON i.persona = p.id_persona
JOIN eventos e ON e.id_evento = i.evento
WHERE p.dni = '12345678';
```

### OMR funciona pero no guarda en API

**Causa**: Módulo `requests` no instalado o `API_DISPONIBLE = False`

**Solución**:
```bash
pip install requests

# Verificar en consola Python
python
>>> from api_client import api_client
>>> api_client.test_conexion()
```

---

## 📊 CONSULTAS ÚTILES

### Estadísticas por evento:

```sql
-- Cantidad de evaluaciones por evento
SELECT e.nombre, COUNT(ev.id_evaluacion) as evaluaciones
FROM eventos e
JOIN inscripciones i ON i.evento = e.id_evento
JOIN evaluaciones ev ON ev.inscripcion = i.id_inscripcion
GROUP BY e.id_evento;

-- Promedio y aprobación
SELECT e.nombre,
       AVG(r.puntaje) as promedio,
       SUM(r.aprobado) as aprobados,
       COUNT(*) as total
FROM eventos e
JOIN inscripciones i ON i.evento = e.id_evento
JOIN evaluaciones ev ON ev.inscripcion = i.id_inscripcion
JOIN resultados r ON r.evaluacion = ev.id_evaluacion
GROUP BY e.id_evento;

-- Respuesta más elegida por pregunta
SELECT numero_pregunta, respuesta_marcada, COUNT(*) as veces
FROM respuestas_omr
GROUP BY numero_pregunta, respuesta_marcada
ORDER BY numero_pregunta, veces DESC;
```

---

## 🚀 COMPILAR A EJECUTABLE

```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar con archivos adicionales
pyinstaller --onefile --windowed \
  --add-data "config.py;." \
  --add-data "api_client.py;." \
  --hidden-import=requests \
  completo.py

# Resultado: dist/completo.exe
```

**Post-compilación:**
1. Copiar `config.py` junto al `.exe`
2. Usuario puede editar `config.py` para cambiar URL
3. Distribuir: `.exe` + `config.py`

---

## 📞 SOPORTE

### Documentación completa:
Ver `DOCUMENTACION_INTEGRACION.md` para:
- Arquitectura detallada
- Flujos JSON de ejemplo
- Troubleshooting avanzado
- Métricas y consultas SQL

### Logs del sistema:
- **Python**: `omr_api.log` (carpeta raíz)
- **Laravel**: `backend/storage/logs/laravel.log`

### Stack tecnológico:
- Python 3.11+ (OpenCV, CustomTkinter, requests)
- Laravel 10 (PHP 8.1+, MySQL 8)
- Vue 3 + Vite (frontend opcional)

---

## 📝 NOTAS IMPORTANTES

⚠️ **NO MODIFICAR** la lógica OMR:
- `detectar_cuadrados_negros()`
- `omr_sobre_recorte()`
- `generar_pdf_resultado()`

✅ **MODIFICABLE**:
- `api_client.py` - Agregar endpoints
- `config.py` - Ajustar configuración
- Validaciones en `procesar_documento_completo()`

---

**Fecha**: Enero 2026  
**Autor**: Arquitecto de Software Senior  
**Versión**: 1.0
