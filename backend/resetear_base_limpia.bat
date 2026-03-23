@echo off
echo ============================================
echo   RESETEAR BASE DE DATOS LIMPIA
echo   Sistema de Capacitaciones - Poder Judicial
echo ============================================
echo.
echo ADVERTENCIA: Esto eliminara TODOS los datos
echo Solo mantendra:
echo   - Usuario admin
echo   - Tipos de evento
echo   - Opciones de menu
echo.
pause

REM Detectar ruta de PHP
set "PHP_PATH=C:\xampp\php\php.exe"
if not exist "%PHP_PATH%" set "PHP_PATH=C:\xampp82\php\php.exe"
if not exist "%PHP_PATH%" (
    echo ERROR: No se encontro PHP en C:\xampp ni en C:\xampp82
    pause
    exit /b 1
)

echo.
echo [1/3] Eliminando todas las tablas...
"%PHP_PATH%" artisan migrate:reset

echo.
echo [2/3] Creando estructura de tablas...
"%PHP_PATH%" artisan migrate

echo.
echo [3/3] Insertando datos esenciales...
"%PHP_PATH%" artisan db:seed

echo.
echo ============================================
echo   COMPLETADO EXITOSAMENTE!
echo ============================================
echo.
echo Credenciales de acceso:
echo Usuario: pjudicial
echo Contraseña: Corte2026
echo.
pause
