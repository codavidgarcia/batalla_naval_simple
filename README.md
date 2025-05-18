# Batalla Naval

Un juego de Batalla Naval implementado en Python con Kivy y PostgreSQL.

## Requisitos

- Python 3.6+
- PostgreSQL
- pgAdmin 4
- Dependencias de Python (ver `requirements.txt`)

## Almacenamiento de Datos

El juego soporta dos modos de almacenamiento:

### Opción 1: PostgreSQL (Recomendado para Desarrollo)

1. Instalar PostgreSQL y pgAdmin 4:
   - En sistemas basados en Debian/Ubuntu: `sudo apt install postgresql postgresql-contrib`
   - En macOS con Homebrew: `brew install postgresql`
   - Descargar pgAdmin 4 desde [pgadmin.org](https://www.pgadmin.org/download/)

2. Instalar las dependencias de Python:

```bash
pip install -r requirements.txt
```

3. Ejecutar el script de configuración:

```bash
./configurar_postgres.sh
```

O configurar manualmente:

```sql
CREATE USER batalla_naval WITH PASSWORD 'password123';
CREATE DATABASE batalla_naval OWNER batalla_naval;
```

Y luego:

```bash
PGPASSWORD=password123 psql -h localhost -U batalla_naval -d batalla_naval -f sql/postgres_schema.sql
PGPASSWORD=password123 psql -h localhost -U batalla_naval -d batalla_naval -f sql/postgres_data.sql
```

### Opción 2: JSON (Fallback Automático)

Si PostgreSQL no está disponible o no se puede conectar, el juego usará automáticamente archivos JSON como almacenamiento:

- `datos/jugadores.json`: Almacena información de los jugadores
- `datos/puntuaciones.json`: Almacena las puntuaciones de los jugadores

No se requiere configuración adicional para usar el modo JSON, ya que se activa automáticamente como fallback.

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
