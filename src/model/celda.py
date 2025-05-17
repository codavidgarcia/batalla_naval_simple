"""
Módulo que define la clase Celda para el juego Batalla Naval.

Este módulo contiene la implementación de la clase Celda, que representa
una celda individual en el tablero de juego.

Autor: Juan David
"""

class Celda:
    """
    Representa una celda individual en el tablero de juego.
    
    Esta clase es fundamental para el juego ya que cada celda puede contener
    una nave o estar vacía, y puede ser impactada por un disparo.
    
    Atributos:
        contiene_nave (bool): Indica si la celda contiene una parte de una nave.
        impactada (bool): Indica si la celda ha sido impactada por un disparo.
    
    Métodos:
        recibir_disparo(): Marca la celda como impactada y retorna si contenía una nave.
        __str__(): Devuelve una representación visual del estado de la celda.
    
    Ejemplo de uso:
        celda = Celda()
        celda.contiene_nave = True
        impacto = celda.recibir_disparo()  # Retorna True porque contiene nave
        print(celda)  # Muestra "X" (nave impactada)
    """
    
    def __init__(self):
        """
        Inicializa una nueva celda vacía y sin impactar.
        
        Por defecto, una celda no contiene nave y no ha sido impactada.
        
        Hola Jona: Aquí estamos creando una nueva celda. Cuando inicializamos
        una celda, establecemos sus atributos iniciales. En este caso, la celda
        comienza sin contener una nave y sin haber sido impactada.
        """
        self.contiene_nave = False
        self.impactada = False
    
    def recibir_disparo(self):
        """
        Marca la celda como impactada por un disparo.
        
        Este método se llama cuando un jugador dispara a esta celda.
        La celda se marca como impactada y se retorna si contenía una nave.
        
        Returns:
            bool: True si la celda contenía una nave, False si estaba vacía.
            
        Raises:
            ValueError: Si la celda ya había sido impactada previamente.
            
        Hola Jona: Este método simula lo que ocurre cuando un jugador dispara
        a esta celda. Primero verificamos si la celda ya fue impactada antes
        (no se puede disparar dos veces al mismo lugar). Luego marcamos la celda
        como impactada y retornamos True si había una nave o False si no.
        """
        if self.impactada:
            raise ValueError("Esta celda ya ha sido impactada")
        
        self.impactada = True
        return self.contiene_nave
    
    def __str__(self):
        """
        Devuelve una representación visual del estado de la celda.
        
        Esta representación se usa para mostrar el tablero en la interfaz.
        
        Returns:
            str: Un carácter que representa el estado de la celda:
                '~' si no ha sido impactada
                'X' si tenía una nave y fue impactada
                'O' si fue impactada pero estaba vacía
                
        Hola Jona: Este método especial __str__ define cómo se ve la celda
        cuando la convertimos a texto. Usamos símbolos diferentes para mostrar
        el estado de cada celda en el tablero:
        - '~' representa agua no impactada
        - 'X' representa una nave impactada
        - 'O' representa un disparo al agua
        """
        if not self.impactada:
            return "~"  # Agua no impactada
        elif self.contiene_nave:
            return "X"  # Nave impactada
        else:
            return "O"  # Disparo al agua
