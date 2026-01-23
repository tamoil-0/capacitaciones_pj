@echo off
title SISTEMA DE ASISTENCIAS - PODER JUDICIAL DE PUNO
color 0A
mode con: cols=80 lines=30

echo.
echo ========================================================================
echo   SISTEMA DE CONTROL DE ASISTENCIAS
echo   Poder Judicial de Puno
echo ========================================================================
echo.
echo   Iniciando servicios, por favor espere...
echo.

REM ============================================================
REM VERIFICAR QUE XAMPP EXISTE
REM ============================================================
if not exist "C:\xampp82\xampp-control.exe" (
    if not exist "C:\xampp\xampp-control.exe" (
        echo [ERROR] XAMPP no encontrado en C:\xampp82 ni C:\xampp
        echo.
        echo Por favor instale XAMPP 8.2 o ajuste la ruta en este archivo.
        pause
        exit /b 1
    )
    set XAMPP_PATH=C:\xampp
) else (
    set XAMPP_PATH=C:\xampp82
)

echo [1/5] XAMPP encontrado en: %XAMPP_PATH%

REM ============================================================
REM INICIAR APACHE
REM ============================================================
echo [2/5] Iniciando Apache...
"%XAMPP_PATH%\apache\bin\httpd.exe" -k start >nul 2>&1
timeout /t 3 /nobreak >nul
echo       OK - Apache iniciado

REM ============================================================
REM INICIAR MYSQL
REM ============================================================
echo [3/5] Iniciando MySQL...
"%XAMPP_PATH%\mysql\bin\mysqld.exe" --defaults-file="%XAMPP_PATH%\mysql\bin\my.ini" --standalone >nul 2>&1
if errorlevel 1 (
    echo       ADVERTENCIA - MySQL puede que ya este corriendo
) else (
    timeout /t 3 /nobreak >nul
    echo       OK - MySQL iniciado
)

REM ============================================================
REM INICIAR BACKEND (Laravel)
REM ============================================================
echo [4/5] Iniciando Backend (Laravel)...
cd /d "%~dp0backend"
start "BACKEND - Laravel API" cmd /k "color 0B && echo BACKEND CORRIENDO - NO CERRAR ESTA VENTANA && echo. && php artisan serve"
timeout /t 2 /nobreak >nul
echo       OK - Backend iniciado en http://localhost:8000

REM ============================================================
REM INICIAR FRONTEND (Vue)
REM ============================================================
echo [5/5] Iniciando Frontend (Vue)...
cd /d "%~dp0frontend"
start "FRONTEND - Vue + Vuetify" cmd /k "color 0E && echo FRONTEND CORRIENDO - NO CERRAR ESTA VENTANA && echo. && npm run dev"
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
echo   - NO cierres las ventanas que se abrieron (Backend y Frontend)
echo   - Para detener el sistema, cierra todas las ventanas
echo   - O ejecuta: DETENER_SISTEMA.bat
echo.
echo ========================================================================
echo.

REM Esperar 5 segundos y abrir el navegador automáticamente
timeout /t 5 /nobreak >nul
echo   Abriendo navegador...
start http://localhost:5173

echo.
echo   Puedes cerrar esta ventana ahora.
echo   El sistema seguira corriendo en las otras ventanas.
echo.
pause
