"""
Módulo para la conexión a la base de datos PostgreSQL.

Este módulo proporciona funciones para conectarse a la base de datos
PostgreSQL y ejecutar consultas SQL.

Autor: Juan David
"""

import psycopg2
from psycopg2 import pool

class ConexionPostgreSQL:
    """
    Clase para gestionar la conexión a la base de datos PostgreSQL.
    
    Esta clase proporciona métodos para conectarse a la base de datos,
    ejecutar consultas y gestionar transacciones.
    
    Atributos:
        pool_conexiones: Pool de conexiones a la base de datos.
    
    Métodos:
        conectar(): Establece la conexión con la base de datos.
        ejecutar_consulta(consulta, parametros): Ejecuta una consulta SQL.
        ejecutar_consulta_con_retorno(consulta, parametros): Ejecuta una consulta y retorna los resultados.
        cerrar_conexion(): Cierra la conexión con la base de datos.
    
    Hola Jona: Esta clase gestiona la conexión a la base de datos PostgreSQL.
    Utilizamos un pool de conexiones para mejorar el rendimiento y la seguridad.
    """
    
    def __init__(self, host, database, user, password, port=5432, min_conexiones=1, max_conexiones=10):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            host (str): Dirección del servidor de base de datos.
            database (str): Nombre de la base de datos.
            user (str): Nombre de usuario.
            password (str): Contraseña.
            port (int): Puerto del servidor (por defecto 5432).
            min_conexiones (int): Número mínimo de conexiones en el pool.
            max_conexiones (int): Número máximo de conexiones en el pool.
            
        Hola Jona: Aquí inicializamos la conexión a la base de datos.
        Creamos un pool de conexiones para mejorar el rendimiento.
        Un pool de conexiones mantiene varias conexiones abiertas y las
        reutiliza, lo que es más eficiente que abrir y cerrar conexiones
        para cada consulta.
        """
        try:
            self.pool_conexiones = pool.ThreadedConnectionPool(
                min_conexiones,
                max_conexiones,
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            print("Pool de conexiones creado exitosamente")
        except Exception as e:
            print(f"Error al crear el pool de conexiones: {e}")
            self.pool_conexiones = None
    
    def obtener_conexion(self):
        """
        Obtiene una conexión del pool.
        
        Returns:
            Connection: Objeto de conexión a la base de datos.
            
        Hola Jona: Este método obtiene una conexión del pool para usarla.
        Cuando terminamos de usar la conexión, debemos devolverla al pool
        con liberar_conexion().
        """
        if self.pool_conexiones:
            return self.pool_conexiones.getconn()
        return None
    
    def liberar_conexion(self, conexion):
        """
        Devuelve una conexión al pool.
        
        Args:
            conexion (Connection): Conexión a devolver al pool.
            
        Hola Jona: Este método devuelve una conexión al pool cuando ya no la necesitamos.
        Es importante liberar las conexiones para que puedan ser reutilizadas.
        """
        if self.pool_conexiones:
            self.pool_conexiones.putconn(conexion)
    
    def ejecutar_consulta(self, consulta, parametros=None):
        """
        Ejecuta una consulta SQL sin retorno de datos.
        
        Args:
            consulta (str): Consulta SQL a ejecutar.
            parametros (tuple, optional): Parámetros para la consulta.
            
        Returns:
            bool: True si la consulta se ejecutó correctamente, False en caso contrario.
            
        Hola Jona: Este método ejecuta una consulta SQL que no retorna datos,
        como INSERT, UPDATE o DELETE. Usamos parámetros para evitar inyección SQL.
        La inyección SQL es un tipo de ataque donde un atacante puede insertar
        código SQL malicioso en una consulta.
        """
        conexion = None
        cursor = None
        try:
            conexion = self.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, parametros)
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al ejecutar la consulta: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion:
                self.liberar_conexion(conexion)
    
    def ejecutar_consulta_con_retorno(self, consulta, parametros=None):
        """
        Ejecuta una consulta SQL y retorna los resultados.
        
        Args:
            consulta (str): Consulta SQL a ejecutar.
            parametros (tuple, optional): Parámetros para la consulta.
            
        Returns:
            list: Lista de tuplas con los resultados, o None si hubo un error.
            
        Hola Jona: Este método ejecuta una consulta SQL que retorna datos,
        como SELECT. Retorna una lista de tuplas, donde cada tupla representa
        una fila del resultado.
        """
        conexion = None
        cursor = None
        try:
            conexion = self.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, parametros)
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conexion:
                self.liberar_conexion(conexion)
    
    def cerrar_pool(self):
        """
        Cierra el pool de conexiones.
        
        Hola Jona: Este método cierra el pool de conexiones cuando ya no lo necesitamos.
        Es importante cerrar el pool al finalizar el programa para liberar recursos.
        """
        if self.pool_conexiones:
            self.pool_conexiones.closeall()
            print("Pool de conexiones cerrado")


# Ejemplo de uso
if __name__ == "__main__":
    """
    Ejemplo de uso de la clase ConexionPostgreSQL.
    
    Hola Jona: Este es un ejemplo de cómo usar la clase ConexionPostgreSQL.
    Primero creamos una instancia de la clase con los datos de conexión.
    Luego ejecutamos algunas consultas de ejemplo.
    """
    # Datos de conexión (reemplazar con los valores correctos)
    host = "localhost"
    database = "batalla_naval"
    user = "postgres"
    password = "password"
    
    # Crear la conexión
    db = ConexionPostgreSQL(host, database, user, password)
    
    # Ejemplo de consulta sin retorno (INSERT)
    consulta_insert = "INSERT INTO jugador (nombre_usuario, contraseña) VALUES (%s, %s)"
    parametros_insert = ("jugador_ejemplo", "contraseña123")
    resultado_insert = db.ejecutar_consulta(consulta_insert, parametros_insert)
    print(f"Inserción exitosa: {resultado_insert}")
    
    # Ejemplo de consulta con retorno (SELECT)
    consulta_select = "SELECT id_jugador, nombre_usuario FROM jugador"
    resultados_select = db.ejecutar_consulta_con_retorno(consulta_select)
    print("Jugadores registrados:")
    for jugador in resultados_select:
        print(f"ID: {jugador[0]}, Nombre: {jugador[1]}")
    
    # Cerrar la conexión
    db.cerrar_pool()
