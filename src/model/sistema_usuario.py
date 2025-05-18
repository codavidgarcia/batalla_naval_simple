from src.model.jugador import Jugador
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

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

        try:
            print("Inicializando la base de datos...")
            # Conexión a PostgreSQL
            self.engine = create_engine('postgresql://batalla_naval:password123@localhost/batalla_naval')

            Base.metadata.create_all(self.engine)

            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            self._cargar_jugadores()
            print("Base de datos inicializada correctamente.")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {str(e)}")
            import traceback
            traceback.print_exc()

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

        try:
            jugador_existente = self.session.query(JugadorDB).filter_by(nombre_usuario=nombre).first()
            if jugador_existente:
                print(f"El jugador {nombre} ya existe en la base de datos.")
                return False

            nuevo_jugador_db = JugadorDB(nombre_usuario=nombre, contraseña=contraseña)
            self.session.add(nuevo_jugador_db)
            self.session.commit()
            print(f"Jugador {nombre} creado en la base de datos con ID: {nuevo_jugador_db.id_jugador}")

            nuevo_jugador = Jugador(nombre, contraseña)
            self.jugadores_registrados.append(nuevo_jugador)

            return True
        except Exception as e:
            print(f"Error al registrar jugador en la base de datos: {str(e)}")
            import traceback
            traceback.print_exc()
            self.session.rollback()
            return False

    def iniciar_sesion(self, nombre, contraseña):
        try:
            jugador_db = self.session.query(JugadorDB).filter_by(
                nombre_usuario=nombre,
                contraseña=contraseña
            ).first()

            if not jugador_db:
                print(f"Credenciales incorrectas para el usuario {nombre}")
                return None

            print(f"Inicio de sesión exitoso para {nombre} con ID: {jugador_db.id_jugador}")

            for jugador in self.jugadores_registrados:
                if jugador.nombre_usuario == nombre:
                    print(f"Jugador {nombre} encontrado en memoria")
                    return jugador

            nuevo_jugador = Jugador(nombre, contraseña)
            self.jugadores_registrados.append(nuevo_jugador)
            print(f"Jugador {nombre} creado en memoria")

            return nuevo_jugador
        except Exception as e:
            print(f"Error al iniciar sesión: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
