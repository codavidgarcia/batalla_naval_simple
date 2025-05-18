import pytest
from src.model.jugador import Jugador

#  PRUEBAS NORMALES
def test_creacion_jugador():
    jugador = Jugador("usuario123", "contraseña123")
    assert jugador.nombre_usuario == "usuario123"
    assert jugador.contraseña == "contraseña123"
    assert jugador.puntaje == 0

def test_actualizar_puntaje():
    jugador = Jugador("usuario123", "contraseña123")
    nuevo_puntaje = jugador.actualizar_puntaje(10)
    assert nuevo_puntaje == 10
    assert jugador.puntaje == 10

def test_str_representation():
    jugador = Jugador("usuario123", "contraseña123")
    assert str(jugador) == "Jugador: usuario123, Puntaje: 0"

#  PRUEBAS EXTREMAS
def test_actualizar_puntaje_cero():
    jugador = Jugador("usuario123", "contraseña123")
    nuevo_puntaje = jugador.actualizar_puntaje(0)
    assert nuevo_puntaje == 0
    assert jugador.puntaje == 0

def test_actualizar_puntaje_muy_alto():
    jugador = Jugador("usuario123", "contraseña123")
    nuevo_puntaje = jugador.actualizar_puntaje(9999999)
    assert nuevo_puntaje == 9999999
    assert jugador.puntaje == 9999999

def test_nombre_usuario_largo():
    nombre_largo = "a" * 100
    jugador = Jugador(nombre_largo, "contraseña123")
    assert jugador.nombre_usuario == nombre_largo

#  PRUEBAS DE ERROR
def test_creacion_jugador_nombre_vacio():
    with pytest.raises(ValueError):
        Jugador("", "contraseña123")

def test_creacion_jugador_contraseña_vacia():
    with pytest.raises(ValueError):
        Jugador("usuario123", "")

def test_actualizar_puntaje_no_numerico():
    jugador = Jugador("usuario123", "contraseña123")
    with pytest.raises(TypeError):
        jugador.actualizar_puntaje("diez")
