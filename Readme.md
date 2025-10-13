# TranscribirAudio

Aplicación para transcribir archivos de audio usando reconocimiento de voz.

## ✨ Características Principales

- **Compatibilidad de formatos**: Soporta WAV, MP3, M4A, FLAC, OGG, AAC
- **Procesamiento por segmentos**: Divide el audio en segmentos de 30 segundos para mejor precisión
- **Guardado automático**: La transcripción se guarda en archivos .txt
- **Progreso en tiempo real**: Muestra el estado de cada segmento procesado
- **Compatibilidad Python 3.13**: Totalmente compatible con la última versión de Python

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

1. **Ejecuta la aplicación** desde la línea de comandos
2. **Selecciona un archivo**: Cuando se abra el diálogo, elige tu archivo de audio
3. **Observa el progreso**: La aplicación procesará el audio por segmentos
4. **Resultado**: Al finalizar, encontrarás el archivo de transcripción guardado automáticamente

## 🔧 Opciones de Ejecución

### Opción 1: Ejecutar directamente
```powershell
# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Ejecutar aplicación
python transcribe_audio.py
```

### Opción 2: Configuración desde cero
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python transcribe_audio.py
```

## 📋 Dependencias
- **SpeechRecognition 3.14.3**: Reconocimiento de voz con Google Speech API (Compatible con Python 3.13)
- **pydub 0.25.1**: Procesamiento y manipulación de audio
- **PyInstaller 6.16.0**: Generación de ejecutables standalone (Compatible con Python 3.13)

## 🎯 Flujo Completo de la Aplicación

1. **Inicio**: Ejecutar el script desde línea de comandos
2. **Selección**: Diálogo para seleccionar archivo de audio
3. **Análisis**: El archivo se analiza y divide en segmentos
4. **Procesamiento**: Transcripción segmento por segmento con progreso en tiempo real
5. **Resultado**: Archivo de texto guardado automáticamente

## ⚠️ Notas Técnicas

- **Python 3.13**: Totalmente compatible con Python 3.13.5 (incluye módulos de compatibilidad)
- **Segmentación**: Procesa audio en segmentos de 30 segundos
- **Compatibilidad**: Soporta múltiples formatos de audio (WAV, MP3, M4A, FLAC, OGG, AAC)
- **Limpieza automática**: Los archivos temporales se eliminan automáticamente
- **Guardado automático**: La transcripción se guarda como archivo .txt
- **Conectividad**: Requiere conexión a internet para Google Speech Recognition

## 📁 Archivos del Proyecto

- `transcribe_audio.py` - Aplicación principal de línea de comandos
- `requirements.txt` - Dependencias del proyecto
