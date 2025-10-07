## abrimos cualquier fichero en la carpeta audios que tenga extension convertible para pasarla a wav
import speech_recognition as sr
from pydub import AudioSegment
import os

# Ruta de la carpeta con los archivos de audio
ruta_audios = "./audios"

# Procesar cada archivo WAV en la carpeta
for archivo in os.listdir(ruta_audios):

    # calculñamos la extension
    extension = os.path.splitext(archivo)[1]

    # si el fichero termina en una extensión conocida, lo procesamos
    if archivo.endswith((".mp3",".ogg",".flac",".opus",".m4a",".wma",".aac")):

        # Cargar el archivo original y exportarlo en formato WAV
        try:
            # Obtener la ruta completa del archivo de audio
            input_file = os.path.join(ruta_audios, archivo)
            
            # Cargar el archivo de audio
            audio = AudioSegment.from_file(input_file)

            output_file = input_file.replace(extension,".wav")
            audio = AudioSegment.from_file(input_file)  # Cambia el formato si es necesario
            audio = audio.set_channels(1).set_frame_rate(16000)
            audio.export(output_file, format="wav")
            print(f"Archivo convertido con éxito: {output_file}")
        except Exception as e:
            print(f"Error al convertir el archivo: {e}")
            
