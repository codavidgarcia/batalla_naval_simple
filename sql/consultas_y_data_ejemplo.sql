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

-- =============================================
-- CONSULTAS BÁSICAS
-- =============================================

-- Consulta 1: Seleccionar todos los jugadores
-- SELECT * FROM jugador;

-- Consulta 2: Seleccionar todas las puntuaciones
-- SELECT * FROM puntuacion;

-- Consulta 3: Seleccionar jugadores con sus puntuaciones
-- SELECT j.nombre_usuario, p.puntos, p.fecha
-- FROM jugador j
-- JOIN puntuacion p ON j.id_jugador = p.id_jugador
-- ORDER BY p.puntos DESC;

-- Consulta 4: Seleccionar las mejores puntuaciones
-- SELECT j.nombre_usuario, p.puntos, p.fecha
-- FROM jugador j
-- JOIN puntuacion p ON j.id_jugador = p.id_jugador
-- ORDER BY p.puntos DESC
-- LIMIT 10;

-- Consulta 5: Seleccionar la puntuación máxima de cada jugador
-- SELECT j.nombre_usuario, MAX(p.puntos) as max_puntos
-- FROM jugador j
-- LEFT JOIN puntuacion p ON j.id_jugador = p.id_jugador
-- GROUP BY j.nombre_usuario
-- ORDER BY max_puntos DESC;