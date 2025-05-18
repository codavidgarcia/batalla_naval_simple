class Celda:
    def __init__(self):
        self.nave = False
        self.disparada = False

    def recibir_disparo(self):
        if self.disparada:
            raise ValueError("Esta celda ya ha sido impactada")

        self.disparada = True
        return self.nave
