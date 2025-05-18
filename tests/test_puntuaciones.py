import pytest
from src.model.puntuaciones import Puntuaciones
from src.model.jugador import Jugador
from src.model.sistema_usuario import SistemaUsuario

@pytest.fixture
def sistema_usuario():
    return SistemaUsuario()

@pytest.fixture
def jugador():
    return Jugador("TestUser", "password123")

@pytest.fixture
def puntuaciones(sistema_usuario, jugador):
    return Puntuaciones(jugador, sistema_usuario.session)

#  PRUEBAS NORMALES
def test_actualizar_puntuacion(puntuaciones, jugador):
    nuevo_puntaje = puntuaciones.actualizar_puntuacion(10)
    assert nuevo_puntaje == 10
    assert jugador.puntaje == 10

def test_mostrar_puntuaciones(puntuaciones):
    try:
        resultado = puntuaciones.mostrar_puntuaciones()
        assert isinstance(resultado, list)
    except Exception as e:
        pytest.fail(f"La función mostrar_puntuaciones() lanzó un error: {e}")

def test_mostrar_puntuaciones_sin_jugadores(sistema_usuario):
    jugador_temp = Jugador("TempUser", "temp123")
    puntuaciones = Puntuaciones(jugador_temp, sistema_usuario.session)
    try:
        resultado = puntuaciones.mostrar_puntuaciones()
        assert isinstance(resultado, list)
    except Exception as e:
        pytest.fail(f"La función mostrar_puntuaciones() lanzó un error con lista vacía: {e}")

#  PRUEBAS EXTREMAS
def test_actualizar_puntuacion_cero(puntuaciones, jugador):
    nuevo_puntaje = puntuaciones.actualizar_puntuacion(0)
    assert nuevo_puntaje == 0
    assert jugador.puntaje == 0

def test_actualizar_puntuacion_negativa(puntuaciones, jugador):
    nuevo_puntaje = puntuaciones.actualizar_puntuacion(-10)
    assert nuevo_puntaje == -10
    assert jugador.puntaje == -10

def test_actualizar_puntuacion_grande(puntuaciones, jugador):
    nuevo_puntaje = puntuaciones.actualizar_puntuacion(9999)
    assert nuevo_puntaje == 9999
    assert jugador.puntaje == 9999

#  PRUEBAS DE ERROR
def test_actualizar_puntuacion_sin_jugador(sistema_usuario):
    puntuaciones = Puntuaciones(None, sistema_usuario.session)
    resultado = puntuaciones.actualizar_puntuacion(10)
    assert resultado is None

def test_actualizar_puntuacion_tipo_incorrecto(puntuaciones):
    with pytest.raises(TypeError):
        puntuaciones.actualizar_puntuacion("diez")

def test_mostrar_puntuaciones_limite(puntuaciones):
    try:
        resultado = puntuaciones.mostrar_puntuaciones(limite=1)
        assert isinstance(resultado, list)
        assert len(resultado) <= 1
    except Exception as e:
        pytest.fail(f"Error al mostrar puntuaciones con límite: {e}")
