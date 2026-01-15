@echo off
REM ════════════════════════════════════════════════════════
REM SCRIPT RÁPIDO PARA COMPILAR - MODO RÁPIDO
REM ════════════════════════════════════════════════════════

echo Compilando Sistema OMR...
pyinstaller Sistema_Calificacion_Examenes.spec --clean --noconfirm
echo.
echo ✓ Listo! El .exe está en: dist\Sistema_Calificacion_Examenes.exe
pause
