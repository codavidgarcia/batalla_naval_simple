#!/usr/bin/env python3
"""
Script para configurar la base de datos PostgreSQL para el juego Batalla Naval.
Este script crea las tablas necesarias y carga datos de ejemplo.
"""

import psycopg2
import os
import sys

def setup_database():
    """Configura la base de datos PostgreSQL."""
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            dbname="batalla_naval",
            user="batalla_naval",
            password="password123",
            host="localhost"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Conexión establecida con PostgreSQL.")
        
        # Ejecutar script de esquema
        schema_path = os.path.join('sql', 'postgres_schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            cursor.execute(schema_sql)
        
        print("Esquema creado correctamente.")
        
        # Ejecutar script de datos
        data_path = os.path.join('sql', 'postgres_data.sql')
        with open(data_path, 'r') as f:
            data_sql = f.read()
            cursor.execute(data_sql)
        
        print("Datos cargados correctamente.")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        print("Base de datos PostgreSQL configurada correctamente.")
        return True
    
    except Exception as e:
        print(f"Error al configurar la base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    print("Configurando base de datos PostgreSQL para Batalla Naval...")
    if setup_database():
        print("Configuración completada con éxito.")
    else:
        print("Error en la configuración.")
        sys.exit(1)
