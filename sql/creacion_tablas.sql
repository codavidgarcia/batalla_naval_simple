-- Tabla de jugadores
CREATE TABLE jugador (
    id_jugador SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contraseña VARCHAR NOT NULL
);

-- Tabla de puntuaciones
CREATE TABLE puntuacion (
    id_puntuacion SERIAL PRIMARY KEY,
    id_jugador INTEGER NOT NULL REFERENCES jugador(id_jugador),
    puntos INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
