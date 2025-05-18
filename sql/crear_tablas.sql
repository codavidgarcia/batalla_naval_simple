DROP TABLE IF EXISTS puntuacion CASCADE;
DROP TABLE IF EXISTS jugador CASCADE;

CREATE TABLE jugador (
    id_jugador SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contraseña TEXT NOT NULL
);

CREATE TABLE puntuacion (
    id_puntuacion SERIAL PRIMARY KEY,
    id_jugador INT NOT NULL,
    puntos INT DEFAULT 0,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jugador) REFERENCES jugador(id_jugador) ON DELETE CASCADE
);

CREATE INDEX idx_puntuacion_jugador ON puntuacion(id_jugador);
