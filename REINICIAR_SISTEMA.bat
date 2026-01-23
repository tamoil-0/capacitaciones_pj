@echo off
title REINICIAR SISTEMA - PODER JUDICIAL DE PUNO
color 0E

echo.
echo ========================================================================
echo   REINICIANDO SISTEMA DE ASISTENCIAS
echo   Poder Judicial de Puno
echo ========================================================================
echo.
echo   Esto detenera y volvera a iniciar todos los servicios...
echo.

REM Detener todo
call DETENER_SISTEMA.bat

echo.
echo   Esperando 5 segundos antes de reiniciar...
timeout /t 5 /nobreak >nul

REM Iniciar todo
call INICIAR_SISTEMA.bat
