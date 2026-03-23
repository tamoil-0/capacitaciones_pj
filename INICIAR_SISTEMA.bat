@echo off
title SISTEMA DE ASISTENCIAS - PODER JUDICIAL DE PUNO
color 0A
mode con: cols=80 lines=25

echo.
echo ========================================================================
echo   SISTEMA DE CONTROL DE ASISTENCIAS
echo   Poder Judicial de Puno
echo ========================================================================
echo.
echo   IMPORTANTE: Asegurate de que Apache y MySQL esten corriendo
echo              en XAMPP Control Panel antes de continuar.
echo.
echo ========================================================================
echo.
pause

echo.
echo   Iniciando Backend y Frontend...
echo.

REM ============================================================
REM DETECTAR RUTA DE PHP
REM ============================================================
set "PHP_PATH=C:\xampp\php\php.exe"
if not exist "%PHP_PATH%" set "PHP_PATH=C:\xampp82\php\php.exe"
if not exist "%PHP_PATH%" (
    echo ERROR: No se encontro PHP en C:\xampp ni en C:\xampp82
    pause
    exit /b 1
)

REM ============================================================
REM INICIAR BACKEND (Laravel)
REM ============================================================
echo [1/2] Iniciando Backend (Laravel)...
cd /d "%~dp0backend"
start "BACKEND - Laravel API" cmd /k "color 0B && echo BACKEND CORRIENDO - NO CERRAR ESTA VENTANA && echo. && "%PHP_PATH%" artisan serve"
timeout /t 2 /nobreak >nul
echo       OK - Backend iniciado en http://localhost:8000

REM ============================================================
REM INICIAR FRONTEND (Vue)
REM ============================================================
echo [2/2] Iniciando Frontend (Vue)...
cd /d "%~dp0frontend"
start "FRONTEND - Vue + Vuetify" cmd /k "color 0E && echo FRONTEND CORRIENDO - NO CERRAR ESTA VENTANA && echo. && call npm run dev"
timeout /t 3 /nobreak >nul
echo       OK - Frontend iniciando en http://localhost:5173

echo.
echo ========================================================================
echo   SISTEMA INICIADO CORRECTAMENTE
echo ========================================================================
echo.
echo   Accede al sistema en tu navegador:
echo   
echo   http://localhost:5173
echo.
echo   Credenciales:
echo   Usuario: pjudicial
echo   Password: Corte2026
echo.
echo ========================================================================
echo.
echo   IMPORTANTE:
echo   - NO cierres las 2 ventanas que se abrieron (Backend y Frontend)
echo   - Para detener: ejecuta DETENER_SISTEMA.bat o cierra las ventanas
echo.
echo ========================================================================
echo.

REM Esperar 5 segundos y abrir el navegador automáticamente
timeout /t 5 /nobreak >nul
echo   Abriendo navegador...
start http://localhost:5173

echo.
echo   Puedes cerrar esta ventana ahora.
echo   El sistema seguira corriendo en las otras 2 ventanas.
echo.
pause
