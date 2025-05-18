from src.model.campo import Campo

class Juego:
    def __init__(self, ancho, alto, num_naves):
        self.ancho = ancho
        self.alto = alto
        self.num_naves = num_naves
        self.campo = Campo(ancho, alto, num_naves)

    def realizar_disparo(self, fila, columna):
        return self.campo.verificar_impacto(fila, columna)

    def verificar_ganador(self):
        if self.campo.naves_restantes == 0:
            return True
        return None

    def reiniciar_juego(self):
        self.campo = Campo(self.ancho, self.alto, self.num_naves)
