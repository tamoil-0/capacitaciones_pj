@echo off
title VERIFICAR SERVICIOS - PODER JUDICIAL DE PUNO
color 0B
mode con: cols=80 lines=20

echo.
echo ========================================================================
echo   VERIFICACION DE SERVICIOS
echo   Poder Judicial de Puno
echo ========================================================================
echo.

REM ============================================================
REM VERIFICAR APACHE (Manual - XAMPP)
REM ============================================================
echo [Apache - XAMPP Control Panel]
tasklist /FI "IMAGENAME eq httpd.exe" 2>NUL | find /I /N "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   Estado: CORRIENDO
) else (
    echo   Estado: DETENIDO - Iniciar desde XAMPP Control Panel
)
echo.

REM ============================================================
REM VERIFICAR MYSQL (Manual - XAMPP)
REM ============================================================
echo [MySQL - XAMPP Control Panel]
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   Estado: CORRIENDO
) else (
    echo   Estado: DETENIDO - Iniciar desde XAMPP Control Panel
)
echo.

REM ============================================================
REM VERIFICAR BACKEND (PHP)
REM ============================================================
echo [Backend - Laravel]
tasklist /FI "IMAGENAME eq php.exe" 2>NUL | find /I /N "php.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   Estado: CORRIENDO
    echo   URL: http://localhost:8000
) else (
    echo   Estado: DETENIDO - Ejecutar INICIAR_SISTEMA.bat
)
echo.

REM ============================================================
REM VERIFICAR FRONTEND (Node)
REM ============================================================
echo [Frontend - Vue]
tasklist /FI "IMAGENAME eq node.exe" 2>NUL | find /I /N "node.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   Estado: CORRIENDO
    echo   URL: http://localhost:5173
) else (
    echo   Estado: DETENIDO - Ejecutar INICIAR_SISTEMA.bat
)
echo.

echo ========================================================================
echo.
pause
