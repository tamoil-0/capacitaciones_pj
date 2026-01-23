@echo off
title DETENER SISTEMA - PODER JUDICIAL DE PUNO
color 0C
mode con: cols=80 lines=20

echo.
echo ========================================================================
echo   DETENIENDO BACKEND Y FRONTEND
echo   Poder Judicial de Puno
echo ========================================================================
echo.

REM ============================================================
REM DETENER PROCESOS DE NODE (Frontend)
REM ============================================================
echo [1/2] Deteniendo Frontend (Vue)...
taskkill /F /IM node.exe >nul 2>&1
if errorlevel 1 (
    echo       INFO - Frontend no estaba corriendo
) else (
    echo       OK - Frontend detenido
)

REM ============================================================
REM DETENER PROCESOS DE PHP (Backend)
REM ============================================================
echo [2/2] Deteniendo Backend (Laravel)...
taskkill /F /IM php.exe >nul 2>&1
if errorlevel 1 (
    echo       INFO - Backend no estaba corriendo
) else (
    echo       OK - Backend detenido
)

echo.
echo ========================================================================
echo   BACKEND Y FRONTEND DETENIDOS
echo ========================================================================
echo.
echo   Apache y MySQL siguen corriendo en XAMPP.
echo   Para detenerlos, usa XAMPP Control Panel.
echo.
echo   Puedes iniciar nuevamente con: INICIAR_SISTEMA.bat
echo.
echo ========================================================================
echo.
pause
