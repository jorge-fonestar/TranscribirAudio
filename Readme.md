# TranscribirAudio - Interfaz Gráfica con Tkinter

Aplicación para transcribir archivos de audio usando reconocimiento de voz con una interfaz gráfica moderna y intuitiva usando Tkinter.

## ✨ Características Principales

### Interfaz Moderna con Tkinter
- **Selector de archivos integrado**: Botón directo para seleccionar archivos de audio
- **Filtros de archivo automáticos**: Solo muestra archivos de audio compatibles (WAV, MP3, M4A, FLAC, OGG, AAC)
- **Información detallada del archivo**: Muestra tamaño, duración, segmentos, canales y frecuencia
- **Configuración flexible**: Permite elegir desde qué segmento comenzar la transcripción

### Progreso en Tiempo Real
- **Barra de progreso visual**: Indica el porcentaje de completado
- **Log en tiempo real**: Muestra el estado de cada segmento procesado
- **Información detallada**: Estado de éxito/error de cada segmento
- **Controles de transcripción**: Botones para cancelar o ver resultado

### Funcionalidades Avanzadas
- **Procesamiento en segundo plano**: La interfaz no se bloquea durante la transcripción
- **Ventana de resultados dedicada**: Muestra el resultado final en una ventana separada
- **Copiado al portapapeles**: Botón para copiar el resultado fácilmente
- **Guardado de archivos**: Permite guardar la transcripción en un archivo .txt
- **Cancelación de proceso**: Opción para cancelar la transcripción en cualquier momento

### Diseño Profesional
- **Tema oscuro**: Interfaz moderna con colores oscuros
- **Tipografía legible**: Fuentes optimizadas para lectura
- **Organización por secciones**: Layout claro y organizado
- **Iconos descriptivos**: Emojis para mejor identificación visual

## 🎵 Recomendaciones de Audio
Preferible convertir los audios a WAV (Mejor mono y a 44100 Hz) con Audacity para mejores resultados de transcripción.

## 📝 Uso del Resultado
Adjunta el resultado en ChatGPT con un prompt similar a este:
```
Resume el texto adjunto y redáctalo como acta de una reunión, hablando directamente de lo que se habló que tenga que ver con cada punto del orden del día: 

Estos son los puntos y el minuto del audio en el que comienza a hablarse de ello:
+ Título del tema
```

## 🚀 Cómo usar la aplicación

1. **Ejecuta la aplicación** (ver opciones de ejecución más abajo)
2. **Selecciona un archivo**: Haz clic en "📁 Seleccionar archivo de audio"
3. **Revisa la información**: Verifica los datos del archivo (duración, segmentos, etc.)
4. **Configura el inicio** (opcional): 
   - Ingresa el número del segmento desde donde empezar
   - Deja vacío para empezar desde el inicio
5. **Inicia la transcripción**: Haz clic en "🚀 Comenzar Transcripción"
6. **Observa el progreso**: Sigue el progreso en tiempo real en el log
7. **Revisa el resultado**: Al finalizar, haz clic en "✅ Ver Resultado"

## 🔧 Opciones de Ejecución

### Opción 1: Compilar ejecutable (Recomendado)
1. Haz doble clic en `compilar_tkinter.bat`
2. El script automáticamente:
   - Creará el entorno virtual `.venv_new`
   - Instalará todas las dependencias
   - Compilará el ejecutable
3. Ejecuta `dist/TranscribirAudio_Tkinter.exe`

### Opción 2: Ejecutar directamente (Desarrollo)
```powershell
# Activar entorno virtual (si existe)
.venv_new\Scripts\Activate.ps1

# Instalar dependencias si es necesario
pip install -r requirements.txt

# Ejecutar aplicación
python main_tkinter.py
```

### Opción 3: Manual
```powershell
# Crear entorno virtual
python -m venv .venv_new

# Activar entorno
.venv_new\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Compilar (opcional)
pyinstaller --clean TranscribirAudio_Tkinter.spec

# O ejecutar directamente
python main_tkinter.py
```

## 📋 Dependencias
- **SpeechRecognition 3.10.0**: Reconocimiento de voz con Google Speech API
- **pydub 0.25.1**: Procesamiento y manipulación de audio
- **PyInstaller 5.13.2**: Generación de ejecutables standalone
- **Tkinter**: Interfaz gráfica (incluido con Python)

## 🎯 Flujo Completo de la Aplicación

1. **Inicio**: Interfaz principal con selector de archivos
2. **Análisis**: Al seleccionar un archivo, se analiza automáticamente
3. **Configuración**: Opción para elegir segmento de inicio
4. **Procesamiento**: Transcripción con progreso en tiempo real
5. **Resultado**: Ventana dedicada con opciones de copia y guardado

## ⚠️ Notas Técnicas

- **Segmentación**: Procesa audio en segmentos de 30 segundos
- **Compatibilidad**: Soporta múltiples formatos de audio
- **Limpieza automática**: Los archivos temporales se eliminan automáticamente
- **Guardado automático**: La transcripción se guarda también como archivo .txt
- **Conectividad**: Requiere conexión a internet para Google Speech Recognition
- **Tkinter nativo**: No requiere dependencias gráficas adicionales

## 📁 Archivos del Proyecto

- `main_tkinter.py` - Aplicación principal con interfaz Tkinter
- `transcribe_audio_kivy.py` - Funciones de transcripción con callback
- `requirements.txt` - Dependencias del proyecto
- `TranscribirAudio_Tkinter.spec` - Configuración de PyInstaller
- `compilar_tkinter.bat` - Script automático de compilación
