# ════════════════════════════════════════════════════════════════
# EXPORTACIÓN A EXCEL - SISTEMA OMR
# ════════════════════════════════════════════════════════════════

## ✅ ARCHIVOS CREADOS/MODIFICADOS

### BACKEND:

1. **app/Exports/EvaluacionesExport.php** (NUEVO)
   - Clase de exportación con diseño profesional
   - Encabezados con fondo azul y texto blanco
   - Filas alternadas con colores
   - Aprobados en verde, Desaprobados en rojo
   - Bordes y alineación profesional
   - Columnas auto-ajustadas

2. **app/Http/Controllers/EvaluacionController.php** (MODIFICADO)
   - Nuevo método: `exportarExcel($id_evento = null)`
   - Guarda en: `public/excel/{tipo_evento}/{nombre_archivo}.xlsx`
   - Retorna la URL del archivo generado

3. **routes/api.php** (MODIFICADO)
   - Nueva ruta: `GET /api/evaluaciones/exportar/{id_evento?}`

4. **public/excel/** (NUEVA CARPETA)
   - Aquí se guardan los archivos Excel
   - Organizado por tipo de evento

### FRONTEND:

5. **frontend/src/views/ExamenesView.vue** (MODIFICADO)
   - Botón "Exportar Excel" agregado
   - Función `exportarExcel()` para llamar al endpoint
   - Descarga automática del archivo
   - Loading state mientras genera

---

## 📊 ESTRUCTURA DEL EXCEL

### Columnas incluidas:
1. N° - Número secuencial
2. DNI - Documento de identidad
3. NOMBRES COMPLETOS - Nombres y apellidos
4. TIPO DE EVENTO - Capacitación, Examen, etc.
5. EVENTO - Nombre del evento específico
6. FECHA EVALUACIÓN - Fecha y hora del examen
7. TOTAL PREGUNTAS - Cantidad total de preguntas
8. CORRECTAS - Respuestas correctas
9. INCORRECTAS - Respuestas incorrectas
10. EN BLANCO - Respuestas no marcadas
11. PUNTAJE - Puntaje numérico
12. NOTA (%) - Porcentaje de nota
13. ESTADO - APROBADO/DESAPROBADO con colores
14. OBSERVACIONES - Comentarios adicionales

---

## 🎨 DISEÑO DEL EXCEL

### Características del diseño:

✅ **Encabezado profesional**
   - Fondo azul oscuro (#1E40AF)
   - Texto blanco en negrita
   - Centrado y con bordes

✅ **Filas de datos**
   - Filas pares con fondo gris claro (#F3F4F6)
   - Filas impares con fondo blanco
   - Bordes suaves en gris (#CCCCCC)

✅ **Columna ESTADO con colores**
   - APROBADO: Verde (#047857 texto, #D1FAE5 fondo)
   - DESAPROBADO: Rojo (#B91C1C texto, #FEE2E2 fondo)
   - Texto en negrita

✅ **Ajustes automáticos**
   - Ancho de columnas optimizado
   - Altura de filas automática
   - Encabezado congelado al hacer scroll

✅ **Alineación inteligente**
   - Números centrados (DNI, puntajes, fechas)
   - Texto alineado a la izquierda (nombres)

---

## 📂 UBICACIÓN DE ARCHIVOS

Los archivos Excel se guardan en:
```
backend/public/excel/{TIPO_EVENTO}/{NOMBRE_EVENTO_FECHA_HORA}.xlsx
```

### Ejemplos:
```
excel/Capacitacion/DERECHO_PENAL_2026-01-15_14-30-00.xlsx
excel/Examen/EXAMEN_FINAL_2026-01-15_16-45-00.xlsx
excel/Curso/DERECHO_LABORAL_2026-01-15_10-00-00.xlsx
```

---

## 🚀 CÓMO USAR

### En el frontend:

1. Ve a la vista "Exámenes"
2. (Opcional) Aplica filtros por evento o estado
3. Haz clic en el botón **"Exportar Excel"** (verde, ícono de Excel)
4. El archivo se descargará automáticamente
5. El Excel estará guardado en `backend/public/excel/`

### Desde la API:

```bash
# Exportar todas las evaluaciones
GET /api/evaluaciones/exportar

# Exportar solo de un evento específico
GET /api/evaluaciones/exportar/7
```

### Respuesta de la API:
```json
{
  "success": true,
  "message": "Excel generado exitosamente",
  "data": {
    "nombre_archivo": "EVALUACION_INTERMEDIA_2026-01-15_14-30-00.xlsx",
    "ruta": "excel/Examen/EVALUACION_INTERMEDIA_2026-01-15_14-30-00.xlsx",
    "url": "http://127.0.0.1:8000/excel/Examen/EVALUACION_INTERMEDIA_2026-01-15_14-30-00.xlsx",
    "tipo_evento": "Examen",
    "evento": "EVALUACIÓN INTERMEDIA"
  }
}
```

---

## 📦 LIBRERÍAS UTILIZADAS

### Backend:
- **maatwebsite/excel** v3.1.54 - Librería Laravel para Excel
- **PhpSpreadsheet** - Motor de generación de Excel (incluido en maatwebsite/excel)

### Frontend:
- **Vuetify** - Botón y componentes UI
- **Axios** - Peticiones HTTP

---

## ✨ CARACTERÍSTICAS ESPECIALES

1. **Filtros aplicados**: Si filtras por evento en el frontend, el Excel solo incluirá ese evento
2. **Nombre inteligente**: El archivo se nombra según el evento y fecha/hora actual
3. **Organización**: Los archivos se organizan automáticamente por tipo de evento
4. **Sin duplicados**: Si existe un archivo con el mismo nombre, se agrega un sufijo
5. **Descarga directa**: El archivo se descarga automáticamente al navegador
6. **Guardado persistente**: El archivo queda guardado en el servidor para futuras consultas

---

## 🔧 REQUISITOS

### Backend:
- PHP >= 8.1
- Laravel 10
- Extensión PHP: `php_zip` (para crear archivos Excel)
- Extensión PHP: `php_gd` o `php_gd2` (opcional, para imágenes)

### Permisos:
- La carpeta `public/excel/` debe tener permisos de escritura
- Laravel debe poder crear subcarpetas automáticamente

---

## 🎯 NOTAS IMPORTANTES

1. Los archivos Excel generados son **permanentes** hasta que los elimines manualmente
2. Puedes acceder a los archivos directamente desde: `http://127.0.0.1:8000/excel/{tipo}/{archivo}.xlsx`
3. El diseño del Excel es **responsive** y se ve bien en Excel, Google Sheets y LibreOffice
4. Los colores y estilos son **compatibles** con todas las versiones de Excel desde 2007
5. Los archivos están en formato **.xlsx** (Excel moderno, no .xls antiguo)

---

## 📈 FUTURAS MEJORAS (OPCIONAL)

- Agregar gráficos al Excel
- Incluir una hoja de resumen con estadísticas
- Exportar respuestas detalladas por pregunta
- Agregar filtros avanzados en el Excel
- Permitir configurar qué columnas exportar
- Programar exportaciones automáticas

---

**Última actualización**: Enero 2026
**Versión**: 1.0
