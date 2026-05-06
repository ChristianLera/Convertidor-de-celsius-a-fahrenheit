# Conversor Profesional de Temperatura
# Autor: Christian Lera
# Versión: 2.1.0

# Configurar la ventana de PowerShell
$Host.UI.RawUI.WindowTitle = "Conversor Profesional de Temperatura - Christian Lera"
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "   🌡️ CONVERSOR PROFESIONAL DE TEMPERATURA" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Autor: Christian Lera" -ForegroundColor Green
Write-Host "Versión: 2.1.0" -ForegroundColor Green
Write-Host ""
Write-Host "Iniciando la aplicación..." -ForegroundColor White
Write-Host ""

# Función para verificar si Python está instalado
function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "[OK] Python detectado: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[ERROR] Python no está instalado en el sistema." -ForegroundColor Red
        Write-Host ""
        Write-Host "Por favor, instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "Asegúrate de marcar 'Add Python to PATH' durante la instalación." -ForegroundColor Yellow
        return $false
    }
}

# Función para verificar tkinter
function Test-TkinterAvailability {
    try {
        $tkinterTest = python -c "import tkinter; print('Tkinter disponible')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Tkinter disponible" -ForegroundColor Green
            return $true
        }
        else {
            throw "Tkinter no disponible"
        }
    }
    catch {
        Write-Host "[ERROR] Tkinter no está disponible." -ForegroundColor Red
        Write-Host "En la mayoría de las instalaciones de Python, tkinter viene incluido." -ForegroundColor Yellow
        Write-Host "Si el problema persiste, reinstala Python con la opción 'tcl/tk' activada." -ForegroundColor Yellow
        return $false
    }
}

# Función para verificar el archivo principal
function Test-MainFile {
    if (Test-Path "ConvertidorGrados.py") {
        Write-Host "[OK] Archivo principal encontrado: ConvertidorGrados.py" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "[ERROR] No se encuentra el archivo ConvertidorGrados.py" -ForegroundColor Red
        Write-Host "Asegúrate de ejecutar este script en la misma carpeta que contiene el programa." -ForegroundColor Yellow
        return $false
    }
}

# Función para mostrar historial de conversiones
function Show-HistoryFile {
    if (Test-Path "historial_tkinter.json") {
        $fileInfo = Get-Item "historial_tkinter.json"
        Write-Host "[INFO] Archivo de historial encontrado - Tamaño: $([math]::Round($fileInfo.Length/1KB, 2)) KB" -ForegroundColor Cyan
    }
    else {
        Write-Host "[INFO] Aún no hay historial. Se creará uno nuevo al realizar conversiones." -ForegroundColor Cyan
    }
}

# Ejecutar verificaciones
$pythonOk = Test-PythonInstallation
if (-not $pythonOk) {
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
$tkinterOk = Test-TkinterAvailability
if (-not $tkinterOk) {
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
$mainFileOk = Test-MainFile
if (-not $mainFileOk) {
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Show-HistoryFile

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "   🚀 Ejecutando el conversor..." -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

try {
    # Ejecutar el programa
    python ConvertidorGrados.py
    
    # Verificar si hubo error
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERROR] La aplicación cerró inesperadamente." -ForegroundColor Red
        Write-Host ""
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    else {
        Write-Host ""
        Write-Host "===============================================" -ForegroundColor Green
        Write-Host "   👋 Aplicación cerrada correctamente" -ForegroundColor Green
        Write-Host "===============================================" -ForegroundColor Green
        Start-Sleep -Seconds 2
    }
}
catch {
    Write-Host ""
    Write-Host "[ERROR] Error al ejecutar la aplicación: $_" -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}