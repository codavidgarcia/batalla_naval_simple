"""
Módulo que define la clase Campo para el juego Batalla Naval.

Este módulo contiene la implementación de la clase Campo, que representa
el tablero de juego donde se colocan las naves y se realizan los disparos.

Autor: Juan David
"""

import random
from src.model.celda import Celda
from src.model.nave import Nave

class Campo:
    """
    Representa el tablero de juego donde se colocan las naves.

    El campo es una matriz de celdas donde se colocan las naves y se realizan
    los disparos. Cada celda puede contener parte de una nave o estar vacía.

    Atributos:
        ancho (int): Número de columnas del tablero.
        alto (int): Número de filas del tablero.
        num_naves (int): Número total de naves en el tablero.
        naves_restantes (int): Número de naves que aún no han sido destruidas.
        tablero (list): Matriz de objetos Celda que representa el tablero.
        naves (list): Lista de objetos Nave colocados en el tablero.

    Métodos:
        colocar_naves(): Coloca las naves aleatoriamente en el tablero.
        evaluar_disparo(fila, columna): Evalúa un disparo en las coordenadas especificadas.
        mostrar_tablero(): Muestra el estado actual del tablero.

    Ejemplo de uso:
        campo = Campo(10, 10, 5)  # Tablero de 10x10 con 5 naves
        impacto = campo.evaluar_disparo(3, 4)  # Realiza un disparo en (3, 4)
        campo.mostrar_tablero()  # Muestra el estado actual del tablero
    """

    def __init__(self, ancho, alto, num_naves):
        """
        Inicializa un nuevo campo de juego.

        Args:
            ancho (int): Número de columnas del tablero.
            alto (int): Número de filas del tablero.
            num_naves (int): Número de naves a colocar en el tablero.

        Raises:
            ValueError: Si los parámetros no son válidos.

        Hola Jona: Aquí estamos creando el tablero de juego. Primero validamos
        que los parámetros sean correctos (no negativos, tamaño adecuado, etc.).
        Luego inicializamos el tablero como una matriz de celdas vacías y
        colocamos las naves aleatoriamente.
        """
        # Validar parámetros
        if ancho <= 0 or alto <= 0 or num_naves <= 0:
            raise ValueError("Los parámetros deben ser positivos")

        if ancho < 2 or alto < 2:
            raise ValueError("El tamaño mínimo del tablero es 2x2")

        if num_naves > ancho * alto:
            raise ValueError("No se pueden colocar más naves que celdas disponibles")

        # Inicializar atributos
        self.ancho = ancho
        self.alto = alto
        self.num_naves = num_naves
        self.naves_restantes = num_naves

        # Crear tablero vacío (matriz de celdas)
        self.tablero = []
        for i in range(alto):
            fila = []
            for j in range(ancho):
                fila.append(Celda())
            self.tablero.append(fila)

        # Lista para almacenar las naves
        self.naves = []

        # Colocar naves aleatoriamente
        self.colocar_naves()

    def colocar_naves(self):
        """
        Coloca las naves aleatoriamente en el tablero.

        Este método coloca el número especificado de naves en posiciones
        aleatorias del tablero, asegurándose de que no se superpongan.

        Hola Jona: Este método coloca las naves en el tablero de forma aleatoria.
        Para simplificar, cada nave ocupa solo una celda (como submarinos).
        Generamos coordenadas aleatorias y verificamos que la celda no contenga
        ya otra nave. Si está libre, colocamos una nueva nave en esa posición.
        """
        naves_colocadas = 0

        while naves_colocadas < self.num_naves:
            # Generar coordenadas aleatorias
            fila = random.randint(0, self.alto - 1)
            columna = random.randint(0, self.ancho - 1)

            # Verificar si la celda está libre
            if not self.tablero[fila][columna].contiene_nave:
                # Marcar la celda como ocupada por una nave
                self.tablero[fila][columna].contiene_nave = True

                # Crear una nueva nave en esta posición
                nueva_nave = Nave([(fila, columna)])
                self.naves.append(nueva_nave)

                naves_colocadas += 1

    def evaluar_disparo(self, fila, columna):
        """
        Evalúa un disparo en las coordenadas especificadas.

        Args:
            fila (int): Fila donde se realiza el disparo.
            columna (int): Columna donde se realiza el disparo.

        Returns:
            bool: True si el disparo impactó una nave, False si fue al agua.

        Raises:
            ValueError: Si las coordenadas están fuera del tablero o la celda ya fue impactada.

        Hola Jona: Este método evalúa lo que ocurre cuando un jugador dispara a
        una celda específica. Primero verificamos que las coordenadas sean válidas
        (dentro del tablero). Luego verificamos si alguna nave está en esa posición.
        Si hay una nave, registramos el impacto y verificamos si la nave ha sido
        destruida. Si todas las naves han sido destruidas, el juego termina.
        """
        # Validar coordenadas
        if fila < 0 or fila >= self.alto or columna < 0 or columna >= self.ancho:
            raise ValueError("Coordenadas fuera del tablero")

        # Obtener la celda
        celda = self.tablero[fila][columna]

        # Verificar si la celda ya fue impactada
        if celda.impactada:
            raise ValueError("Esta celda ya ha sido impactada")

        # Verificar impacto en naves
        for nave in self.naves:
            if nave.verificar_impacto((fila, columna)):
                # La nave fue impactada
                celda.recibir_disparo()

                # Verificar si la nave fue destruida
                if nave.esta_destruida():
                    self.naves_restantes -= 1

                return True

        # No impactó ninguna nave
        celda.recibir_disparo()
        return False

    def mostrar_tablero(self):
        """
        Muestra el estado actual del tablero.

        Returns:
            str: Representación del tablero como texto.

        Hola Jona: Este método genera una representación visual del tablero
        para mostrar al jugador. Cada celda se representa con un carácter:
        '~' para agua, 'X' para nave impactada, 'O' para disparo al agua.
        """
        representacion = ""

        # Añadir encabezado de columnas
        representacion += "  " + " ".join(str(i) for i in range(self.ancho)) + "\n"

        # Añadir filas con números
        for i in range(self.alto):
            representacion += f"{i} " + " ".join(str(celda) for celda in self.tablero[i]) + "\n"

        return representacion
