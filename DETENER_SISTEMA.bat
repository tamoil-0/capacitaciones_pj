@echo off
title DETENER SISTEMA - PODER JUDICIAL DE PUNO
color 0C
mode con: cols=80 lines=20

echo.
echo ========================================================================
echo   DETENIENDO SISTEMA DE ASISTENCIAS
echo   Poder Judicial de Puno
echo ========================================================================
echo.

REM ============================================================
REM DETENER PROCESOS DE NODE (Frontend)
REM ============================================================
echo [1/4] Deteniendo Frontend (Vue)...
taskkill /F /IM node.exe >nul 2>&1
if errorlevel 1 (
    echo       INFO - Frontend no estaba corriendo
) else (
    echo       OK - Frontend detenido
)

REM ============================================================
REM DETENER PROCESOS DE PHP (Backend)
REM ============================================================
echo [2/4] Deteniendo Backend (Laravel)...
taskkill /F /IM php.exe >nul 2>&1
if errorlevel 1 (
    echo       INFO - Backend no estaba corriendo
) else (
    echo       OK - Backend detenido
)

REM ============================================================
REM DETENER APACHE
REM ============================================================
echo [3/4] Deteniendo Apache...
if exist "C:\xampp82\apache\bin\httpd.exe" (
    C:\xampp82\apache\bin\httpd.exe -k stop >nul 2>&1
) else if exist "C:\xampp\apache\bin\httpd.exe" (
    C:\xampp\apache\bin\httpd.exe -k stop >nul 2>&1
)
timeout /t 2 /nobreak >nul
echo       OK - Apache detenido

REM ============================================================
REM DETENER MYSQL
REM ============================================================
echo [4/4] Deteniendo MySQL...
if exist "C:\xampp82\mysql\bin\mysqladmin.exe" (
    C:\xampp82\mysql\bin\mysqladmin.exe -u root shutdown >nul 2>&1
) else if exist "C:\xampp\mysql\bin\mysqladmin.exe" (
    C:\xampp\mysql\bin\mysqladmin.exe -u root shutdown >nul 2>&1
)
timeout /t 2 /nobreak >nul
echo       OK - MySQL detenido

echo.
echo ========================================================================
echo   SISTEMA DETENIDO CORRECTAMENTE
echo ========================================================================
echo.
echo   Todos los servicios han sido detenidos.
echo   Puedes iniciar nuevamente con: INICIAR_SISTEMA.bat
echo.
echo ========================================================================
echo.
pause
