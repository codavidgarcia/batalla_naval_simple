"""
Consultas ORM para la base de datos de Batalla Naval.
Este archivo define las funciones para realizar consultas a la base de datos utilizando SQLAlchemy.

Autor: Juan David
"""

from sqlalchemy import func, desc, and_, or_, not_
from sqlalchemy.exc import IntegrityError
from src.model.db_models import Jugador, Juego, Campo, Celda, Nave, Puntuacion, nave_celda

class JugadorQueries:
    """Consultas relacionadas con los jugadores."""

    @staticmethod
    def crear_jugador(session, nombre_usuario, contraseña):
        """
        Crea un nuevo jugador en la base de datos.

        Args:
            session: Sesión de SQLAlchemy
            nombre_usuario (str): Nombre de usuario
            contraseña (str): Contraseña del usuario

        Returns:
            Jugador: Objeto jugador creado, o None si hubo un error

        Hola Jona: Este método crea un nuevo jugador en la base de datos.
        Primero verificamos si ya existe un jugador con ese nombre de usuario.
        Si no existe, creamos un nuevo jugador y lo añadimos a la sesión.
        """
        try:
            # Verificar si ya existe un jugador con ese nombre
            jugador_existente = session.query(Jugador).filter(Jugador.nombre_usuario == nombre_usuario).first()
            if jugador_existente:
                return None

            # Crear el jugador
            nuevo_jugador = Jugador(
                nombre_usuario=nombre_usuario,
                contraseña=contraseña
            )

            # Añadir a la sesión y confirmar
            session.add(nuevo_jugador)
            session.commit()

            return nuevo_jugador
        except IntegrityError:
            # Error de integridad (por ejemplo, nombre de usuario duplicado)
            session.rollback()
            return None
        except Exception as e:
            session.rollback()
            print(f"Error al crear jugador: {str(e)}")
            return None

    @staticmethod
    def verificar_credenciales(session, nombre_usuario, contraseña):
        """
        Verifica las credenciales de un jugador.

        Args:
            session: Sesión de SQLAlchemy
            nombre_usuario (str): Nombre de usuario
            contraseña (str): Contraseña del usuario

        Returns:
            Jugador: Objeto jugador si las credenciales son correctas, None en caso contrario

        Hola Jona: Este método verifica si las credenciales de un jugador son correctas.
        Buscamos un jugador con el nombre de usuario y contraseña proporcionados.
        Si lo encontramos, retornamos el objeto jugador. Si no, retornamos None.
        """
        try:
            # Buscar el jugador por nombre de usuario y contraseña
            jugador = session.query(Jugador).filter(
                Jugador.nombre_usuario == nombre_usuario,
                Jugador.contraseña == contraseña
            ).first()

            return jugador
        except Exception as e:
            print(f"Error al verificar credenciales: {str(e)}")
            return None

    @staticmethod
    def obtener_jugador_por_id(session, id_jugador):
        """
        Obtiene un jugador por su ID.

        Args:
            session: Sesión de SQLAlchemy
            id_jugador (int): ID del jugador

        Returns:
            Jugador: Objeto jugador, o None si no existe

        Hola Jona: Este método obtiene un jugador por su ID.
        Simplemente buscamos un jugador con el ID proporcionado.
        """
        return session.query(Jugador).filter(Jugador.id_jugador == id_jugador).first()

class JuegoQueries:
    """Consultas relacionadas con los juegos."""

    @staticmethod
    def crear_juego(session, jugador_id):
        """
        Crea un nuevo juego y lo asocia con un jugador.

        Args:
            session: Sesión de SQLAlchemy
            jugador_id (int): ID del jugador

        Returns:
            Juego: Objeto juego creado, o None si hubo un error

        Hola Jona: Este método crea un nuevo juego y lo asocia con un jugador.
        Primero obtenemos el jugador por su ID. Si existe, creamos un nuevo juego
        y lo asociamos con el jugador. Luego añadimos el juego a la sesión y confirmamos.
        """
        try:
            # Obtener el jugador
            jugador = session.query(Jugador).filter(Jugador.id_jugador == jugador_id).first()
            if not jugador:
                return None

            # Crear el juego
            nuevo_juego = Juego(estado='en curso')

            # Asociar el jugador al juego
            nuevo_juego.jugadores.append(jugador)

            # Añadir a la sesión y confirmar
            session.add(nuevo_juego)
            session.commit()

            return nuevo_juego
        except Exception as e:
            session.rollback()
            print(f"Error al crear juego: {str(e)}")
            return None

    @staticmethod
    def actualizar_estado_juego(session, juego_id, nuevo_estado):
        """
        Actualiza el estado de un juego.

        Args:
            session: Sesión de SQLAlchemy
            juego_id (int): ID del juego
            nuevo_estado (str): Nuevo estado del juego

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario

        Hola Jona: Este método actualiza el estado de un juego.
        Primero obtenemos el juego por su ID. Si existe, actualizamos su estado
        y confirmamos los cambios.
        """
        try:
            juego = session.query(Juego).filter(Juego.id_juego == juego_id).first()
            if not juego:
                return False

            juego.estado = nuevo_estado
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error al actualizar estado del juego: {str(e)}")
            return False

class CampoQueries:
    """Consultas relacionadas con los campos de juego."""

    @staticmethod
    def crear_campo(session, jugador_id, juego_id, ancho, alto, num_naves):
        """
        Crea un nuevo campo de juego.

        Args:
            session: Sesión de SQLAlchemy
            jugador_id (int): ID del jugador
            juego_id (int): ID del juego
            ancho (int): Ancho del campo
            alto (int): Alto del campo
            num_naves (int): Número de naves

        Returns:
            Campo: Objeto campo creado, o None si hubo un error

        Hola Jona: Este método crea un nuevo campo de juego.
        Un campo pertenece a un jugador y a un juego específicos.
        Creamos un nuevo campo con los parámetros proporcionados y lo añadimos a la sesión.
        """
        try:
            # Crear el campo
            nuevo_campo = Campo(
                id_jugador=jugador_id,
                id_juego=juego_id,
                ancho=ancho,
                alto=alto,
                num_naves=num_naves,
                naves_restantes=num_naves
            )

            # Añadir a la sesión y confirmar
            session.add(nuevo_campo)
            session.commit()

            return nuevo_campo
        except Exception as e:
            session.rollback()
            print(f"Error al crear campo: {str(e)}")
            return None

class CeldaQueries:
    """Consultas relacionadas con las celdas del campo."""

    @staticmethod
    def crear_celda(session, campo_id, fila, columna):
        """
        Crea una nueva celda en el campo.

        Args:
            session: Sesión de SQLAlchemy
            campo_id (int): ID del campo
            fila (int): Número de fila
            columna (int): Número de columna

        Returns:
            Celda: Objeto celda creado, o None si hubo un error

        Hola Jona: Este método crea una nueva celda en el campo.
        Cada celda tiene una posición (fila, columna) en el campo.
        Creamos una nueva celda con los parámetros proporcionados y la añadimos a la sesión.
        """
        try:
            # Crear la celda
            nueva_celda = Celda(
                id_campo=campo_id,
                fila=fila,
                columna=columna,
                fue_disparada=False
            )

            # Añadir a la sesión y confirmar
            session.add(nueva_celda)
            session.commit()

            return nueva_celda
        except IntegrityError:
            # Error de integridad (por ejemplo, celda duplicada)
            session.rollback()
            return None
        except Exception as e:
            session.rollback()
            print(f"Error al crear celda: {str(e)}")
            return None

    @staticmethod
    def marcar_disparo(session, campo_id, fila, columna):
        """
        Marca una celda como disparada.

        Args:
            session: Sesión de SQLAlchemy
            campo_id (int): ID del campo
            fila (int): Número de fila
            columna (int): Número de columna

        Returns:
            Celda: Objeto celda actualizado, o None si no existe

        Hola Jona: Este método marca una celda como disparada.
        Primero buscamos la celda por su posición en el campo.
        Si existe, la marcamos como disparada y confirmamos los cambios.
        """
        try:
            celda = session.query(Celda).filter(
                Celda.id_campo == campo_id,
                Celda.fila == fila,
                Celda.columna == columna
            ).first()

            if not celda:
                return None

            celda.fue_disparada = True
            session.commit()

            return celda
        except Exception as e:
            session.rollback()
            print(f"Error al marcar disparo: {str(e)}")
            return None

class NaveQueries:
    """Consultas relacionadas con las naves."""

    @staticmethod
    def crear_nave(session, campo_id, tipo, tamaño, celdas_ids):
        """
        Crea una nueva nave y la asocia con celdas.

        Args:
            session: Sesión de SQLAlchemy
            campo_id (int): ID del campo
            tipo (str): Tipo de nave
            tamaño (int): Tamaño de la nave
            celdas_ids (list): Lista de IDs de celdas que ocupa la nave

        Returns:
            Nave: Objeto nave creado, o None si hubo un error

        Hola Jona: Este método crea una nueva nave y la asocia con celdas.
        Primero creamos la nave con los parámetros proporcionados.
        Luego asociamos la nave con las celdas especificadas.
        """
        try:
            # Crear la nave
            nueva_nave = Nave(
                id_campo=campo_id,
                tipo=tipo,
                tamaño=tamaño,
                esta_destruida=False
            )

            # Añadir a la sesión
            session.add(nueva_nave)
            session.flush()  # Para obtener el ID de la nave

            # Asociar las celdas a la nave
            for celda_id in celdas_ids:
                celda = session.query(Celda).filter(Celda.id_celda == celda_id).first()
                if celda:
                    nueva_nave.celdas.append(celda)

            # Confirmar los cambios
            session.commit()

            return nueva_nave
        except Exception as e:
            session.rollback()
            print(f"Error al crear nave: {str(e)}")
            return None

    @staticmethod
    def verificar_nave_destruida(session, nave_id):
        """
        Verifica si una nave está destruida (todas sus celdas fueron disparadas).

        Args:
            session: Sesión de SQLAlchemy
            nave_id (int): ID de la nave

        Returns:
            bool: True si la nave está destruida, False en caso contrario

        Hola Jona: Este método verifica si una nave está destruida.
        Una nave está destruida cuando todas sus celdas han sido disparadas.
        Obtenemos la nave y sus celdas, y verificamos si todas las celdas han sido disparadas.
        """
        # Obtener la nave con sus celdas
        nave = session.query(Nave).filter(Nave.id_nave == nave_id).first()
        if not nave:
            return False

        # Verificar si todas las celdas de la nave fueron disparadas
        for celda in nave.celdas:
            if not celda.fue_disparada:
                return False

        return True

class PuntuacionQueries:
    """Consultas relacionadas con las puntuaciones."""

    @staticmethod
    def registrar_puntuacion(session, jugador_id, juego_id, puntos):
        """
        Registra una puntuación para un jugador en un juego.

        Args:
            session: Sesión de SQLAlchemy
            jugador_id (int): ID del jugador
            juego_id (int): ID del juego
            puntos (int): Puntos a registrar

        Returns:
            Puntuacion: Objeto puntuación creado, o None si hubo un error

        Hola Jona: Este método registra una puntuación para un jugador en un juego.
        Primero verificamos si ya existe una puntuación para este jugador y juego.
        Si existe, actualizamos la puntuación. Si no, creamos una nueva puntuación.
        """
        try:
            # Verificar si ya existe una puntuación para este jugador y juego
            puntuacion = session.query(Puntuacion).filter(
                Puntuacion.id_jugador == jugador_id,
                Puntuacion.id_juego == juego_id
            ).first()

            if puntuacion:
                # Actualizar puntuación existente
                puntuacion.puntos = puntos
            else:
                # Crear nueva puntuación
                puntuacion = Puntuacion(
                    id_jugador=jugador_id,
                    id_juego=juego_id,
                    puntos=puntos
                )
                session.add(puntuacion)

            session.commit()
            return puntuacion
        except Exception as e:
            session.rollback()
            print(f"Error al registrar puntuación: {str(e)}")
            return None
