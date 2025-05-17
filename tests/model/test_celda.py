"""
Pruebas unitarias para la clase Celda.

Este módulo contiene pruebas para verificar el funcionamiento
correcto de la clase Celda del modelo.

Autor: Juan David
"""

import unittest
from src.model.celda import Celda

class TestCelda(unittest.TestCase):
    """
    Pruebas para la clase Celda.
    """

    def test_inicializacion(self):
        """Prueba la inicialización de una celda."""
        celda = Celda()
        self.assertFalse(celda.contiene_nave)
        self.assertFalse(celda.impactada)

    def test_asignar_nave(self):
        """Prueba asignar una nave a una celda."""
        celda = Celda()
        celda.contiene_nave = True
        self.assertTrue(celda.contiene_nave)

    def test_disparar_agua(self):
        """Prueba disparar a una celda sin nave."""
        celda = Celda()
        resultado = celda.recibir_disparo()
        self.assertFalse(resultado)  # No impactó una nave
        self.assertTrue(celda.impactada)

    def test_disparar_nave(self):
        """Prueba disparar a una celda con nave."""
        celda = Celda()
        celda.contiene_nave = True
        resultado = celda.recibir_disparo()
        self.assertTrue(resultado)  # Impactó una nave
        self.assertTrue(celda.impactada)

    def test_disparar_celda_ya_disparada(self):
        """Prueba disparar a una celda que ya fue disparada."""
        celda = Celda()
        celda.recibir_disparo()
        with self.assertRaises(ValueError):
            celda.recibir_disparo()

    def test_representacion_celda_agua(self):
        """Prueba la representación de una celda de agua."""
        celda = Celda()
        self.assertEqual(str(celda), "~")

    def test_representacion_celda_agua_disparada(self):
        """Prueba la representación de una celda de agua disparada."""
        celda = Celda()
        celda.recibir_disparo()
        self.assertEqual(str(celda), "O")

    def test_representacion_celda_nave(self):
        """Prueba la representación de una celda con nave."""
        celda = Celda()
        celda.contiene_nave = True
        self.assertEqual(str(celda), "~")  # No se muestra la nave

    def test_representacion_celda_nave_disparada(self):
        """Prueba la representación de una celda con nave disparada."""
        celda = Celda()
        celda.contiene_nave = True
        celda.recibir_disparo()
        self.assertEqual(str(celda), "X")

if __name__ == '__main__':
    unittest.main()
