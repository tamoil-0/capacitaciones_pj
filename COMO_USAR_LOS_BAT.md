# 🚀 GUÍA RÁPIDA - USO DEL SISTEMA

## 📁 Archivos .bat Creados

Encontrarás estos archivos en la carpeta del proyecto:

```
capacitaciones_pj/
├── INICIAR_SISTEMA.bat         ← USAR ESTE PARA INICIAR TODO ⭐
├── DETENER_SISTEMA.bat         ← Detener todos los servicios
├── REINICIAR_SISTEMA.bat       ← Reiniciar todo
├── VERIFICAR_SERVICIOS.bat     ← Ver qué está corriendo
└── ABRIR_NAVEGADOR.bat         ← Abrir el sistema en navegador
```

---

## ⭐ USO DIARIO (PARA USUARIOS SIN CONOCIMIENTOS TÉCNICOS)

### 🟢 INICIAR EL SISTEMA

**Paso 1:** Abrir **XAMPP Control Panel** y hacer clic en **START** en:
- ✅ Apache
- ✅ MySQL

**Paso 2:** Hacer **DOBLE CLIC** en:
```
INICIAR_SISTEMA.bat
```

**¿Qué hace?**
- ✅ Inicia el Backend (Laravel)
- ✅ Inicia el Frontend (Vue)
- ✅ Abre automáticamente el navegador

**Resultado:**
- Se abrirán **2 ventanas negras** → **NO LAS CIERRES**
- El navegador se abrirá automáticamente en: `http://localhost:5173`
- Login: `pjudicial` / `Corte2026`

---

### 🔴 DETENER EL SISTEMA

**Al terminar el día:**

**Paso 1:** Hacer DOBLE CLIC en:
```
DETENER_SISTEMA.bat
```
(Esto detiene Backend y Frontend)

**Paso 2:** En **XAMPP Control Panel**, hacer clic en **STOP** en:
- Apache
- MySQL

**¿Qué hace?**
- ✅ Cierra las 2 ventanas negras (Backend y Frontend)
- ✅ Libera memoria RAM

---

### 🔄 REINICIAR EL SISTEMA

**Si algo falla o se traba, hacer DOBLE CLIC en:**
```
REINICIAR_SISTEMA.bat
```

**¿Qué hace?**
- ✅ Detiene todo
- ✅ Espera 5 segundos
- ✅ Inicia todo de nuevo

---

### 🔍 VERIFICAR SI ESTÁ CORRIENDO

**Para ver el estado de los servicios, hacer DOBLE CLIC en:**
```
VERIFICAR_SERVICIOS.bat
```

**Muestra:**
- ✅ Apache: CORRIENDO o DETENIDO
- ✅ MySQL: CORRIENDO o DETENIDO
- ✅ Backend: CORRIENDO o DETENIDO
- ✅ Frontend: CORRIENDO o DETENIDO

---

## 📋 INSTRUCCIONES PASO A PASO

### Primera Vez que Usas el Sistema:

1. **Descargar el proyecto** desde Git (ya hecho)
2. **Instalar dependencias** (solo una vez):
   ```bash
   cd backend
   composer install
   cd ../frontend
   npm install
   ```
3. **Crear base de datos** en phpMyAdmin:
   - Nombre: `capacitaciones`
   - Cotejamiento: `utf8mb4_unicode_ci`
4. **Migrar datos**::
   - Inicia Apache y MySQL desde XAMPP Control Panel
   - Ejecut
   ```bash
   cd backend
   php artisan migrate:fresh --seed
   ```
5. **LISTO!** Ahora solo usa `INICIAR_SISTEMA.bat`

---

### Uso Normal (Todos los Días):
Abrir XAMPP Control Panel
   - Start → Apache
   - Start → MySQL
   - Doble clic en `INICIAR_SISTEMA.bat`
   - Esperar que se abra el navegador
   - Iniciar sesión

2. **Trabajar todo el día:**
   - Las 2 ventanas negras deben permanecer abiertas
   - Si cierras una por error → ejecutar `REINICIAR_SISTEMA.bat`

3. **Al salir:**
   - Doble clic en `DETENER_SISTEMA.bat`
   - En XAMPP Control Panel: Stop → Apache y MySQL
3. **Al salir:**
   - Doble clic en `DETENER_SISTEMA.bat`
   - Apagar la computadora

---

## 🖥️ ¿Qué Son las Ventanas Negras?

Cuando ejecutes `INICIAR_SISTEMA.bat` verás **3 ventanas**:

### Ventana 1: Principal (Verde)
```
========================================================================
  IMPORTANTE: Asegurate de que Apache y MySQL esten corriendo
              en XAMPP Control Panel antes de continuar.

========================================================================

Presione una tecla para continuar . . .

[1/2] Iniciando Backend... OK
[2/2] XAMPP encontrado
[2/5] Iniciando Apache... OK
[3/5] Iniciando MySQL... OK
[4/5] Iniciando Backend... OK
[5/5] Iniciando Frontend... OK

SISTEMA INICIADO CORRECTAMENTE
```
**Esta puedes cerrarla después que todo inicie.**

---

### Ventana 2: BACKEND (Azul)
```
BACKEND CORRIENDO - NO CERRAR ESTA VENTANA

Laravel development server started: http://127.0.0.1:8000
```
**⚠️ NO CERRAR - Backend dejará de funcionar**

---

### Ventana 3: FRONTEND (Amarillo)
```
FRONTEND CORRIENDO - NO CERRAR ESTA VENTANA

  VITE v5.0.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```
**⚠️ NO CERRAR - Frontend dejará de funcionar**

---

## ❌ PROBLEMAS COMUNES

### "El sistema no inicia"

**Solución:**
1. Abrir `VERIFICAR_SERVICIOS.bat`
2. Ver qué está detenido
3. Ejecutar `REINICIAR_SISTEMA.bat`

---

### "Cerré una ventana negra por error"

**Solución:**
1. Ejecutar `DETENER_SISTEMA.bat`
2. Ejecutar `INICIAR_SISTEMA.bat`

---

### "No se abre el navegador automáticamente"

**Solución:**
1. Abrir manualmente: `http://localhost:5173`
2. O ejecutar `ABRIR_NAVEGADOR.bat`

---

### "Dice que el puerto está ocupado"

**Solución:**
1. Ejecutar `DETENER_SISTEMA.bat`
2. Esperar 10 segundos
3. Ejecutar `INICIAR_SISTEMA.bat`

---

### "MySQL no inicia"

**Solución:**
1. Abrir XAMPP Control Panel manualmente
2. Click en "Start" en MySQL
3. Luego ejecutar `INICIAR_SISTEMA.bat`

---

## 🎯 RESUMEN PARA USUARIOS NO TÉCNICOS

### Solo necesitas saber esto:

1. **Para iniciar:** Doble clic en `INICIAR_SISTEMA.bat`
2. **Para detener:** Doble clic en `DETENER_SISTEMA.bat`
3. **Si falla algo:** Doble clic en `REINICIAR_SISTEMA.bat`

### NO necesitas saber:
- ❌ Comandos de terminal
- ❌ Qué es Laravel o Vue
- ❌ Cómo funciona Apache o MySQL
- ❌ Conceptos técnicos

**Todo está automatizado** ✅

---

## 📞 SOPORTE

Si ninguno de los archivos .bat funciona:
1. Contactar al área de TI
2. Verificar que XAMPP esté instalado en `C:\xampp82` o `C:\xampp`
3. Revisar que se hayan instalado las dependencias

---

**Desarrollado para:** Poder Judicial de Puno 🏛️  
**Versión:** 2.0 - Con scripts automatizados  
**Fecha:** Enero 2026
