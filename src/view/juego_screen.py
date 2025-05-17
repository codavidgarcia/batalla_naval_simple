"""
Módulo que define la pantalla de juego para el juego Batalla Naval.

Este módulo contiene la implementación de la pantalla donde se desarrolla
el juego, permitiendo al usuario configurar el tablero, realizar disparos
y ver el estado del juego.

Autor: Juan David
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from src.controller.controlador import Controlador
import os

# Cargar el archivo KV que define la interfaz
kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'juego.kv')
Builder.load_file(os.path.abspath(kv_path))

class JuegoScreen(Screen):
    """
    Pantalla donde se desarrolla el juego.

    Esta pantalla permite al usuario configurar el tablero, iniciar el juego,
    realizar disparos y ver el estado actual del juego.

    Atributos:
        tablero_texto (StringProperty): Texto que muestra el estado del tablero.
        mensaje (StringProperty): Mensaje para el usuario (resultados de acciones, errores, etc.).
        estado_juego (StringProperty): Estado actual del juego (en progreso, terminado, etc.).
        controlador (Controlador): Instancia del controlador que gestiona la lógica del juego.

    Métodos:
        iniciar_juego(): Inicia una nueva partida con los parámetros especificados.
        realizar_disparo(): Realiza un disparo en las coordenadas especificadas.
        reiniciar_juego(): Reinicia la partida actual.
        actualizar_estado_juego(): Actualiza la visualización del estado del juego.
        volver(): Vuelve al menú principal.

    Hola Jona: Esta clase representa la pantalla donde se juega la partida.
    Aquí definimos las propiedades que se mostrarán en la interfaz (tablero,
    mensajes, estado) y los métodos que responden a las acciones del usuario
    (iniciar juego, disparar, reiniciar, etc.).
    """

    # Propiedades que se actualizan en la interfaz
    tablero_texto = StringProperty("")
    mensaje = StringProperty("")
    estado_juego = StringProperty("")

    def __init__(self, **kwargs):
        """
        Inicializa la pantalla de juego.

        Hola Jona: Aquí inicializamos la pantalla de juego. Creamos una instancia
        del controlador que gestionará toda la lógica del juego. Las propiedades
        tablero_texto, mensaje y estado_juego se actualizarán durante el juego
        y se mostrarán automáticamente en la interfaz.
        """
        super(JuegoScreen, self).__init__(**kwargs)
        self.controlador = Controlador()

    def on_enter(self):
        """
        Se llama cuando se entra a esta pantalla.

        Hola Jona: Este método se llama automáticamente cuando el usuario
        navega a esta pantalla. Aquí inicializamos los campos de entrada
        con valores predeterminados y actualizamos el estado del juego.
        """
        # Inicializar campos de entrada con valores predeterminados
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

        # Actualizar estado del juego
        self.actualizar_estado_juego()

    def iniciar_juego(self):
        """
        Inicia una nueva partida con los parámetros especificados.

        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Iniciar Juego". Obtenemos los valores de los campos de entrada (ancho,
        alto, número de naves), validamos que sean correctos y creamos una nueva
        partida con esos parámetros.
        """
        try:
            # Obtener valores de entrada
            ancho_texto = self.ids.ancho_input.text.strip()
            alto_texto = self.ids.alto_input.text.strip()
            naves_texto = self.ids.naves_input.text.strip()

            # Convertir a enteros (usar valores predeterminados si están vacíos)
            ancho = int(ancho_texto) if ancho_texto else 10
            alto = int(alto_texto) if alto_texto else 10
            num_naves = int(naves_texto) if naves_texto else 5

            # Validar rangos
            if ancho < 2 or ancho > 20:
                ancho = 10
            if alto < 2 or alto > 20:
                alto = 10
            if num_naves < 1 or num_naves > ancho * alto:
                num_naves = min(5, ancho * alto // 2)

            # Iniciar juego
            self.controlador.iniciar_juego(ancho, alto, num_naves)
            self.mensaje = "Juego iniciado. ¡Buena suerte!"

            # Actualizar tablero
            self.actualizar_estado_juego()

        except Exception as e:
            self.mensaje = f"Error: {str(e)}"

    def realizar_disparo(self):
        """
        Realiza un disparo en las coordenadas especificadas.

        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Realizar Disparo". Obtenemos las coordenadas de los campos de entrada,
        validamos que sean correctas y realizamos el disparo. Luego actualizamos
        el estado del juego y mostramos el resultado del disparo.
        """
        try:
            # Validar que haya un juego activo
            if not self.controlador.juego:
                self.mensaje = "Debes iniciar un juego primero."
                return

            # Obtener coordenadas
            fila_texto = self.ids.fila_input.text.strip()
            columna_texto = self.ids.columna_input.text.strip()

            # Validar que se hayan ingresado coordenadas
            if not fila_texto or not columna_texto:
                self.mensaje = "Debes especificar fila y columna."
                return

            # Convertir a enteros
            fila = int(fila_texto)
            columna = int(columna_texto)

            # Validar rangos
            if (fila < 0 or fila >= self.controlador.juego.alto or
                columna < 0 or columna >= self.controlador.juego.ancho):
                self.mensaje = f"Coordenadas fuera de rango. Rango válido: filas (0-{self.controlador.juego.alto-1}), columnas (0-{self.controlador.juego.ancho-1})"
                return

            # Realizar disparo
            impacto = self.controlador.realizar_disparo(fila, columna)

            # Mostrar resultado
            if impacto:
                self.mensaje = "¡Impacto en una nave!"
            else:
                self.mensaje = "Disparo al agua."

            # Limpiar campos de entrada
            self.ids.fila_input.text = ""
            self.ids.columna_input.text = ""

            # Actualizar tablero
            self.actualizar_estado_juego()

        except ValueError as e:
            if "ya ha sido impactada" in str(e):
                self.mensaje = "Esta celda ya ha sido impactada."
            else:
                self.mensaje = "Entrada inválida. Usa números enteros."
        except Exception as e:
            self.mensaje = f"Error: {str(e)}"

    def reiniciar_juego(self):
        """
        Reinicia la partida actual.

        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Reiniciar Juego". Reiniciamos el juego actual y actualizamos el estado.
        """
        if self.controlador.reiniciar_juego():
            self.mensaje = "Juego reiniciado."
            self.actualizar_estado_juego()
        else:
            self.mensaje = "No hay un juego activo para reiniciar."

    def actualizar_estado_juego(self):
        """
        Actualiza la visualización del estado del juego.

        Hola Jona: Este método actualiza la visualización del estado del juego
        en la interfaz. Obtenemos la representación del tablero y el estado
        actual del juego (en progreso, terminado, etc.) y los mostramos.
        """
        try:
            # Obtener representación del tablero
            self.tablero_texto = self.controlador.obtener_representacion_tablero()

            # Verificar estado del juego
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
        """
        Vuelve al menú principal.

        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Volver al Menú". Simplemente cambiamos la pantalla actual a la pantalla
        de menú.
        """
        self.manager.current = "menu"
