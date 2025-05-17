"""
Pruebas unitarias para la clase Controlador.

Este módulo contiene pruebas para verificar el funcionamiento
correcto de la clase Controlador.

Autor: Juan David
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.controller.controlador import Controlador
from src.model.jugador import Jugador

class TestControlador(unittest.TestCase):
    """
    Pruebas para la clase Controlador.
    """

    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear una instancia del controlador con una base de datos en memoria
        from src.model.db_models import DatabaseManager
        db_manager = DatabaseManager(db_url='sqlite:///:memory:')
        db_manager.create_tables()
        session = db_manager.get_session()

        # Crear una instancia del controlador con la sesión de base de datos en memoria
        self.controlador = Controlador(db_manager=db_manager, session=session)

        # Limpiar la lista de jugadores para las pruebas
        self.controlador.jugadores = []

    def tearDown(self):
        """Limpieza después de las pruebas."""
        # Cerrar la sesión
        if self.controlador.session:
            self.controlador.session.close()

    def test_inicializacion(self):
        """Prueba la inicialización del controlador."""
        self.assertIsNone(self.controlador.juego)
        self.assertIsNone(self.controlador.jugador_activo)
        self.assertIsInstance(self.controlador.jugadores, list)
        self.assertIsNotNone(self.controlador.db_manager)
        self.assertIsNotNone(self.controlador.session)

    def test_iniciar_juego(self):
        """Prueba iniciar un juego."""
        self.controlador.iniciar_juego(5, 5, 3)

        self.assertIsNotNone(self.controlador.juego)
        self.assertEqual(self.controlador.juego.campo.ancho, 5)
        self.assertEqual(self.controlador.juego.campo.alto, 5)
        self.assertEqual(len(self.controlador.juego.campo.naves), 3)

    def test_iniciar_juego_con_jugador_activo(self):
        """Prueba iniciar un juego con un jugador activo."""
        # Registrar un jugador e iniciar sesión
        self.controlador.registrar_jugador("usuario_test", "contraseña123")
        self.controlador.iniciar_sesion("usuario_test", "contraseña123")

        # Iniciar un juego
        self.controlador.iniciar_juego(5, 5, 3)

        self.assertIsNotNone(self.controlador.juego)
        self.assertEqual(self.controlador.juego.campo.ancho, 5)
        self.assertEqual(self.controlador.juego.campo.alto, 5)
        self.assertEqual(len(self.controlador.juego.campo.naves), 3)

    def test_iniciar_juego_valores_invalidos(self):
        """Prueba iniciar un juego con valores inválidos."""
        # Ancho inválido
        with self.assertRaises(ValueError):
            self.controlador.iniciar_juego(0, 5, 3)

        # Alto inválido
        with self.assertRaises(ValueError):
            self.controlador.iniciar_juego(5, 0, 3)

        # Número de naves inválido
        with self.assertRaises(ValueError):
            self.controlador.iniciar_juego(5, 5, 0)

    def test_realizar_disparo(self):
        """Prueba realizar un disparo."""
        # Iniciar un juego
        self.controlador.iniciar_juego(3, 3, 1)

        # Realizar un disparo
        resultado = self.controlador.realizar_disparo(0, 0)

        # El resultado debe ser un booleano
        self.assertIsInstance(resultado, bool)

    def test_realizar_disparo_sin_juego(self):
        """Prueba realizar un disparo sin un juego activo."""
        with self.assertRaises(ValueError):
            self.controlador.realizar_disparo(0, 0)

    def test_realizar_disparo_fuera_de_rango(self):
        """Prueba realizar un disparo fuera del rango del tablero."""
        # Iniciar un juego
        self.controlador.iniciar_juego(3, 3, 1)

        # Realizar un disparo fuera del rango
        with self.assertRaises(ValueError):
            self.controlador.realizar_disparo(3, 0)

    def test_realizar_disparo_celda_ya_disparada(self):
        """Prueba realizar un disparo a una celda que ya fue disparada."""
        # Iniciar un juego
        self.controlador.iniciar_juego(3, 3, 1)

        # Realizar un disparo
        self.controlador.realizar_disparo(0, 0)

        # Realizar otro disparo en la misma celda
        with self.assertRaises(ValueError):
            self.controlador.realizar_disparo(0, 0)

    def test_registrar_jugador(self):
        """Prueba registrar un jugador."""
        resultado = self.controlador.registrar_jugador("usuario_test", "contraseña123")

        self.assertTrue(resultado)
        self.assertEqual(len(self.controlador.jugadores), 1)
        self.assertEqual(self.controlador.jugadores[0].nombre_usuario, "usuario_test")

    def test_registrar_jugador_existente(self):
        """Prueba registrar un jugador con un nombre que ya existe."""
        # Registrar un jugador
        self.controlador.registrar_jugador("usuario_test", "contraseña123")

        # Intentar registrar otro jugador con el mismo nombre
        resultado = self.controlador.registrar_jugador("usuario_test", "otra_contraseña")

        self.assertFalse(resultado)
        self.assertEqual(len(self.controlador.jugadores), 1)

    def test_registrar_jugador_nombre_vacio(self):
        """Prueba registrar un jugador con un nombre vacío."""
        resultado = self.controlador.registrar_jugador("", "contraseña123")

        self.assertFalse(resultado)
        self.assertEqual(len(self.controlador.jugadores), 0)

    def test_registrar_jugador_contraseña_vacia(self):
        """Prueba registrar un jugador con una contraseña vacía."""
        resultado = self.controlador.registrar_jugador("usuario_test", "")

        self.assertFalse(resultado)
        self.assertEqual(len(self.controlador.jugadores), 0)

    def test_registrar_multiples_jugadores(self):
        """Prueba registrar múltiples jugadores."""
        # Registrar varios jugadores
        self.controlador.registrar_jugador("usuario1", "contraseña1")
        self.controlador.registrar_jugador("usuario2", "contraseña2")
        self.controlador.registrar_jugador("usuario3", "contraseña3")

        self.assertEqual(len(self.controlador.jugadores), 3)

    def test_iniciar_sesion(self):
        """Prueba iniciar sesión con un jugador existente."""
        # Registrar un jugador
        self.controlador.registrar_jugador("usuario_test", "contraseña123")

        # Iniciar sesión
        resultado = self.controlador.iniciar_sesion("usuario_test", "contraseña123")

        self.assertTrue(resultado)
        self.assertIsNotNone(self.controlador.jugador_activo)
        self.assertEqual(self.controlador.jugador_activo.nombre_usuario, "usuario_test")

    def test_iniciar_sesion_credenciales_incorrectas(self):
        """Prueba iniciar sesión con credenciales incorrectas."""
        # Registrar un jugador
        self.controlador.registrar_jugador("usuario_test", "contraseña123")

        # Intentar iniciar sesión con contraseña incorrecta
        resultado = self.controlador.iniciar_sesion("usuario_test", "contraseña_incorrecta")

        self.assertFalse(resultado)
        self.assertIsNone(self.controlador.jugador_activo)

    def test_iniciar_sesion_usuario_no_existente(self):
        """Prueba iniciar sesión con un usuario que no existe."""
        resultado = self.controlador.iniciar_sesion("usuario_inexistente", "contraseña123")

        self.assertFalse(resultado)
        self.assertIsNone(self.controlador.jugador_activo)

    def test_iniciar_sesion_multiples_veces(self):
        """Prueba iniciar sesión múltiples veces con diferentes usuarios."""
        # Registrar varios jugadores
        self.controlador.registrar_jugador("usuario1", "contraseña1")
        self.controlador.registrar_jugador("usuario2", "contraseña2")

        # Iniciar sesión con el primer usuario
        self.controlador.iniciar_sesion("usuario1", "contraseña1")
        self.assertEqual(self.controlador.jugador_activo.nombre_usuario, "usuario1")

        # Iniciar sesión con el segundo usuario
        self.controlador.iniciar_sesion("usuario2", "contraseña2")
        self.assertEqual(self.controlador.jugador_activo.nombre_usuario, "usuario2")

    def test_actualizar_puntaje(self):
        """Prueba actualizar el puntaje del jugador activo."""
        # Registrar un jugador e iniciar sesión
        self.controlador.registrar_jugador("usuario_test", "contraseña123")
        self.controlador.iniciar_sesion("usuario_test", "contraseña123")

        # Actualizar el puntaje
        nuevo_puntaje = self.controlador.actualizar_puntaje(10)

        self.assertEqual(nuevo_puntaje, 10)
        self.assertEqual(self.controlador.jugador_activo.puntaje, 10)

    def test_actualizar_puntaje_sin_jugador_activo(self):
        """Prueba actualizar el puntaje sin un jugador activo."""
        resultado = self.controlador.actualizar_puntaje(10)

        self.assertIsNone(resultado)

    def test_actualizar_puntaje_multiples_veces(self):
        """Prueba actualizar el puntaje múltiples veces."""
        # Registrar un jugador e iniciar sesión
        self.controlador.registrar_jugador("usuario_test", "contraseña123")
        self.controlador.iniciar_sesion("usuario_test", "contraseña123")

        # Actualizar el puntaje varias veces
        self.controlador.actualizar_puntaje(10)
        self.controlador.actualizar_puntaje(5)
        nuevo_puntaje = self.controlador.actualizar_puntaje(3)

        self.assertEqual(nuevo_puntaje, 18)
        self.assertEqual(self.controlador.jugador_activo.puntaje, 18)

    def test_actualizar_puntaje_negativo(self):
        """Prueba actualizar el puntaje con un valor negativo."""
        # Registrar un jugador e iniciar sesión
        self.controlador.registrar_jugador("usuario_test", "contraseña123")
        self.controlador.iniciar_sesion("usuario_test", "contraseña123")

        # Establecer un puntaje inicial
        self.controlador.actualizar_puntaje(20)

        # Actualizar con un valor negativo
        nuevo_puntaje = self.controlador.actualizar_puntaje(-5)

        self.assertEqual(nuevo_puntaje, 15)
        self.assertEqual(self.controlador.jugador_activo.puntaje, 15)

    def test_obtener_representacion_tablero(self):
        """Prueba obtener la representación del tablero."""
        # Iniciar un juego
        self.controlador.iniciar_juego(3, 3, 1)

        representacion = self.controlador.obtener_representacion_tablero()

        self.assertIsInstance(representacion, str)
        self.assertIn("0 1 2", representacion)  # Encabezado de columnas

    def test_obtener_representacion_tablero_sin_juego(self):
        """Prueba obtener la representación del tablero sin un juego activo."""
        representacion = self.controlador.obtener_representacion_tablero()

        self.assertEqual(representacion, "No hay un juego activo")

    def test_obtener_representacion_tablero_despues_de_disparo(self):
        """Prueba obtener la representación del tablero después de un disparo."""
        # Iniciar un juego
        self.controlador.iniciar_juego(3, 3, 1)

        # Realizar un disparo
        self.controlador.realizar_disparo(0, 0)

        representacion = self.controlador.obtener_representacion_tablero()

        self.assertIsInstance(representacion, str)
        # Debería contener un marcador de disparo (O o X)
        self.assertTrue("O" in representacion or "X" in representacion)

    def test_reiniciar_juego(self):
        """Prueba reiniciar el juego."""
        # Iniciar un juego
        self.controlador.iniciar_juego(3, 3, 1)

        # Realizar un disparo
        self.controlador.realizar_disparo(0, 0)

        # Reiniciar el juego
        resultado = self.controlador.reiniciar_juego()

        self.assertTrue(resultado)
        # Verificar que la celda ya no está disparada
        self.assertFalse(self.controlador.juego.campo.tablero[0][0].impactada)

    def test_reiniciar_juego_sin_juego(self):
        """Prueba reiniciar el juego sin un juego activo."""
        resultado = self.controlador.reiniciar_juego()

        self.assertFalse(resultado)

    def test_juego_terminado(self):
        """Prueba verificar si el juego está terminado."""
        # Iniciar un juego
        self.controlador.iniciar_juego(3, 3, 1)

        # El juego no debería estar terminado inicialmente
        self.assertFalse(self.controlador.juego_terminado())

    def test_juego_terminado_sin_juego(self):
        """Prueba verificar si el juego está terminado sin un juego activo."""
        resultado = self.controlador.juego_terminado()

        self.assertFalse(resultado)

    def test_juego_terminado_despues_de_destruir_naves(self):
        """Prueba verificar si el juego está terminado después de destruir todas las naves."""
        # Iniciar un juego
        self.controlador.iniciar_juego(3, 3, 1)

        # Encontrar y disparar a todas las celdas con naves
        for i in range(self.controlador.juego.campo.alto):
            for j in range(self.controlador.juego.campo.ancho):
                if self.controlador.juego.campo.tablero[i][j].contiene_nave:
                    self.controlador.realizar_disparo(i, j)

        # El juego debería estar terminado
        self.assertTrue(self.controlador.juego_terminado())

    def test_obtener_puntuaciones(self):
        """Prueba obtener las puntuaciones."""
        # Registrar un jugador e iniciar sesión
        self.controlador.registrar_jugador("usuario_test", "contraseña123")
        self.controlador.iniciar_sesion("usuario_test", "contraseña123")

        # Actualizar el puntaje
        self.controlador.actualizar_puntaje(10)

        # Obtener las puntuaciones
        puntuaciones = self.controlador.obtener_puntuaciones()

        self.assertIsInstance(puntuaciones, list)

    def test_obtener_puntuaciones_multiples_jugadores(self):
        """Prueba obtener las puntuaciones con múltiples jugadores."""
        # Registrar varios jugadores
        self.controlador.registrar_jugador("usuario1", "contraseña1")
        self.controlador.registrar_jugador("usuario2", "contraseña2")

        # Iniciar sesión y actualizar puntaje del primer jugador
        self.controlador.iniciar_sesion("usuario1", "contraseña1")
        self.controlador.actualizar_puntaje(10)

        # Iniciar sesión y actualizar puntaje del segundo jugador
        self.controlador.iniciar_sesion("usuario2", "contraseña2")
        self.controlador.actualizar_puntaje(20)

        # Obtener las puntuaciones
        puntuaciones = self.controlador.obtener_puntuaciones()

        self.assertIsInstance(puntuaciones, list)
        # Debería haber al menos 2 puntuaciones
        self.assertTrue(len(puntuaciones) >= 2)

    def test_obtener_puntuaciones_limite(self):
        """Prueba obtener las puntuaciones con un límite."""
        # Registrar varios jugadores
        self.controlador.registrar_jugador("usuario1", "contraseña1")
        self.controlador.registrar_jugador("usuario2", "contraseña2")
        self.controlador.registrar_jugador("usuario3", "contraseña3")

        # Iniciar sesión y actualizar puntaje de cada jugador
        self.controlador.iniciar_sesion("usuario1", "contraseña1")
        self.controlador.actualizar_puntaje(10)

        self.controlador.iniciar_sesion("usuario2", "contraseña2")
        self.controlador.actualizar_puntaje(20)

        self.controlador.iniciar_sesion("usuario3", "contraseña3")
        self.controlador.actualizar_puntaje(30)

        # Obtener las puntuaciones con límite 2
        puntuaciones = self.controlador.obtener_puntuaciones(2)

        # Debería haber exactamente 2 puntuaciones
        self.assertTrue(len(puntuaciones) <= 2)

if __name__ == '__main__':
    unittest.main()
