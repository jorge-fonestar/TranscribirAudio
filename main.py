import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
import os
import threading
from pydub import AudioSegment

from transcribe_audio_kivy import transcribir_archivo_kivy_mejorado

class TranscriberLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # Título de la aplicación
        self.title_label = Label(
            text='TranscribirAudio - Selecciona un archivo de audio',
            size_hint_y=None,
            height=50,
            font_size=18,
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.title_label)
        
        # Selector de archivos
        self.filechooser = FileChooserIconView(
            filters=['*.wav', '*.mp3', '*.m4a', '*.flac', '*.ogg', '*.aac']
        )
        self.filechooser.bind(selection=self.on_file_selected)
        self.add_widget(self.filechooser)
        
        # Botón para transcribir (inicialmente deshabilitado)
        self.transcribe_btn = Button(
            text='Selecciona un archivo de audio primero',
            size_hint_y=None,
            height=50,
            disabled=True
        )
        self.transcribe_btn.bind(on_press=self.show_segment_dialog)
        self.add_widget(self.transcribe_btn)
        
        # Variables para el archivo seleccionado
        self.selected_file = None
        self.total_segments = 0
        
    def on_file_selected(self, instance, selection):
        """Se ejecuta cuando se selecciona un archivo"""
        if selection:
            self.selected_file = selection[0]
            filename = os.path.basename(self.selected_file)
            
            # Calcular el número total de segmentos
            try:
                audio = AudioSegment.from_file(self.selected_file)
                duration_ms = len(audio)
                self.total_segments = (duration_ms // 30000) + (1 if duration_ms % 30000 > 0 else 0)
                
                self.transcribe_btn.text = f'Transcribir: {filename} ({self.total_segments} segmentos)'
                self.transcribe_btn.disabled = False
                self.title_label.text = f'Archivo seleccionado: {filename}'
            except Exception as e:
                self.transcribe_btn.text = f'Error al leer el archivo: {str(e)}'
                self.transcribe_btn.disabled = True
        else:
            self.selected_file = None
            self.total_segments = 0
            self.transcribe_btn.text = 'Selecciona un archivo de audio primero'
            self.transcribe_btn.disabled = True
            self.title_label.text = 'TranscribirAudio - Selecciona un archivo de audio'
    
    def show_segment_dialog(self, instance):
        """Muestra el diálogo para seleccionar el segmento de inicio"""
        if not self.selected_file:
            return
            
        # Crear el contenido del popup
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Etiqueta informativa
        info_label = Label(
            text=f'Archivo: {os.path.basename(self.selected_file)}\n'
                 f'Total de segmentos: {self.total_segments}\n'
                 f'Duración aproximada: {(self.total_segments * 30) // 60}:{(self.total_segments * 30) % 60:02d}\n\n'
                 f'¿Desde qué segmento quieres comenzar?\n'
                 f'(Deja vacío para empezar desde el inicio)',
            text_size=(400, None),
            halign='center'
        )
        content.add_widget(info_label)
        
        # Campo de entrada
        self.segment_input = TextInput(
            hint_text=f'Número del segmento (1-{self.total_segments}) o vacío para inicio',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        content.add_widget(self.segment_input)
        
        # Botones
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        cancel_btn = Button(text='Cancelar')
        start_btn = Button(text='Comenzar Transcripción')
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(start_btn)
        content.add_widget(button_layout)
        
        # Crear popup
        self.segment_popup = Popup(
            title='Configurar Transcripción',
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        cancel_btn.bind(on_press=self.segment_popup.dismiss)
        start_btn.bind(on_press=self.start_transcription)
        
        self.segment_popup.open()
    
    def start_transcription(self, instance):
        """Inicia el proceso de transcripción"""
        try:
            start_segment_text = self.segment_input.text.strip()
            start_segment = 0
            
            if start_segment_text:
                start_segment = int(start_segment_text) - 1  # Convertir a índice base 0
                if start_segment < 0 or start_segment >= self.total_segments:
                    self.show_error(f'El segmento debe estar entre 1 y {self.total_segments}')
                    return
            
            # Cerrar el popup de configuración
            self.segment_popup.dismiss()
            
            # Mostrar ventana de progreso
            self.show_progress_window(start_segment)
            
            # Iniciar transcripción en hilo separado
            thread = threading.Thread(
                target=self.transcribe_in_background,
                args=(self.selected_file, start_segment)
            )
            thread.daemon = True
            thread.start()
            
        except ValueError:
            self.show_error('Por favor, introduce un número válido')
        except Exception as e:
            self.show_error(f'Error: {str(e)}')
    
    def show_error(self, message):
        """Muestra un mensaje de error"""
        error_popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        error_popup.open()
    
    def show_progress_window(self, start_segment):
        """Muestra la ventana de progreso"""
        # Crear contenido de la ventana de progreso
        progress_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Etiqueta de estado
        self.status_label = Label(
            text=f'Iniciando transcripción desde segmento {start_segment + 1}...',
            size_hint_y=None,
            height=50
        )
        progress_content.add_widget(self.status_label)
        
        # Área de log
        self.log_text = TextInput(
            text='Preparando transcripción...\n',
            readonly=True,
            size_hint=(1, 1)
        )
        scroll_log = ScrollView()
        scroll_log.add_widget(self.log_text)
        progress_content.add_widget(scroll_log)
        
        # Botón para cerrar (inicialmente deshabilitado)
        self.close_btn = Button(
            text='Procesando... Por favor espera',
            size_hint_y=None,
            height=50,
            disabled=True
        )
        self.close_btn.bind(on_press=self.close_progress)
        progress_content.add_widget(self.close_btn)
        
        # Crear popup de progreso
        self.progress_popup = Popup(
            title=f'Transcribiendo: {os.path.basename(self.selected_file)}',
            content=progress_content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        
        self.progress_popup.open()
    
    def transcribe_in_background(self, file_path, start_segment):
        """Ejecuta la transcripción en segundo plano"""
        try:
            resultado = transcribir_archivo_kivy_mejorado(
                file_path, 
                start_segment, 
                callback=self.update_progress
            )
            
            # Actualizar interfaz en el hilo principal
            Clock.schedule_once(lambda dt: self.transcription_completed(resultado), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.transcription_error(str(e)), 0)
    
    def update_progress(self, message):
        """Actualiza el progreso (llamado desde el callback)"""
        Clock.schedule_once(lambda dt: self._update_progress_ui(message), 0)
    
    def _update_progress_ui(self, message):
        """Actualiza la interfaz de progreso en el hilo principal"""
        if hasattr(self, 'log_text'):
            self.log_text.text += message + '\n'
            # Auto-scroll hacia abajo
            self.log_text.cursor = (len(self.log_text.text), 0)
    
    def transcription_completed(self, resultado):
        """Se ejecuta cuando la transcripción se completa"""
        self.status_label.text = '¡Transcripción completada!'
        self.log_text.text += '\n=== TRANSCRIPCIÓN COMPLETADA ===\n'
        self.log_text.text += resultado
        self.close_btn.text = 'Cerrar y ver resultado'
        self.close_btn.disabled = False
        self.transcription_result = resultado
    
    def transcription_error(self, error_msg):
        """Se ejecuta cuando hay un error en la transcripción"""
        self.status_label.text = 'Error en la transcripción'
        self.log_text.text += f'\nERROR: {error_msg}\n'
        self.close_btn.text = 'Cerrar'
        self.close_btn.disabled = False
        self.transcription_result = None
    
    def close_progress(self, instance):
        """Cierra la ventana de progreso"""
        self.progress_popup.dismiss()
        
        # Si hay resultado, mostrarlo
        if hasattr(self, 'transcription_result') and self.transcription_result:
            self.show_result_window()
    
    def show_result_window(self):
        """Muestra la ventana con el resultado final"""
        result_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Título
        title_label = Label(
            text=f'Resultado de: {os.path.basename(self.selected_file)}',
            size_hint_y=None,
            height=40,
            font_size=16
        )
        result_content.add_widget(title_label)
        
        # Texto del resultado
        result_text = TextInput(
            text=self.transcription_result,
            readonly=True
        )
        scroll_result = ScrollView()
        scroll_result.add_widget(result_text)
        result_content.add_widget(scroll_result)
        
        # Botón para cerrar
        close_btn = Button(
            text='Cerrar',
            size_hint_y=None,
            height=50
        )
        result_content.add_widget(close_btn)
        
        # Popup de resultado
        result_popup = Popup(
            title='Transcripción Completada',
            content=result_content,
            size_hint=(0.95, 0.9),
            auto_dismiss=False
        )
        
        close_btn.bind(on_press=result_popup.dismiss)
        result_popup.open()

class TranscriberApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Fondo oscuro
        return TranscriberLayout()

if __name__ == '__main__':
    TranscriberApp().run()
