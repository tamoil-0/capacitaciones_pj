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

echo.
echo [1/3] Eliminando todas las tablas...
php artisan migrate:reset

echo.
echo [2/3] Creando estructura de tablas...
php artisan migrate

echo.
echo [3/3] Insertando datos esenciales...
php artisan db:seed

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
