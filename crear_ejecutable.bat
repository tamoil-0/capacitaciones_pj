@echo off
echo =====================================================
echo   CREADOR DE EJECUTABLE - Sistema OCR Examenes
echo   Poder Judicial de Puno
echo =====================================================
echo.

REM Limpiar carpetas de builds anteriores
echo [1/4] Limpiando carpetas build y dist...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo       OK - Carpetas limpiadas

echo.
echo [2/4] Verificando PyInstaller...
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo       ERROR - PyInstaller no esta instalado
    echo       Instalar con: pip install pyinstaller
    pause
    exit /b 1
)
echo       OK - PyInstaller disponible

echo.
echo [3/4] Creando ejecutable... (esto puede tomar 2-3 minutos)
python -m PyInstaller --onefile --windowed ^
    --name="Sistema_Calificacion_Examenes" ^
    --add-data="poppler;poppler" ^
    --add-data="pj.jpg;." ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=customtkinter ^
    --hidden-import=pdf2image ^
    --hidden-import=reportlab ^
    --hidden-import=requests ^
    --collect-all customtkinter ^
    --exclude-module=torch ^
    --exclude-module=tensorflow ^
    --exclude-module=matplotlib ^
    --exclude-module=ultralytics ^
    --exclude-module=pygame ^
    --exclude-module=scipy ^
    --exclude-module=pandas ^
    --clean ^
    completo.py

if errorlevel 1 (
    echo       ERROR - Fallo la creacion del ejecutable
    pause
    exit /b 1
)
echo       OK - Ejecutable creado

echo.
echo [4/4] Copiando archivos de soporte...
copy /y api_client.py dist\ >nul 2>&1
if exist config.py copy /y config.py dist\ >nul 2>&1
copy /y pj.jpg dist\ >nul 2>&1
echo       OK - Archivos copiados

echo.
echo =====================================================
echo   COMPLETADO EXITOSAMENTE
echo =====================================================
echo.
echo Ejecutable creado en: dist\Sistema_Calificacion_Examenes.exe
echo.
echo Para distribuir:
echo   - Copiar toda la carpeta dist\ a la maquina destino
echo   - Incluye: .exe + api_client.py + config.py + pj.jpg + poppler\
echo.
dir dist\*.exe
echo.
pause
