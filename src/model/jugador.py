class Jugador:
    def __init__(self, nombre_usuario, contraseña):
        if not nombre_usuario:
            raise ValueError("El nombre de usuario no puede estar vacío")
        if not contraseña:
            raise ValueError("La contraseña no puede estar vacía")

        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.puntaje = 0

    def actualizar_puntaje(self, puntos):
        self.puntaje += puntos
        return self.puntaje

    def __str__(self):
        return f"Jugador: {self.nombre_usuario}, Puntaje: {self.puntaje}"
