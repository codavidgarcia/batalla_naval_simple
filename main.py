"""
Archivo principal del juego Batalla Naval simplificado.

Este archivo inicia la aplicación Kivy y configura las pantallas del juego.

"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.view.menu_screen import MenuScreen
from src.view.juego_screen import JuegoScreen
from src.view.registro_screen import RegistroScreen
from src.view.login_screen import LoginScreen
from src.view.puntuaciones_screen import PuntuacionesScreen

class BatallaNavalApp(App):
    """
    Aplicación principal del juego Batalla Naval.

    Esta clase configura la aplicación Kivy y crea las pantallas del juego.

    Hola Jona: Esta es la clase principal de la aplicación. Hereda de App,
    que es la clase base para todas las aplicaciones Kivy. El método build()
    se llama cuando se inicia la aplicación y debe retornar el widget raíz
    de la aplicación. En nuestro caso, creamos un ScreenManager que gestiona
    las diferentes pantallas del juego.
    """

    def build(self):
        """
        Construye la interfaz de la aplicación.

        Returns:
            ScreenManager: Gestor de pantallas con las pantallas del juego.
        """
        # Crear el gestor de pantallas
        sm = ScreenManager()

        # Añadir las pantallas
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(JuegoScreen(name="juego"))
        sm.add_widget(RegistroScreen(name="registro"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(PuntuacionesScreen(name="puntuaciones"))

        return sm

if __name__ == "__main__":
    BatallaNavalApp().run()
