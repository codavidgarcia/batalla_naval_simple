"""
Módulo que define la clase Jugador para el juego Batalla Naval.

Este módulo contiene la implementación de la clase Jugador, que representa
a un jugador del juego Batalla Naval.

Autor: Juan David
"""

class Jugador:
    """
    Representa a un jugador del juego Batalla Naval.

    Esta clase almacena la información de un jugador, incluyendo su nombre
    de usuario, contraseña y puntaje.

    Atributos:
        nombre_usuario (str): Nombre de usuario del jugador.
        contraseña (str): Contraseña del jugador.
        puntaje (int): Puntaje acumulado del jugador.

    Métodos:
        actualizar_puntaje(puntos): Añade puntos al puntaje actual del jugador.

    Ejemplo de uso:
        jugador = Jugador("usuario1", "contraseña123")
        jugador.actualizar_puntaje(10)  # Añade 10 puntos
        print(jugador.puntaje)  # Muestra 10
    """

    def __init__(self, nombre_usuario, contraseña):
        """
        Inicializa un nuevo jugador.

        Args:
            nombre_usuario (str): Nombre de usuario del jugador.
            contraseña (str): Contraseña del jugador.

        Raises:
            ValueError: Si el nombre de usuario o la contraseña están vacíos.

        Hola Jona: Aquí estamos creando un nuevo jugador con su nombre de usuario
        y contraseña. También inicializamos su puntaje en 0. En una aplicación
        real, deberíamos almacenar la contraseña de forma segura (con hash),
        pero para simplificar, la guardamos como texto plano.
        """
        if not nombre_usuario:
            raise ValueError("El nombre de usuario no puede estar vacío")
        if not contraseña:
            raise ValueError("La contraseña no puede estar vacía")

        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.puntaje = 0

    def actualizar_puntaje(self, puntos):
        """
        Añade puntos al puntaje actual del jugador.

        Args:
            puntos (int): Cantidad de puntos a añadir.

        Returns:
            int: Nuevo puntaje del jugador.

        Hola Jona: Este método actualiza el puntaje del jugador añadiendo
        la cantidad de puntos especificada. Por ejemplo, si el jugador gana
        una partida, podríamos llamar a este método para añadir 10 puntos.
        """
        self.puntaje += puntos
        return self.puntaje

    def __str__(self):
        """
        Devuelve una representación en cadena del jugador.

        Returns:
            str: Representación del jugador.
        """
        return f"Jugador: {self.nombre_usuario}, Puntaje: {self.puntaje}"
