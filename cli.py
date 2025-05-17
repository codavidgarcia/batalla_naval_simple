"""
Versión de línea de comandos (CLI) del juego Batalla Naval.

Este archivo proporciona una interfaz de línea de comandos para jugar
al juego Batalla Naval sin necesidad de una interfaz gráfica.

Autor: Juan David
"""

import os
import sys
from src.controller.controlador import Controlador

class BatallaNavalCLI:
    """
    Interfaz de línea de comandos para el juego Batalla Naval.

    Esta clase proporciona una interfaz de texto para jugar al juego
    Batalla Naval desde la línea de comandos.

    Atributos:
        controlador (Controlador): Instancia del controlador que gestiona la lógica del juego.

    Métodos:
        mostrar_menu(): Muestra el menú principal.
        jugar_sin_registro(): Inicia una partida sin registro.
        registrar_usuario(): Registra un nuevo usuario.
        iniciar_sesion(): Inicia sesión con un usuario existente.
        jugar(): Inicia una partida con el usuario actual.
        limpiar_pantalla(): Limpia la pantalla de la consola.

    Hola Jona: Esta clase implementa una interfaz de línea de comandos para
    el juego Batalla Naval. Proporciona métodos para mostrar menús, registrar
    usuarios, iniciar sesión y jugar partidas, todo desde la consola.
    """

    def __init__(self):
        """
        Inicializa la interfaz de línea de comandos.

        Hola Jona: Aquí inicializamos la interfaz de línea de comandos.
        Creamos una instancia del controlador que gestionará toda la lógica
        del juego.
        """
        self.controlador = Controlador()

    def limpiar_pantalla(self):
        """
        Limpia la pantalla de la consola.

        Hola Jona: Este método limpia la pantalla de la consola para mejorar
        la legibilidad. Detecta el sistema operativo y ejecuta el comando
        adecuado (cls para Windows, clear para Unix/Linux/MacOS).
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu(self):
        """
        Muestra el menú principal y procesa la opción seleccionada.

        Hola Jona: Este método muestra el menú principal con las opciones
        disponibles y procesa la opción seleccionada por el usuario.
        """
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
        """
        Registra un nuevo usuario.

        Hola Jona: Este método solicita al usuario un nombre de usuario y
        una contraseña, y los utiliza para registrar un nuevo usuario en el sistema.
        """
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
        """
        Inicia sesión con un usuario existente.

        Hola Jona: Este método solicita al usuario sus credenciales y las utiliza
        para iniciar sesión en el sistema. Si las credenciales son correctas,
        inicia una partida con ese usuario.
        """
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
        """
        Muestra las mejores puntuaciones.

        Hola Jona: Este método muestra una tabla con las mejores puntuaciones
        almacenadas en la base de datos, ordenadas de mayor a menor.
        """
        self.limpiar_pantalla()
        print("=" * 40)
        print("       MEJORES PUNTUACIONES")
        print("=" * 40)

        # Obtener puntuaciones del controlador
        puntuaciones = self.controlador.obtener_puntuaciones()

        if not puntuaciones:
            print("\nNo hay puntuaciones registradas.")
        else:
            # Mostrar tabla de puntuaciones
            print("\nPosición  |  Jugador  |  Puntos")
            print("-" * 40)

            for i, p in enumerate(puntuaciones, 1):
                print(f"{i:^9} | {p['nombre_usuario']:<10} | {p['puntaje']:>6}")

        print("\n" + "=" * 40)
        input("\nPresione Enter para volver al menú principal...")

    def jugar_sin_registro(self):
        """
        Inicia una partida sin registro.

        Hola Jona: Este método inicia una partida sin necesidad de registrarse
        o iniciar sesión. Simplemente configura un juego con valores predeterminados.
        """
        self.limpiar_pantalla()
        print("=" * 40)
        print("       JUGAR SIN REGISTRO")
        print("=" * 40)

        # Configurar juego con valores predeterminados
        ancho = 10
        alto = 10
        num_naves = 5

        print(f"Configuración: Tablero de {ancho}x{alto} con {num_naves} naves")
        input("Presione Enter para comenzar...")

        # Iniciar juego
        self.controlador.iniciar_juego(ancho, alto, num_naves)
        self.jugar()

    def jugar(self):
        """
        Inicia una partida con la configuración actual.

        Hola Jona: Este método implementa el bucle principal del juego.
        Muestra el tablero, solicita coordenadas para disparar y actualiza
        el estado del juego hasta que termine la partida.
        """
        # Si no hay un juego activo, configurar uno
        if not self.controlador.juego:
            self.limpiar_pantalla()
            print("=" * 40)
            print("       CONFIGURACIÓN DEL JUEGO")
            print("=" * 40)

            try:
                ancho = int(input("Ancho del tablero (2-20, predeterminado 10): ") or "10")
                alto = int(input("Alto del tablero (2-20, predeterminado 10): ") or "10")
                num_naves = int(input("Número de naves (1-100, predeterminado 5): ") or "5")

                # Validar rangos
                if ancho < 2 or ancho > 20:
                    ancho = 10
                if alto < 2 or alto > 20:
                    alto = 10
                if num_naves < 1 or num_naves > ancho * alto:
                    num_naves = min(5, ancho * alto // 2)

                # Iniciar juego
                self.controlador.iniciar_juego(ancho, alto, num_naves)
            except ValueError:
                input("Entrada inválida. Se usarán valores predeterminados. Presione Enter para continuar...")
                self.controlador.iniciar_juego(10, 10, 5)

        # Bucle principal del juego
        while not self.controlador.juego_terminado():
            self.limpiar_pantalla()
            print("=" * 40)
            print("       BATALLA NAVAL")
            print("=" * 40)

            # Mostrar información del jugador
            if self.controlador.jugador_activo:
                print(f"Jugador: {self.controlador.jugador_activo.nombre_usuario}")
                print(f"Puntaje: {self.controlador.jugador_activo.puntaje}")

            # Mostrar tablero
            print("\nTablero:")
            print(self.controlador.obtener_representacion_tablero())

            # Solicitar coordenadas
            try:
                fila = int(input("Fila: "))
                columna = int(input("Columna: "))

                # Realizar disparo
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

        # Juego terminado
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

# Punto de entrada principal
if __name__ == "__main__":
    """
    Punto de entrada principal del programa CLI.

    Hola Jona: Esta condición verifica si este archivo se está ejecutando
    directamente (no importado como módulo). Si es así, creamos una instancia
    de la interfaz de línea de comandos y mostramos el menú principal.
    """
    cli = BatallaNavalCLI()
    cli.mostrar_menu()
