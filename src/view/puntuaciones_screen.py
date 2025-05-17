"""
Módulo que define la pantalla de puntuaciones para el juego Batalla Naval.

Este módulo contiene la implementación de la pantalla que muestra
las mejores puntuaciones del juego.

Autor: Juan David
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from src.controller.controlador import Controlador
import os

# Cargar el archivo KV que define la interfaz
kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'puntuaciones.kv')
Builder.load_file(os.path.abspath(kv_path))

class PuntuacionesScreen(Screen):
    """
    Pantalla que muestra las mejores puntuaciones.
    
    Esta pantalla muestra una tabla con las mejores puntuaciones
    almacenadas en la base de datos, ordenadas de mayor a menor.
    
    Atributos:
        puntuaciones_texto (StringProperty): Texto que muestra las puntuaciones.
        controlador (Controlador): Instancia del controlador que gestiona la lógica del juego.
    
    Métodos:
        actualizar_puntuaciones(): Actualiza la lista de puntuaciones.
        volver(): Vuelve al menú principal.
    
    Hola Jona: Esta clase representa la pantalla que muestra las mejores puntuaciones.
    Aquí definimos la propiedad puntuaciones_texto que se mostrará en la interfaz y
    los métodos que responden a las acciones del usuario (actualizar, volver).
    """
    
    # Propiedad que se actualiza en la interfaz
    puntuaciones_texto = StringProperty("")
    
    def __init__(self, **kwargs):
        """
        Inicializa la pantalla de puntuaciones.
        
        Hola Jona: Aquí inicializamos la pantalla de puntuaciones. Creamos una instancia
        del controlador que gestionará la lógica de las puntuaciones. La propiedad
        puntuaciones_texto se actualizará con la lista de puntuaciones y se mostrará
        en la interfaz.
        """
        super(PuntuacionesScreen, self).__init__(**kwargs)
        self.controlador = Controlador()
    
    def on_enter(self):
        """
        Se llama cuando se entra a esta pantalla.
        
        Hola Jona: Este método se llama automáticamente cuando el usuario
        navega a esta pantalla. Aquí actualizamos la lista de puntuaciones
        para mostrar las más recientes.
        """
        self.actualizar_puntuaciones()
    
    def actualizar_puntuaciones(self):
        """
        Actualiza la lista de puntuaciones.
        
        Hola Jona: Este método obtiene las mejores puntuaciones del controlador
        y las formatea como texto para mostrarlas en la interfaz. Las puntuaciones
        se muestran ordenadas de mayor a menor.
        """
        # Obtener puntuaciones del controlador
        puntuaciones = self.controlador.obtener_puntuaciones()
        
        if not puntuaciones:
            self.puntuaciones_texto = "No hay puntuaciones registradas."
            return
        
        # Formatear puntuaciones como texto
        texto = "MEJORES PUNTUACIONES\n"
        texto += "=" * 40 + "\n"
        texto += "Posición  |  Jugador  |  Puntos\n"
        texto += "-" * 40 + "\n"
        
        for i, p in enumerate(puntuaciones, 1):
            texto += f"{i:^9} | {p['nombre_usuario']:<10} | {p['puntaje']:>6}\n"
        
        self.puntuaciones_texto = texto
    
    def volver(self):
        """
        Vuelve al menú principal.
        
        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Volver al Menú". Simplemente cambiamos la pantalla actual a la pantalla
        de menú.
        """
        self.manager.current = "menu"
