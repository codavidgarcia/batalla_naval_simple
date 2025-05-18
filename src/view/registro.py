from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from src.controller.controlador import Controlador
import os

kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'registro.kv')
Builder.load_file(os.path.abspath(kv_path))

class RegistroScreen(Screen):
    mensaje = StringProperty("")
    
    def __init__(self, **kwargs):
        super(RegistroScreen, self).__init__(**kwargs)
        self.controlador = Controlador()
    
    def on_enter(self):
        if hasattr(self.ids, 'usuario_input'):
            self.ids.usuario_input.text = ""
        if hasattr(self.ids, 'contraseña_input'):
            self.ids.contraseña_input.text = ""
        
        self.mensaje = ""
    
    def registrar(self):
        usuario = self.ids.usuario_input.text.strip()
        contraseña = self.ids.contraseña_input.text.strip()
        
        if not usuario or not contraseña:
            self.mensaje = "❌ Todos los campos son obligatorios."
            return
        
        if self.controlador.registrar_jugador(usuario, contraseña):
            self.mensaje = "✅ Usuario registrado correctamente."
            self.ids.usuario_input.text = ""
            self.ids.contraseña_input.text = ""
        else:
            self.mensaje = "❌ Error al registrar usuario. El nombre de usuario ya existe o es inválido."
    
    def volver(self):
        self.manager.current = "menu"
