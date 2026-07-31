# Sistema de Gestión de Capacitaciones

Aplicación integral para administrar eventos de capacitación, participantes, asistencias y evaluaciones. Combina una plataforma web con un módulo de escritorio para procesar hojas ópticas y centralizar los resultados.

## Descripción

El sistema cubre el flujo completo de una capacitación: creación del evento, inscripción de participantes, control de entrada y salida, calificación de exámenes y generación de reportes.

La solución está compuesta por:

| Componente | Tecnología | Función |
| --- | --- | --- |
| API | Laravel 10 y PHP 8.2 | Autenticación, reglas de negocio y persistencia |
| Interfaz web | Vue 3, Vuetify y Vite | Administración y operación del sistema |
| Base de datos | MySQL o MariaDB | Usuarios, eventos, personas, registros y evaluaciones |
| Módulo OMR | Python 3.10 y OpenCV | Lectura de hojas ópticas y cálculo de resultados |

## Funcionalidades principales

- Gestión de convocatorias, cursos y otros eventos.
- Administración de usuarios, personas e inscripciones.
- Importación masiva de participantes desde Excel.
- Registro de entrada y salida mediante DNI.
- Validación de duplicados y control del orden de asistencia.
- Operación concurrente con actualización periódica de datos.
- Procesamiento de exámenes mediante reconocimiento óptico de marcas.
- Consulta de resultados y evidencias por participante.
- Generación de reportes individuales en PDF.
- Exportación de asistencias y evaluaciones a Excel.
- Autenticación de la API mediante Laravel Sanctum.

## Requisitos

- PHP 8.1 o superior, recomendado PHP 8.2.
- Composer 2.
- MySQL 8 o MariaDB compatible.
- Node.js 18 o superior y npm.
- Python 3.10 para utilizar o desarrollar el módulo OMR.
- Poppler para convertir páginas PDF en imágenes durante la calificación.

En Windows puede utilizarse XAMPP 8.2 para disponer de Apache, PHP y MySQL en un solo entorno.

## Instalación

### 1. Obtener el proyecto

```bash
git clone <URL_DEL_REPOSITORIO>
cd <CARPETA_DEL_PROYECTO>
```

### 2. Preparar la API

```bash
cd backend
composer install
copy .env.example .env
php artisan key:generate
```

Configure la conexión en `backend/.env`:

```env
APP_ENV=local
APP_DEBUG=true
APP_URL=http://127.0.0.1:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=capacitaciones
DB_USERNAME=root
DB_PASSWORD=
```

Cree la base de datos antes de ejecutar las migraciones:

```sql
CREATE DATABASE capacitaciones
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Revise las credenciales iniciales definidas en `backend/database/seeders/UsuariosSeeder.php` y sustitúyalas antes de desplegar el sistema.

Después, cree las tablas y cargue los datos iniciales:

```bash
php artisan migrate --seed
```

> `php artisan migrate:fresh --seed` elimina todas las tablas existentes. Úselo únicamente en entornos de desarrollo que puedan reiniciarse.

### 3. Preparar la interfaz web

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

La interfaz utiliza por defecto la API disponible en `http://127.0.0.1:8000/api`. La dirección puede modificarse en `frontend/src/axios.js`.

### 4. Iniciar el backend

```bash
cd backend
php artisan serve
```

Servicios locales predeterminados:

- Interfaz web: `http://localhost:5173`
- API: `http://127.0.0.1:8000/api`

## Módulo de calificación OMR

El archivo `completo.py` contiene la aplicación de escritorio encargada de:

1. Obtener los eventos finalizados desde la API.
2. Cargar el archivo de respuestas correctas.
3. Convertir las hojas PDF en imágenes.
4. Detectar marcas, respuestas y DNI.
5. Calcular el puntaje de cada participante.
6. Generar el reporte y la evidencia de calificación.
7. Sincronizar los resultados con el backend.

Instale sus dependencias desde la raíz del proyecto:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python completo.py
```

Antes de ejecutarlo, revise la dirección de la API y las rutas de Poppler definidas en `config.py` y `api_client.py`.

## Estructura del repositorio

```text
.
├── backend/                 API Laravel
│   ├── app/                 Controladores, modelos, importaciones y reportes
│   ├── database/            Migraciones y datos iniciales
│   └── routes/api.php       Rutas de la API
├── frontend/                Aplicación Vue
│   └── src/                 Vistas, componentes, rutas y estado
├── poppler/                 Utilidades para procesar documentos PDF
├── ENTREGA_FINAL/           Documentación técnica en PDF
├── completo.py              Aplicación de calificación OMR
├── api_client.py            Integración del módulo OMR con la API
├── config.py                Configuración del módulo de escritorio
└── requirements.txt         Dependencias de Python
```

## Documentación

La carpeta `ENTREGA_FINAL` contiene:

- [Manual de usuario](ENTREGA_FINAL/manual_usuario.pdf).
- [Memoria descriptiva](ENTREGA_FINAL/memoria_descriptiva.pdf).
- [Documento de código fuente](ENTREGA_FINAL/codigo_fuente.pdf).

## Comandos útiles

### Backend

```bash
php artisan migrate
php artisan db:seed
php artisan route:list
php artisan config:clear
php artisan cache:clear
php artisan test
```

### Frontend

```bash
npm run dev
npm run build
npm run preview
```

## Despliegue

Para preparar una versión de producción:

```bash
cd backend
composer install --no-dev --optimize-autoloader
php artisan config:cache
php artisan route:cache

cd ../frontend
npm ci
npm run build
```

Además:

- Configure `APP_ENV=production` y `APP_DEBUG=false`.
- Utilice credenciales únicas y seguras.
- Restrinja CORS a los dominios autorizados.
- Proteja el archivo `.env` y no lo publique en el repositorio.
- Configure copias de seguridad de la base de datos y de los reportes.

## Solución de problemas

### La interfaz no se conecta con la API

- Confirme que `php artisan serve` esté activo.
- Revise la URL configurada en `frontend/src/axios.js`.
- Verifique la configuración de CORS y los puertos del firewall.

### Error de conexión con la base de datos

- Compruebe las variables `DB_*` de `backend/.env`.
- Confirme que MySQL o MariaDB esté iniciado.
- Ejecute `php artisan config:clear` después de cambiar el entorno.

### Composer o npm no se reconocen

- Compruebe que PHP, Composer y Node.js estén incluidos en la variable `PATH`.
- Cierre y abra nuevamente la terminal después de instalarlos.

### El módulo OMR no convierte un PDF

- Verifique la instalación o ruta de Poppler.
- Confirme que el documento pueda abrirse y que las hojas estén correctamente escaneadas.
- Revise que las marcas de referencia sean visibles y que la resolución sea suficiente.

## Seguridad

- No publique archivos `.env`, registros, resultados reales ni credenciales.
- Cambie las claves iniciales antes de utilizar el sistema.
- Mantenga actualizadas las dependencias de PHP, JavaScript y Python.
- Valide los archivos Excel y PDF antes de procesarlos.
- Utilice HTTPS y copias de seguridad en producción.

## Licencia

El uso y la distribución del proyecto dependen de la licencia definida por su responsable. Si el repositorio se distribuirá públicamente, añada un archivo `LICENSE` con las condiciones correspondientes.
