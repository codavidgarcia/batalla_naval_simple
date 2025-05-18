import pytest
from src.model.celda import Celda

# Pruebas normales
def test_creacion_celda():
    celda = Celda()
    assert celda.nave == False
    assert celda.disparada == False

def test_recibir_disparo_sin_nave():
    celda = Celda()
    resultado = celda.recibir_disparo()
    assert resultado == False
    assert celda.disparada == True

def test_recibir_disparo_con_nave():
    celda = Celda()
    celda.nave = True
    resultado = celda.recibir_disparo()
    assert resultado == True
    assert celda.disparada == True

# Pruebas extremas
def test_cambiar_estado_nave():
    celda = Celda()
    celda.nave = True
    assert celda.nave == True
    celda.nave = False
    assert celda.nave == False

def test_cambiar_estado_disparada():
    celda = Celda()
    celda.disparada = True
    assert celda.disparada == True

# Pruebas Error
def test_disparo_repetido():
    celda = Celda()
    celda.recibir_disparo()
    with pytest.raises(ValueError):
        celda.recibir_disparo()

# Pruebas adicionales
def test_celda_con_nave_no_disparada():
    celda = Celda()
    celda.nave = True
    assert celda.nave == True
    assert celda.disparada == False

def test_celda_sin_nave_disparada():
    celda = Celda()
    celda.recibir_disparo()
    assert celda.nave == False
    assert celda.disparada == True

def test_celda_con_nave_disparada():
    celda = Celda()
    celda.nave = True
    celda.recibir_disparo()
    assert celda.nave == True
    assert celda.disparada == True
