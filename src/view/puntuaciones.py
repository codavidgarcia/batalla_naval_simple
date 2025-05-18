from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from src.controller.controlador import Controlador
import os

kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'puntuaciones.kv')
Builder.load_file(os.path.abspath(kv_path))

class PuntuacionesScreen(Screen):
    puntuaciones_texto = StringProperty("")
    
    def __init__(self, **kwargs):
        super(PuntuacionesScreen, self).__init__(**kwargs)
        self.controlador = Controlador()
    
    def on_enter(self):
        self.actualizar_puntuaciones()
    
    def actualizar_puntuaciones(self):
        puntuaciones = self.controlador.obtener_puntuaciones()
        
        if not puntuaciones:
            self.puntuaciones_texto = "No hay puntuaciones registradas."
            return
        
        texto = "MEJORES PUNTUACIONES\n"
        texto += "=" * 40 + "\n"
        texto += "Posición  |  Jugador  |  Puntos\n"
        texto += "-" * 40 + "\n"
        
        for i, p in enumerate(puntuaciones, 1):
            texto += f"{i:^9} | {p['nombre_usuario']:<10} | {p['puntaje']:>6}\n"
        
        self.puntuaciones_texto = texto
    
    def volver(self):
        self.manager.current = "menu"
