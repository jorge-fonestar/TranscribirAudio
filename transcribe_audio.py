import whisper
from pydub import AudioSegment
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import tempfile


# Cargar el modelo de Whisper (se carga una sola vez)
print("Cargando modelo de Whisper (small)... Esto puede tardar la primera vez.")
modelo = whisper.load_model("small")
print("Modelo cargado.")


# Función para transcribir un archivo individual
def transcribir_archivo(ruta_archivo_audio, preguntar_segmento=True):
    """
    Transcribe un archivo de audio individual usando Whisper
    """
    try:
        nombre_archivo = os.path.basename(ruta_archivo_audio)
        directorio_padre = os.path.dirname(ruta_archivo_audio)

        print(f"Procesando archivo: {nombre_archivo}")

        # Cargar el archivo de audio con pydub para obtener duracion
        audio = AudioSegment.from_file(ruta_archivo_audio)
        duracion_total = len(audio) / 1000  # duracion en segundos

        print(f"Archivo cargado:")
        print(f"  - Duración total: {duracion_total/60:.1f} minutos ({duracion_total:.0f} segundos)")

        # Convertir a WAV mono 16kHz para Whisper
        audio_mono = audio.set_channels(1).set_frame_rate(16000)

        # Exportar a archivo temporal WAV
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            audio_mono.export(tmp_path, format="wav")

        # Nombre del archivo de salida
        nombre_base = os.path.splitext(nombre_archivo)[0]
        nombre_archivo_transcripcion = nombre_base + "_transcripcion.txt"
        ruta_archivo_transcripcion = os.path.join(directorio_padre, nombre_archivo_transcripcion)

        print(f"\nIniciando transcripción con Whisper...")
        print(f"  - Detección automática de idioma por segmento")
        print(f"Archivo de salida: {nombre_archivo_transcripcion}")

        # Transcribir con Whisper
        resultado = modelo.transcribe(
            tmp_path,
            verbose=True,  # Muestra progreso en consola
        )

        # Escribir resultado al archivo
        with open(ruta_archivo_transcripcion, "w", encoding="utf-8") as f:
            idioma_detectado = resultado.get("language", "desconocido")
            f.write(f"[Idioma principal detectado: {idioma_detectado}]\n\n")

            for segmento in resultado["segments"]:
                inicio = segmento["start"]
                fin = segmento["end"]
                texto = segmento["text"].strip()

                # Formatear timestamps
                inicio_str = f"{int(inicio)//3600:02}:{(int(inicio)%3600)//60:02}:{int(inicio)%60:02}"
                fin_str = f"{int(fin)//3600:02}:{(int(fin)%3600)//60:02}:{int(fin)%60:02}"

                f.write(f"[{inicio_str} -> {fin_str}] {texto}\n")

        # Limpiar archivo temporal
        os.remove(tmp_path)

        print(f"\nTranscripción completa guardada en: {ruta_archivo_transcripcion}")
        print(f"Idioma principal detectado: {resultado.get('language', 'desconocido')}")
        return True

    except Exception as e:
        print(f"Error al procesar el archivo {ruta_archivo_audio}: {e}")
        return False


# Función para procesar una carpeta de archivos
def procesar_carpeta(ruta_carpeta):
    """
    Procesa todos los archivos de audio en una carpeta
    """
    archivos_procesados = 0
    formatos_audio = (".mp3", ".ogg", ".flac", ".opus", ".m4a", ".wma", ".aac", ".wav")

    print(f"Procesando carpeta: {ruta_carpeta}")

    archivos_audio = []
    for archivo in os.listdir(ruta_carpeta):
        if archivo.lower().endswith(formatos_audio):
            archivos_audio.append(archivo)

    total_archivos = len(archivos_audio)
    if total_archivos == 0:
        print("No se encontraron archivos de audio en la carpeta.")
        return 0

    print(f"Se encontraron {total_archivos} archivos de audio.")

    for i, archivo in enumerate(archivos_audio, 1):
        print(f"\n{'='*50}")
        print(f"Procesando archivo {i}/{total_archivos}: {archivo}")
        print(f"{'='*50}")

        ruta_archivo_audio = os.path.join(ruta_carpeta, archivo)
        if transcribir_archivo(ruta_archivo_audio, preguntar_segmento=False):
            archivos_procesados += 1
            print(f"Archivo {i}/{total_archivos} completado exitosamente.")
        else:
            print(f"Error procesando archivo {i}/{total_archivos}.")

    print(f"\nResumen: Se procesaron {archivos_procesados}/{total_archivos} archivos de audio.")
    return archivos_procesados


# Función para seleccionar archivo o carpeta
def seleccionar_origen():
    """
    Permite al usuario seleccionar un archivo o carpeta mediante interfaz gráfica
    """
    root = tk.Tk()
    root.withdraw()

    respuesta = messagebox.askyesno(
        "Seleccionar origen",
        "¿Desea seleccionar un archivo individual?\n\n"
        "Sí = Seleccionar archivo\n"
        "No = Seleccionar carpeta"
    )

    if respuesta:
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[
                ("Archivos de audio", "*.mp3 *.wav *.ogg *.flac *.opus *.m4a *.wma *.aac"),
                ("Todos los archivos", "*.*")
            ]
        )
    else:
        ruta = filedialog.askdirectory(
            title="Seleccionar carpeta con archivos de audio"
        )

    root.destroy()
    return ruta


# Función principal
def main():
    """
    Función principal que coordina la ejecución del programa
    """
    print("=== Transcriptor de Audio (Whisper) ===")
    print("Soporta múltiples idiomas con detección automática")
    print("Seleccione un archivo de audio o una carpeta con archivos de audio")

    ruta_origen = seleccionar_origen()

    if not ruta_origen:
        print("No se seleccionó ningún archivo o carpeta. Saliendo...")
        return

    print(f"Origen seleccionado: {ruta_origen}")

    if os.path.isfile(ruta_origen):
        print("Procesando archivo individual...")
        if transcribir_archivo(ruta_origen, preguntar_segmento=True):
            print("¡Transcripción completada exitosamente!")
        else:
            print("Error durante la transcripción.")

    elif os.path.isdir(ruta_origen):
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
