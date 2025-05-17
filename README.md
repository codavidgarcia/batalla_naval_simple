# Batalla Naval - Versión Simplificada

Este proyecto es una versión simplificada del juego Batalla Naval, implementado en Python con arquitectura MVC (Modelo-Vista-Controlador) y persistencia de datos usando SQLAlchemy.

## Características

- Juego de Batalla Naval completo con interfaz de línea de comandos (CLI) y gráfica (GUI)
- Sistema de usuarios con registro e inicio de sesión
- Persistencia de datos usando SQLAlchemy (ORM para bases de datos)
- Puntuaciones guardadas en base de datos
- Colocación aleatoria de naves
- Pruebas unitarias completas (76 tests)

## Estructura del Proyecto

El proyecto sigue una arquitectura MVC clara:

- **Modelo**: Clases que representan los datos y la lógica del juego.
  - `src/model/celda.py`: Representa una celda del tablero.
  - `src/model/nave.py`: Representa una nave en el juego.
  - `src/model/campo.py`: Representa el tablero de juego.
  - `src/model/juego.py`: Gestiona la lógica del juego.
  - `src/model/jugador.py`: Representa a un jugador.
  - `src/model/db_models.py`: Modelos ORM para la base de datos con SQLAlchemy.

- **Vista**: Interfaces de usuario.
  - `src/view/ventana_principal.py`: Ventana principal de la GUI.
  - `src/view/ventana_juego.py`: Ventana donde se juega la partida.
  - `src/view/ventana_login.py`: Ventana de inicio de sesión.

- **Controlador**: Coordina la interacción entre el modelo y la vista.
  - `src/controller/controlador.py`: Controlador principal del juego.

- **Pruebas**: Pruebas unitarias para verificar el funcionamiento del código.
  - `tests/model/`: Pruebas para los modelos.
  - `tests/controller/`: Pruebas para el controlador.
  - `tests/db/`: Pruebas para la base de datos.

## Requisitos

- Python 3.6 o superior
- SQLAlchemy 1.4.0 o superior (para la persistencia de datos)
- PyQt5 (para la interfaz gráfica)
- SQLite (incluido en Python)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/batalla-naval-simple.git
   cd batalla-naval-simple
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

### Interfaz Gráfica

Para ejecutar el juego con interfaz gráfica:

```bash
python main.py
```

### Línea de Comandos (CLI)

Para ejecutar el juego desde la línea de comandos:

```bash
python cli.py
```

## Pruebas

Para ejecutar todas las pruebas unitarias:

```bash
python run_tests.py
```

## Base de Datos

El juego utiliza SQLAlchemy como ORM (Object-Relational Mapping) para interactuar con la base de datos. Por defecto, utiliza SQLite, pero se puede configurar para usar PostgreSQL.

## Diagrama de Clases

\`\`\`
classDiagram
    direction LR

    class SistemaUsuario {
        +list~Jugador~ JugadoresRegistrados
        +bool RegistrarJugador()
        +bool IniciarSesion()
    }

    class Jugador {
        +str NombreUsuario
        +str Contrasenia
        +int Puntaje
        +str CambiarContrasenia()
        +int Actualizar_Puntaje()
    }

    class Juego {
        +int ancho
        +int alto
        +int num_naves
        +bool RealizarDisparo()
        +Jugador VerificarGanador()
        +void ReiniciarJuego()
    }

    class Campo {
        +list~list~ Celdas
        +int alto
        +int ancho
        +bool VerificarImpacto()
        +void NavesAleatorias()
        +void ColocarNaves()
        +void MostrarCampo()
    }

    class Celda {
        +bool Nave
        +bool Disparar
        +bool RecibirDisparo()
    }

    class Nave {
        +list Posicion
        +bool VerificarImpacto()
    }

    class Puntuaciones {
        +Jugador jugador
        +void ActualizarPuntuacion()
        +void MostrarPuntuaciones()
    }

    SistemaUsuario "1" --> "n" Jugador : gestiona
    Juego --> Campo : contiene
    Juego --> SistemaUsuario : usa
    Campo "1" *-- "n" Celda : composición
    Campo "1" --> "n" Nave : coloca
    Celda --> Nave : referencia
    Puntuaciones --> Jugador : pertenece a
    Celda --> Puntuaciones : reporta
\`\`\`

## Autor

Juan David

## Licencia

Este proyecto está bajo la Licencia MIT.
