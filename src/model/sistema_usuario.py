from src.model.jugador import Jugador
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from src.model.json_storage import JSONStorage

Base = declarative_base()

class JugadorDB(Base):
    __tablename__ = 'jugador'

    id_jugador = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    contraseña = Column(String, nullable=False)

    puntuaciones = relationship("PuntuacionDB", back_populates="jugador", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Jugador(id={self.id_jugador}, nombre={self.nombre_usuario})>"

class PuntuacionDB(Base):
    __tablename__ = 'puntuacion'

    id_puntuacion = Column(Integer, primary_key=True)
    id_jugador = Column(Integer, ForeignKey('jugador.id_jugador'), nullable=False)
    puntos = Column(Integer, default=0)
    fecha = Column(DateTime, default=datetime.now)

    jugador = relationship("JugadorDB", back_populates="puntuaciones")

    def __repr__(self):
        return f"<Puntuacion(id={self.id_puntuacion}, jugador_id={self.id_jugador}, puntos={self.puntos})>"

class SistemaUsuario:
    def __init__(self):
        self.jugadores_registrados = []
        self.db_ok = False
        self.json_storage = None

        try:
            print("Intentando inicializar PostgreSQL...")
            # Conexión a PostgreSQL
            self.engine = create_engine('postgresql://batalla_naval:password123@localhost/batalla_naval')

            Base.metadata.create_all(self.engine)

            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            self._cargar_jugadores()
            self.db_ok = True
            print("PostgreSQL inicializado correctamente.")
        except Exception as e:
            print(f"Error al inicializar PostgreSQL: {str(e)}")
            print("Usando JSON como almacenamiento (fallback)...")
            self.json_storage = JSONStorage()
            print("Almacenamiento JSON inicializado correctamente.")

    def _cargar_jugadores(self):
        try:
            jugadores_db = self.session.query(JugadorDB).all()
            print(f"Jugadores encontrados en la base de datos: {len(jugadores_db)}")

            for jugador_db in jugadores_db:
                jugador = Jugador(jugador_db.nombre_usuario, jugador_db.contraseña)
                print(f"Cargando jugador: {jugador_db.nombre_usuario}")

                puntuaciones = self.session.query(PuntuacionDB).filter_by(id_jugador=jugador_db.id_jugador).all()
                print(f"Puntuaciones encontradas para {jugador_db.nombre_usuario}: {len(puntuaciones)}")

                if puntuaciones:
                    max_puntaje = max(p.puntos for p in puntuaciones)
                    jugador.puntaje = max_puntaje
                    print(f"Puntaje máximo para {jugador_db.nombre_usuario}: {max_puntaje}")

                self.jugadores_registrados.append(jugador)
        except Exception as e:
            print(f"Error al cargar jugadores: {str(e)}")
            import traceback
            traceback.print_exc()

    def registrar_jugador(self, nombre, contraseña):
        if not nombre or nombre.strip() == "":
            return False

        for jugador in self.jugadores_registrados:
            if jugador.nombre_usuario == nombre:
                return False

        # Si PostgreSQL está disponible, usarlo
        if self.db_ok:
            try:
                jugador_existente = self.session.query(JugadorDB).filter_by(nombre_usuario=nombre).first()
                if jugador_existente:
                    print(f"El jugador {nombre} ya existe en la base de datos.")
                    return False

                nuevo_jugador_db = JugadorDB(nombre_usuario=nombre, contraseña=contraseña)
                self.session.add(nuevo_jugador_db)
                self.session.commit()
                print(f"Jugador {nombre} creado en PostgreSQL con ID: {nuevo_jugador_db.id_jugador}")

                nuevo_jugador = Jugador(nombre, contraseña)
                self.jugadores_registrados.append(nuevo_jugador)

                return True
            except Exception as e:
                print(f"Error al registrar jugador en PostgreSQL: {str(e)}")
                import traceback
                traceback.print_exc()
                self.session.rollback()

                # Si falla PostgreSQL, intentar con JSON
                print("Intentando registrar jugador con JSON (fallback)...")
                return self._registrar_jugador_json(nombre, contraseña)
        else:
            # Usar JSON como fallback
            return self._registrar_jugador_json(nombre, contraseña)

    def _registrar_jugador_json(self, nombre, contraseña):
        try:
            resultado = self.json_storage.registrar_jugador(nombre, contraseña)
            if resultado:
                print(f"Jugador {nombre} registrado correctamente en JSON.")
                nuevo_jugador = Jugador(nombre, contraseña)
                self.jugadores_registrados.append(nuevo_jugador)
            return resultado
        except Exception as e:
            print(f"Error al registrar jugador en JSON: {str(e)}")
            return False

    def iniciar_sesion(self, nombre, contraseña):
        # Si PostgreSQL está disponible, usarlo
        if self.db_ok:
            try:
                jugador_db = self.session.query(JugadorDB).filter_by(
                    nombre_usuario=nombre,
                    contraseña=contraseña
                ).first()

                if not jugador_db:
                    print(f"Credenciales incorrectas para el usuario {nombre} en PostgreSQL")
                    return None

                print(f"Inicio de sesión exitoso para {nombre} con ID: {jugador_db.id_jugador} en PostgreSQL")

                for jugador in self.jugadores_registrados:
                    if jugador.nombre_usuario == nombre:
                        print(f"Jugador {nombre} encontrado en memoria")
                        return jugador

                nuevo_jugador = Jugador(nombre, contraseña)
                nuevo_jugador.id = jugador_db.id_jugador
                self.jugadores_registrados.append(nuevo_jugador)
                print(f"Jugador {nombre} creado en memoria")

                return nuevo_jugador
            except Exception as e:
                print(f"Error al iniciar sesión en PostgreSQL: {str(e)}")
                import traceback
                traceback.print_exc()

                # Si falla PostgreSQL, intentar con JSON
                print("Intentando iniciar sesión con JSON (fallback)...")
                return self._iniciar_sesion_json(nombre, contraseña)
        else:
            # Usar JSON como fallback
            return self._iniciar_sesion_json(nombre, contraseña)

    def _iniciar_sesion_json(self, nombre, contraseña):
        try:
            jugador_json = self.json_storage.iniciar_sesion(nombre, contraseña)
            if jugador_json:
                print(f"Inicio de sesión exitoso para {nombre} en JSON")

                for jugador in self.jugadores_registrados:
                    if jugador.nombre_usuario == nombre:
                        print(f"Jugador {nombre} encontrado en memoria")
                        return jugador

                nuevo_jugador = Jugador(nombre, contraseña)
                nuevo_jugador.id = jugador_json['id']
                self.jugadores_registrados.append(nuevo_jugador)
                print(f"Jugador {nombre} creado en memoria desde JSON")

                return nuevo_jugador
            else:
                print(f"Credenciales incorrectas para el usuario {nombre} en JSON")
                return None
        except Exception as e:
            print(f"Error al iniciar sesión en JSON: {str(e)}")
            return None

    def obtener_puntuaciones(self, limite=10):
        """Obtiene las puntuaciones más altas de los jugadores."""
        # Si PostgreSQL está disponible, usarlo
        if self.db_ok:
            try:
                # Consulta para obtener las puntuaciones más altas
                puntuaciones = self.session.query(
                    JugadorDB.nombre_usuario,
                    PuntuacionDB.puntos,
                    PuntuacionDB.fecha
                ).join(
                    PuntuacionDB, JugadorDB.id_jugador == PuntuacionDB.id_jugador
                ).order_by(
                    PuntuacionDB.puntos.desc()
                ).limit(limite).all()

                # Formatear resultados
                resultado = []
                for p in puntuaciones:
                    resultado.append({
                        'nombre_usuario': p[0],
                        'puntaje': p[1],
                        'fecha': p[2].isoformat() if p[2] else None
                    })

                return resultado
            except Exception as e:
                print(f"Error al obtener puntuaciones de PostgreSQL: {str(e)}")
                import traceback
                traceback.print_exc()

                # Si falla PostgreSQL, intentar con JSON
                print("Intentando obtener puntuaciones con JSON (fallback)...")
                return self._obtener_puntuaciones_json(limite)
        else:
            # Usar JSON como fallback
            return self._obtener_puntuaciones_json(limite)

    def _obtener_puntuaciones_json(self, limite=10):
        """Obtiene las puntuaciones más altas de los jugadores desde JSON."""
        try:
            return self.json_storage.obtener_puntuaciones(limite)
        except Exception as e:
            print(f"Error al obtener puntuaciones de JSON: {str(e)}")
            return []

    def actualizar_puntuacion(self, jugador, puntos):
        """Actualiza la puntuación de un jugador."""
        if not jugador or not hasattr(jugador, 'id') or jugador.id is None:
            print("No se puede actualizar la puntuación: jugador no válido o sin ID")
            return None

        # Si PostgreSQL está disponible, usarlo
        if self.db_ok:
            try:
                # Crear nueva puntuación
                nueva_puntuacion = PuntuacionDB(id_jugador=jugador.id, puntos=puntos)
                self.session.add(nueva_puntuacion)
                self.session.commit()
                print(f"Puntuación {puntos} registrada para {jugador.nombre_usuario} en PostgreSQL")

                # Actualizar el objeto jugador
                jugador.puntaje = puntos
                return puntos
            except Exception as e:
                print(f"Error al actualizar puntuación en PostgreSQL: {str(e)}")
                self.session.rollback()

                # Si falla PostgreSQL, intentar con JSON
                print("Intentando actualizar puntuación con JSON (fallback)...")
                return self._actualizar_puntuacion_json(jugador, puntos)
        else:
            # Usar JSON como fallback
            return self._actualizar_puntuacion_json(jugador, puntos)

    def _actualizar_puntuacion_json(self, jugador, puntos):
        """Actualiza la puntuación de un jugador en JSON."""
        try:
            resultado = self.json_storage.actualizar_puntuacion(jugador.id, puntos)
            if resultado is not None:
                print(f"Puntuación {puntos} registrada para {jugador.nombre_usuario} en JSON")
                jugador.puntaje = puntos
            return resultado
        except Exception as e:
            print(f"Error al actualizar puntuación en JSON: {str(e)}")
            return None
