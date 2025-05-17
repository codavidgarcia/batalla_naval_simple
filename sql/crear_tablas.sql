-- Script SQL para crear las tablas del juego Batalla Naval
-- Autor: Juan David

-- Hola Jona: Este script crea las tablas necesarias para almacenar los datos
-- del juego Batalla Naval en una base de datos PostgreSQL. Cada tabla representa
-- una entidad del juego (jugador, juego, campo, celda, nave) y las relaciones
-- entre ellas.

-- Eliminar tablas si existen para evitar conflictos
DROP TABLE IF EXISTS nave_celda CASCADE;
DROP TABLE IF EXISTS nave CASCADE;
DROP TABLE IF EXISTS celda CASCADE;
DROP TABLE IF EXISTS campo CASCADE;
DROP TABLE IF EXISTS puntuacion CASCADE;
DROP TABLE IF EXISTS jugador_juego CASCADE;
DROP TABLE IF EXISTS juego CASCADE;
DROP TABLE IF EXISTS jugador CASCADE;

-- Tabla de jugadores
CREATE TABLE jugador (
    id_jugador SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hola Jona: La tabla jugador almacena la información de los usuarios registrados.
-- SERIAL es un tipo de dato que genera automáticamente un número único para cada
-- nuevo jugador. PRIMARY KEY indica que id_jugador es la clave primaria de la tabla.
-- UNIQUE NOT NULL indica que nombre_usuario debe ser único y no puede ser nulo.

-- Tabla de juegos
CREATE TABLE juego (
    id_juego SERIAL PRIMARY KEY,
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'en curso'
);

-- Hola Jona: La tabla juego almacena la información de cada partida.
-- estado puede ser 'en curso', 'terminado', etc.

-- Tabla de relación entre jugadores y juegos
CREATE TABLE jugador_juego (
    id_jugador INT NOT NULL,
    id_juego INT NOT NULL,
    PRIMARY KEY (id_jugador, id_juego),
    FOREIGN KEY (id_jugador) REFERENCES jugador(id_jugador) ON DELETE CASCADE,
    FOREIGN KEY (id_juego) REFERENCES juego(id_juego) ON DELETE CASCADE
);

-- Hola Jona: La tabla jugador_juego es una tabla de relación que conecta
-- jugadores con juegos. Es necesaria porque un jugador puede participar en
-- muchos juegos y un juego puede tener varios jugadores (relación muchos a muchos).
-- PRIMARY KEY (id_jugador, id_juego) indica que la combinación de ambos campos
-- es la clave primaria de la tabla.
-- FOREIGN KEY ... REFERENCES ... indica que estos campos hacen referencia a
-- otras tablas. ON DELETE CASCADE significa que si se elimina un jugador o un
-- juego, también se eliminarán automáticamente sus registros relacionados.

-- Tabla de campos de juego
CREATE TABLE campo (
    id_campo SERIAL PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_juego INT NOT NULL,
    ancho INT NOT NULL,
    alto INT NOT NULL,
    num_naves INT NOT NULL,
    naves_restantes INT NOT NULL,
    FOREIGN KEY (id_jugador) REFERENCES jugador(id_jugador) ON DELETE CASCADE,
    FOREIGN KEY (id_juego) REFERENCES juego(id_juego) ON DELETE CASCADE
);

-- Hola Jona: La tabla campo almacena la información del tablero de juego.
-- Cada campo pertenece a un jugador en un juego específico.

-- Tabla de celdas
CREATE TABLE celda (
    id_celda SERIAL PRIMARY KEY,
    id_campo INT NOT NULL,
    fila INT NOT NULL,
    columna INT NOT NULL,
    fue_disparada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_campo) REFERENCES campo(id_campo) ON DELETE CASCADE,
    UNIQUE (id_campo, fila, columna)
);

-- Hola Jona: La tabla celda almacena la información de cada celda del tablero.
-- UNIQUE (id_campo, fila, columna) asegura que no pueda haber dos celdas
-- en la misma posición del mismo campo.

-- Tabla de naves
CREATE TABLE nave (
    id_nave SERIAL PRIMARY KEY,
    id_campo INT NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    tamaño INT NOT NULL,
    esta_destruida BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_campo) REFERENCES campo(id_campo) ON DELETE CASCADE
);

-- Hola Jona: La tabla nave almacena la información de cada nave en el juego.
-- tipo puede ser "Submarino", "Portaaviones", etc.
-- tamaño indica cuántas celdas ocupa la nave.

-- Tabla de relación entre naves y celdas
CREATE TABLE nave_celda (
    id_nave INT NOT NULL,
    id_celda INT NOT NULL,
    PRIMARY KEY (id_nave, id_celda),
    FOREIGN KEY (id_nave) REFERENCES nave(id_nave) ON DELETE CASCADE,
    FOREIGN KEY (id_celda) REFERENCES celda(id_celda) ON DELETE CASCADE
);

-- Hola Jona: La tabla nave_celda es una tabla de relación que conecta
-- naves con celdas. Es necesaria porque una nave puede ocupar varias celdas
-- y una celda puede contener parte de una nave (relación muchos a muchos).

-- Tabla de puntuaciones
CREATE TABLE puntuacion (
    id_puntuacion SERIAL PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_juego INT NOT NULL,
    puntos INT DEFAULT 0,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jugador) REFERENCES jugador(id_jugador) ON DELETE CASCADE,
    FOREIGN KEY (id_juego) REFERENCES juego(id_juego) ON DELETE CASCADE
);

-- Hola Jona: La tabla puntuacion almacena los puntos obtenidos por cada
-- jugador en cada juego.

-- Crear índices para mejorar el rendimiento de las consultas
CREATE INDEX idx_celda_campo ON celda(id_campo);
CREATE INDEX idx_nave_campo ON nave(id_campo);
CREATE INDEX idx_puntuacion_jugador ON puntuacion(id_jugador);
CREATE INDEX idx_puntuacion_juego ON puntuacion(id_juego);

-- Hola Jona: Los índices ayudan a que las consultas sean más rápidas.
-- Por ejemplo, idx_celda_campo hace que sea más rápido buscar todas las
-- celdas de un campo específico.
