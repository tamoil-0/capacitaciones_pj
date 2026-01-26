@echo off
REM ════════════════════════════════════════════════════════
REM SCRIPT RÁPIDO PARA COMPILAR - MODO RÁPIDO
REM ════════════════════════════════════════════════════════

echo Compilando Sistema OMR...
pyinstaller Sistema_Calificacion_Examenes.spec --clean --noconfirm

REM Copiar logo al directorio dist
if exist "pj.jpg" (
    copy /Y "pj.jpg" "dist\pj.jpg" >nul
    echo ✓ Logo copiado
)

echo.
echo ✓ Listo! El .exe está en: dist\Sistema_Calificacion_Examenes.exe
pause
