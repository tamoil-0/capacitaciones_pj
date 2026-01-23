# 🖥️ GUÍA: Instalar en Nueva Máquina

## ✅ Requisitos de la Nueva Máquina
- ✅ XAMPP 8.2 instalado
- ✅ Conexión a Internet (para clonar Git)
- ⚠️ Composer y Node.js (si no están, te digo cómo instalarlos)

---

## 📋 PASO A PASO COMPLETO

### 🔵 PASO 1: Descargar el Proyecto desde Git

```bash
# Abrir terminal en C:\xampp\htdocs
cd C:\xampp\htdocs

# Clonar el repositorio
git clone https://github.com/tamoil-0/capacitaciones_pj.git

# Entrar a la carpeta
cd capacitaciones_pj
```

**Resultado esperado:**
```
✅ Carpeta: C:\xampp\htdocs\capacitaciones_pj
✅ Contenido: backend/, frontend/, completo.py, dist/, etc.
```

---

### 🔵 PASO 2: Verificar/Instalar Composer (Backend)

**Verificar si ya está instalado:**
```bash
composer --version
```

**Si dice "no reconocido", instalarlo:**
1. Descargar: https://getcomposer.org/download/
2. Ejecutar `Composer-Setup.exe`
3. Siguiente → Siguiente → Instalar
4. **Cerrar y REABRIR la terminal**

---

### 🔵 PASO 3: Instalar Dependencias del Backend

```bash
cd C:\xampp\htdocs\capacitaciones_pj\backend

# Instalar paquetes de Laravel
composer install
```

**Esto puede tomar 2-3 minutos** ☕

**Si hay error de memoria:**
```bash
# Aumentar límite de memoria temporalmente
set COMPOSER_MEMORY_LIMIT=-1
composer install
```

---

### 🔵 PASO 4: Configurar Archivo .env

```bash
# Copiar ejemplo de configuración
copy .env.example .env

# Generar clave de encriptación
php artisan key:generate
```

**Editar `backend/.env` con tus datos:**
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=capacitaciones
DB_USERNAME=root
DB_PASSWORD=
```

⚠️ **IMPORTANTE:** En XAMPP 8.2, la contraseña de root es **VACÍA** (dejar sin valor)

---

### 🔴 PASO 5: CREAR BASE DE DATOS (MANUAL - OBLIGATORIO)

⚠️ **ESTE ES EL PASO MÁS IMPORTANTE**

**Laravel NO crea la base de datos automáticamente. Debes crearla TÚ:**

1. **Iniciar Apache y MySQL en XAMPP**
   - Abrir XAMPP Control Panel
   - Start → Apache
   - Start → MySQL

2. **Abrir phpMyAdmin:**
   ```
   http://localhost/phpmyadmin
   ```

3. **Crear la base de datos:**
   - Clic en "**Nueva**" (lado izquierdo)
   - Nombre: `capacitaciones`
   - Cotejamiento: `utf8mb4_unicode_ci`
   - Clic en "**Crear**"

**Captura de lo que verás:**
```
┌─────────────────────────────────────┐
│ phpMyAdmin                          │
├─────────────────────────────────────┤
│ ▶ Nueva                             │ ← Hacer clic aquí
│ ▶ information_schema                │
│ ▶ mysql                             │
│ ▶ performance_schema                │
└─────────────────────────────────────┘

Luego:
┌─────────────────────────────────────┐
│ Crear base de datos                 │
├─────────────────────────────────────┤
│ Nombre: [capacitaciones_________]   │
│ Cotejamiento: [utf8mb4_unicode_ci▼] │
│                                     │
│            [Crear]                  │
└─────────────────────────────────────┘
```

✅ **Verás el mensaje:** "Base de datos capacitaciones ha sido creada"

---

### 🔵 PASO 6: Crear Tablas y Datos Iniciales

```bash
cd C:\xampp\htdocs\capacitaciones_pj\backend

# Crear TODAS las tablas y datos
php artisan migrate:fresh --seed
```

**¿Qué hace este comando?**
- ✅ Crea 15+ tablas (usuarios, eventos, personas, inscripciones, etc.)
- ✅ Inserta usuario admin: `pjudicial` / `Corte2026`
- ✅ Inserta tipos de eventos (Convocatorias, Cursos, Otros)
- ✅ Configura opciones del menú

**Salida esperada:**
```
Migration table created successfully.
Migrating: 2014_10_12_000000_create_usuarios_table
Migrated:  2014_10_12_000000_create_usuarios_table (45.23ms)
Migrating: 2014_10_12_100000_create_personas_table
Migrated:  2014_10_12_100000_create_personas_table (38.45ms)
...
Seeding: UsuariosSeeder
Seeded:  UsuariosSeeder (12.34ms)
...
Database seeding completed successfully.
```

---

### 🔵 PASO 7: Verificar/Instalar Node.js (Frontend)

**Verificar si ya está instalado:**
```bash
node --version
npm --version
```

**Si dice "no reconocido", instalarlo:**
1. Descargar: https://nodejs.org/ (versión LTS)
2. Ejecutar instalador
3. Siguiente → Siguiente → Instalar
4. **Cerrar y REABRIR la terminal**

---

### 🔵 PASO 8: Instalar Dependencias del Frontend

```bash
cd C:\xampp\htdocs\capacitaciones_pj\frontend

# Instalar paquetes de Vue
npm install
```

**Esto puede tomar 3-5 minutos** ☕

---

### 🔵 PASO 9: Iniciar el Sistema

#### 🎯 MÉTODO FÁCIL (Recomendado):

**Hacer DOBLE CLIC en:**
```
INICIAR_SISTEMA.bat
```

✅ **Esto hará TODO automáticamente:**
- Inicia Apache y MySQL
- Inicia Backend (Laravel)
- Inicia Frontend (Vue)
- Abre el navegador automáticamente

**¡LISTO!** No necesitas hacer nada más.

📖 **Ver guía completa:** [COMO_USAR_LOS_BAT.md](COMO_USAR_LOS_BAT.md)

---

#### 🔧 MÉTODO MANUAL (Solo si el .bat falla):

**Terminal 1 - Backend (Laravel):**
```bash
cd C:\xampp\htdocs\capacitaciones_pj\backend
php artisan serve
```

**Terminal 2 - Frontend (Vue):**
```bash
cd C:\xampp\htdocs\capacitaciones_pj\frontend
npm run dev
```

---

### 🔵 PASO 10: Acceder al Sistema

**Abrir navegador:**
```
http://localhost:5173
```

**Credenciales:**
```
Usuario: pjudicial
Contraseña: Corte2026
```

---

## ✅ RESUMEN - COMANDOS COMPLETOS

```bash
# 1. Clonar proyecto
cd C:\xampp\htdocs
git clone https://github.com/tamoil-0/capacitaciones_pj.git
cd capacitaciones_pj

# 2. Backend
cd backend
composer install
copy .env.example .env
php artisan key:generate

# 3. CREAR BASE DE DATOS EN PHPMYADMIN (http://localhost/phpmyadmin)
#    Nombre: capacitaciones
#    Cotejamiento: utf8mb4_unicode_ci

# 4. Migrar y sembrar datos
php artisan migrate:fresh --seed

# 5. Frontend
cd ..\frontend
npm install

# 6. Iniciar servicios (dos terminales separadas)
# Terminal 1:
cd backend
php artisan serve

# Terminal 2:
cd frontend
npm run dev

# 7. Abrir: http://localhost:5173
#    Usuario: pjudicial
#    Contraseña: Corte2026
```

---

## 🚨 ERRORES COMUNES Y SOLUCIONES

### Error: "Unknown database 'capacitaciones'"
```
❌ PROBLEMA: No creaste la base de datos
✅ SOLUCIÓN: Ir a phpMyAdmin y crear la BD manualmente (Paso 5)
```

### Error: "composer: command not found"
```
❌ PROBLEMA: Composer no está instalado o no está en PATH
✅ SOLUCIÓN: 
   1. Instalar Composer desde: https://getcomposer.org/download/
   2. Cerrar y reabrir terminal
```

### Error: "npm: command not found"
```
❌ PROBLEMA: Node.js no está instalado
✅ SOLUCIÓN:
   1. Instalar Node.js desde: https://nodejs.org/
   2. Cerrar y reabrir terminal
```

### Error: "Port 3000 already in use"
```
❌ PROBLEMA: Otro programa usa el puerto
✅ SOLUCIÓN:
   Cerrar otros programas o cambiar puerto en vite.config.js
```

### Error: "SQLSTATE[HY000] [2002] No connection could be made"
```
❌ PROBLEMA: MySQL no está corriendo
✅ SOLUCIÓN:
   1. Abrir XAMPP Control Panel
   2. Start → MySQL
```

### Error: "Access denied for user 'root'@'localhost'"
```
❌ PROBLEMA: Contraseña incorrecta en .env
✅ SOLUCIÓN:
   Editar backend/.env:
   DB_PASSWORD=    (dejar vacío para XAMPP)
```

---

## 📱 ¿Y EL EJECUTABLE (.exe)?

El ejecutable del sistema OCR está en: `dist\Sistema_Calificacion_Examenes.exe`

**Para usarlo:**
1. Ya está incluido en el repositorio
2. Simplemente ejecutar: `dist\Sistema_Calificacion_Examenes.exe`
3. NO necesita instalación adicional

**Para distribuir a otras máquinas:**
- Copiar toda la carpeta `dist\` a USB
- Ejecutar en cualquier Windows 10/11

---

## 🎯 CHECKLIST FINAL

Antes de decir que está listo, verificar:

- ✅ Apache corriendo en XAMPP
- ✅ MySQL corriendo en XAMPP
- ✅ Base de datos `capacitaciones` creada en phpMyAdmin
- ✅ Tablas creadas con `php artisan migrate:fresh --seed`
- ✅ Backend corriendo: `php artisan serve`
- ✅ Frontend corriendo: `npm run dev`
- ✅ Login funciona con: pjudicial / Corte2026

---

**¿TODO LISTO?** 🎉

Ahora puedes usar el sistema completo en la nueva máquina.

---

**Desarrollado para:** Poder Judicial de Puno 🏛️  
**Fecha:** Enero 2026
