@echo off
REM ════════════════════════════════════════════════════════
REM SCRIPT PARA COMPILAR A .EXE - SISTEMA OMR
REM ════════════════════════════════════════════════════════

echo ════════════════════════════════════════════════════════
echo COMPILANDO SISTEMA OMR A .EXE
echo ════════════════════════════════════════════════════════
echo.

echo [1/5] Limpiando compilaciones anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
echo      ✓ Carpetas limpiadas
echo.

echo [2/5] Verificando Python...
python --version
if errorlevel 1 (
    echo      ✗ ERROR: Python no encontrado
    pause
    exit /b 1
)
echo      ✓ Python OK
echo.

echo [3/5] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo      ✗ ERROR al instalar dependencias
    pause
    exit /b 1
)
echo      ✓ Dependencias instaladas
echo.

echo [4/5] Compilando con PyInstaller...
pyinstaller Sistema_Calificacion_Examenes.spec
if errorlevel 1 (
    echo      ✗ ERROR en la compilación
    pause
    exit /b 1
)
echo      ✓ Compilación exitosa
echo.

echo [5/5] Verificando archivos generados...
if exist "dist\Sistema_Calificacion_Examenes.exe" (
    echo      ✓ EXE creado: dist\Sistema_Calificacion_Examenes.exe
) else (
    echo      ✗ ERROR: EXE no encontrado
    pause
    exit /b 1
)

REM Copiar logo al directorio dist
if exist "pj.jpg" (
    copy /Y "pj.jpg" "dist\pj.jpg" >nul
    echo      ✓ Logo copiado a dist\
) else (
    echo      ⚠ Logo pj.jpg no encontrado
)
echo.

echo ════════════════════════════════════════════════════════
echo ✓ COMPILACIÓN COMPLETADA EXITOSAMENTE
echo ════════════════════════════════════════════════════════
echo.
echo El ejecutable está en: dist\Sistema_Calificacion_Examenes.exe
echo.
echo IMPORTANTE: Para usar en otra máquina, necesitas copiar:
echo   1. Sistema_Calificacion_Examenes.exe
echo   2. La carpeta _internal (que está junto al .exe)
echo   3. pj.jpg (logo institucional)
echo.
pause
