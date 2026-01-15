# ════════════════════════════════════════════════════════════════
# INSTRUCCIONES PARA CREAR Y DISTRIBUIR EL .EXE
# ════════════════════════════════════════════════════════════════

## 📦 PASO 1: COMPILAR EL .EXE

### En tu máquina de desarrollo (donde tienes Python):

1. Abre PowerShell o CMD en la carpeta del proyecto
2. Ejecuta:
   ```
   compilar.bat
   ```
   
   O manualmente:
   ```
   pip install -r requirements.txt
   pyinstaller Sistema_Calificacion_Examenes.spec
   ```

3. Espera a que termine la compilación (puede tomar 2-5 minutos)

---

## 📁 PASO 2: ARCHIVOS GENERADOS

Después de compilar, se creará la carpeta `dist/` con:

```
dist/
├── Sistema_Calificacion_Examenes.exe    ← EXE principal
└── _internal/                           ← Carpeta con dependencias
    ├── poppler/                         ← Herramienta para PDFs
    ├── config.py                        ← Configuración API
    ├── api_client.py                    ← Cliente API
    └── [muchas DLLs y archivos]
```

---

## 💾 PASO 3: COPIAR A OTRA MÁQUINA

Para usar en otra computadora **SIN PYTHON**, necesitas copiar:

### ✅ ARCHIVOS OBLIGATORIOS:
1. **Sistema_Calificacion_Examenes.exe** (el ejecutable)
2. **Carpeta _internal/** (COMPLETA, con todo su contenido)

### 📂 Estructura final en la otra máquina:
```
MiCarpeta/
├── Sistema_Calificacion_Examenes.exe
└── _internal/
    ├── poppler/
    ├── config.py
    ├── api_client.py
    └── [otros archivos...]
```

⚠️ **IMPORTANTE**: El .exe y la carpeta `_internal` deben estar en el mismo directorio.

---

## ⚙️ PASO 4: CONFIGURACIÓN EN LA OTRA MÁQUINA

Antes de ejecutar, debes configurar la URL de la API Laravel:

1. Abre `_internal/config.py` con un editor de texto
2. Cambia la línea:
   ```python
   API_BASE_URL = "http://127.0.0.1:8000/api"
   ```
   
   Por la IP del servidor donde está Laravel:
   ```python
   API_BASE_URL = "http://192.168.1.100:8000/api"
   ```

3. Guarda el archivo

---

## 🚀 PASO 5: EJECUTAR

1. Doble clic en `Sistema_Calificacion_Examenes.exe`
2. La aplicación debe abrir normalmente
3. Si la API Laravel está corriendo, verás los eventos cargados

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### ❌ Error: "No se puede abrir el archivo"
- Asegúrate de que la carpeta `_internal` está junto al .exe

### ❌ Error: "Poppler no encontrado"
- Verifica que `_internal/poppler/Library/bin` existe

### ❌ Error: "No se pudo importar api_client"
- Verifica que `_internal/config.py` y `_internal/api_client.py` existen

### ❌ No carga los eventos
- Verifica que la URL de la API en `config.py` es correcta
- Verifica que el servidor Laravel está corriendo
- Verifica que no hay firewall bloqueando la conexión

---

## 📋 REQUISITOS EN LA MÁQUINA DE DESTINO

### ✅ NO necesita:
- Python
- pip
- Ninguna librería Python
- Visual Studio
- OpenCV instalado

### ⚠️ SI necesita (incluido en Windows 10/11):
- Windows 10/11 (64 bits)
- .NET Framework (generalmente ya instalado)
- Visual C++ Redistributable (se instala automáticamente)

---

## 📦 DISTRIBUCIÓN COMPLETA (OPCIÓN PORTABLE)

Si quieres hacer un paquete completo en ZIP:

1. Crea una carpeta: `SistemaOMR_Portable`
2. Copia dentro:
   - Sistema_Calificacion_Examenes.exe
   - _internal/ (carpeta completa)
   - INSTRUCCIONES.txt (este archivo)
   - config.py (copia adicional para fácil edición)

3. Comprímelo en ZIP
4. Envíalo a la otra máquina
5. Descomprímelo y listo

---

## 🔧 CONFIGURACIÓN AVANZADA

### Cambiar timeout de API:
Edita `_internal/config.py`:
```python
REQUEST_TIMEOUT = 30  # Aumentar si la red es lenta
```

### Desactivar caché:
Edita `_internal/config.py`:
```python
CACHE_ENABLED = False
```

### Modo debug:
Edita `_internal/config.py`:
```python
DEBUG_MODE = True
```

---

## 📊 TAMAÑO APROXIMADO

- **EXE + _internal**: ~250-350 MB
- **Comprimido en ZIP**: ~100-150 MB

---

## ✨ CARACTERÍSTICAS DEL .EXE

✅ Funciona sin instalar nada
✅ Incluye todas las librerías necesarias
✅ Incluye Poppler para procesar PDFs
✅ Interfaz gráfica completa
✅ Conexión con API Laravel
✅ Procesa hojas de respuestas OMR
✅ Genera PDFs de evidencia
✅ Guarda resultados en la base de datos

---

## 🆘 SOPORTE

Si hay problemas, revisa:
1. Que la carpeta `_internal` está completa
2. Que la URL de la API es correcta
3. Que el servidor Laravel está corriendo
4. Los logs en la consola (si la abres con CMD)

---

**Última actualización**: Enero 2026
**Versión**: 1.0
