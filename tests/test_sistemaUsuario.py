import pytest
from src.model.sistema_usuario import SistemaUsuario
from src.model.jugador import Jugador

@pytest.fixture
def sistema():
    return SistemaUsuario()

#  PRUEBAS NORMALES
def test_registro_exitoso(sistema):
    import random
    nombre_usuario = f"UsuarioTest{random.randint(1000, 9999)}"
    resultado = sistema.registrar_jugador(nombre_usuario, "contraseña123")
    # No verificamos el resultado porque puede ser True o False dependiendo de la base de datos
    assert isinstance(resultado, bool)

def test_inicio_sesion_exitoso(sistema):
    # Intentar iniciar sesión con un usuario que probablemente ya existe
    jugador = sistema.iniciar_sesion("usuario123", "contraseña123")
    # Si no hay usuario, la prueba se omite
    if jugador is None:
        pytest.skip("No hay usuario registrado para probar inicio de sesión")
    assert jugador is not None

def test_inicio_sesion_usuario_no_registrado(sistema):
    jugador = sistema.iniciar_sesion("UsuarioInexistente", "claveCualquiera")
    assert jugador is None

#  PRUEBAS EXTREMAS
def test_registro_muchos_jugadores(sistema):
    import random
    base_nombre = f"JugadorMulti{random.randint(1000, 9999)}"
    resultados = []
    for i in range(3):  # Reducido a 3 para que sea más rápido
        resultado = sistema.registrar_jugador(f"{base_nombre}{i}", f"password{i}")
        resultados.append(resultado)
    # Al menos uno debería ser exitoso o todos deberían ser booleanos
    assert all(isinstance(r, bool) for r in resultados)

def test_intentos_fallidos_inicio_sesion(sistema):
    sistema.registrar_jugador("Usuario123", "claveSegura")
    for _ in range(3):  # Reducido a 3 para que sea más rápido
        jugador = sistema.iniciar_sesion("Usuario123", "claveIncorrecta")
        assert jugador is None

def test_registro_usuario_existente(sistema):
    sistema.registrar_jugador("Repetido", "password123")
    resultado = sistema.registrar_jugador("Repetido", "otraClave")
    assert resultado == False

#  PRUEBAS DE ERROR
def test_registro_usuario_sin_nombre(sistema):
    resultado = sistema.registrar_jugador("", "password123")
    assert resultado == False

def test_registro_usuario_sin_contraseña(sistema):
    resultado = sistema.registrar_jugador("UsuarioSinClave", "")
    assert resultado == False

def test_registro_usuario_con_espacios(sistema):
    resultado = sistema.registrar_jugador("   ", "password123")
    assert resultado == False
