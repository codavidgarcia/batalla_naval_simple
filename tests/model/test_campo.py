"""
Pruebas unitarias para la clase Campo.

Este módulo contiene pruebas para verificar el funcionamiento
correcto de la clase Campo del modelo.

Autor: Juan David
"""

import unittest
from src.model.campo import Campo

class TestCampo(unittest.TestCase):
    """
    Pruebas para la clase Campo.
    """

    def test_inicializacion(self):
        """Prueba la inicialización de un campo."""
        campo = Campo(5, 5, 3)

        self.assertEqual(campo.ancho, 5)
        self.assertEqual(campo.alto, 5)
        self.assertEqual(len(campo.tablero), 5)  # 5 filas
        self.assertEqual(len(campo.tablero[0]), 5)  # 5 columnas
        self.assertEqual(len(campo.naves), 3)
        self.assertEqual(campo.naves_restantes, 3)

    def test_inicializacion_valores_invalidos(self):
        """Prueba la inicialización con valores inválidos."""
        # Ancho y alto deben ser al menos 1
        with self.assertRaises(ValueError):
            Campo(0, 5, 1)

        with self.assertRaises(ValueError):
            Campo(5, 0, 1)

        # Número de naves debe ser al menos 1
        with self.assertRaises(ValueError):
            Campo(5, 5, 0)

        # Número de naves no puede ser mayor que el número de celdas
        with self.assertRaises(ValueError):
            Campo(2, 2, 5)

    def test_colocar_naves(self):
        """Prueba la colocación de naves en el campo."""
        campo = Campo(5, 5, 3)

        # Verificar que se colocaron 3 naves
        self.assertEqual(len(campo.naves), 3)

        # Verificar que cada nave tiene una posición válida
        for nave in campo.naves:
            for pos in nave.posiciones:
                fila, columna = pos
                self.assertTrue(0 <= fila < campo.alto)
                self.assertTrue(0 <= columna < campo.ancho)
                self.assertTrue(campo.tablero[fila][columna].contiene_nave)

    def test_evaluar_disparo_agua(self):
        """Prueba evaluar un disparo al agua."""
        campo = Campo(3, 3, 1)

        # Encontrar una celda sin nave
        fila_sin_nave, columna_sin_nave = None, None
        for i in range(campo.alto):
            for j in range(campo.ancho):
                if not campo.tablero[i][j].contiene_nave:
                    fila_sin_nave, columna_sin_nave = i, j
                    break
            if fila_sin_nave is not None:
                break

        # Disparar a la celda sin nave
        resultado = campo.evaluar_disparo(fila_sin_nave, columna_sin_nave)
        self.assertFalse(resultado)  # No impactó una nave
        self.assertTrue(campo.tablero[fila_sin_nave][columna_sin_nave].impactada)

    def test_evaluar_disparo_nave(self):
        """Prueba evaluar un disparo a una nave."""
        campo = Campo(3, 3, 1)

        # Encontrar una celda con nave
        fila_con_nave, columna_con_nave = None, None
        for i in range(campo.alto):
            for j in range(campo.ancho):
                if campo.tablero[i][j].contiene_nave:
                    fila_con_nave, columna_con_nave = i, j
                    break
            if fila_con_nave is not None:
                break

        # Disparar a la celda con nave
        resultado = campo.evaluar_disparo(fila_con_nave, columna_con_nave)
        self.assertTrue(resultado)  # Impactó una nave
        self.assertTrue(campo.tablero[fila_con_nave][columna_con_nave].impactada)

    def test_evaluar_disparo_fuera_de_rango(self):
        """Prueba evaluar un disparo fuera del rango del campo."""
        campo = Campo(3, 3, 1)

        with self.assertRaises(ValueError):
            campo.evaluar_disparo(3, 0)

        with self.assertRaises(ValueError):
            campo.evaluar_disparo(0, 3)

        with self.assertRaises(ValueError):
            campo.evaluar_disparo(-1, 0)

    def test_evaluar_disparo_celda_ya_disparada(self):
        """Prueba evaluar un disparo a una celda que ya fue disparada."""
        campo = Campo(3, 3, 1)

        # Disparar a una celda
        campo.evaluar_disparo(0, 0)

        # Disparar nuevamente a la misma celda
        with self.assertRaises(ValueError):
            campo.evaluar_disparo(0, 0)

    def test_mostrar_tablero(self):
        """Prueba mostrar el tablero."""
        campo = Campo(2, 2, 1)

        representacion = campo.mostrar_tablero()

        # Verificar que la representación tiene el formato esperado
        self.assertIsInstance(representacion, str)
        self.assertIn("0 1", representacion)  # Encabezado de columnas
        self.assertIn("0", representacion)    # Número de fila
        self.assertIn("1", representacion)    # Número de fila
        self.assertIn("~", representacion)    # Celda de agua

if __name__ == '__main__':
    unittest.main()
