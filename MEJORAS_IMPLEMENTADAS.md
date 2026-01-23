# Sistema de Capacitaciones - Poder Judicial de Puno

## 📋 Resumen del Sistema

Sistema integral de gestión de capacitaciones con tres tipos de eventos diferentes:

1. **CONVOCATORIAS** (Tipo 1) - Exámenes con calificación automática OMR
2. **CURSOS** (Tipo 2) - Control de asistencias con entrada/salida
3. **OTROS EVENTOS** (Tipo 3) - Control de asistencias con entrada/salida

---

## 🎯 Mejoras Implementadas (Enero 2026)

### 1. **Sistema de Validación de 30 Minutos** ✅

**Backend:**
- Nuevo campo `estado` en la tabla `registros` (valores: "A TIEMPO", "TARDANZA")
- Validación automática al registrar asistencia:
  - Si la entrada se registra dentro de 30 minutos del inicio del evento → **"A TIEMPO"**
  - Si la entrada se registra después de 30 minutos → **"TARDANZA"**
- Mensajes informativos indican cuántos minutos/horas llegó tarde el participante

**Archivos modificados:**
- `backend/app/Models/Registro.php` - Agregado campo `estado` al fillable
- `backend/app/Http/Controllers/RegistroController.php` - Lógica de validación con Carbon
- `backend/database/migrations/2026_01_23_083831_add_estado_to_registros_table.php` - Nueva migración

### 2. **Reportes Excel de Asistencias** ✅

**Características:**
- Diseño profesional con encabezados institucionales (Poder Judicial de Puno)
- Tabla con 10 columnas detalladas:
  - N°, DNI, Nombres Completos, Tipo Evento, Evento, Tipo Registro, Fecha, Hora, Estado, Observaciones
- Código de colores:
  - 🟢 Verde: Entradas a tiempo
  - 🟠 Naranja: Salidas y tardanzas
  - ⚪ Gris: Otros registros
- Sección de estadísticas:
  - Total de registros
  - Total de entradas
  - Total de salidas
  - Otros registros
- Filtros automáticos en todas las columnas
- Archivos guardados en: `public/excel/{TipoEvento}/Asistencias_{NombreEvento}_{timestamp}.xlsx`

**Archivos creados:**
- `backend/app/Exports/AsistenciasExcelExport.php` - Clase de exportación

**Endpoints:**
- `GET /api/registros/exportar/{id_evento?}` - Exportar asistencias por evento

### 3. **Mejoras de UI/UX** ✅

**AsistentesView.vue:**
- ❌ Eliminado icono confuso "ojo" (`mdi-eye`)
- ✅ Nuevo icono intuitivo "clipboard-text-clock" con tooltip "Ver historial de asistencias"
- 📊 Botón de exportación Excel con card elegante y efecto hover
- Variante "tonal" en botones para mejor visibilidad

**EventosView.vue:**
- 🎯 Títulos dinámicos según tipo de evento:
  - CONVOCATORIAS → "CONVOCATORIAS - Exámenes OMR"
  - CURSOS → "CURSOS - Control de Asistencias"
  - OTROS → "OTROS EVENTOS - Control de Asistencias"
- 💡 Alertas informativas explicando el propósito de cada tipo
- 🔄 Botones de acción con tooltips explicativos:
  - CONVOCATORIAS → "Ver Exámenes" (icono: file-document-check)
  - CURSOS/OTROS → "Ver Asistencias" (icono: clipboard-check)

**EventosExamenesView.vue:**
- Título claro: "CONVOCATORIAS - Eventos con Exámenes OMR"
- Alerta informativa sobre sistema OMR y completo.py

**ExamenesView.vue:**
- Título actualizado: "CONVOCATORIAS - Resultados de Exámenes OMR"
- Alerta con criterios de aprobación: **20/30 puntos mínimo**

### 4. **Diseño Elegante Global** ✅

**Archivo:** `frontend/src/assets/personalice.css`

**Mejoras aplicadas:**
- ✨ Transiciones suaves en todas las cards (0.3s ease)
- 🎨 Efectos hover con elevación de sombras
- 🔘 Botones con transformación translateY(-2px) al hover
- 📊 Chips y alerts con bordes redondeados
- 🎨 Colores personalizados consistentes:
  - Success: #4caf50
  - Error: #f44336
  - Warning: #ff9800
  - Info: #2196f3
- 📱 Diseño responsive optimizado para móviles

---

## 🏗️ Arquitectura del Sistema

### Tipos de Evento

```
tipo_eventos
├── id_tipe: 1 → CONVOCATORIAS (Exámenes OMR con completo.py)
├── id_tipe: 2 → CURSOS (Solo asistencias)
└── id_tipe: 3 → OTROS (Solo asistencias)
```

### Flujo de Trabajo

**CONVOCATORIAS:**
1. Crear evento tipo CONVOCATORIAS
2. Inscribir participantes
3. Generar plantillas OMR
4. Escanear con `completo.py` (Python OMR scanner)
5. Ver resultados en "Exámenes"
6. Exportar evaluaciones a Excel

**CURSOS/OTROS:**
1. Crear evento tipo CURSOS u OTROS
2. Inscribir participantes
3. Registrar entradas/salidas con validación de 30 minutos
4. Ver historial de asistencias
5. Exportar reportes de asistencias a Excel

### Base de Datos

**Tabla: registros**
```sql
CREATE TABLE registros (
    id_registro BIGINT PRIMARY KEY AUTO_INCREMENT,
    inscripcion BIGINT NOT NULL,
    tipo VARCHAR(50) NOT NULL,          -- 'entrada', 'salida', 'otro'
    estado VARCHAR(50) DEFAULT 'A TIEMPO', -- 'A TIEMPO', 'TARDANZA'
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (inscripcion) REFERENCES inscripciones(id_inscripcion)
);
```

---

## 📦 Stack Tecnológico

**Backend:**
- Laravel 10
- PHP 8.2.12
- PhpSpreadsheet 5.4.0 (Generación de Excel)
- Sanctum (Autenticación)
- MySQL

**Frontend:**
- Vue 3 (Composition API)
- Vuetify 3 (Material Design)
- Axios (HTTP Client)
- Vue Router

**Desktop Application:**
- Python 3.10+
- CustomTkinter (GUI)
- OpenCV (Procesamiento de imágenes OMR)
- Poppler (PDF a imágenes)

---

## 🚀 Instalación y Configuración

### Backend (Laravel)

```bash
cd backend
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve
```

### Frontend (Vue 3)

```bash
cd frontend
npm install
npm run dev
```

### Python OMR Scanner

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python completo.py
```

---

## 📊 Endpoints API Principales

### Registros de Asistencia

```http
POST   /api/registros/{id_evento}/{dni}
       Body: { "tipo": "entrada" | "salida" | "otro" }
       Response: { "estado": "A TIEMPO" | "TARDANZA", "registro": {...} }

GET    /api/registros/exportar/{id_evento?}
       Response: { "success": true, "data": { "url": "...", "nombre_archivo": "..." } }
```

### Evaluaciones (Exámenes OMR)

```http
GET    /api/evaluaciones
       Response: Lista de evaluaciones con resultados

GET    /api/evaluaciones/exportar/{id_evento?}
       Response: Archivo Excel con resultados de exámenes
```

---

## ✅ Criterios de Validación

### Asistencias
- **A TIEMPO**: Registro de entrada dentro de 30 minutos del inicio del evento
- **TARDANZA**: Registro de entrada después de 30 minutos del inicio

### Exámenes OMR
- **APROBADO**: Puntaje ≥ 20 puntos (de 30 totales)
- **DESAPROBADO**: Puntaje < 20 puntos

---

## 📝 Notas Importantes

1. **Validación de 30 minutos**: Solo se aplica a registros de tipo "entrada". Los registros de "salida" y "otro" no tienen validación de tiempo.

2. **Exportación Excel**: Los archivos se generan en `backend/public/excel/{TipoEvento}/` y son accesibles vía URL pública.

3. **Tipo de Evento**: El sistema distingue automáticamente entre CONVOCATORIAS (exámenes) y CURSOS/OTROS (asistencias) en toda la interfaz.

4. **Diseño Responsive**: Todas las vistas están optimizadas para dispositivos móviles y tablets.

---

## 🔧 Mantenimiento

### Logs
- Backend: `backend/storage/logs/laravel.log`
- Frontend: Consola del navegador (F12)
- Python: Consola de terminal

### Limpieza de Archivos Excel
```bash
# Eliminar archivos Excel antiguos (más de 30 días)
cd backend/public/excel
find . -name "*.xlsx" -mtime +30 -delete
```

---

## 👥 Roles de Usuario

1. **Administrador** (id_rol: 1) - Acceso completo
2. **Organizador** (id_rol: 2) - Gestión de eventos y asistencias
3. **Invitado** (id_rol: 3) - Solo lectura

---

## 📞 Soporte

Para soporte técnico o consultas, contactar al equipo de desarrollo del Poder Judicial de Puno.

---

**Última actualización:** Enero 23, 2026
**Versión del sistema:** 2.0.0
