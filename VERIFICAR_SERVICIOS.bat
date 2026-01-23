@echo off
title VERIFICAR SERVICIOS - PODER JUDICIAL DE PUNO
color 0B
mode con: cols=80 lines=25

echo.
echo ========================================================================
echo   VERIFICACION DE SERVICIOS
echo   Poder Judicial de Puno
echo ========================================================================
echo.

REM ============================================================
REM VERIFICAR APACHE
REM ============================================================
echo [Apache]
tasklist /FI "IMAGENAME eq httpd.exe" 2>NUL | find /I /N "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   Estado: CORRIENDO
    echo   Puerto: 80
) else (
    echo   Estado: DETENIDO
)
echo.

REM ============================================================
REM VERIFICAR MYSQL
REM ============================================================
echo [MySQL]
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   Estado: CORRIENDO
    echo   Puerto: 3306
) else (
    echo   Estado: DETENIDO
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
    echo   Estado: DETENIDO
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
    echo   Estado: DETENIDO
)
echo.

echo ========================================================================
echo.
echo   Si algun servicio esta DETENIDO, ejecuta: INICIAR_SISTEMA.bat
echo.
echo ========================================================================
echo.
pause
