from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.view.menu import MenuScreen
from src.view.juego import JuegoScreen
from src.view.registro import RegistroScreen
from src.view.login import LoginScreen
from src.view.puntuaciones import PuntuacionesScreen
from src.controller.controlador import Controlador

class BatallaNavalApp(App):
    def build(self):
        controlador = Controlador()

        sm = ScreenManager()

        sm.add_widget(MenuScreen(name="menu"))

        juego_screen = JuegoScreen(name="juego")
        juego_screen.controlador = controlador

        registro_screen = RegistroScreen(name="registro")
        registro_screen.controlador = controlador

        login_screen = LoginScreen(name="login")
        login_screen.controlador = controlador

        puntuaciones_screen = PuntuacionesScreen(name="puntuaciones")
        puntuaciones_screen.controlador = controlador

        sm.add_widget(juego_screen)
        sm.add_widget(registro_screen)
        sm.add_widget(login_screen)
        sm.add_widget(puntuaciones_screen)

        return sm

if __name__ == "__main__":
    BatallaNavalApp().run()
