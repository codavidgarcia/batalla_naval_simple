from src.model.sistema_usuario import SistemaUsuario
from src.model.juego import Juego
from src.model.puntuaciones import Puntuaciones

class Controlador:
    def __init__(self):
        self.sistema_usuario = SistemaUsuario()
        self.juego = None
        self.jugador_activo = None
        self.puntuaciones = None

    def registrar_jugador(self, nombre, contraseña):
        return self.sistema_usuario.registrar_jugador(nombre, contraseña)

    def iniciar_sesion(self, nombre, contraseña):
        jugador = self.sistema_usuario.iniciar_sesion(nombre, contraseña)
        if jugador:
            self.jugador_activo = jugador
            self.puntuaciones = Puntuaciones(jugador, self.sistema_usuario.session)
            return True
        return False

    def iniciar_juego(self, ancho, alto, num_naves):
        self.juego = Juego(ancho, alto, num_naves)

    def realizar_disparo(self, fila, columna):
        if not self.juego:
            raise ValueError("No hay un juego activo")

        impacto = self.juego.realizar_disparo(fila, columna)

        if self.juego.verificar_ganador() and self.jugador_activo and self.puntuaciones:
            self.puntuaciones.actualizar_puntuacion(10)

        return impacto

    def obtener_puntuaciones(self, limite=10):
        if self.puntuaciones:
            return self.puntuaciones.mostrar_puntuaciones(limite)
        return []

    def obtener_representacion_tablero(self):
        if self.juego:
            return self.juego.campo.mostrar_campo()
        return "No hay un juego activo"

    def reiniciar_juego(self):
        if self.juego:
            self.juego.reiniciar_juego()
            return True
        return False

    def juego_terminado(self):
        if self.juego:
            return self.juego.verificar_ganador() is not None
        return False
