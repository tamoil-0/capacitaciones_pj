# 📦 GUÍA DE INSTALACIÓN - OTRA MÁQUINA

## 🎯 Sistema de Capacitaciones - Poder Judicial de Puno

Esta guía te ayudará a instalar el sistema completo en una **máquina nueva que solo tenga XAMPP instalado**.

---

## 📋 REQUISITOS PREVIOS

✅ **XAMPP 8.2** instalado en `C:\xampp82\` (o ajustar rutas)
- Debe incluir:
  - Apache
  - MySQL/MariaDB
  - PHP 8.2+

✅ **Node.js 18+** (descargar de https://nodejs.org/)

✅ **Composer** (descargar de https://getcomposer.org/)

---

## 🚀 PASOS DE INSTALACIÓN

### 1️⃣ COPIAR ARCHIVOS

1. Copiar la carpeta completa `capacitaciones_pj` a `C:\xampp82\htdocs\`
2. La ruta final debe ser: `C:\xampp82\htdocs\capacitaciones_pj\`

---

### 2️⃣ INICIAR XAMPP

1. Abrir **XAMPP Control Panel**: `C:\xampp82\xampp-control.exe`
2. Hacer clic en **[Start]** junto a:
   - ✅ **Apache**
   - ✅ **MySQL**
3. Verificar que ambos servicios estén corriendo (botón cambia a [Stop])

---

### 3️⃣ CREAR BASE DE DATOS

1. Abrir navegador y ir a: **http://localhost/phpmyadmin**
2. Hacer clic en **"Nueva"** (lado izquierdo)
3. Nombre de la base de datos: `capacitaciones`
4. Cotejamiento: `utf8mb4_unicode_ci`
5. Hacer clic en **"Crear"**

---

### 4️⃣ CONFIGURAR BACKEND (Laravel)

Abrir **PowerShell** o **CMD** y ejecutar:

```powershell
cd C:\xampp82\htdocs\capacitaciones_pj\backend

# Instalar dependencias de Composer
composer install

# Verificar que existe el archivo .env
# Si NO existe, crearlo con este contenido:
```

**Contenido del archivo `.env`** (crear si no existe):

```env
APP_NAME="Sistema de Capacitaciones - Poder Judicial"
APP_ENV=local
APP_KEY=
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=capacitaciones
DB_USERNAME=root
DB_PASSWORD=

SESSION_DRIVER=database
SESSION_LIFETIME=120

CACHE_STORE=database
```

Luego ejecutar:

```powershell
# Generar key de la aplicación
php artisan key:generate

# Crear tabla de sesiones
php artisan session:table

# Ejecutar migraciones y seeders (crear tablas y usuario)
php artisan migrate:fresh --seed --force
```

**✅ Esto creará el usuario:**
- Usuario: `pjudicial`
- Contraseña: `Corte2026`

---

### 5️⃣ CONFIGURAR FRONTEND (Vue.js)

Abrir **otra terminal** PowerShell/CMD:

```powershell
cd C:\xampp82\htdocs\capacitaciones_pj\frontend

# Instalar dependencias de Node.js
npm install
```

---

### 6️⃣ INICIAR EL SISTEMA

#### **Opción A: Usar archivos .BAT (RECOMENDADO)**

Hacer doble clic en:
```
C:\xampp82\htdocs\capacitaciones_pj\INICIAR_SISTEMA.bat
```

Esto abrirá:
- Backend en: http://localhost:8000
- Frontend en: http://localhost:5173

#### **Opción B: Iniciar manualmente**

**Terminal 1 - Backend:**
```powershell
cd C:\xampp82\htdocs\capacitaciones_pj\backend
php artisan serve
```

**Terminal 2 - Frontend:**
```powershell
cd C:\xampp82\htdocs\capacitaciones_pj\frontend
npm run dev
```

---

## 🎉 ACCEDER AL SISTEMA

1. Abrir navegador
2. Ir a: **http://localhost:5173**
3. Iniciar sesión con:
   - **Usuario:** `pjudicial`
   - **Contraseña:** `Corte2026`

---

## 🛠️ SISTEMA OMR (OPCIONAL)

Si vas a usar el sistema de calificación de exámenes:

### Opción 1: Ejecutar script Python

```powershell
cd C:\xampp82\htdocs\capacitaciones_pj
python completo.py
```

**Requisitos:**
- Python 3.8+
- Instalar dependencias: `pip install -r requirements.txt`

### Opción 2: Usar ejecutable (si existe)

Si existe el archivo `Sistema_Calificacion_Examenes.exe`:
1. Hacer doble clic en el ejecutable
2. Asegurarse de que `pj.jpg` esté en la misma carpeta

---

## 📁 ESTRUCTURA IMPORTANTE

```
C:\xampp82\htdocs\capacitaciones_pj\
├── backend/                    → API Laravel
│   └── public/
│       └── resultados_omr/    → Aquí se guardan los PDFs del OMR
├── frontend/                   → Interfaz Vue.js
├── completo.py                → Sistema OMR (opcional)
├── pj.jpg                     → Logo institucional
├── INICIAR_SISTEMA.bat        → Iniciar todo el sistema
├── DETENER_SISTEMA.bat        → Detener servicios
└── REINICIAR_SISTEMA.bat      → Reiniciar sistema
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS COMUNES

### ❌ Error: "No se puede conectar a la base de datos"

**Solución:**
1. Verificar que MySQL esté corriendo en XAMPP
2. Verificar que la base de datos `capacitaciones` existe
3. Revisar credenciales en `backend/.env`

### ❌ Error: "SQLSTATE[HY000] [1045] Access denied"

**Solución:**
1. Abrir `backend/.env`
2. Verificar:
   ```
   DB_USERNAME=root
   DB_PASSWORD=
   ```
3. Guardar y ejecutar: `php artisan migrate:fresh --seed --force`

### ❌ Error: "npm: command not found"

**Solución:**
1. Instalar Node.js desde https://nodejs.org/
2. Reiniciar la terminal
3. Verificar con: `node --version` y `npm --version`

### ❌ Error: "composer: command not found"

**Solución:**
1. Instalar Composer desde https://getcomposer.org/
2. Reiniciar la terminal
3. Verificar con: `composer --version`

### ❌ Error al iniciar frontend: "Port 5173 already in use"

**Solución:**
1. Cerrar cualquier instancia anterior de `npm run dev`
2. O cambiar el puerto en `frontend/vite.config.js`

---

## 📞 SOPORTE

Si tienes problemas:

1. Verificar que XAMPP esté corriendo (Apache y MySQL)
2. Verificar que la base de datos `capacitaciones` exista
3. Revisar los logs:
   - Backend: `backend/storage/logs/laravel.log`
   - Frontend: Consola del navegador (F12)

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] XAMPP instalado
- [ ] Apache corriendo
- [ ] MySQL corriendo
- [ ] Base de datos `capacitaciones` creada
- [ ] Node.js instalado
- [ ] Composer instalado
- [ ] `composer install` ejecutado
- [ ] `npm install` ejecutado
- [ ] `php artisan key:generate` ejecutado
- [ ] `php artisan migrate:fresh --seed --force` ejecutado
- [ ] Backend corriendo (http://localhost:8000)
- [ ] Frontend corriendo (http://localhost:5173)
- [ ] Puedo iniciar sesión con pjudicial/Corte2026

---

**¡Sistema listo para usar! 🚀**
