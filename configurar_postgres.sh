#!/bin/bash

# Script para configurar PostgreSQL para el juego Batalla Naval

echo "Configurando PostgreSQL para Batalla Naval..."

# Verificar si PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL no está instalado. Por favor, instálalo primero."
    echo "En sistemas basados en Debian/Ubuntu: sudo apt install postgresql postgresql-contrib"
    echo "En macOS con Homebrew: brew install postgresql"
    exit 1
fi

# Verificar si el servicio PostgreSQL está en ejecución
if ! pg_isready &> /dev/null; then
    echo "El servicio PostgreSQL no está en ejecución. Por favor, inícialo primero."
    echo "En sistemas basados en Debian/Ubuntu: sudo service postgresql start"
    echo "En macOS con Homebrew: brew services start postgresql"
    exit 1
fi

# Crear usuario y base de datos
echo "Creando usuario y base de datos..."
sudo -u postgres psql -c "CREATE USER batalla_naval WITH PASSWORD 'password123';" || echo "El usuario ya existe o no se pudo crear."
sudo -u postgres psql -c "CREATE DATABASE batalla_naval OWNER batalla_naval;" || echo "La base de datos ya existe o no se pudo crear."

# Crear tablas y cargar datos
echo "Creando tablas y cargando datos..."
PGPASSWORD=password123 psql -h localhost -U batalla_naval -d batalla_naval -f sql/postgres_schema.sql
PGPASSWORD=password123 psql -h localhost -U batalla_naval -d batalla_naval -f sql/postgres_data.sql

echo "Configuración completada."
echo "Listo pgAdmin 4 para conectarse a la base de datos:"
echo "  - Host: localhost"
echo "  - Puerto: 5432"
echo "  - Base de datos: batalla_naval"
echo "  - Usuario: batalla_naval"
echo "  - Contraseña: password123"
