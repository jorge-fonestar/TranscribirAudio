import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
from pydub import AudioSegment
import time

from transcribe_audio_kivy import transcribir_archivo_kivy_mejorado

class TranscribirAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TranscribirAudio - Interfaz Mejorada")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.selected_file = tk.StringVar()
        self.total_segments = 0
        self.transcription_in_progress = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2b2b2b', foreground='white')
        style.configure('Info.TLabel', font=('Arial', 10), background='#2b2b2b', foreground='white')
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="🎵 TranscribirAudio - Selecciona un archivo de audio", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de selección de archivo
        file_frame = ttk.LabelFrame(main_frame, text="Selección de Archivo", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botón para seleccionar archivo
        self.select_btn = ttk.Button(
            file_frame, 
            text="📁 Seleccionar archivo de audio", 
            command=self.select_file,
            style='Custom.TButton'
        )
        self.select_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Label de archivo seleccionado
        self.file_label = ttk.Label(
            file_frame, 
            text="Ningún archivo seleccionado", 
            style='Info.TLabel',
            wraplength=700
        )
        self.file_label.pack(fill=tk.X)
        
        # Frame de información
        info_frame = ttk.LabelFrame(main_frame, text="Información del Archivo", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.info_label = ttk.Label(
            info_frame, 
            text="Selecciona un archivo para ver su información", 
            style='Info.TLabel'
        )
        self.info_label.pack(fill=tk.X)
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración de Transcripción", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Segmento de inicio
        segment_frame = ttk.Frame(config_frame)
        segment_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(segment_frame, text="Comenzar desde segmento:", style='Info.TLabel').pack(side=tk.LEFT)
        
        self.segment_var = tk.StringVar()
        self.segment_entry = ttk.Entry(
            segment_frame, 
            textvariable=self.segment_var, 
            width=10,
            font=('Arial', 10)
        )
        self.segment_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        ttk.Label(segment_frame, text="(vacío = desde el inicio)", style='Info.TLabel').pack(side=tk.LEFT, padx=(5, 0))
        
        # Botón de transcribir
        self.transcribe_btn = ttk.Button(
            config_frame, 
            text="🚀 Comenzar Transcripción", 
            command=self.start_transcription,
            style='Custom.TButton',
            state='disabled'
        )
        self.transcribe_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Frame de progreso
        self.progress_frame = ttk.LabelFrame(main_frame, text="Progreso de Transcripción", padding="10")
        self.progress_frame.pack(fill=tk.BOTH, expand=True)
        self.progress_frame.pack_forget()  # Ocultar inicialmente
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Label de estado
        self.status_label = ttk.Label(
            self.progress_frame, 
            text="", 
            style='Info.TLabel'
        )
        self.status_label.pack(fill=tk.X, pady=(0, 10))
        
        # Área de log
        log_frame = ttk.Frame(self.progress_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para el log
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget para el log
        self.log_text = tk.Text(
            log_frame, 
            wrap=tk.WORD, 
            yscrollcommand=scrollbar.set,
            bg='#1e1e1e',
            fg='#ffffff',
            font=('Consolas', 9),
            state='disabled'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Botones de control
        control_frame = ttk.Frame(self.progress_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.cancel_btn = ttk.Button(
            control_frame, 
            text="❌ Cancelar", 
            command=self.cancel_transcription,
            state='disabled'
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.finish_btn = ttk.Button(
            control_frame, 
            text="✅ Ver Resultado", 
            command=self.show_result,
            state='disabled'
        )
        self.finish_btn.pack(side=tk.RIGHT)
        
    def select_file(self):
        """Selecciona un archivo de audio"""
        file_types = [
            ("Archivos de audio", "*.wav *.mp3 *.m4a *.flac *.ogg *.aac"),
            ("WAV files", "*.wav"),
            ("MP3 files", "*.mp3"),
            ("M4A files", "*.m4a"),
            ("FLAC files", "*.flac"),
            ("OGG files", "*.ogg"),
            ("AAC files", "*.aac"),
            ("Todos los archivos", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=file_types
        )
        
        if filename:
            self.selected_file.set(filename)
            self.analyze_file(filename)
            
    def analyze_file(self, filename):
        """Analiza el archivo seleccionado"""
        try:
            # Mostrar información básica
            file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
            self.file_label.config(text=f"📄 {os.path.basename(filename)}")
            
            # Analizar audio
            self.log_message("Analizando archivo de audio...")
            audio = AudioSegment.from_file(filename)
            duration_seconds = len(audio) / 1000
            self.total_segments = (len(audio) // 30000) + (1 if len(audio) % 30000 > 0 else 0)
            
            # Mostrar información
            duration_str = f"{int(duration_seconds // 60):02d}:{int(duration_seconds % 60):02d}"
            info_text = (f"📊 Información del archivo:\n"
                        f"• Tamaño: {file_size:.1f} MB\n"
                        f"• Duración: {duration_str}\n"
                        f"• Segmentos (30s c/u): {self.total_segments}\n"
                        f"• Canales: {audio.channels}\n"
                        f"• Frecuencia: {audio.frame_rate} Hz")
            
            self.info_label.config(text=info_text)
            
            # Habilitar transcripción
            self.transcribe_btn.config(state='normal')
            self.segment_entry.config(state='normal')
            
            # Actualizar placeholder del segmento
            self.segment_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el archivo:\n{str(e)}")
            self.info_label.config(text="❌ Error al analizar el archivo")
            self.transcribe_btn.config(state='disabled')
    
    def start_transcription(self):
        """Inicia el proceso de transcripción"""
        if not self.selected_file.get():
            messagebox.showwarning("Advertencia", "Selecciona un archivo primero")
            return
            
        if self.transcription_in_progress:
            messagebox.showinfo("Información", "Ya hay una transcripción en progreso")
            return
        
        # Validar segmento de inicio
        try:
            start_segment_text = self.segment_var.get().strip()
            start_segment = 0
            
            if start_segment_text:
                start_segment = int(start_segment_text) - 1  # Convertir a índice base 0
                if start_segment < 0 or start_segment >= self.total_segments:
                    messagebox.showerror("Error", f"El segmento debe estar entre 1 y {self.total_segments}")
                    return
                    
        except ValueError:
            messagebox.showerror("Error", "El segmento debe ser un número válido")
            return
        
        # Mostrar frame de progreso
        self.progress_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar interfaz para transcripción
        self.transcribe_btn.config(state='disabled')
        self.select_btn.config(state='disabled')
        self.segment_entry.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.finish_btn.config(state='disabled')
        
        # Limpiar log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Configurar progreso
        self.progress_bar.config(maximum=self.total_segments - start_segment)
        self.progress_bar.config(value=0)
        
        # Variables de control
        self.transcription_in_progress = True
        self.start_segment = start_segment
        self.transcription_result = None
        
        # Iniciar transcripción en hilo separado
        self.transcription_thread = threading.Thread(
            target=self.run_transcription,
            args=(self.selected_file.get(), start_segment),
            daemon=True
        )
        self.transcription_thread.start()
        
    def run_transcription(self, file_path, start_segment):
        """Ejecuta la transcripción en segundo plano"""
        try:
            result = transcribir_archivo_kivy_mejorado(
                file_path,
                start_segment,
                callback=self.update_progress_callback
            )
            
            # Actualizar interfaz en el hilo principal
            self.root.after(0, lambda: self.transcription_completed(result))
            
        except Exception as e:
            self.root.after(0, lambda: self.transcription_error(str(e)))
    
    def update_progress_callback(self, message):
        """Callback para actualizar el progreso"""
        self.root.after(0, lambda: self.update_progress_ui(message))
    
    def update_progress_ui(self, message):
        """Actualiza la interfaz de progreso"""
        # Actualizar log
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
        # Extraer información de progreso del mensaje
        if '[' in message and '%]' in message:
            try:
                # Extraer porcentaje del mensaje
                start = message.find('[') + 1
                end = message.find('%]')
                if start > 0 and end > start:
                    percentage = float(message[start:end])
                    segments_completed = int((percentage / 100) * (self.total_segments - self.start_segment))
                    self.progress_bar.config(value=segments_completed)
                    
                    # Actualizar status
                    self.status_label.config(text=f"Progreso: {percentage:.1f}% - {segments_completed}/{self.total_segments - self.start_segment} segmentos")
            except:
                pass  # Si no se puede parsear, continúa
    
    def transcription_completed(self, result):
        """Se ejecuta cuando la transcripción se completa"""
        self.transcription_in_progress = False
        self.transcription_result = result
        
        # Actualizar interfaz
        self.progress_bar.config(value=self.progress_bar.cget('maximum'))
        self.status_label.config(text="✅ ¡Transcripción completada!")
        self.cancel_btn.config(state='disabled')
        self.finish_btn.config(state='normal')
        
        # Log final
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, "\n" + "="*50 + "\n")
        self.log_text.insert(tk.END, "🎉 TRANSCRIPCIÓN COMPLETADA\n")
        self.log_text.insert(tk.END, "="*50 + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
        # Restablecer botones
        self.transcribe_btn.config(state='normal')
        self.select_btn.config(state='normal')
        self.segment_entry.config(state='normal')
    
    def transcription_error(self, error_msg):
        """Se ejecuta cuando hay un error en la transcripción"""
        self.transcription_in_progress = False
        
        # Actualizar interfaz
        self.status_label.config(text="❌ Error en la transcripción")
        self.cancel_btn.config(state='disabled')
        
        # Log de error
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"\n❌ ERROR: {error_msg}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
        # Restablecer botones
        self.transcribe_btn.config(state='normal')
        self.select_btn.config(state='normal')
        self.segment_entry.config(state='normal')
        
        messagebox.showerror("Error de Transcripción", f"Ocurrió un error durante la transcripción:\n\n{error_msg}")
    
    def cancel_transcription(self):
        """Cancela la transcripción en progreso"""
        if messagebox.askyesno("Cancelar", "¿Estás seguro de que deseas cancelar la transcripción?"):
            self.transcription_in_progress = False
            self.status_label.config(text="🚫 Transcripción cancelada")
            self.cancel_btn.config(state='disabled')
            
            # Restablecer botones
            self.transcribe_btn.config(state='normal')
            self.select_btn.config(state='normal')
            self.segment_entry.config(state='normal')
    
    def show_result(self):
        """Muestra la ventana con el resultado"""
        if not self.transcription_result:
            messagebox.showwarning("Advertencia", "No hay resultado disponible")
            return
        
        # Crear ventana de resultado
        result_window = tk.Toplevel(self.root)
        result_window.title("Resultado de la Transcripción")
        result_window.geometry("800x600")
        result_window.configure(bg='#2b2b2b')
        
        # Frame principal
        main_frame = ttk.Frame(result_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text=f"📄 Resultado: {os.path.basename(self.selected_file.get())}", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Área de texto con scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        result_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            bg='#f0f0f0',
            fg='#000000',
            font=('Arial', 10),
            state='normal'
        )
        result_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=result_text.yview)
        
        # Insertar resultado
        result_text.insert(1.0, self.transcription_result)
        result_text.config(state='disabled')
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def copy_to_clipboard():
            result_window.clipboard_clear()
            result_window.clipboard_append(self.transcription_result)
            messagebox.showinfo("Copiado", "Texto copiado al portapapeles")
        
        def save_to_file():
            file_path = filedialog.asksaveasfilename(
                title="Guardar transcripción",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(self.transcription_result)
                    messagebox.showinfo("Guardado", f"Transcripción guardada en:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al guardar archivo:\n{str(e)}")
        
        ttk.Button(button_frame, text="📋 Copiar", command=copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="💾 Guardar", command=save_to_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Cerrar", command=result_window.destroy).pack(side=tk.RIGHT)
    
    def log_message(self, message):
        """Añade un mensaje al log"""
        if hasattr(self, 'log_text'):
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, message + '\n')
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')


def main():
    root = tk.Tk()
    app = TranscribirAudioApp(root)
    
    # Configurar el cierre de la aplicación
    def on_closing():
        if app.transcription_in_progress:
            if messagebox.askyesno("Cerrar", "Hay una transcripción en progreso. ¿Deseas cerrar la aplicación?"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()