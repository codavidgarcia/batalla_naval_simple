from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from src.controller.controlador import Controlador
import os

kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'juego.kv')
Builder.load_file(os.path.abspath(kv_path))

class JuegoScreen(Screen):
    tablero_texto = StringProperty("")
    mensaje = StringProperty("")
    estado_juego = StringProperty("")

    def __init__(self, **kwargs):
        super(JuegoScreen, self).__init__(**kwargs)
        self.controlador = Controlador()

    def on_enter(self):
        if hasattr(self.ids, 'ancho_input'):
            self.ids.ancho_input.text = "10"
        if hasattr(self.ids, 'alto_input'):
            self.ids.alto_input.text = "10"
        if hasattr(self.ids, 'naves_input'):
            self.ids.naves_input.text = "5"
        if hasattr(self.ids, 'fila_input'):
            self.ids.fila_input.text = ""
        if hasattr(self.ids, 'columna_input'):
            self.ids.columna_input.text = ""

        self.actualizar_estado_juego()

    def iniciar_juego(self):
        try:
            ancho_texto = self.ids.ancho_input.text.strip()
            alto_texto = self.ids.alto_input.text.strip()
            naves_texto = self.ids.naves_input.text.strip()

            ancho = int(ancho_texto) if ancho_texto else 10
            alto = int(alto_texto) if alto_texto else 10
            num_naves = int(naves_texto) if naves_texto else 5

            if ancho < 2 or ancho > 20:
                ancho = 10
            if alto < 2 or alto > 20:
                alto = 10
            if num_naves < 1 or num_naves > ancho * alto:
                num_naves = min(5, ancho * alto // 2)

            self.controlador.iniciar_juego(ancho, alto, num_naves)
            self.mensaje = "Juego iniciado. ¡Buena suerte!"

            self.actualizar_estado_juego()

        except Exception as e:
            self.mensaje = f"Error: {str(e)}"

    def realizar_disparo(self):
        try:
            if not self.controlador.juego:
                self.mensaje = "Debes iniciar un juego primero."
                return

            fila_texto = self.ids.fila_input.text.strip()
            columna_texto = self.ids.columna_input.text.strip()

            if not fila_texto or not columna_texto:
                self.mensaje = "Debes especificar fila y columna."
                return

            fila = int(fila_texto)
            columna = int(columna_texto)

            if (fila < 0 or fila >= self.controlador.juego.alto or
                columna < 0 or columna >= self.controlador.juego.ancho):
                self.mensaje = f"Coordenadas fuera de rango. Rango válido: filas (0-{self.controlador.juego.alto-1}), columnas (0-{self.controlador.juego.ancho-1})"
                return

            impacto = self.controlador.realizar_disparo(fila, columna)

            if impacto:
                self.mensaje = "¡Impacto en una nave!"
            else:
                self.mensaje = "Disparo al agua."

            self.ids.fila_input.text = ""
            self.ids.columna_input.text = ""

            self.actualizar_estado_juego()

        except ValueError as e:
            if "ya ha sido impactada" in str(e):
                self.mensaje = "Esta celda ya ha sido impactada."
            else:
                self.mensaje = "Entrada inválida. Usa números enteros."
        except Exception as e:
            self.mensaje = f"Error: {str(e)}"

    def reiniciar_juego(self):
        if self.controlador.reiniciar_juego():
            self.mensaje = "Juego reiniciado."
            self.actualizar_estado_juego()
        else:
            self.mensaje = "No hay un juego activo para reiniciar."

    def actualizar_estado_juego(self):
        try:
            self.tablero_texto = self.controlador.obtener_representacion_tablero()

            if self.controlador.juego:
                if self.controlador.juego_terminado():
                    self.estado_juego = "¡JUEGO TERMINADO!"
                    if self.controlador.jugador_activo:
                        self.estado_juego += f" Puntos: {self.controlador.jugador_activo.puntaje}"
                else:
                    naves_restantes = self.controlador.juego.campo.naves_restantes
                    self.estado_juego = f"Naves restantes: {naves_restantes}"
            else:
                self.estado_juego = "Configura el tablero y presiona 'Iniciar Juego'"
        except Exception as e:
            self.tablero_texto = "Error al actualizar el tablero"
            self.estado_juego = f"Error: {str(e)}"

    def volver(self):
        self.manager.current = "menu"
