"""
Pruebas unitarias para la clase Nave.

Este módulo contiene pruebas para verificar el funcionamiento
correcto de la clase Nave del modelo.

Autor: Juan David
"""

import unittest
from src.model.nave import Nave

class TestNave(unittest.TestCase):
    """
    Pruebas para la clase Nave.
    """

    def test_inicializacion(self):
        """Prueba la inicialización de una nave."""
        posiciones = [(0, 0), (0, 1), (0, 2)]
        nave = Nave(posiciones)

        self.assertEqual(nave.posiciones, posiciones)
        self.assertEqual(len(nave.posiciones), 3)
        self.assertFalse(nave.esta_destruida())
        self.assertEqual(len(nave.impactos), 0)

    def test_verificar_impacto_positivo(self):
        """Prueba verificar un impacto positivo en la nave."""
        posiciones = [(1, 1), (1, 2)]
        nave = Nave(posiciones)

        # Verificar impacto en una posición de la nave
        resultado = nave.verificar_impacto((1, 1))

        self.assertTrue(resultado)
        self.assertEqual(len(nave.impactos), 1)
        self.assertTrue((1, 1) in nave.impactos)

    def test_verificar_impacto_negativo(self):
        """Prueba verificar un impacto negativo (fuera de la nave)."""
        posiciones = [(1, 1), (1, 2)]
        nave = Nave(posiciones)

        # Verificar impacto en una posición fuera de la nave
        resultado = nave.verificar_impacto((0, 0))

        self.assertFalse(resultado)
        self.assertEqual(len(nave.impactos), 0)

    def test_verificar_impacto_repetido(self):
        """Prueba verificar un impacto en una posición ya impactada."""
        posiciones = [(1, 1), (1, 2)]
        nave = Nave(posiciones)

        # Primer impacto
        nave.verificar_impacto((1, 1))

        # Segundo impacto en la misma posición
        resultado = nave.verificar_impacto((1, 1))

        self.assertFalse(resultado)
        self.assertEqual(len(nave.impactos), 1)

    def test_esta_destruida_parcial(self):
        """Prueba verificar si una nave está destruida (parcialmente impactada)."""
        posiciones = [(1, 1), (1, 2), (1, 3)]
        nave = Nave(posiciones)

        # Impactar solo una posición
        nave.verificar_impacto((1, 1))

        # La nave no debería estar destruida
        self.assertFalse(nave.esta_destruida())

    def test_esta_destruida_completa(self):
        """Prueba verificar si una nave está destruida (completamente impactada)."""
        posiciones = [(1, 1), (1, 2)]
        nave = Nave(posiciones)

        # Impactar todas las posiciones
        nave.verificar_impacto((1, 1))
        nave.verificar_impacto((1, 2))

        # La nave debería estar destruida
        self.assertTrue(nave.esta_destruida())

if __name__ == '__main__':
    unittest.main()
