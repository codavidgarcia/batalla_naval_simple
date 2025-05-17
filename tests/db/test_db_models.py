"""
Pruebas unitarias para los modelos de la base de datos.

Este módulo contiene pruebas para verificar el funcionamiento
correcto de los modelos ORM de la base de datos.

Autor: Juan David
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import patch
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from src.model.db_models import (
    Base, DatabaseManager, Jugador, Juego, Campo, Celda, Nave, Puntuacion
)

class TestDBModels(unittest.TestCase):
    """
    Pruebas para los modelos de la base de datos.
    """

    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Usar SQLite en memoria para las pruebas
        self.db_manager = DatabaseManager(db_url='sqlite:///:memory:')
        self.db_manager.create_tables()
        self.session = self.db_manager.get_session()

    def tearDown(self):
        """Limpieza después de las pruebas."""
        # Cerrar la sesión
        self.session.close()

    def test_crear_jugador(self):
        """Prueba crear un jugador en la base de datos."""
        # Crear un jugador
        jugador = Jugador(nombre_usuario="usuario_test", contraseña="contraseña123")

        # Añadir a la sesión y guardar
        self.session.add(jugador)
        self.session.commit()

        # Verificar que se guardó correctamente
        jugador_db = self.session.query(Jugador).filter_by(nombre_usuario="usuario_test").first()

        self.assertIsNotNone(jugador_db)
        self.assertEqual(jugador_db.nombre_usuario, "usuario_test")
        self.assertEqual(jugador_db.contraseña, "contraseña123")

    def test_crear_juego(self):
        """Prueba crear un juego en la base de datos."""
        # Crear un jugador
        jugador = Jugador(nombre_usuario="usuario_test", contraseña="contraseña123")
        self.session.add(jugador)
        self.session.commit()

        # Crear un juego
        juego = Juego(estado="activo")
        juego.jugadores.append(jugador)

        # Añadir a la sesión y guardar
        self.session.add(juego)
        self.session.commit()

        # Verificar que se guardó correctamente
        juego_db = self.session.query(Juego).first()

        self.assertIsNotNone(juego_db)
        self.assertEqual(juego_db.estado, "activo")
        self.assertIsInstance(juego_db.fecha_inicio, datetime)
        self.assertEqual(len(juego_db.jugadores), 1)
        self.assertEqual(juego_db.jugadores[0].nombre_usuario, "usuario_test")

    def test_crear_campo(self):
        """Prueba crear un campo en la base de datos."""
        # Crear un jugador
        jugador = Jugador(nombre_usuario="usuario_test", contraseña="contraseña123")
        self.session.add(jugador)
        self.session.commit()

        # Crear un juego
        juego = Juego(estado="activo")
        juego.jugadores.append(jugador)
        self.session.add(juego)
        self.session.commit()

        # Crear un campo
        campo = Campo(
            id_jugador=jugador.id_jugador,
            id_juego=juego.id_juego,
            ancho=5,
            alto=5,
            num_naves=3,
            naves_restantes=3
        )

        # Añadir a la sesión y guardar
        self.session.add(campo)
        self.session.commit()

        # Verificar que se guardó correctamente
        campo_db = self.session.query(Campo).first()

        self.assertIsNotNone(campo_db)
        self.assertEqual(campo_db.ancho, 5)
        self.assertEqual(campo_db.alto, 5)
        self.assertEqual(campo_db.num_naves, 3)
        self.assertEqual(campo_db.naves_restantes, 3)
        self.assertEqual(campo_db.id_jugador, jugador.id_jugador)
        self.assertEqual(campo_db.id_juego, juego.id_juego)

    def test_crear_celda(self):
        """Prueba crear una celda en la base de datos."""
        # Crear un jugador
        jugador = Jugador(nombre_usuario="usuario_test", contraseña="contraseña123")
        self.session.add(jugador)
        self.session.commit()

        # Crear un juego
        juego = Juego(estado="activo")
        juego.jugadores.append(jugador)
        self.session.add(juego)
        self.session.commit()

        # Crear un campo
        campo = Campo(
            id_jugador=jugador.id_jugador,
            id_juego=juego.id_juego,
            ancho=5,
            alto=5,
            num_naves=3,
            naves_restantes=3
        )
        self.session.add(campo)
        self.session.commit()

        # Crear una celda
        celda = Celda(
            id_campo=campo.id_campo,
            fila=2,
            columna=3,
            fue_disparada=False
        )

        # Añadir a la sesión y guardar
        self.session.add(celda)
        self.session.commit()

        # Verificar que se guardó correctamente
        celda_db = self.session.query(Celda).first()

        self.assertIsNotNone(celda_db)
        self.assertEqual(celda_db.fila, 2)
        self.assertEqual(celda_db.columna, 3)
        self.assertFalse(celda_db.fue_disparada)
        self.assertEqual(celda_db.id_campo, campo.id_campo)

    def test_crear_nave(self):
        """Prueba crear una nave en la base de datos."""
        # Crear un jugador
        jugador = Jugador(nombre_usuario="usuario_test", contraseña="contraseña123")
        self.session.add(jugador)
        self.session.commit()

        # Crear un juego
        juego = Juego(estado="activo")
        juego.jugadores.append(jugador)
        self.session.add(juego)
        self.session.commit()

        # Crear un campo
        campo = Campo(
            id_jugador=jugador.id_jugador,
            id_juego=juego.id_juego,
            ancho=5,
            alto=5,
            num_naves=3,
            naves_restantes=3
        )
        self.session.add(campo)
        self.session.commit()

        # Crear una nave
        nave = Nave(
            id_campo=campo.id_campo,
            tipo="Submarino",
            tamaño=3,
            esta_destruida=False
        )

        # Añadir a la sesión y guardar
        self.session.add(nave)
        self.session.commit()

        # Verificar que se guardó correctamente
        nave_db = self.session.query(Nave).first()

        self.assertIsNotNone(nave_db)
        self.assertEqual(nave_db.tipo, "Submarino")
        self.assertEqual(nave_db.tamaño, 3)
        self.assertFalse(nave_db.esta_destruida)
        self.assertEqual(nave_db.id_campo, campo.id_campo)

    def test_crear_puntuacion(self):
        """Prueba crear una puntuación en la base de datos."""
        # Crear un jugador
        jugador = Jugador(nombre_usuario="usuario_test", contraseña="contraseña123")
        self.session.add(jugador)
        self.session.commit()

        # Crear un juego
        juego = Juego(estado="terminado")
        juego.jugadores.append(jugador)
        self.session.add(juego)
        self.session.commit()

        # Crear una puntuación
        puntuacion = Puntuacion(
            id_jugador=jugador.id_jugador,
            id_juego=juego.id_juego,
            puntos=100
        )

        # Añadir a la sesión y guardar
        self.session.add(puntuacion)
        self.session.commit()

        # Verificar que se guardó correctamente
        puntuacion_db = self.session.query(Puntuacion).first()

        self.assertIsNotNone(puntuacion_db)
        self.assertEqual(puntuacion_db.puntos, 100)
        self.assertEqual(puntuacion_db.id_jugador, jugador.id_jugador)
        self.assertEqual(puntuacion_db.id_juego, juego.id_juego)
        self.assertIsInstance(puntuacion_db.fecha, datetime)

    def test_relacion_jugador_juego(self):
        """Prueba la relación entre jugador y juego."""
        # Crear un jugador
        jugador = Jugador(nombre_usuario="usuario_test", contraseña="contraseña123")
        self.session.add(jugador)
        self.session.commit()

        # Crear dos juegos
        juego1 = Juego(estado="activo")
        juego2 = Juego(estado="terminado")

        # Asociar los juegos al jugador
        jugador.juegos.append(juego1)
        jugador.juegos.append(juego2)

        # Guardar
        self.session.add_all([juego1, juego2])
        self.session.commit()

        # Verificar las relaciones
        jugador_db = self.session.query(Jugador).first()

        self.assertEqual(len(jugador_db.juegos), 2)
        self.assertEqual(jugador_db.juegos[0].estado, "activo")
        self.assertEqual(jugador_db.juegos[1].estado, "terminado")

        # Verificar la relación inversa
        juego_db = self.session.query(Juego).filter_by(estado="activo").first()

        self.assertEqual(len(juego_db.jugadores), 1)
        self.assertEqual(juego_db.jugadores[0].nombre_usuario, "usuario_test")

if __name__ == '__main__':
    unittest.main()
