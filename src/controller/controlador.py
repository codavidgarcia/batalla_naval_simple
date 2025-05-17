"""
Módulo que define el controlador principal para el juego Batalla Naval.

Este módulo contiene la implementación del controlador que coordina
la interacción entre los modelos y las vistas del juego.

Autor: Juan David
"""

from src.model.juego import Juego
from src.model.jugador import Jugador
from src.model.db_models import DatabaseManager

class Controlador:
    """
    Controlador principal del juego Batalla Naval.

    Esta clase coordina la interacción entre los modelos y las vistas del juego.
    Gestiona el estado del juego, los jugadores y las acciones del usuario.

    Atributos:
        juego (Juego): Instancia actual del juego.
        jugador_activo (Jugador): Jugador que está jugando actualmente.
        jugadores (list): Lista de jugadores registrados.
        db_manager (DatabaseManager): Gestor de la base de datos.
        session: Sesión actual de la base de datos.

    Métodos:
        iniciar_juego(ancho, alto, num_naves): Inicia una nueva partida.
        realizar_disparo(fila, columna): Realiza un disparo en las coordenadas especificadas.
        registrar_jugador(nombre, contraseña): Registra un nuevo jugador.
        iniciar_sesion(nombre, contraseña): Inicia sesión con un jugador existente.
        actualizar_puntaje(puntos): Actualiza el puntaje del jugador activo.

    Ejemplo de uso:
        controlador = Controlador()
        controlador.registrar_jugador("usuario1", "contraseña123")
        controlador.iniciar_sesion("usuario1", "contraseña123")
        controlador.iniciar_juego(10, 10, 5)
        controlador.realizar_disparo(3, 4)
    """

    def __init__(self, db_manager=None, session=None):
        """
        Inicializa el controlador.

        Args:
            db_manager (DatabaseManager, optional): Gestor de la base de datos.
                Si no se proporciona, se crea uno nuevo.
            session (Session, optional): Sesión de la base de datos.
                Si no se proporciona, se crea una nueva.

        Hola Jona: Aquí estamos inicializando el controlador del juego.
        El controlador es el componente central que coordina todo el juego.
        Inicialmente, no hay ningún juego activo ni jugador activo, y la
        lista de jugadores está vacía. También inicializamos la conexión
        a la base de datos.
        """
        self.juego = None
        self.jugador_activo = None
        self.jugadores = []

        # Inicializar la base de datos
        try:
            print("Inicializando la base de datos...")
            if db_manager is None:
                self.db_manager = DatabaseManager()
                self.db_manager.create_tables()
                self.session = self.db_manager.get_session()
            else:
                self.db_manager = db_manager
                self.session = session if session is not None else db_manager.get_session()
            print("Base de datos inicializada correctamente.")

            # Cargar jugadores desde la base de datos
            self._cargar_jugadores()
        except Exception as e:
            print(f"Error al inicializar la base de datos: {str(e)}")
            import traceback
            traceback.print_exc()
            # Crear una sesión de emergencia
            if hasattr(self, 'db_manager'):
                self.session = self.db_manager.get_session()

    def _cargar_jugadores(self):
        """
        Carga los jugadores desde la base de datos.

        Hola Jona: Este método carga los jugadores desde la base de datos
        y los añade a la lista de jugadores en memoria. Esto nos permite
        tener acceso rápido a los jugadores sin tener que consultar la
        base de datos cada vez.
        """
        try:
            # Obtener todos los jugadores de la base de datos
            from src.model.db_models import Jugador as JugadorDB
            jugadores_db = self.session.query(JugadorDB).all()

            print(f"Jugadores encontrados en la base de datos: {len(jugadores_db)}")

            # Convertir a objetos Jugador del modelo
            for jugador_db in jugadores_db:
                jugador = Jugador(jugador_db.nombre_usuario, jugador_db.contraseña)
                print(f"Cargando jugador: {jugador_db.nombre_usuario}")

                # Obtener puntuaciones del jugador
                from src.model.db_models import Puntuacion
                puntuaciones = self.session.query(Puntuacion).filter_by(id_jugador=jugador_db.id_jugador).all()
                print(f"Puntuaciones encontradas para {jugador_db.nombre_usuario}: {len(puntuaciones)}")

                if puntuaciones:
                    # Asignar el puntaje más alto
                    max_puntaje = max(p.puntos for p in puntuaciones)
                    jugador.puntaje = max_puntaje
                    print(f"Puntaje máximo para {jugador_db.nombre_usuario}: {max_puntaje}")

                self.jugadores.append(jugador)

            # Si no hay jugadores, crear uno de ejemplo
            if not self.jugadores:
                print("No hay jugadores en la base de datos. Creando jugador de ejemplo...")
                self.registrar_jugador("jugador1", "contraseña1")

        except Exception as e:
            print(f"Error al cargar jugadores: {str(e)}")
            import traceback
            traceback.print_exc()

    def iniciar_juego(self, ancho, alto, num_naves):
        """
        Inicia una nueva partida del juego.

        Args:
            ancho (int): Número de columnas del tablero.
            alto (int): Número de filas del tablero.
            num_naves (int): Número de naves a colocar en el tablero.

        Hola Jona: Este método crea una nueva partida del juego con los
        parámetros especificados. Creamos una instancia de la clase Juego
        y la guardamos como el juego activo. También creamos un registro
        en la base de datos si hay un jugador activo.
        """
        # Crear el juego en memoria
        self.juego = Juego(ancho, alto, num_naves)

        # Si hay un jugador activo, crear el juego en la base de datos
        if self.jugador_activo:
            try:
                # Obtener el ID del jugador
                from src.model.db_models import Jugador as JugadorDB
                jugador_db = self.session.query(JugadorDB).filter_by(nombre_usuario=self.jugador_activo.nombre_usuario).first()

                if not jugador_db:
                    print(f"No se encontró el jugador {self.jugador_activo.nombre_usuario} en la base de datos.")
                    return

                # Crear el juego en la base de datos
                from src.model.db_models import Juego as JuegoDB
                juego_db = JuegoDB(estado='activo')
                juego_db.jugadores.append(jugador_db)
                self.session.add(juego_db)
                self.session.commit()

                # Crear el campo en la base de datos
                from src.model.db_models import Campo
                campo_db = Campo(
                    id_jugador=jugador_db.id_jugador,
                    id_juego=juego_db.id_juego,
                    ancho=ancho,
                    alto=alto,
                    num_naves=num_naves,
                    naves_restantes=num_naves
                )
                self.session.add(campo_db)
                self.session.commit()

                # Crear las celdas del campo
                from src.model.db_models import Celda
                for fila in range(alto):
                    for columna in range(ancho):
                        celda = Celda(
                            id_campo=campo_db.id_campo,
                            fila=fila,
                            columna=columna,
                            estado='agua'
                        )
                        self.session.add(celda)

                self.session.commit()
                print(f"Juego creado en la base de datos con ID: {juego_db.id_juego}")

            except Exception as e:
                print(f"Error al crear juego en la base de datos: {str(e)}")
                import traceback
                traceback.print_exc()
                self.session.rollback()

    def realizar_disparo(self, fila, columna):
        """
        Realiza un disparo en las coordenadas especificadas.

        Args:
            fila (int): Fila donde se realiza el disparo.
            columna (int): Columna donde se realiza el disparo.

        Returns:
            bool: True si el disparo impactó una nave, False si fue al agua.

        Raises:
            ValueError: Si no hay un juego activo, las coordenadas están fuera del tablero,
                       o la celda ya fue impactada.

        Hola Jona: Este método permite al jugador realizar un disparo en el juego.
        Primero verificamos que haya un juego activo. Luego delegamos la acción
        al juego, que se encarga de evaluar el impacto. Si el juego termina después
        del disparo y hay un jugador activo, actualizamos su puntaje.
        """
        if not self.juego:
            raise ValueError("No hay un juego activo")

        impacto = self.juego.realizar_disparo(fila, columna)

        # Si el juego terminó y hay un jugador activo, actualizar puntaje
        if self.juego.esta_terminado() and self.jugador_activo:
            self.actualizar_puntaje(10)  # 10 puntos por ganar

        return impacto

    def registrar_jugador(self, nombre, contraseña):
        """
        Registra un nuevo jugador.

        Args:
            nombre (str): Nombre de usuario del jugador.
            contraseña (str): Contraseña del jugador.

        Returns:
            bool: True si el registro fue exitoso, False si el nombre ya existe o es inválido.

        Hola Jona: Este método registra un nuevo jugador en el sistema.
        Primero verificamos que el nombre de usuario no esté vacío y que no
        exista ya un jugador con ese nombre. Luego creamos un nuevo jugador
        y lo añadimos a la lista de jugadores. También lo registramos en la
        base de datos.
        """
        # Validar nombre de usuario
        if not nombre or nombre.strip() == "":
            return False

        # Verificar si el nombre ya existe
        for jugador in self.jugadores:
            if jugador.nombre_usuario == nombre:
                return False

        try:
            # Crear el jugador directamente en la base de datos
            from src.model.db_models import Jugador as JugadorDB

            # Verificar si ya existe en la base de datos
            jugador_existente = self.session.query(JugadorDB).filter_by(nombre_usuario=nombre).first()
            if jugador_existente:
                print(f"El jugador {nombre} ya existe en la base de datos.")
                return False

            # Crear nuevo jugador en la base de datos
            nuevo_jugador_db = JugadorDB(nombre_usuario=nombre, contraseña=contraseña)
            self.session.add(nuevo_jugador_db)
            self.session.commit()
            print(f"Jugador {nombre} creado en la base de datos con ID: {nuevo_jugador_db.id_jugador}")

            # Crear y añadir el nuevo jugador en memoria
            nuevo_jugador = Jugador(nombre, contraseña)
            self.jugadores.append(nuevo_jugador)

            return True
        except Exception as e:
            print(f"Error al registrar jugador en la base de datos: {str(e)}")
            import traceback
            traceback.print_exc()
            self.session.rollback()
            return False

    def iniciar_sesion(self, nombre, contraseña):
        """
        Inicia sesión con un jugador existente.

        Args:
            nombre (str): Nombre de usuario del jugador.
            contraseña (str): Contraseña del jugador.

        Returns:
            bool: True si el inicio de sesión fue exitoso, False si las credenciales son incorrectas.

        Hola Jona: Este método permite a un jugador iniciar sesión en el sistema.
        Buscamos un jugador con el nombre de usuario y contraseña proporcionados.
        Si lo encontramos, lo establecemos como el jugador activo y retornamos True.
        """
        try:
            # Verificar credenciales directamente en la base de datos
            from src.model.db_models import Jugador as JugadorDB

            # Buscar el jugador en la base de datos
            jugador_db = self.session.query(JugadorDB).filter_by(
                nombre_usuario=nombre,
                contraseña=contraseña
            ).first()

            if not jugador_db:
                print(f"Credenciales incorrectas para el usuario {nombre}")
                return False

            print(f"Inicio de sesión exitoso para {nombre} con ID: {jugador_db.id_jugador}")

            # Buscar el jugador en memoria
            for jugador in self.jugadores:
                if jugador.nombre_usuario == nombre:
                    self.jugador_activo = jugador
                    print(f"Jugador {nombre} encontrado en memoria y establecido como activo")
                    return True

            # Si no existe en memoria, crearlo
            nuevo_jugador = Jugador(nombre, contraseña)
            self.jugadores.append(nuevo_jugador)
            self.jugador_activo = nuevo_jugador
            print(f"Jugador {nombre} creado en memoria y establecido como activo")

            return True
        except Exception as e:
            print(f"Error al iniciar sesión: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def actualizar_puntaje(self, puntos):
        """
        Actualiza el puntaje del jugador activo.

        Args:
            puntos (int): Cantidad de puntos a añadir.

        Returns:
            int: Nuevo puntaje del jugador, o None si no hay jugador activo.

        Hola Jona: Este método actualiza el puntaje del jugador activo.
        Si hay un jugador activo, le añadimos los puntos especificados y
        retornamos su nuevo puntaje. Si no hay jugador activo, no hacemos nada.
        También actualizamos el puntaje en la base de datos.
        """
        if self.jugador_activo:
            # Actualizar puntaje en memoria
            nuevo_puntaje = self.jugador_activo.actualizar_puntaje(puntos)

            # Actualizar puntaje en la base de datos
            try:
                # Obtener el jugador de la base de datos
                from src.model.db_models import Jugador as JugadorDB
                jugador_db = self.session.query(JugadorDB).filter_by(nombre_usuario=self.jugador_activo.nombre_usuario).first()

                if not jugador_db:
                    # Si el jugador no existe en la base de datos, crearlo
                    jugador_db = JugadorDB(
                        nombre_usuario=self.jugador_activo.nombre_usuario,
                        contraseña=self.jugador_activo.contraseña
                    )
                    self.session.add(jugador_db)
                    self.session.commit()

                # Crear un nuevo juego si no existe
                from src.model.db_models import Juego as JuegoDB
                juego_db = JuegoDB(estado='terminado')
                juego_db.jugadores.append(jugador_db)
                self.session.add(juego_db)
                self.session.commit()

                # Registrar la puntuación
                from src.model.db_models import Puntuacion
                puntuacion = Puntuacion(
                    id_jugador=jugador_db.id_jugador,
                    id_juego=juego_db.id_juego,
                    puntos=nuevo_puntaje
                )
                self.session.add(puntuacion)
                self.session.commit()

                print(f"Puntuación registrada: {nuevo_puntaje} puntos para {jugador_db.nombre_usuario} en juego {juego_db.id_juego}")

            except Exception as e:
                print(f"Error al actualizar puntaje en la base de datos: {str(e)}")
                import traceback
                traceback.print_exc()
                self.session.rollback()

            return nuevo_puntaje
        return None

    def obtener_representacion_tablero(self):
        """
        Obtiene una representación visual del tablero.

        Returns:
            str: Representación del tablero como texto, o un mensaje si no hay juego activo.

        Hola Jona: Este método obtiene una representación visual del tablero
        para mostrar al jugador. Si hay un juego activo, delegamos esta tarea
        al juego. Si no hay juego activo, retornamos un mensaje indicándolo.
        """
        if self.juego:
            return self.juego.obtener_representacion_tablero()
        return "No hay un juego activo"

    def reiniciar_juego(self):
        """
        Reinicia el juego actual.

        Returns:
            bool: True si se reinició el juego, False si no hay juego activo.

        Hola Jona: Este método reinicia el juego actual. Si hay un juego activo,
        llamamos a su método reiniciar y retornamos True. Si no hay juego activo,
        retornamos False.
        """
        if self.juego:
            self.juego.reiniciar()
            return True
        return False

    def juego_terminado(self):
        """
        Verifica si el juego actual ha terminado.

        Returns:
            bool: True si el juego ha terminado, False si no ha terminado o no hay juego activo.

        Hola Jona: Este método verifica si el juego actual ha terminado.
        Si hay un juego activo, delegamos esta tarea al juego. Si no hay
        juego activo, retornamos False.
        """
        if self.juego:
            return self.juego.esta_terminado()
        return False

    def obtener_puntuaciones(self, limite=10):
        """
        Obtiene las mejores puntuaciones.

        Args:
            limite (int): Número máximo de puntuaciones a obtener.

        Returns:
            list: Lista de diccionarios con las puntuaciones.

        Hola Jona: Este método obtiene las mejores puntuaciones de la base de datos.
        Retorna una lista de diccionarios, donde cada diccionario contiene el nombre
        de usuario y el puntaje. Las puntuaciones están ordenadas de mayor a menor.
        """
        try:
            # Obtener puntuaciones de la base de datos
            from src.model.db_models import Puntuacion, Jugador as JugadorDB

            # Verificar si hay puntuaciones en la base de datos
            count = self.session.query(Puntuacion).count()
            print(f"Número de puntuaciones en la base de datos: {count}")

            # Si no hay puntuaciones, crear algunas de ejemplo
            if count == 0 and self.jugador_activo:
                print("No hay puntuaciones. Creando puntuaciones de ejemplo...")
                # Crear puntuaciones de ejemplo
                self.actualizar_puntaje(10)
                self.actualizar_puntaje(20)
                self.actualizar_puntaje(30)

            # Consulta para obtener las mejores puntuaciones
            resultados = self.session.query(
                Puntuacion, JugadorDB
            ).join(
                JugadorDB, Puntuacion.id_jugador == JugadorDB.id_jugador
            ).order_by(
                Puntuacion.puntos.desc()
            ).limit(limite).all()

            print(f"Resultados de la consulta: {len(resultados)}")

            # Convertir a formato de diccionario
            puntuaciones = []
            for puntuacion, jugador in resultados:
                puntuaciones.append({
                    'nombre_usuario': jugador.nombre_usuario,
                    'puntaje': puntuacion.puntos
                })
                print(f"Puntuación: {jugador.nombre_usuario} - {puntuacion.puntos}")

            return puntuaciones
        except Exception as e:
            print(f"Error al obtener puntuaciones: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
