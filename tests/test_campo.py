from src.model.campo import Campo
import pytest

# Pruebas Normales
def test_creacion_campo_dimensiones():
    campo = Campo(5, 5, 3)
    assert len(campo.celdas) == 5
    assert len(campo.celdas[0]) == 5

def test_campo_inicializado():
    campo = Campo(5, 5, 3)
    assert campo.ancho == 5
    assert campo.alto == 5
    assert campo.num_naves == 3
    assert campo.naves_restantes == 3

def test_verificar_impacto():
    campo = Campo(5, 5, 3)
    # Colocar una nave manualmente en una posición conocida
    campo.celdas[2][2] = 1  # Nave sin disparar
    impacto = campo.verificar_impacto(2, 2)
    assert impacto == True
    assert campo.naves_restantes == 2

# Pruebas Extremas
def test_campo_tamano_minimo():
    with pytest.raises(ValueError):
        Campo(1, 1, 1)

def test_campo_tamano_maximo():
    # En la versión simplificada, no hay límite máximo explícito
    campo = Campo(20, 20, 5)
    assert campo.ancho == 20
    assert campo.alto == 20

def test_campo_mas_naves_que_espacios():
    with pytest.raises(ValueError):
        Campo(3, 3, 10)

# Pruebas de Error
def test_campo_valores_negativos():
    with pytest.raises(ValueError):
        Campo(-5, 5, 3)

def test_verificar_impacto_fuera_de_rango():
    campo = Campo(5, 5, 3)
    with pytest.raises(ValueError):
        campo.verificar_impacto(5, 5)  # Fuera de rango

def test_verificar_impacto_celda_ya_impactada():
    campo = Campo(5, 5, 3)
    # Disparar a una celda
    campo.verificar_impacto(2, 2)
    # Disparar a la misma celda de nuevo
    with pytest.raises(ValueError):
        campo.verificar_impacto(2, 2)

# Pruebas adicionales
def test_mostrar_campo():
    campo = Campo(3, 3, 1)
    representacion = campo.mostrar_campo()
    assert isinstance(representacion, str)
    assert len(representacion.split('\n')) > 3  # Al menos 3 líneas (encabezado + 3 filas)

def test_naves_aleatorias():
    campo = Campo(5, 5, 3)
    # Reiniciar el tablero a todo agua
    campo.celdas = [[0 for _ in range(campo.ancho)] for _ in range(campo.alto)]
    # Reiniciar naves
    campo.naves_aleatorias()
    # Contar naves después
    naves_despues = sum(1 for fila in campo.celdas for celda in fila if celda == 1)
    assert naves_despues == 3

def test_colocar_naves():
    campo = Campo(5, 5, 3)
    # Reiniciar el tablero a todo agua
    campo.celdas = [[0 for _ in range(campo.ancho)] for _ in range(campo.alto)]
    # Colocar naves
    campo.colocar_naves()
    # Contar naves
    naves = sum(1 for fila in campo.celdas for celda in fila if celda == 1)
    assert naves == 3
