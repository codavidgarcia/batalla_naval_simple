"""
Script para probar la funcionalidad de puntuaciones.
"""

from src.model.db_models import DatabaseManager, Jugador, Juego, Puntuacion

def main():
    # Inicializar la base de datos
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    try:
        # Crear un jugador de prueba
        jugador = session.query(Jugador).filter_by(nombre_usuario="jugador_test").first()
        if not jugador:
            jugador = Jugador(nombre_usuario="jugador_test", contraseña="123456")
            session.add(jugador)
            session.commit()
            print(f"Jugador creado con ID: {jugador.id_jugador}")
        else:
            print(f"Jugador encontrado con ID: {jugador.id_jugador}")
        
        # Crear un juego
        juego = Juego(estado="terminado")
        juego.jugadores.append(jugador)
        session.add(juego)
        session.commit()
        print(f"Juego creado con ID: {juego.id_juego}")
        
        # Crear una puntuación
        puntuacion = Puntuacion(
            id_jugador=jugador.id_jugador,
            id_juego=juego.id_juego,
            puntos=100
        )
        session.add(puntuacion)
        session.commit()
        print(f"Puntuación registrada: 100 puntos para {jugador.nombre_usuario}")
        
        # Verificar puntuaciones
        puntuaciones = session.query(Puntuacion).all()
        print(f"Número de puntuaciones en la base de datos: {len(puntuaciones)}")
        
        for p in puntuaciones:
            j = session.query(Jugador).filter_by(id_jugador=p.id_jugador).first()
            print(f"Puntuación: {j.nombre_usuario} - {p.puntos}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
