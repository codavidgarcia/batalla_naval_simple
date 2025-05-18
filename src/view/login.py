from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from src.controller.controlador import Controlador
import os

kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'login.kv')
Builder.load_file(os.path.abspath(kv_path))

class LoginScreen(Screen):
    mensaje = StringProperty("")
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.controlador = Controlador()
    
    def on_enter(self):
        if hasattr(self.ids, 'usuario_input'):
            self.ids.usuario_input.text = ""
        if hasattr(self.ids, 'contraseña_input'):
            self.ids.contraseña_input.text = ""
        
        self.mensaje = ""
    
    def iniciar_sesion(self):
        usuario = self.ids.usuario_input.text.strip()
        contraseña = self.ids.contraseña_input.text.strip()
        
        if not usuario or not contraseña:
            self.mensaje = "❌ Todos los campos son obligatorios."
            return
        
        if self.controlador.iniciar_sesion(usuario, contraseña):
            self.mensaje = "✅ Inicio de sesión exitoso."
            juego_screen = self.manager.get_screen("juego")
            juego_screen.controlador = self.controlador
            self.manager.current = "juego"
        else:
            self.mensaje = "❌ Credenciales incorrectas."
    
    def volver(self):
        self.manager.current = "menu"
