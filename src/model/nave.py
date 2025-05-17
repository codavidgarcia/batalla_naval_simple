"""
Módulo que define la clase Nave para el juego Batalla Naval.

Este módulo contiene la implementación de la clase Nave, que representa
una nave en el tablero de juego.

Autor: Juan David
"""

class Nave:
    """
    Representa una nave en el tablero de juego.
    
    Una nave ocupa una o más celdas en el tablero y puede ser impactada
    por disparos. Una nave está destruida cuando todas sus partes han sido impactadas.
    
    Atributos:
        posiciones (list): Lista de coordenadas (fila, columna) que ocupa la nave.
        impactos (set): Conjunto de coordenadas que ya han sido impactadas.
    
    Métodos:
        verificar_impacto(coordenada): Verifica si un disparo impacta la nave.
        esta_destruida(): Determina si todas las partes de la nave han sido impactadas.
    
    Ejemplo de uso:
        nave = Nave([(0, 0), (0, 1)])  # Nave de 2 celdas
        impacto = nave.verificar_impacto((0, 0))  # Retorna True
        destruida = nave.esta_destruida()  # Retorna False (falta impactar (0, 1))
    """
    
    def __init__(self, posiciones):
        """
        Inicializa una nueva nave con las posiciones especificadas.
        
        Args:
            posiciones (list): Lista de coordenadas (fila, columna) que ocupa la nave.
            
        Hola Jona: Aquí estamos creando una nueva nave. Una nave ocupa una o más
        posiciones en el tablero. Por ejemplo, un submarino podría ocupar solo
        la posición (3, 4), mientras que un portaaviones podría ocupar
        [(5, 2), (5, 3), (5, 4), (5, 5), (5, 6)]. También inicializamos un
        conjunto vacío para registrar qué partes de la nave han sido impactadas.
        """
        self.posiciones = posiciones
        self.impactos = set()
    
    def verificar_impacto(self, coordenada):
        """
        Verifica si un disparo impacta la nave y registra el impacto.
        
        Args:
            coordenada (tuple): Coordenada del disparo (fila, columna).
            
        Returns:
            bool: True si la coordenada impacta la nave, False en caso contrario.
            
        Hola Jona: Este método verifica si un disparo ha impactado la nave.
        Primero comprobamos si la coordenada del disparo está en alguna de las
        posiciones que ocupa la nave. Luego verificamos si esa parte de la nave
        ya había sido impactada antes. Si es un nuevo impacto, lo registramos
        en el conjunto de impactos y retornamos True.
        """
        if coordenada in self.posiciones and coordenada not in self.impactos:
            self.impactos.add(coordenada)
            return True
        return False
    
    def esta_destruida(self):
        """
        Verifica si la nave ha sido completamente destruida.
        
        Una nave está destruida cuando todas sus partes han sido impactadas.
        
        Returns:
            bool: True si todas las partes de la nave han sido impactadas, False en caso contrario.
            
        Hola Jona: Este método verifica si la nave está completamente destruida.
        Una nave está destruida cuando todas sus partes han sido impactadas.
        Convertimos la lista de posiciones a un conjunto y comparamos si es igual
        al conjunto de impactos. Si son iguales, significa que todas las partes
        han sido impactadas y la nave está destruida.
        """
        return set(self.posiciones) == self.impactos
