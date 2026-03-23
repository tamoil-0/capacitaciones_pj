@echo off
chcp 65001 >nul
title Preparar Sistema para USB - Poder Judicial Puno
color 0A

echo.
echo ═══════════════════════════════════════════════════════════
echo  📦 PREPARACIÓN DEL SISTEMA PARA TRASLADAR POR USB
echo ═══════════════════════════════════════════════════════════
echo.
echo Este script preparará todo lo necesario para copiar a USB
echo.

:: 1. EXPORTAR BASE DE DATOS
echo [1/4] 📊 Exportando base de datos...
cd C:\xampp\mysql\bin
.\mysqldump.exe -u root capacitaciones > "%~dp0capacitaciones_BACKUP.sql"
if errorlevel 1 (
    echo ❌ Error al exportar la base de datos
    pause
    exit /b 1
)
echo ✅ Base de datos exportada: capacitaciones_BACKUP.sql
echo.

:: 2. CREAR CARPETA TEMPORAL PARA USB
echo [2/4] 📁 Creando carpeta para USB...
set "CARPETA_USB=%USERPROFILE%\Desktop\CAPACITACIONES_PARA_USB"
if exist "%CARPETA_USB%" rmdir /s /q "%CARPETA_USB%"
mkdir "%CARPETA_USB%"
echo.

:: 3. COPIAR ARCHIVOS
echo [3/4] 📋 Copiando archivos necesarios (esto puede tardar varios minutos)...
cd "%~dp0"

:: Crear archivos de exclusión temporal (solo excluir .git)
echo .git\ > "%TEMP%\exclude_backend.txt"
echo .gitignore >> "%TEMP%\exclude_backend.txt"
echo .gitattributes >> "%TEMP%\exclude_backend.txt"

echo .git\ > "%TEMP%\exclude_frontend.txt"
echo .gitignore >> "%TEMP%\exclude_frontend.txt"
echo .gitattributes >> "%TEMP%\exclude_frontend.txt"

:: Copiar archivos raíz
xcopy /Y /Q "*.bat" "%CARPETA_USB%\" >nul
xcopy /Y /Q "*.md" "%CARPETA_USB%\" >nul
xcopy /Y /Q "*.sql" "%CARPETA_USB%\" >nul
xcopy /Y /Q "*.py" "%CARPETA_USB%\" >nul
xcopy /Y /Q "*.html" "%CARPETA_USB%\" >nul
xcopy /Y /Q "*.txt" "%CARPETA_USB%\" >nul
xcopy /Y /Q "*.spec" "%CARPETA_USB%\" >nul

:: Copiar dist/ con el .exe
xcopy /E /I /Y /Q "dist" "%CARPETA_USB%\dist\" >nul

:: Copiar poppler
xcopy /E /I /Y /Q "poppler" "%CARPETA_USB%\poppler\" >nul

:: Copiar backend COMPLETO (con vendor porque la otra PC no tiene Composer)
echo    - Copiando backend (esto puede tardar, incluye todas las librerías)...
xcopy /E /I /Y /Q "backend" "%CARPETA_USB%\backend\" /EXCLUDE:%TEMP%\exclude_backend.txt >nul

:: Copiar frontend COMPLETO (con node_modules porque la otra PC no tiene Node.js)
echo    - Copiando frontend (esto puede tardar, incluye todas las librerías)...
xcopy /E /I /Y /Q "frontend" "%CARPETA_USB%\frontend\" /EXCLUDE:%TEMP%\exclude_frontend.txt >nul

echo ✅ Archivos copiados
echo.

:: 4. CREAR INSTRUCCIONES
echo [4/4] 📝 Creando instrucciones...
(
echo ═══════════════════════════════════════════════════════════
echo  INSTRUCCIONES DE INSTALACIÓN EN LA OTRA COMPUTADORA
echo ═══════════════════════════════════════════════════════════
echo.
echo REQUISITOS:
echo - XAMPP 8.2 instalado en C:\xampp82 o C:\xampp
echo - NADA MÁS ^(todo viene incluido^)
echo.
echo ═══════════════════════════════════════════════════════════
echo ⚠️  PASO 1: CONFIGURAR PHP.INI ^(MUY IMPORTANTE^)
echo ═══════════════════════════════════════════════════════════
echo.
echo Seguir TODOS los pasos del archivo: CONFIGURAR_PHP_INI.txt
echo.
echo Resumen rápido:
echo   1. Abrir XAMPP - Config - PHP ^(php.ini^)
echo   2. Buscar y QUITAR ; de estas extensiones:
echo      extension=zip, gd, mbstring, xml, curl, fileinfo
echo   3. Cambiar: memory_limit = 512M
echo   4. Guardar y reiniciar Apache
echo.
echo ═══════════════════════════════════════════════════════════
echo PASO 2: COPIAR ARCHIVOS
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Copiar toda esta carpeta a: C:\xampp\htdocs\
echo    ^(o C:\xampp82\htdocs\ si usas XAMPP 8.2^)
echo    ^(debe quedar: C:\xampp\htdocs\capacitaciones_pj\^)
echo    NOTA: Puede tardar varios minutos, son muchos archivos.
echo.
echo ═══════════════════════════════════════════════════════════
echo PASO 3: INICIAR SERVICIOS
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Abrir XAMPP Control Panel
echo 2. Clic en Start para:
echo    ✅ Apache
echo    ✅ MySQL
echo.
echo ═══════════════════════════════════════════════════════════
echo PASO 4: CREAR BASE DE DATOS
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Abrir en navegador: http://localhost/phpmyadmin
echo 2. Clic en "Nueva" ^(izquierda^)
echo 3. Nombre de la base: capacitaciones
echo 4. Clic en "Crear"
echo 5. Clic en "Importar" ^(arriba^)
echo 6. Seleccionar archivo: capacitaciones_BACKUP.sql
echo 7. Clic en "Continuar" ^(abajo^)
echo.
echo 4. Ejecutar el sistema:
echo    - Doble clic en: INICIAR_SISTEMA.bat
echo    - Se abrirán 2 ventanas negras ^(NO CERRAR^)
echo    - Se abrirá automáticamente el navegador
echo.
echo 5. Acceso al sistema web:
echo    - Usuario: pjudicial
echo    - Contraseña: Corte2026
echo.
echo 6. Sistema de Calificaciones ^(OCR para examenes^):
echo    - Ir a carpeta: dist\
echo    - Doble clic en: Sistema_Calificacion_Examenes.exe
echo    - Puede crear acceso directo en el escritorio
echo.
echo ═══════════════════════════════════════════════════════════
echo  SOLUCIÓN DE PROBLEMAS
echo ═══════════════════════════════════════════════════════════
echo.
echo Si el sistema no abre:
echo 1. Verificar que Apache y MySQL estén en verde en XAMPP
echo 2. Verificar que importaste la base de datos
echo 3. Ejecutar nuevamente: INICIAR_SISTEMA.bat
echo.
echo ═══════════════════════════════════════════════════════════
echo  IMPORTANTE: Guardar estas instrucciones
echo ═══════════════════════════════════════════════════════════
) > "%CARPETA_USB%\INSTRUCCIONES_INSTALACION.txt"

echo ✅ Instrucciones creadas
echo.
echo ═══════════════════════════════════════════════════════════
echo  ✅ TODO LISTO PARA COPIAR AL USB
echo ═══════════════════════════════════════════════════════════
echo.
echo 📁 Carpeta preparada en:
echo    %CARPETA_USB%
echo.
echo 📋 Contenido preparado:
echo    ✅ Todos los archivos del sistema
echo    ✅ Base de datos: capacitaciones_BACKUP.sql
echo    ✅ Ejecutable: dist\Sistema_Calificacion_Examenes.exe
echo    ✅ Scripts .bat para iniciar el sistema
echo    ✅ Instrucciones de instalación
echo.
echo 💾 SIGUIENTE PASO:
echo    1. Copiar TODO lo que está en el escritorio a tu USB
echo    2. Llevar el USB a la otra computadora
echo    3. Seguir las instrucciones en: INSTRUCCIONES_INSTALACION.txt
echo.
echo ═══════════════════════════════════════════════════════════
pause
