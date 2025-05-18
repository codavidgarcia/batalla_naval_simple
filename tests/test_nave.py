import pytest
from src.model.nave import Nave

# Pruebas normales
def test_creacion_nave():
    posicion = [(1, 1)]
    nave = Nave(posicion)
    assert nave.posicion == posicion

def test_verificar_impacto_positivo():
    posicion = [(1, 1), (1, 2), (1, 3)]
    nave = Nave(posicion)
    assert nave.verificar_impacto((1, 2)) == True

def test_verificar_impacto_negativo():
    posicion = [(1, 1), (1, 2), (1, 3)]
    nave = Nave(posicion)
    assert nave.verificar_impacto((2, 2)) == False

# Pruebas extremas
def test_nave_sin_posicion():
    posicion = []
    nave = Nave(posicion)
    assert nave.posicion == []
    assert nave.verificar_impacto((1, 1)) == False

def test_nave_con_muchas_posiciones():
    posicion = [(i, i) for i in range(100)]
    nave = Nave(posicion)
    assert len(nave.posicion) == 100
    assert nave.verificar_impacto((50, 50)) == True

def test_nave_con_posiciones_duplicadas():
    posicion = [(1, 1), (1, 1), (2, 2)]
    nave = Nave(posicion)
    assert len(nave.posicion) == 3  # No elimina duplicados
    assert nave.verificar_impacto((1, 1)) == True

# Pruebas de error
def test_verificar_impacto_con_coordenada_none():
    posicion = [(1, 1), (1, 2)]
    nave = Nave(posicion)
    assert nave.verificar_impacto(None) == False

def test_verificar_impacto_con_coordenada_invalida():
    posicion = [(1, 1), (1, 2)]
    nave = Nave(posicion)
    assert nave.verificar_impacto("coordenada") == False

def test_verificar_impacto_con_coordenada_incompleta():
    posicion = [(1, 1), (1, 2)]
    nave = Nave(posicion)
    assert nave.verificar_impacto((1,)) == False
