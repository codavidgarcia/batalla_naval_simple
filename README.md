# Batalla Naval

Un juego de Batalla Naval implementado en Python con Kivy y PostgreSQL.

## Requisitos

- Python 3.6+
- PostgreSQL
- pgAdmin 4
- Dependencias de Python (ver `requirements.txt`)

## Configuración de la Base de Datos PostgreSQL

1. Instalar PostgreSQL y pgAdmin 4
2. Crear un usuario y una base de datos en PostgreSQL:

```sql
CREATE USER batalla_naval WITH PASSWORD 'password123';
CREATE DATABASE batalla_naval OWNER batalla_naval;
```

3. Ejecutar el script de configuración:

```bash
python setup_postgres.py
```

## Uso de pgAdmin 4 con la Base de Datos

1. Abrir pgAdmin 4
2. Registrar un nuevo servidor:
   - Nombre: Batalla Naval
   - Host: localhost
   - Puerto: 5432 (predeterminado)
   - Base de datos: batalla_naval
   - Usuario: batalla_naval
   - Contraseña: password123

3. Explorar las tablas:
   - `jugador`: Información de los jugadores
   - `puntuacion`: Puntuaciones de los jugadores

## Ejecución del Juego

```bash
python main.py
```

## Ejecución de la Versión CLI

```bash
python cli.py
```

## Ejecución de Pruebas

```bash
python -m pytest tests/
```
