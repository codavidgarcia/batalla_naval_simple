"""
Pruebas unitarias para la clase Juego.

Este módulo contiene pruebas para verificar el funcionamiento
correcto de la clase Juego del modelo.

Autor: Juan David
"""

import unittest
from src.model.juego import Juego

class TestJuego(unittest.TestCase):
    """
    Pruebas para la clase Juego.
    """

    def test_inicializacion(self):
        """Prueba la inicialización de un juego."""
        juego = Juego(5, 5, 3)

        self.assertIsNotNone(juego.campo)
        self.assertEqual(juego.campo.ancho, 5)
        self.assertEqual(juego.campo.alto, 5)
        self.assertEqual(len(juego.campo.naves), 3)
        self.assertFalse(juego.esta_terminado())

    def test_inicializacion_valores_invalidos(self):
        """Prueba la inicialización con valores inválidos."""
        # Ancho y alto deben ser al menos 1
        with self.assertRaises(ValueError):
            Juego(0, 5, 1)

        with self.assertRaises(ValueError):
            Juego(5, 0, 1)

        # Número de naves debe ser al menos 1
        with self.assertRaises(ValueError):
            Juego(5, 5, 0)

        # Número de naves no puede ser mayor que el número de celdas
        with self.assertRaises(ValueError):
            Juego(2, 2, 5)

    def test_realizar_disparo(self):
        """Prueba realizar un disparo en el juego."""
        juego = Juego(3, 3, 1)

        # Realizar un disparo
        resultado = juego.realizar_disparo(0, 0)

        # El resultado debe ser un booleano
        self.assertIsInstance(resultado, bool)

        # La celda debe estar disparada
        self.assertTrue(juego.campo.tablero[0][0].impactada)

    def test_realizar_disparo_fuera_de_rango(self):
        """Prueba realizar un disparo fuera del rango del campo."""
        juego = Juego(3, 3, 1)

        with self.assertRaises(ValueError):
            juego.realizar_disparo(3, 0)

        with self.assertRaises(ValueError):
            juego.realizar_disparo(0, 3)

        with self.assertRaises(ValueError):
            juego.realizar_disparo(-1, 0)

    def test_realizar_disparo_celda_ya_disparada(self):
        """Prueba realizar un disparo a una celda que ya fue disparada."""
        juego = Juego(3, 3, 1)

        juego.realizar_disparo(0, 0)

        with self.assertRaises(ValueError):
            juego.realizar_disparo(0, 0)

    def test_esta_terminado(self):
        """Prueba verificar si el juego está terminado."""
        juego = Juego(3, 3, 1)

        # El juego no debería estar terminado inicialmente
        self.assertFalse(juego.esta_terminado())

        # Encontrar y disparar a todas las celdas con naves
        for i in range(juego.campo.alto):
            for j in range(juego.campo.ancho):
                if juego.campo.tablero[i][j].contiene_nave:
                    juego.realizar_disparo(i, j)

        # El juego debería estar terminado
        self.assertTrue(juego.esta_terminado())

    def test_reiniciar(self):
        """Prueba reiniciar el juego."""
        juego = Juego(3, 3, 1)

        # Realizar un disparo
        juego.realizar_disparo(0, 0)

        # Reiniciar el juego
        juego.reiniciar()

        # Verificar que el juego se reinició correctamente
        self.assertFalse(juego.esta_terminado())

        # Verificar que ninguna celda fue disparada
        for i in range(juego.campo.alto):
            for j in range(juego.campo.ancho):
                self.assertFalse(juego.campo.tablero[i][j].impactada)

    def test_obtener_representacion_tablero(self):
        """Prueba obtener la representación del tablero."""
        juego = Juego(2, 2, 1)

        representacion = juego.obtener_representacion_tablero()

        # Verificar que la representación tiene el formato esperado
        self.assertIsInstance(representacion, str)
        self.assertIn("0 1", representacion)  # Encabezado de columnas
        self.assertIn("0", representacion)    # Número de fila
        self.assertIn("1", representacion)    # Número de fila
        self.assertIn("~", representacion)    # Celda de agua

if __name__ == '__main__':
    unittest.main()
