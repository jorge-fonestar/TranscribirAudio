# TranscribirAudio

Aplicación para transcribir archivos de audio usando **Whisper de OpenAI** con detección automática de idioma.

## ✨ Características Principales

- **Detección automática de idioma**: Soporta inglés, chino, español y muchos más sin configuración
- **Audio multilingüe**: Maneja archivos con mezcla de idiomas (code-switching)
- **Compatibilidad de formatos**: Soporta WAV, MP3, M4A, FLAC, OGG, AAC, OPUS, WMA
- **Timestamps por segmento**: Cada línea de la transcripción incluye marca de tiempo inicio y fin
- **Procesamiento local**: No requiere conexión a internet (tras la descarga inicial del modelo)
- **Guardado automático**: La transcripción se guarda en archivos .txt
- **Procesamiento por lotes**: Puede procesar carpetas completas de archivos de audio

## 🎵 Recomendaciones de Audio
Preferible convertir los audios a WAV (mejor mono y a 44100 Hz) con Audacity para mejores resultados de transcripción.

## 📝 Uso del Resultado
Adjunta el resultado en ChatGPT con un prompt similar a este:
```
Resume el texto adjunto y redáctalo como acta de una reunión, hablando directamente de lo que se habló que tenga que ver con cada punto del orden del día:

Estos son los puntos y el minuto del audio en el que comienza a hablarse de ello:
+ Título del tema
```

## 🚀 Cómo usar la aplicación

1. **Ejecuta la aplicación** desde la línea de comandos
2. **Selecciona**: Elige un archivo de audio individual o una carpeta completa
3. **Espera**: Whisper procesará el audio automáticamente
4. **Resultado**: El archivo `_transcripcion.txt` se guarda junto al audio original

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

# Instalar PyTorch (CPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python transcribe_audio.py
```

### Requisito externo: ffmpeg
Whisper necesita `ffmpeg` instalado y en el PATH:
```powershell
# Con winget
winget install Gyan.FFmpeg

# O con chocolatey
choco install ffmpeg
```

## 📋 Dependencias
- **openai-whisper**: Motor de transcripción con detección automática de idioma
- **pydub 0.25.1**: Procesamiento y manipulación de audio
- **torch + torchaudio**: Backend de inferencia para Whisper
- **ffmpeg**: Requerido externamente para decodificación de audio

## 🧠 Modelo de Whisper

El script usa el modelo `small` por defecto (~461 MB). Se descarga automáticamente la primera vez.

| Modelo | Tamaño | Velocidad (CPU) | Precisión |
|--------|--------|-----------------|-----------|
| `tiny` | ~75 MB | Muy rápida | Básica |
| `base` | ~142 MB | Rápida | Buena |
| `small` | ~461 MB | Media | Muy buena |
| `medium` | ~1.5 GB | Lenta | Excelente |
| `large` | ~2.9 GB | Muy lenta | Máxima |

Para cambiar el modelo, edita la línea `modelo = whisper.load_model("small")` en `transcribe_audio.py`.

## ⚠️ Notas Técnicas

- **Python 3.13**: Totalmente compatible
- **Ejecución local**: No requiere conexión a internet una vez descargado el modelo
- **GPU opcional**: Funciona en CPU; con GPU NVIDIA (CUDA) es significativamente más rápido
- **Limpieza automática**: Los archivos temporales se eliminan automáticamente

## 📁 Archivos del Proyecto

- `transcribe_audio.py` - Aplicación principal de línea de comandos
- `requirements.txt` - Dependencias del proyecto
