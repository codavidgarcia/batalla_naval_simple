import random

class Campo:
    def __init__(self, ancho, alto, num_naves):
        if ancho <= 0 or alto <= 0 or num_naves <= 0:
            raise ValueError("Los parámetros deben ser positivos")

        if ancho < 2 or alto < 2:
            raise ValueError("El tamaño mínimo del tablero es 2x2")

        if num_naves > ancho * alto:
            raise ValueError("No se pueden colocar más naves que celdas disponibles")

        self.ancho = ancho
        self.alto = alto
        self.num_naves = num_naves
        self.naves_restantes = num_naves

        self.celdas = [[0 for _ in range(ancho)] for _ in range(alto)]

        self.posiciones_naves = []

        self.naves_aleatorias()

    def naves_aleatorias(self):
        naves_colocadas = 0

        while naves_colocadas < self.num_naves:
            fila = random.randint(0, self.alto - 1)
            columna = random.randint(0, self.ancho - 1)

            if self.celdas[fila][columna] == 0:
                self.celdas[fila][columna] = 1

                self.posiciones_naves.append((fila, columna))

                naves_colocadas += 1

    def colocar_naves(self):
        self.naves_aleatorias()

    def verificar_impacto(self, fila, columna):
        if fila < 0 or fila >= self.alto or columna < 0 or columna >= self.ancho:
            raise ValueError("Coordenadas fuera del tablero")

        if self.celdas[fila][columna] >= 2:
            raise ValueError("Esta celda ya ha sido impactada")

        es_nave = self.celdas[fila][columna] == 1

        if es_nave:
            self.celdas[fila][columna] = 3
            self.naves_restantes -= 1
        else:
            self.celdas[fila][columna] = 2

        return es_nave

    def mostrar_campo(self):
        representacion = ""

        representacion += "  " + " ".join(str(i) for i in range(self.ancho)) + "\n"

        for i in range(self.alto):
            representacion += f"{i} "
            for j in range(self.ancho):
                if self.celdas[i][j] == 0:
                    representacion += "~ "
                elif self.celdas[i][j] == 1:
                    representacion += "~ "
                elif self.celdas[i][j] == 2:
                    representacion += "O "
                elif self.celdas[i][j] == 3:
                    representacion += "X "
            representacion += "\n"

        return representacion
