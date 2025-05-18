from src.model.sistema_usuario import PuntuacionDB

class Puntuaciones:
    def __init__(self, jugador, session):
        self.jugador = jugador
        self.session = session

    def actualizar_puntuacion(self, puntos):
        if self.jugador:
            nuevo_puntaje = self.jugador.actualizar_puntaje(puntos)

            try:
                from src.model.sistema_usuario import JugadorDB
                jugador_db = self.session.query(JugadorDB).filter_by(nombre_usuario=self.jugador.nombre_usuario).first()

                if not jugador_db:
                    print(f"No se encontró el jugador {self.jugador.nombre_usuario} en la base de datos.")
                    return nuevo_puntaje

                puntuacion = PuntuacionDB(
                    id_jugador=jugador_db.id_jugador,
                    puntos=nuevo_puntaje
                )
                self.session.add(puntuacion)
                self.session.commit()

                print(f"Puntuación registrada: {nuevo_puntaje} puntos para {self.jugador.nombre_usuario}")

            except Exception as e:
                print(f"Error al actualizar puntaje en la base de datos: {str(e)}")
                import traceback
                traceback.print_exc()
                self.session.rollback()

            return nuevo_puntaje
        return None

    def mostrar_puntuaciones(self, limite=10):
        try:
            from src.model.sistema_usuario import PuntuacionDB, JugadorDB

            resultados = self.session.query(
                PuntuacionDB, JugadorDB
            ).join(
                JugadorDB, PuntuacionDB.id_jugador == JugadorDB.id_jugador
            ).order_by(
                PuntuacionDB.puntos.desc()
            ).limit(limite).all()

            puntuaciones = []
            for puntuacion, jugador in resultados:
                puntuaciones.append({
                    'nombre_usuario': jugador.nombre_usuario,
                    'puntaje': puntuacion.puntos
                })

            return puntuaciones
        except Exception as e:
            print(f"Error al obtener puntuaciones: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
