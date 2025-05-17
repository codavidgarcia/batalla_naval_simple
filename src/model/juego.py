"""
Módulo que define la clase Juego para el juego Batalla Naval.

Este módulo contiene la implementación de la clase Juego, que representa
una partida del juego Batalla Naval.

Autor: Juan David
"""

from src.model.campo import Campo

class Juego:
    """
    Representa una partida del juego Batalla Naval.

    Esta clase gestiona la lógica principal del juego, incluyendo la creación
    del campo, la realización de disparos y la verificación del estado del juego.

    Atributos:
        campo (Campo): El tablero de juego donde se colocan las naves.

    Métodos:
        realizar_disparo(fila, columna): Realiza un disparo en las coordenadas especificadas.
        esta_terminado(): Verifica si el juego ha terminado (todas las naves destruidas).
        reiniciar(): Reinicia el juego con los mismos parámetros.

    Ejemplo de uso:
        juego = Juego(10, 10, 5)  # Tablero de 10x10 con 5 naves
        impacto = juego.realizar_disparo(3, 4)  # Realiza un disparo en (3, 4)
        terminado = juego.esta_terminado()  # Verifica si el juego ha terminado
    """

    def __init__(self, ancho, alto, num_naves):
        """
        Inicializa una nueva partida del juego.

        Args:
            ancho (int): Número de columnas del tablero.
            alto (int): Número de filas del tablero.
            num_naves (int): Número de naves a colocar en el tablero.

        Hola Jona: Aquí estamos creando una nueva partida del juego. Guardamos
        los parámetros iniciales (ancho, alto, número de naves) para poder
        reiniciar el juego más tarde. Luego creamos el campo de juego con estos
        parámetros.
        """
        self.ancho = ancho
        self.alto = alto
        self.num_naves = num_naves
        self.campo = Campo(ancho, alto, num_naves)

    def realizar_disparo(self, fila, columna):
        """
        Realiza un disparo en las coordenadas especificadas.

        Args:
            fila (int): Fila donde se realiza el disparo.
            columna (int): Columna donde se realiza el disparo.

        Returns:
            bool: True si el disparo impactó una nave, False si fue al agua.

        Raises:
            ValueError: Si las coordenadas están fuera del tablero o la celda ya fue impactada.

        Hola Jona: Este método es el que usa el jugador para realizar un disparo.
        Simplemente delegamos la acción al campo de juego, que se encarga de
        evaluar el impacto y actualizar el estado del juego.
        """
        return self.campo.evaluar_disparo(fila, columna)

    def esta_terminado(self):
        """
        Verifica si el juego ha terminado (todas las naves destruidas).

        Returns:
            bool: True si todas las naves han sido destruidas, False en caso contrario.

        Hola Jona: Este método verifica si el juego ha terminado. El juego termina
        cuando todas las naves han sido destruidas (naves_restantes = 0).
        """
        return self.campo.naves_restantes == 0

    def reiniciar(self):
        """
        Reinicia el juego con los mismos parámetros.

        Hola Jona: Este método reinicia el juego creando un nuevo campo con los
        mismos parámetros que tenía el juego original. Esto es útil cuando el
        jugador quiere jugar otra partida sin cambiar la configuración.
        """
        self.campo = Campo(self.ancho, self.alto, self.num_naves)

    def obtener_representacion_tablero(self):
        """
        Obtiene una representación visual del tablero.

        Returns:
            str: Representación del tablero como texto.

        Hola Jona: Este método obtiene una representación visual del tablero
        para mostrar al jugador. Delegamos esta tarea al campo de juego.
        """
        return self.campo.mostrar_tablero()
