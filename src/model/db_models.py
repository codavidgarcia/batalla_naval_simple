"""
Modelos ORM para la base de datos de Batalla Naval.
Este archivo define los modelos SQLAlchemy para interactuar con la base de datos.

Autor: Juan David
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

# Crear la base para los modelos declarativos
Base = declarative_base()

# Hola Jona: Aquí definimos las tablas de la base de datos usando SQLAlchemy.
# SQLAlchemy es un ORM (Object-Relational Mapping) que nos permite trabajar
# con la base de datos usando objetos Python en lugar de SQL directamente.

# Definir la tabla de asociación entre jugador y juego
jugador_juego = Table(
    'jugador_juego',
    Base.metadata,
    Column('id_jugador', Integer, ForeignKey('jugador.id_jugador'), primary_key=True),
    Column('id_juego', Integer, ForeignKey('juego.id_juego'), primary_key=True)
)

# Definir la tabla de asociación entre nave y celda
nave_celda = Table(
    'nave_celda',
    Base.metadata,
    Column('id_nave', Integer, ForeignKey('nave.id_nave'), primary_key=True),
    Column('id_celda', Integer, ForeignKey('celda.id_celda'), primary_key=True)
)

class Jugador(Base):
    """Modelo para la tabla jugador."""
    __tablename__ = 'jugador'
    
    id_jugador = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    contraseña = Column(String, nullable=False)
    
    # Relaciones
    juegos = relationship("Juego", secondary=jugador_juego, back_populates="jugadores")
    campos = relationship("Campo", back_populates="jugador")
    puntuaciones = relationship("Puntuacion", back_populates="jugador")
    
    def __repr__(self):
        return f"<Jugador(id={self.id_jugador}, nombre={self.nombre_usuario})>"

    # Hola Jona: Esta clase representa la tabla 'jugador' en la base de datos.
    # Cada atributo de la clase corresponde a una columna en la tabla.
    # Las relaciones definen cómo esta tabla se relaciona con otras tablas.

class Juego(Base):
    """Modelo para la tabla juego."""
    __tablename__ = 'juego'
    
    id_juego = Column(Integer, primary_key=True)
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(20), default='en curso')
    
    # Relaciones
    jugadores = relationship("Jugador", secondary=jugador_juego, back_populates="juegos")
    campos = relationship("Campo", back_populates="juego")
    puntuaciones = relationship("Puntuacion", back_populates="juego")
    
    def __repr__(self):
        return f"<Juego(id={self.id_juego}, estado={self.estado})>"

    # Hola Jona: Esta clase representa la tabla 'juego' en la base de datos.
    # La relación con jugadores es muchos a muchos, por eso usamos una tabla
    # intermedia (jugador_juego).

class Campo(Base):
    """Modelo para la tabla campo."""
    __tablename__ = 'campo'
    
    id_campo = Column(Integer, primary_key=True)
    id_jugador = Column(Integer, ForeignKey('jugador.id_jugador'), nullable=False)
    id_juego = Column(Integer, ForeignKey('juego.id_juego'), nullable=False)
    ancho = Column(Integer, nullable=False)
    alto = Column(Integer, nullable=False)
    num_naves = Column(Integer, nullable=False)
    naves_restantes = Column(Integer, nullable=False)
    
    # Relaciones
    jugador = relationship("Jugador", back_populates="campos")
    juego = relationship("Juego", back_populates="campos")
    celdas = relationship("Celda", back_populates="campo", cascade="all, delete-orphan")
    naves = relationship("Nave", back_populates="campo", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Campo(id={self.id_campo}, tamaño={self.ancho}x{self.alto})>"

    # Hola Jona: Esta clase representa la tabla 'campo' en la base de datos.
    # Un campo pertenece a un jugador y a un juego específicos.
    # El parámetro cascade="all, delete-orphan" significa que si eliminamos
    # un campo, también se eliminarán todas sus celdas y naves.

class Celda(Base):
    """Modelo para la tabla celda."""
    __tablename__ = 'celda'
    
    id_celda = Column(Integer, primary_key=True)
    id_campo = Column(Integer, ForeignKey('campo.id_campo'), nullable=False)
    fila = Column(Integer, nullable=False)
    columna = Column(Integer, nullable=False)
    fue_disparada = Column(Boolean, default=False)
    
    # Restricción única para evitar celdas duplicadas en el mismo campo
    __table_args__ = (
        UniqueConstraint('id_campo', 'fila', 'columna', name='uq_celda_campo_posicion'),
    )
    
    # Relaciones
    campo = relationship("Campo", back_populates="celdas")
    naves = relationship("Nave", secondary=nave_celda, back_populates="celdas")
    
    def __repr__(self):
        return f"<Celda(id={self.id_celda}, fila={self.fila}, columna={self.columna}, disparada={self.fue_disparada})>"

    # Hola Jona: Esta clase representa la tabla 'celda' en la base de datos.
    # Cada celda pertenece a un campo y puede estar asociada a una nave.
    # La restricción única asegura que no puede haber dos celdas en la misma
    # posición del mismo campo.

class Nave(Base):
    """Modelo para la tabla nave."""
    __tablename__ = 'nave'
    
    id_nave = Column(Integer, primary_key=True)
    id_campo = Column(Integer, ForeignKey('campo.id_campo'), nullable=False)
    tipo = Column(String(30), nullable=False)
    tamaño = Column(Integer, nullable=False)
    esta_destruida = Column(Boolean, default=False)
    
    # Relaciones
    campo = relationship("Campo", back_populates="naves")
    celdas = relationship("Celda", secondary=nave_celda, back_populates="naves")
    
    def __repr__(self):
        return f"<Nave(id={self.id_nave}, tipo={self.tipo}, tamaño={self.tamaño})>"

    # Hola Jona: Esta clase representa la tabla 'nave' en la base de datos.
    # Cada nave pertenece a un campo y puede ocupar varias celdas.
    # La relación con celdas es muchos a muchos, por eso usamos una tabla
    # intermedia (nave_celda).

class Puntuacion(Base):
    """Modelo para la tabla puntuacion."""
    __tablename__ = 'puntuacion'
    
    id_puntuacion = Column(Integer, primary_key=True)
    id_jugador = Column(Integer, ForeignKey('jugador.id_jugador'), nullable=False)
    id_juego = Column(Integer, ForeignKey('juego.id_juego'), nullable=False)
    puntos = Column(Integer, default=0)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    jugador = relationship("Jugador", back_populates="puntuaciones")
    juego = relationship("Juego", back_populates="puntuaciones")
    
    def __repr__(self):
        return f"<Puntuacion(id={self.id_puntuacion}, jugador_id={self.id_jugador}, puntos={self.puntos})>"

    # Hola Jona: Esta clase representa la tabla 'puntuacion' en la base de datos.
    # Cada puntuación está asociada a un jugador y a un juego específicos.

# Clase para gestionar la conexión a la base de datos
class DatabaseManager:
    """Clase para gestionar la conexión a la base de datos."""
    
    def __init__(self, db_url=None):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_url (str, optional): URL de conexión a la base de datos.
                Si no se proporciona, se usará SQLite en memoria.
        """
        if db_url is None:
            # Si no se proporciona una URL, usar SQLite en un archivo
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'datos', 'batalla_naval.db')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            db_url = f'sqlite:///{db_path}'
        
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Crea todas las tablas en la base de datos."""
        Base.metadata.create_all(self.engine)
        
    def drop_tables(self):
        """Elimina todas las tablas de la base de datos."""
        Base.metadata.drop_all(self.engine)
        
    def get_session(self):
        """Obtiene una nueva sesión de la base de datos."""
        return self.Session()

    # Hola Jona: Esta clase gestiona la conexión a la base de datos.
    # Proporciona métodos para crear y eliminar tablas, y para obtener
    # una sesión para interactuar con la base de datos.
