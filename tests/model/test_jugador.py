"""
Pruebas unitarias para la clase Jugador.

Este módulo contiene pruebas para verificar el funcionamiento
correcto de la clase Jugador del modelo.

Autor: Juan David
"""

import unittest
from src.model.jugador import Jugador

class TestJugador(unittest.TestCase):
    """
    Pruebas para la clase Jugador.
    """

    def test_inicializacion(self):
        """Prueba la inicialización de un jugador."""
        jugador = Jugador("usuario1", "contraseña123")

        self.assertEqual(jugador.nombre_usuario, "usuario1")
        self.assertEqual(jugador.contraseña, "contraseña123")
        self.assertEqual(jugador.puntaje, 0)

    def test_inicializacion_valores_invalidos(self):
        """Prueba la inicialización con valores inválidos."""
        # Nombre de usuario no puede estar vacío
        with self.assertRaises(ValueError):
            Jugador("", "contraseña123")

        # Contraseña no puede estar vacía
        with self.assertRaises(ValueError):
            Jugador("usuario1", "")

    def test_actualizar_puntaje(self):
        """Prueba actualizar el puntaje de un jugador."""
        jugador = Jugador("usuario1", "contraseña123")

        # Actualizar el puntaje
        nuevo_puntaje = jugador.actualizar_puntaje(10)

        self.assertEqual(nuevo_puntaje, 10)
        self.assertEqual(jugador.puntaje, 10)

        # Actualizar el puntaje nuevamente
        nuevo_puntaje = jugador.actualizar_puntaje(5)

        self.assertEqual(nuevo_puntaje, 15)
        self.assertEqual(jugador.puntaje, 15)

    def test_actualizar_puntaje_negativo(self):
        """Prueba actualizar el puntaje con un valor negativo."""
        jugador = Jugador("usuario1", "contraseña123")

        # Establecer un puntaje inicial
        jugador.actualizar_puntaje(20)

        # Actualizar con un valor negativo
        nuevo_puntaje = jugador.actualizar_puntaje(-5)

        self.assertEqual(nuevo_puntaje, 15)
        self.assertEqual(jugador.puntaje, 15)

    def test_actualizar_puntaje_cero(self):
        """Prueba actualizar el puntaje con cero."""
        jugador = Jugador("usuario1", "contraseña123")

        # Establecer un puntaje inicial
        jugador.actualizar_puntaje(10)

        # Actualizar con cero
        nuevo_puntaje = jugador.actualizar_puntaje(0)

        self.assertEqual(nuevo_puntaje, 10)
        self.assertEqual(jugador.puntaje, 10)

    def test_representacion_jugador(self):
        """Prueba la representación de un jugador."""
        jugador = Jugador("usuario1", "contraseña123")

        representacion = str(jugador)

        self.assertIn("usuario1", representacion)
        self.assertNotIn("contraseña123", representacion)  # La contraseña no debe aparecer

if __name__ == '__main__':
    unittest.main()
