INSERT INTO jugador (nombre_usuario, contraseña)
VALUES ('jugador1', 'contraseña123');

SELECT id_jugador, nombre_usuario
FROM jugador
ORDER BY id_jugador;

UPDATE jugador
SET contraseña = 'nueva_contraseña'
WHERE nombre_usuario = 'jugador1';

DELETE FROM jugador
WHERE nombre_usuario = 'jugador1';

INSERT INTO puntuacion (id_jugador, puntos)
VALUES (1, 10);

SELECT j.nombre_usuario, p.puntos, p.fecha
FROM puntuacion p
JOIN jugador j ON p.id_jugador = j.id_jugador
ORDER BY p.puntos DESC
LIMIT 10;

UPDATE puntuacion
SET puntos = puntos + 5
WHERE id_jugador = 1 AND id_puntuacion = 1;
