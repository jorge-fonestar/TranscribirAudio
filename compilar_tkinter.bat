@echo off
echo ========================================
echo  Compilador de TranscribirAudio (Tkinter) para Windows
echo ========================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo.
echo Activando entorno virtual...
if not exist .venv_new (
    echo Creando entorno virtual...
    python -m venv .venv_new
    if errorlevel 1 (
        echo Error: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

call .venv_new\Scripts\activate.bat
if errorlevel 1 (
    echo Error: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo.
echo Actualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo Limpiando compilaciones anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo.
echo ========================================
echo  COMPILANDO APLICACION (TKINTER)...
echo ========================================
pyinstaller --clean TranscribirAudio_Tkinter.spec
if errorlevel 1 (
    echo Error: Falló la compilación
    pause
    exit /b 1
)

echo.
if exist dist\TranscribirAudio_Tkinter.exe (
    echo ========================================
    echo  COMPILACION EXITOSA!
    echo ========================================
    echo El ejecutable está en: dist\TranscribirAudio_Tkinter.exe
    echo.
    dir dist\TranscribirAudio_Tkinter.exe
    echo.
    echo ¿Deseas ejecutar la aplicación ahora? (S/N)
    set /p runApp=
    if /i "%runApp%"=="S" (
        start "" "dist\TranscribirAudio_Tkinter.exe"
    )
    echo.
    echo ¿Deseas abrir la carpeta de distribución? (S/N)
    set /p openFolder=
    if /i "%openFolder%"=="S" (
        explorer dist
    )
) else (
    echo ========================================
    echo  ERROR EN LA COMPILACION
    echo ========================================
    echo No se encontró el ejecutable. Revisa los mensajes de error arriba.
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul