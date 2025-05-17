-- Consultas SQL básicas para el juego Batalla Naval
-- Autor: Juan David

-- Hola Jona: Este archivo contiene ejemplos de consultas SQL básicas para
-- interactuar con la base de datos del juego Batalla Naval. Incluye ejemplos
-- de SELECT, INSERT, UPDATE y DELETE para cada tabla.

-- =====================
-- CONSULTAS DE JUGADOR
-- =====================

-- Insertar un nuevo jugador
INSERT INTO jugador (nombre_usuario, contraseña)
VALUES ('jugador1', 'contraseña123');

-- Hola Jona: Esta consulta inserta un nuevo jugador en la tabla jugador.
-- No necesitamos especificar id_jugador porque es SERIAL (se genera automáticamente).
-- No necesitamos especificar fecha_registro porque tiene un valor por defecto (CURRENT_TIMESTAMP).

-- Obtener todos los jugadores
SELECT id_jugador, nombre_usuario, fecha_registro
FROM jugador
ORDER BY fecha_registro DESC;

-- Esta consulta selecciona todos los jugadores ordenados por fecha de registro.
-- No incluimos la contraseña por razones de seguridad.

-- Actualizar la contraseña de un jugador
UPDATE jugador
SET contraseña = 'nueva_contraseña'
WHERE nombre_usuario = 'jugador1';

-- Hola Jona: Esta consulta actualiza la contraseña del jugador con nombre_usuario 'jugador1'.

-- Eliminar un jugador
DELETE FROM jugador
WHERE nombre_usuario = 'jugador1';

-- Hola Jona: Esta consulta elimina al jugador con nombre_usuario 'jugador1'.
-- Debido a ON DELETE CASCADE en las tablas relacionadas, también se eliminarán
-- todos los registros relacionados con este jugador.

-- =====================
-- CONSULTAS DE JUEGO
-- =====================

-- Insertar un nuevo juego
INSERT INTO juego (estado)
VALUES ('en curso');

-- Esta consulta inserta un nuevo juego en la tabla juego.
-- No necesitamos especificar id_juego porque es SERIAL.
-- No necesitamos especificar fecha_inicio porque tiene un valor por defecto.

-- Obtener todos los juegos
SELECT id_juego, fecha_inicio, estado
FROM juego
ORDER BY fecha_inicio DESC;

-- Hola Jona: Esta consulta selecciona todos los juegos ordenados por fecha de inicio.

-- Actualizar el estado de un juego
UPDATE juego
SET estado = 'terminado'
WHERE id_juego = 1;

-- Hola Jona: Esta consulta actualiza el estado del juego con id_juego 1.

-- Eliminar un juego
DELETE FROM juego
WHERE id_juego = 1;

-- Hola Jona: Esta consulta elimina el juego con id_juego 1.
-- Debido a ON DELETE CASCADE, también se eliminarán todos los registros relacionados.

-- =====================
-- CONSULTAS DE RELACIÓN JUGADOR-JUEGO
-- =====================

-- Asociar un jugador a un juego
INSERT INTO jugador_juego (id_jugador, id_juego)
VALUES (1, 1);

-- Hola Jona: Esta consulta asocia al jugador con id_jugador 1 con el juego con id_juego 1.

-- Obtener todos los juegos de un jugador
SELECT j.id_juego, j.fecha_inicio, j.estado
FROM juego j
JOIN jugador_juego jj ON j.id_juego = jj.id_juego
WHERE jj.id_jugador = 1
ORDER BY j.fecha_inicio DESC;

-- Hola Jona: Esta consulta selecciona todos los juegos del jugador con id_jugador 1.
-- JOIN conecta las tablas juego y jugador_juego.

-- Eliminar la asociación de un jugador con un juego
DELETE FROM jugador_juego
WHERE id_jugador = 1 AND id_juego = 1;

-- Hola Jona: Esta consulta elimina la asociación entre el jugador 1 y el juego 1.

-- =====================
-- CONSULTAS DE CAMPO
-- =====================

-- Insertar un nuevo campo
INSERT INTO campo (id_jugador, id_juego, ancho, alto, num_naves, naves_restantes)
VALUES (1, 1, 10, 10, 5, 5);

-- Hola Jona: Esta consulta inserta un nuevo campo para el jugador 1 en el juego 1.

-- Obtener el campo de un jugador en un juego
SELECT id_campo, ancho, alto, num_naves, naves_restantes
FROM campo
WHERE id_jugador = 1 AND id_juego = 1;

-- Hola Jona: Esta consulta selecciona el campo del jugador 1 en el juego 1.

-- Actualizar el número de naves restantes
UPDATE campo
SET naves_restantes = naves_restantes - 1
WHERE id_campo = 1;

-- Hola Jona: Esta consulta reduce en 1 el número de naves restantes en el campo con id_campo 1.

-- =====================
-- CONSULTAS DE CELDA
-- =====================

-- Insertar una nueva celda
INSERT INTO celda (id_campo, fila, columna)
VALUES (1, 0, 0);

-- Hola Jona: Esta consulta inserta una nueva celda en la posición (0, 0) del campo 1.

-- Obtener todas las celdas de un campo
SELECT id_celda, fila, columna, fue_disparada
FROM celda
WHERE id_campo = 1
ORDER BY fila, columna;

-- Hola Jona: Esta consulta selecciona todas las celdas del campo 1, ordenadas por fila y columna.

-- Marcar una celda como disparada
UPDATE celda
SET fue_disparada = TRUE
WHERE id_campo = 1 AND fila = 0 AND columna = 0;

-- Hola Jona: Esta consulta marca como disparada la celda en la posición (0, 0) del campo 1.

-- =====================
-- CONSULTAS DE NAVE
-- =====================

-- Insertar una nueva nave
INSERT INTO nave (id_campo, tipo, tamaño)
VALUES (1, 'Submarino', 1);

-- Hola Jona: Esta consulta inserta una nueva nave de tipo Submarino en el campo 1.

-- Obtener todas las naves de un campo
SELECT id_nave, tipo, tamaño, esta_destruida
FROM nave
WHERE id_campo = 1;

-- Hola Jona: Esta consulta selecciona todas las naves del campo 1.

-- Marcar una nave como destruida
UPDATE nave
SET esta_destruida = TRUE
WHERE id_nave = 1;

-- Hola Jona: Esta consulta marca como destruida la nave con id_nave 1.

-- =====================
-- CONSULTAS DE RELACIÓN NAVE-CELDA
-- =====================

-- Asociar una nave a una celda
INSERT INTO nave_celda (id_nave, id_celda)
VALUES (1, 1);

-- Hola Jona: Esta consulta asocia la nave 1 con la celda 1.

-- Obtener todas las celdas ocupadas por una nave
SELECT c.id_celda, c.fila, c.columna, c.fue_disparada
FROM celda c
JOIN nave_celda nc ON c.id_celda = nc.id_celda
WHERE nc.id_nave = 1
ORDER BY c.fila, c.columna;

-- Hola Jona: Esta consulta selecciona todas las celdas ocupadas por la nave 1.

-- =====================
-- CONSULTAS DE PUNTUACIÓN
-- =====================

-- Insertar una nueva puntuación
INSERT INTO puntuacion (id_jugador, id_juego, puntos)
VALUES (1, 1, 10);

-- Hola Jona: Esta consulta registra una puntuación de 10 puntos para el jugador 1 en el juego 1.

-- Obtener las mejores puntuaciones
SELECT j.nombre_usuario, p.puntos, p.fecha
FROM puntuacion p
JOIN jugador j ON p.id_jugador = j.id_jugador
ORDER BY p.puntos DESC
LIMIT 10;

-- Hola Jona: Esta consulta selecciona las 10 mejores puntuaciones, ordenadas de mayor a menor.

-- Actualizar la puntuación de un jugador en un juego
UPDATE puntuacion
SET puntos = puntos + 5
WHERE id_jugador = 1 AND id_juego = 1;

-- Hola Jona: Esta consulta añade 5 puntos a la puntuación del jugador 1 en el juego 1.

-- =====================
-- CONSULTAS COMPLEJAS
-- =====================

-- Obtener el estado completo de un juego
SELECT 
    j.id_juego, j.estado,
    c.id_campo, c.ancho, c.alto, c.naves_restantes,
    jug.nombre_usuario,
    p.puntos
FROM juego j
JOIN campo c ON j.id_juego = c.id_juego
JOIN jugador jug ON c.id_jugador = jug.id_jugador
LEFT JOIN puntuacion p ON j.id_juego = p.id_juego AND jug.id_jugador = p.id_jugador
WHERE j.id_juego = 1;

-- Hola Jona: Esta consulta obtiene información completa sobre el juego 1,
-- incluyendo el campo, el jugador y la puntuación.

-- Verificar si una nave está destruida (todas sus celdas han sido disparadas)
SELECT 
    n.id_nave,
    n.tipo,
    CASE 
        WHEN COUNT(c.id_celda) = SUM(CASE WHEN c.fue_disparada THEN 1 ELSE 0 END) THEN TRUE
        ELSE FALSE
    END AS esta_destruida
FROM nave n
JOIN nave_celda nc ON n.id_nave = nc.id_nave
JOIN celda c ON nc.id_celda = c.id_celda
WHERE n.id_nave = 1
GROUP BY n.id_nave, n.tipo;

-- Hola Jona: Esta consulta verifica si la nave 1 está destruida, comprobando
-- si todas sus celdas han sido disparadas.

-- Obtener el ranking de jugadores por puntuación total
SELECT 
    j.nombre_usuario,
    SUM(p.puntos) AS puntuacion_total,
    COUNT(DISTINCT p.id_juego) AS juegos_jugados
FROM jugador j
LEFT JOIN puntuacion p ON j.id_jugador = p.id_jugador
GROUP BY j.id_jugador, j.nombre_usuario
ORDER BY puntuacion_total DESC;

-- Hola Jona: Esta consulta obtiene un ranking de jugadores por puntuación total,
-- incluyendo el número de juegos jugados por cada uno.
