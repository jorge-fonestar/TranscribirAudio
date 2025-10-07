import speech_recognition as sr
from pydub import AudioSegment
import os

# Función para dividir el audio en segmentos de 1 minuto (60,000 ms)
def dividir_audio(audio, duracion_segmento_ms=60000):
    duracion_audio = len(audio)
    segmentos = []
    for i in range(0, duracion_audio, duracion_segmento_ms):
        segmento = audio[i:i+duracion_segmento_ms]
        segmentos.append(segmento)
    return segmentos

# Función para transcribir un archivo individual, adaptada para Kivy/Android
def transcribir_archivo_kivy(ruta_archivo_audio):
    """Versión original de transcripción sin callback"""
    try:
        nombre_archivo = os.path.basename(ruta_archivo_audio)
        directorio_padre = os.path.dirname(ruta_archivo_audio)
        audio = AudioSegment.from_file(ruta_archivo_audio)
        audio = audio.set_channels(1).set_frame_rate(16000)
        segmentos = dividir_audio(audio, 30000)
        total_segmentos = len(segmentos)
        reconocedor = sr.Recognizer()
        nombre_base = os.path.splitext(nombre_archivo)[0]
        nombre_archivo_transcripcion = nombre_base + "_transcripcion.txt"
        ruta_archivo_transcripcion = os.path.join(directorio_padre, nombre_archivo_transcripcion)
        with open(ruta_archivo_transcripcion, "w", encoding="utf-8") as f:
            f.write("")
        resultado = []
        for idx in range(total_segmentos):
            segmento = segmentos[idx]
            nombre_archivo_segmento = f"segmento_{idx}.wav"
            segmento.export(nombre_archivo_segmento, format="wav")
            with sr.AudioFile(nombre_archivo_segmento) as source:
                audio_segmento = reconocedor.record(source)
            try:
                texto_segmento = reconocedor.recognize_google(audio_segmento, language="es-ES")
                segundo = idx * 30
                segundo_str = f"{segundo // 3600:02}:{(segundo % 3600) // 60:02}:{segundo % 60:02}"
                resultado.append(f"{segundo_str} -> {texto_segmento}")
                with open(ruta_archivo_transcripcion, "a", encoding="utf-8") as f:
                    f.write(f"{segundo_str} -> {texto_segmento}\n")
            except sr.UnknownValueError:
                resultado.append(f"{segundo_str} -> [No se pudo entender el segmento]")
            except sr.RequestError as e:
                resultado.append(f"{segundo_str} -> [Error de servicio: {e}]")
            os.remove(nombre_archivo_segmento)
        return "\n".join(resultado)
    except Exception as e:
        return f"Error al procesar el archivo {ruta_archivo_audio}: {e}"

# Función mejorada con callback para mostrar progreso
def transcribir_archivo_kivy_mejorado(ruta_archivo_audio, segmento_inicio=0, callback=None):
    """
    Versión mejorada con callback para mostrar progreso en tiempo real
    
    Args:
        ruta_archivo_audio: Ruta del archivo a transcribir
        segmento_inicio: Índice del segmento desde donde comenzar (base 0)
        callback: Función para recibir actualizaciones de progreso
    """
    def log(mensaje):
        """Función auxiliar para logging"""
        if callback:
            callback(mensaje)
    
    try:
        nombre_archivo = os.path.basename(ruta_archivo_audio)
        directorio_padre = os.path.dirname(ruta_archivo_audio)
        
        log(f"Cargando archivo: {nombre_archivo}")
        
        # Cargar y procesar el audio
        audio = AudioSegment.from_file(ruta_archivo_audio)
        log(f"Duración original: {len(audio)/1000:.1f} segundos")
        
        audio = audio.set_channels(1).set_frame_rate(16000)
        log("Audio convertido a mono, 16kHz")
        
        # Dividir en segmentos
        segmentos = dividir_audio(audio, 30000)  # 30 segundos por segmento
        total_segmentos = len(segmentos)
        
        log(f"Audio dividido en {total_segmentos} segmentos de 30 segundos")
        
        if segmento_inicio >= total_segmentos:
            raise ValueError(f"Segmento inicial {segmento_inicio + 1} supera el total de {total_segmentos}")
        
        if segmento_inicio > 0:
            log(f"Comenzando desde el segmento {segmento_inicio + 1} de {total_segmentos}")
        
        # Preparar reconocedor
        reconocedor = sr.Recognizer()
        
        # Crear archivo de transcripción
        nombre_base = os.path.splitext(nombre_archivo)[0]
        nombre_archivo_transcripcion = nombre_base + "_transcripcion.txt"
        ruta_archivo_transcripcion = os.path.join(directorio_padre, nombre_archivo_transcripcion)
        
        with open(ruta_archivo_transcripcion, "w", encoding="utf-8") as f:
            f.write(f"Transcripción de: {nombre_archivo}\n")
            f.write(f"Comenzando desde segmento: {segmento_inicio + 1}\n")
            f.write("=" * 50 + "\n\n")
        
        log(f"Archivo de transcripción creado: {nombre_archivo_transcripcion}")
        
        resultado = []
        segmentos_procesados = 0
        
        # Procesar segmentos desde el índice especificado
        for idx in range(segmento_inicio, total_segmentos):
            segmento = segmentos[idx]
            nombre_archivo_segmento = f"segmento_{idx}.wav"
            
            segundo = idx * 30
            segundo_str = f"{segundo // 3600:02}:{(segundo % 3600) // 60:02}:{segundo % 60:02}"
            
            progreso = ((idx - segmento_inicio + 1) / (total_segmentos - segmento_inicio)) * 100
            log(f"[{progreso:.1f}%] Procesando segmento {idx + 1}/{total_segmentos} ({segundo_str})")
            
            try:
                # Exportar segmento temporal
                segmento.export(nombre_archivo_segmento, format="wav")
                
                # Transcribir segmento
                with sr.AudioFile(nombre_archivo_segmento) as source:
                    audio_segmento = reconocedor.record(source)
                
                try:
                    texto_segmento = reconocedor.recognize_google(audio_segmento, language="es-ES")
                    linea_resultado = f"{segundo_str} -> {texto_segmento}"
                    resultado.append(linea_resultado)
                    
                    # Guardar en archivo
                    with open(ruta_archivo_transcripcion, "a", encoding="utf-8") as f:
                        f.write(linea_resultado + "\n")
                    
                    log(f"✓ Segmento {idx + 1}: {texto_segmento[:50]}{'...' if len(texto_segmento) > 50 else ''}")
                    
                except sr.UnknownValueError:
                    linea_resultado = f"{segundo_str} -> [No se pudo entender el segmento]"
                    resultado.append(linea_resultado)
                    with open(ruta_archivo_transcripcion, "a", encoding="utf-8") as f:
                        f.write(linea_resultado + "\n")
                    log(f"⚠ Segmento {idx + 1}: No se pudo entender")
                    
                except sr.RequestError as e:
                    linea_resultado = f"{segundo_str} -> [Error de servicio: {e}]"
                    resultado.append(linea_resultado)
                    with open(ruta_archivo_transcripcion, "a", encoding="utf-8") as f:
                        f.write(linea_resultado + "\n")
                    log(f"✗ Segmento {idx + 1}: Error de servicio - {e}")
                
                # Limpiar archivo temporal
                if os.path.exists(nombre_archivo_segmento):
                    os.remove(nombre_archivo_segmento)
                
                segmentos_procesados += 1
                
            except Exception as e:
                log(f"✗ Error procesando segmento {idx + 1}: {e}")
                if os.path.exists(nombre_archivo_segmento):
                    os.remove(nombre_archivo_segmento)
                continue
        
        log(f"Transcripción completada: {segmentos_procesados} segmentos procesados")
        log(f"Archivo guardado en: {ruta_archivo_transcripcion}")
        
        return "\n".join(resultado)
        
    except Exception as e:
        error_msg = f"Error al procesar el archivo {ruta_archivo_audio}: {e}"
        log(f"✗ {error_msg}")
        return error_msg
