import os
import sys
from src.controller.controlador import Controlador

class BatallaNavalCLI:
    def __init__(self):
        self.controlador = Controlador()

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu(self):
        while True:
            self.limpiar_pantalla()
            print("=" * 40)
            print("       BATALLA NAVAL - MENÚ PRINCIPAL")
            print("=" * 40)
            print("1. Jugar sin registro")
            print("2. Registrarse")
            print("3. Iniciar sesión")
            print("4. Ver puntuaciones")
            print("5. Salir")
            print("=" * 40)

            opcion = input("Seleccione una opción (1-5): ")

            if opcion == "1":
                self.jugar_sin_registro()
            elif opcion == "2":
                self.registrar_usuario()
            elif opcion == "3":
                self.iniciar_sesion()
            elif opcion == "4":
                self.mostrar_puntuaciones()
            elif opcion == "5":
                print("¡Gracias por jugar!")
                sys.exit(0)
            else:
                input("Opción inválida. Presione Enter para continuar...")

    def registrar_usuario(self):
        self.limpiar_pantalla()
        print("=" * 40)
        print("       REGISTRO DE USUARIO")
        print("=" * 40)

        nombre = input("Nombre de usuario: ")
        contraseña = input("Contraseña: ")

        if not nombre or not contraseña:
            input("Todos los campos son obligatorios. Presione Enter para continuar...")
            return

        if self.controlador.registrar_jugador(nombre, contraseña):
            input("Usuario registrado correctamente. Presione Enter para continuar...")
        else:
            input("Error al registrar usuario. El nombre de usuario ya existe o es inválido. Presione Enter para continuar...")

    def iniciar_sesion(self):
        self.limpiar_pantalla()
        print("=" * 40)
        print("       INICIAR SESIÓN")
        print("=" * 40)

        nombre = input("Nombre de usuario: ")
        contraseña = input("Contraseña: ")

        if not nombre or not contraseña:
            input("Todos los campos son obligatorios. Presione Enter para continuar...")
            return

        if self.controlador.iniciar_sesion(nombre, contraseña):
            input("Inicio de sesión exitoso. Presione Enter para jugar...")
            self.jugar()
        else:
            input("Credenciales incorrectas. Presione Enter para continuar...")

    def mostrar_puntuaciones(self):
        self.limpiar_pantalla()
        print("=" * 40)
        print("       MEJORES PUNTUACIONES")
        print("=" * 40)

        puntuaciones = self.controlador.obtener_puntuaciones()

        if not puntuaciones:
            print("\nNo hay puntuaciones registradas.")
        else:
            print("\nPosición  |  Jugador  |  Puntos")
            print("-" * 40)

            for i, p in enumerate(puntuaciones, 1):
                print(f"{i:^9} | {p['nombre_usuario']:<10} | {p['puntaje']:>6}")

        print("\n" + "=" * 40)
        input("\nPresione Enter para volver al menú principal...")

    def jugar_sin_registro(self):
        self.limpiar_pantalla()
        print("=" * 40)
        print("       JUGAR SIN REGISTRO")
        print("=" * 40)

        ancho = 10
        alto = 10
        num_naves = 5

        print(f"Configuración: Tablero de {ancho}x{alto} con {num_naves} naves")
        input("Presione Enter para comenzar...")

        self.controlador.iniciar_juego(ancho, alto, num_naves)
        self.jugar()

    def jugar(self):
        if not self.controlador.juego:
            self.limpiar_pantalla()
            print("=" * 40)
            print("       CONFIGURACIÓN DEL JUEGO")
            print("=" * 40)

            try:
                ancho = int(input("Ancho del tablero (2-20, predeterminado 10): ") or "10")
                alto = int(input("Alto del tablero (2-20, predeterminado 10): ") or "10")
                num_naves = int(input("Número de naves (1-100, predeterminado 5): ") or "5")

                if ancho < 2 or ancho > 20:
                    ancho = 10
                if alto < 2 or alto > 20:
                    alto = 10
                if num_naves < 1 or num_naves > ancho * alto:
                    num_naves = min(5, ancho * alto // 2)

                self.controlador.iniciar_juego(ancho, alto, num_naves)
            except ValueError:
                input("Entrada inválida. Se usarán valores predeterminados. Presione Enter para continuar...")
                self.controlador.iniciar_juego(10, 10, 5)

        while not self.controlador.juego_terminado():
            self.limpiar_pantalla()
            print("=" * 40)
            print("       BATALLA NAVAL")
            print("=" * 40)

            if self.controlador.jugador_activo:
                print(f"Jugador: {self.controlador.jugador_activo.nombre_usuario}")
                print(f"Puntaje: {self.controlador.jugador_activo.puntaje}")

            print("\nTablero:")
            print(self.controlador.obtener_representacion_tablero())

            try:
                fila = int(input("Fila: "))
                columna = int(input("Columna: "))

                impacto = self.controlador.realizar_disparo(fila, columna)

                if impacto:
                    input("¡Impacto en una nave! Presione Enter para continuar...")
                else:
                    input("Disparo al agua. Presione Enter para continuar...")
            except ValueError as e:
                if "ya ha sido impactada" in str(e):
                    input("Esta celda ya ha sido impactada. Presione Enter para continuar...")
                else:
                    input("Entrada inválida. Use números enteros. Presione Enter para continuar...")
            except Exception as e:
                input(f"Error: {str(e)}. Presione Enter para continuar...")

        self.limpiar_pantalla()
        print("=" * 40)
        print("       ¡JUEGO TERMINADO!")
        print("=" * 40)
        print("\nTablero final:")
        print(self.controlador.obtener_representacion_tablero())

        if self.controlador.jugador_activo:
            print(f"\nJugador: {self.controlador.jugador_activo.nombre_usuario}")
            print(f"Puntaje final: {self.controlador.jugador_activo.puntaje}")

        input("\nPresione Enter para volver al menú principal...")

if __name__ == "__main__":
    cli = BatallaNavalCLI()
    cli.mostrar_menu()
