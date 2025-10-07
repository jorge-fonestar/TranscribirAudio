import speech_recognition as sr
from pydub import AudioSegment
import os
import tkinter as tk
from tkinter import filedialog, messagebox


# Función para dividir el audio en segmentos de 1 minuto (60,000 ms)
def dividir_audio(audio, duracion_segmento_ms=60000):
    duracion_audio = len(audio)
    segmentos = []
    
    
    # Iterar sobre el audio en incrementos de 1 minuto
    for i in range(0, duracion_audio, duracion_segmento_ms):
        segmento = audio[i:i+duracion_segmento_ms]
        segmentos.append(segmento)
    
    return segmentos

# Función para transcribir un archivo individual
def transcribir_archivo(ruta_archivo_audio, preguntar_segmento=True):
    """
    Transcribe un archivo de audio individual
    """
    try:
        # Obtener el nombre del archivo sin la ruta
        nombre_archivo = os.path.basename(ruta_archivo_audio)
        directorio_padre = os.path.dirname(ruta_archivo_audio)
        
        print(f"Procesando archivo: {nombre_archivo}")
        
        # Cargar el archivo de audio
        audio = AudioSegment.from_file(ruta_archivo_audio)

        # Convertir a monofónico y cambiar la tasa de muestreo a 16000Hz
        audio = audio.set_channels(1).set_frame_rate(16000)

        # Dividir el audio en segmentos de 30 segundos
        segmentos = dividir_audio(audio, 30000)
        
        # Calcular el total de segmentos
        total_segmentos = len(segmentos)
        duracion_total = len(audio) / 1000  # duración en segundos
        
        print(f"Archivo cargado:")
        print(f"  - Duración total: {duracion_total/60:.1f} minutos ({duracion_total:.0f} segundos)")
        print(f"  - Total de segmentos de 30s: {total_segmentos}")
        
        # Preguntar desde qué segmento empezar solo si se especifica
        segmento_inicio = 0
        if preguntar_segmento:
            respuesta = input(f"\n¿Desde qué segmento quiere empezar? (1-{total_segmentos}, o Enter para empezar desde el primero): ").strip()
            
            if respuesta:
                try:
                    segmento_inicio = int(respuesta) - 1  # Convertir a índice base 0
                    if segmento_inicio < 0 or segmento_inicio >= total_segmentos:
                        print(f"Número inválido. Empezando desde el segmento 1.")
                        segmento_inicio = 0
                    else:
                        print(f"Empezando desde el segmento {segmento_inicio + 1}")
                except ValueError:
                    print("Entrada inválida. Empezando desde el segmento 1.")
                    segmento_inicio = 0

        # Inicializa el reconocedor de voz
        reconocedor = sr.Recognizer()

        # Nombre del archivo de salida para la transcripción
        nombre_base = os.path.splitext(nombre_archivo)[0]
        nombre_archivo_transcripcion = nombre_base + "_transcripcion.txt"
        ruta_archivo_transcripcion = os.path.join(directorio_padre, nombre_archivo_transcripcion)

        # Determinar si es una continuación o un inicio nuevo
        if segmento_inicio == 0:
            # Asegurarse de que el archivo de transcripción esté vacío al principio
            with open(ruta_archivo_transcripcion, "w", encoding="utf-8") as f:
                f.write("")
        else:
            # Si continuamos desde un segmento específico, verificar si el archivo existe
            if not os.path.exists(ruta_archivo_transcripcion):
                print(f"Creando nuevo archivo de transcripción: {nombre_archivo_transcripcion}")
                with open(ruta_archivo_transcripcion, "w", encoding="utf-8") as f:
                    f.write("")

        print(f"\nIniciando transcripción...")
        print(f"Archivo de salida: {nombre_archivo_transcripcion}")
        
        # Bucle para procesar cada segmento desde el segmento de inicio
        for idx in range(segmento_inicio, total_segmentos):
            segmento = segmentos[idx]
            print(f"\nProcesando segmento {idx + 1}/{total_segmentos}...")
            
            # Guardar cada segmento como archivo WAV temporal
            nombre_archivo_segmento = f"segmento_{idx}.wav"
            segmento.export(nombre_archivo_segmento, format="wav")

            # Cargar el archivo de audio de cada segmento
            with sr.AudioFile(nombre_archivo_segmento) as source:
                audio_segmento = reconocedor.record(source)

            # Intentar transcribir el segmento
            try:
                texto_segmento = reconocedor.recognize_google(audio_segmento, language="es-ES")
                
                # Añadir el texto transcrito al archivo de transcripción
                with open(ruta_archivo_transcripcion, "a", encoding="utf-8") as f:
                    segundo = idx * 30
                    segundo_str = f"{segundo // 3600:02}:{(segundo % 3600) // 60:02}:{segundo % 60:02}"
                    f.write(f"{segundo_str} -> {texto_segmento}\n")
                
                print(f"Segmento {idx + 1}/{total_segmentos} transcrito correctamente.")
                
            except sr.UnknownValueError:
                print(f"No se pudo entender el segmento {idx + 1}/{total_segmentos}.")
            except sr.RequestError as e:
                print(f"Error al solicitar resultados del servicio de Google para el segmento {idx + 1}/{total_segmentos}: {e}")

            # Eliminar el archivo temporal del segmento
            os.remove(nombre_archivo_segmento)

        print(f"Transcripción completa guardada en: {ruta_archivo_transcripcion}")
        return True
        
    except Exception as e:
        print(f"Error al procesar el archivo {ruta_archivo_audio}: {e}")
        return False
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

# Función para procesar una carpeta de archivos
def procesar_carpeta(ruta_carpeta):
    """
    Procesa todos los archivos de audio en una carpeta
    """
    archivos_procesados = 0
    formatos_audio = (".mp3", ".ogg", ".flac", ".opus", ".m4a", ".wma", ".aac", ".wav")
    
    print(f"Procesando carpeta: {ruta_carpeta}")
    
    # Primero, contar cuántos archivos de audio hay
    archivos_audio = []
    for archivo in os.listdir(ruta_carpeta):
        if archivo.lower().endswith(formatos_audio):
            archivos_audio.append(archivo)
    
    total_archivos = len(archivos_audio)
    if total_archivos == 0:
        print("No se encontraron archivos de audio en la carpeta.")
        return 0
    
    print(f"Se encontraron {total_archivos} archivos de audio.")
    print("Los archivos se procesarán completos (desde el inicio).")
    
    # Procesar cada archivo de audio en la carpeta
    for i, archivo in enumerate(archivos_audio, 1):
        print(f"\n{'='*50}")
        print(f"Procesando archivo {i}/{total_archivos}: {archivo}")
        print(f"{'='*50}")
        
        ruta_archivo_audio = os.path.join(ruta_carpeta, archivo)
        if transcribir_archivo(ruta_archivo_audio, preguntar_segmento=False):
            archivos_procesados += 1
            print(f"✓ Archivo {i}/{total_archivos} completado exitosamente.")
        else:
            print(f"✗ Error procesando archivo {i}/{total_archivos}.")
    
    print(f"\nResumen: Se procesaron {archivos_procesados}/{total_archivos} archivos de audio.")
    return archivos_procesados

# Función para seleccionar archivo o carpeta
def seleccionar_origen():
    """
    Permite al usuario seleccionar un archivo o carpeta mediante interfaz gráfica
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    
    # Preguntar al usuario si quiere seleccionar archivo o carpeta
    respuesta = messagebox.askyesno(
        "Seleccionar origen", 
        "¿Desea seleccionar un archivo individual?\n\n"
        "Sí = Seleccionar archivo\n"
        "No = Seleccionar carpeta"
    )
    
    if respuesta:  # Seleccionar archivo
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[
                ("Archivos de audio", "*.mp3 *.wav *.ogg *.flac *.opus *.m4a *.wma *.aac"),
                ("Todos los archivos", "*.*")
            ]
        )
    else:  # Seleccionar carpeta
        ruta = filedialog.askdirectory(
            title="Seleccionar carpeta con archivos de audio"
        )
    
    root.destroy()
    return ruta
    # Esta función ya no se usa en la versión Kivy
    return None

# Función principal
def main():
    """
    Función principal que coordina la ejecución del programa
    """
    print("=== Transcriptor de Audio ===")
    print("Seleccione un archivo de audio o una carpeta con archivos de audio")
    
    # Seleccionar origen (archivo o carpeta)
    ruta_origen = seleccionar_origen()
    
    if not ruta_origen:
        print("No se seleccionó ningún archivo o carpeta. Saliendo...")
        return
    
    print(f"Origen seleccionado: {ruta_origen}")
    
    # Verificar si es un archivo o directorio
    if os.path.isfile(ruta_origen):
        # Es un archivo individual
        print("Procesando archivo individual...")
        if transcribir_archivo(ruta_origen, preguntar_segmento=True):
            print("¡Transcripción completada exitosamente!")
        else:
            print("Error durante la transcripción.")
    
    elif os.path.isdir(ruta_origen):
        # Es un directorio
        print("Procesando carpeta...")
        archivos_procesados = procesar_carpeta(ruta_origen)
        if archivos_procesados > 0:
            print(f"¡Transcripción completada! Se procesaron {archivos_procesados} archivos.")
        else:
            print("No se encontraron archivos de audio válidos en la carpeta.")
    
    else:
        print("La ruta seleccionada no es válida.")

if __name__ == "__main__":
    main()
