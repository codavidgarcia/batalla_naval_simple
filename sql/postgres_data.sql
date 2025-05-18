-- Datos de ejemplo para PostgreSQL

-- Insertar jugadores
INSERT INTO jugador (nombre_usuario, contraseña) VALUES
('usuario1', 'password123'),
('usuario2', 'password456'),
('usuario3', 'password789');

-- Insertar puntuaciones
INSERT INTO puntuacion (id_jugador, puntos, fecha) VALUES
(1, 100, CURRENT_TIMESTAMP),
(1, 150, CURRENT_TIMESTAMP),
(2, 200, CURRENT_TIMESTAMP),
(3, 50, CURRENT_TIMESTAMP);
