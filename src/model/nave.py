class Nave:
    def __init__(self, posicion):
        self.posicion = posicion

    def verificar_impacto(self, coordenada):
        return coordenada in self.posicion
