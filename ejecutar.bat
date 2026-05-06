@echo off
title Conversor Profesional de Temperatura - Christian Lera
color 0A

echo ===============================================
echo    🌡️ CONVERSOR PROFESIONAL DE TEMPERATURA
echo ===============================================
echo.
echo Autor: Christian Lera
echo Version: 2.1.0
echo.
echo Iniciando la aplicacion...
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado en el sistema.
    echo.
    echo Por favor, instala Python desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

:: Mostrar versión de Python
echo [OK] Python detectado:
python --version
echo.

:: Verificar si tkinter está disponible
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Tkinter no esta disponible.
    echo En la mayoria de las instalaciones de Python, tkinter viene incluido.
    echo Si el problema persiste, reinstala Python con la opcion "tcl/tk" activada.
    echo.
    pause
    exit /b 1
)

echo [OK] Tkinter disponible
echo.
echo ===============================================
echo    🚀 Ejecutando el conversor...
echo ===============================================
echo.

:: Ejecutar el programa
python ConvertidorGrados.py

:: Si el programa cerró inesperadamente
if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion cerro inesperadamente.
    echo.
    pause
)

:: Si el programa cerró normalmente
echo.
echo ===============================================
echo    👋 Aplicacion cerrada correctamente
echo ===============================================
timeout /t 2 >nul