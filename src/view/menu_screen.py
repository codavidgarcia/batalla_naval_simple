"""
Módulo que define la pantalla de menú para el juego Batalla Naval.

Este módulo contiene la implementación de la pantalla de menú principal
del juego, que permite al usuario navegar a las diferentes secciones.

Autor: Juan David
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

# Cargar el archivo KV que define la interfaz
kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'menu.kv')
Builder.load_file(os.path.abspath(kv_path))

class MenuScreen(Screen):
    """
    Pantalla de menú principal del juego.
    
    Esta pantalla muestra las opciones principales del juego:
    - Jugar sin registro
    - Salir
    
    Hola Jona: Esta clase representa la pantalla de menú principal del juego.
    En Kivy, una Screen es una pantalla completa de la aplicación. La interfaz
    visual de esta pantalla está definida en el archivo menu.kv, que cargamos
    al inicio del módulo. Esta clase es muy simple porque toda la lógica de
    navegación está en el archivo KV.
    """
    pass  # No necesitamos añadir funcionalidad adicional aquí
