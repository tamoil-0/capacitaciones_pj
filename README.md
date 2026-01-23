# 🏛️ Sistema de Control de Asistencias - Poder Judicial de Puno

Sistema web para gestión de asistencias en eventos de capacitación, convocatorias y cursos del Poder Judicial.

## 📋 Características

- ✅ Registro de asistencias por DNI (con escáner)
- ✅ Control de entrada/salida con validaciones inteligentes
- ✅ Múltiples operadores simultáneos (hasta 3 máquinas)
- ✅ Actualización automática en tiempo real (cada 5 segundos)
- ✅ Exportación a Excel con formato profesional
- ✅ Gestión de eventos, personas e inscripciones
- ✅ Sistema de evaluaciones
- ✅ Validación anti-duplicados (30 segundos)
- ✅ Control de estado (no permite entrada sin salida previa)

## 🛠️ Tecnologías

**Backend:**
- Laravel 10
- PHP 8.2
- MySQL/MariaDB
- PhpSpreadsheet (Excel)

**Frontend:**
- Vue 3 (Composition API)
- Vuetify 3
- Vite
- Axios

## 📦 Requisitos Previos

- XAMPP 8.2 (incluye PHP 8.2 + MySQL)
- Node.js 18+ y npm
- Git
- Composer

## 🚀 Instalación en Nueva Máquina

### 1️⃣ Clonar el Repositorio

```bash
cd C:\xampp\htdocs
git clone https://github.com/tamoil-0/capacitaciones_pj.git
cd capacitaciones_pj
```

### 2️⃣ Configurar Backend (Laravel)

```bash
cd backend

# Instalar dependencias de Composer
composer install

# Copiar archivo de configuración
copy .env.example .env

# Generar key de aplicación
php artisan key:generate
```

**Editar `.env`** con los datos de tu base de datos:
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=capacitaciones
DB_USERNAME=root
DB_PASSWORD=
```

### 3️⃣ Crear Base de Datos (OBLIGATORIO - HACER PRIMERO)

⚠️ **MUY IMPORTANTE:** Laravel NO crea la base de datos automáticamente. Debes crearla MANUALMENTE antes de ejecutar migraciones.

**Abrir phpMyAdmin:** `http://localhost/phpmyadmin`

1. Clic en "Nueva" (lado izquierdo)
2. Nombre de la base de datos: `capacitaciones`
3. Cotejamiento: `utf8mb4_unicode_ci`
4. Clic en "Crear"

![Crear BD](https://i.imgur.com/placeholder.png)

### 4️⃣ Ejecutar Migraciones y Seeders

⚠️ **SOLO después de crear la base de datos**, ejecutar:

```bash
cd backend

# Crear TABLAS y datos iniciales dentro de la BD
php artisan migrate:fresh --seed
```

**¿Qué hace este comando?**
- ✅ Crea todas las tablas (usuarios, eventos, personas, inscripciones, etc.)
- ✅ Inserta datos iniciales (usuario admin, tipos de eventos, opciones)
- ✅ Configura relaciones entre tablas
- ❌ NO crea la base de datos (debes hacerlo en paso 3️⃣)

**Datos creados automáticamente:**
- Usuario: `pjudicial`
- Contraseña: `Corte2026`
- Tipos de evento (Convocatorias, Cursos, Otros)
- Opciones de menú

### 5️⃣ Configurar Frontend (Vue)

```bash
cd ..\frontend

# Instalar dependencias de npm
npm install
```

**Editar `frontend/src/axios.js`** si necesitas cambiar la URL del backend:
```javascript
baseURL: "http://localhost/capacitaciones_pj/backend/api",
```

### 6️⃣ Iniciar Servicios

#### 🎯 MÉTODO FÁCIL (Recomendado - Un solo clic):

**Hacer doble clic en:**
```
INICIAR_SISTEMA.bat
```

✅ **Esto iniciará AUTOMÁTICAMENTE:**
- Apache + MySQL
- Backend (Laravel)
- Frontend (Vue)
- Navegador en `http://localhost:5173`

**Para detener todo:**
```
DETENER_SISTEMA.bat
```

📖 **Ver guía completa:** [COMO_USAR_LOS_BAT.md](COMO_USAR_LOS_BAT.md)

---

#### 🔧 MÉTODO MANUAL (Avanzado):

**Backend:**
```bash
cd backend
php artisan serve
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Acceder a: `http://localhost:5173`

## 🔐 Credenciales Iniciales

```
Usuario: pjudicial
Contraseña: Corte2026
```

## 📂 Estructura del Proyecto

```
capacitaciones_pj/
├── backend/                 # Laravel API
│   ├── app/
│   │   ├── Http/Controllers/
│   │   ├── Models/
│   │   └── Exports/        # Generadores de Excel
│   ├── database/
│   │   ├── migrations/     # Estructura de BD
│   │   └── seeders/        # Datos iniciales
│   └── routes/
│       └── api.php         # Rutas del API
│
├── frontend/               # Vue 3 + Vuetify
│   ├── src/
│   │   ├── views/         # Páginas
│   │   ├── components/    # Componentes reutilizables
│   │   ├── router/        # Rutas
│   │   └── stores/        # Pinia stores
│   └── public/
│
├── completo.py            # Script Python OCR (opcional)
└── README.md
```

## 🔄 Resetear Base de Datos

Si necesitas limpiar todos los datos y empezar desde cero:

```bash
cd backend
php artisan migrate:fresh --seed
```

O usa el script:
```bash
resetear_base_limpia.bat
```

## 🌐 Configurar en Red Local (Múltiples Máquinas)

### En la Máquina Servidor:

1. Obtener IP local:
```bash
ipconfig
# Ejemplo: 192.168.1.100
```

2. Permitir acceso en firewall de Windows

### En las Máquinas Cliente:

Editar `frontend/src/axios.js`:
```javascript
baseURL: "http://192.168.1.100/capacitaciones_pj/backend/api",
```

Acceder desde navegador:
```
http://192.168.1.100:5173
```

## �️ Sistema OCR de Calificación de Exámenes (Ejecutable)

El sistema incluye un script Python (`completo.py`) que puede convertirse en un ejecutable standalone (.exe) para usarse en máquinas sin Python instalado.

### Crear Ejecutable:

**Requisitos:**
- Python 3.10
- PyInstaller 6.3.0+

**Comando:**
```bash
python -m PyInstaller --onefile --windowed --name="Sistema_Calificacion_Examenes" --add-data="poppler;poppler" --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=cv2 --hidden-import=numpy --hidden-import=customtkinter --hidden-import=pdf2image --hidden-import=reportlab --hidden-import=requests --collect-all customtkinter --exclude-module=torch --exclude-module=tensorflow --exclude-module=matplotlib --exclude-module=ultralytics --exclude-module=pygame --exclude-module=scipy --exclude-module=pandas --clean completo.py
```

**Resultado:**
- Ejecutable en: `dist/Sistema_Calificacion_Examenes.exe` (~100 MB)
- Archivos de soporte copiados automáticamente: `api_client.py`, `config.py`

**Distribución:**
Para usar en otra máquina, copiar toda la carpeta `dist/` que incluye:
- `Sistema_Calificacion_Examenes.exe`
- `api_client.py` (conexión con Laravel)
- `config.py` (configuración)
- `poppler/` (procesamiento PDF - incluido automáticamente)

## �📊 Uso del Sistema

### Registro de Asistencias:

1. Ir a: **Eventos → Ver Asistencias**
2. Seleccionar tipo (Entrada/Salida)
3. Escanear DNI o escribir manualmente
4. El sistema valida automáticamente:
   - ✅ Persona inscrita
   - ✅ No duplicados en 30 segundos
   - ✅ Estado correcto (entrada/salida)

### Exportar a Excel:

1. Botón **"Exportar Asistencias a Excel"**
2. Archivo se descarga con:
   - Datos completos de asistentes
   - Fecha y hora de registro
   - Estado (A tiempo / Tardanza)
   - Estadísticas

## 🐛 Solución de Problemas

**Error: "Base de datos no existe" o "Unknown database 'capacitaciones'"**
```
CAUSA: No creaste la base de datos manualmente
SOLUCIÓN:
1. Abrir http://localhost/phpmyadmin
2. Crear base de datos: capacitaciones
3. Cotejamiento: utf8mb4_unicode_ci
4. Luego ejecutar: php artisan migrate:fresh --seed
```

**Error: "SQLSTATE[HY000] [1045] Access denied for user..."**
```
CAUSA: Credenciales incorrectas en .env
SOLUCIÓN:
1. Editar backend/.env
2. Verificar: DB_USERNAME=root y DB_PASSWORD= (vacío para XAMPP)
3. Ejecutar: php artisan config:clear
```

**Error: "composer no reconocido"**
```bash
# Descargar Composer desde: https://getcomposer.org/download/
```

**Error: "npm no reconocido"**
```bash
# Descargar Node.js desde: https://nodejs.org/
```

**Puerto 80 ocupado:**
- Detener Skype o IIS
- O cambiar puerto de Apache en XAMPP

**Frontend no conecta con Backend:**
- Verificar que Apache esté corriendo
- Revisar `axios.js` tiene la URL correcta
- Verificar CORS en `backend/config/cors.php`

## 📝 Notas Importantes

- ⚠️ Cambiar credenciales de admin en producción
- ⚠️ Configurar `.env` con datos reales
- ⚠️ NO subir `.env` a Git (ya está en .gitignore)
- ✅ Sistema soporta hasta 3 operadores simultáneos
- ✅ Auto-actualización cada 5 segundos

## 👨‍💻 Desarrollo

**Comandos útiles:**

```bash
# Backend
php artisan migrate          # Ejecutar migraciones
php artisan db:seed          # Ejecutar seeders
php artisan route:list       # Ver rutas
php artisan config:clear     # Limpiar caché

# Frontend  
npm run dev                  # Modo desarrollo
npm run build                # Compilar producción
npm run preview              # Preview producción
```

## 📄 Licencia

Poder Judicial de Puno - Uso Interno

## 🆘 Soporte

Para problemas o consultas, contactar al área de TI.

---

**Desarrollado para la Corte Superior de Justicia de Puno** 🏛️
