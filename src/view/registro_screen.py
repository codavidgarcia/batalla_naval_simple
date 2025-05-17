"""
Módulo que define la pantalla de registro para el juego Batalla Naval.

Este módulo contiene la implementación de la pantalla de registro
que permite a los usuarios crear una nueva cuenta.

Autor: Juan David
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from src.controller.controlador import Controlador
import os

# Cargar el archivo KV que define la interfaz
kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'registro.kv')
Builder.load_file(os.path.abspath(kv_path))

class RegistroScreen(Screen):
    """
    Pantalla de registro de usuarios.
    
    Esta pantalla permite a los usuarios crear una nueva cuenta
    proporcionando un nombre de usuario y una contraseña.
    
    Atributos:
        mensaje (StringProperty): Mensaje para el usuario (éxito, error, etc.).
        controlador (Controlador): Instancia del controlador que gestiona la lógica del juego.
    
    Métodos:
        registrar(): Registra un nuevo usuario con los datos proporcionados.
        volver(): Vuelve al menú principal.
    
    Hola Jona: Esta clase representa la pantalla de registro de usuarios.
    Aquí definimos la propiedad mensaje que se mostrará en la interfaz y
    los métodos que responden a las acciones del usuario (registrar, volver).
    """
    
    # Propiedad que se actualiza en la interfaz
    mensaje = StringProperty("")
    
    def __init__(self, **kwargs):
        """
        Inicializa la pantalla de registro.
        
        Hola Jona: Aquí inicializamos la pantalla de registro. Creamos una instancia
        del controlador que gestionará la lógica del registro. La propiedad mensaje
        se actualizará durante el proceso de registro y se mostrará en la interfaz.
        """
        super(RegistroScreen, self).__init__(**kwargs)
        self.controlador = Controlador()
    
    def on_enter(self):
        """
        Se llama cuando se entra a esta pantalla.
        
        Hola Jona: Este método se llama automáticamente cuando el usuario
        navega a esta pantalla. Aquí limpiamos los campos de entrada y el mensaje.
        """
        # Limpiar campos de entrada
        if hasattr(self.ids, 'usuario_input'):
            self.ids.usuario_input.text = ""
        if hasattr(self.ids, 'contraseña_input'):
            self.ids.contraseña_input.text = ""
        
        # Limpiar mensaje
        self.mensaje = ""
    
    def registrar(self):
        """
        Registra un nuevo usuario con los datos proporcionados.
        
        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Registrarse". Obtenemos el nombre de usuario y la contraseña de los campos
        de entrada, validamos que no estén vacíos y registramos al usuario usando
        el controlador. Si el registro es exitoso, mostramos un mensaje de éxito.
        Si no, mostramos un mensaje de error.
        """
        # Obtener datos de entrada
        usuario = self.ids.usuario_input.text.strip()
        contraseña = self.ids.contraseña_input.text.strip()
        
        # Validar datos
        if not usuario or not contraseña:
            self.mensaje = "❌ Todos los campos son obligatorios."
            return
        
        # Registrar usuario
        if self.controlador.registrar_jugador(usuario, contraseña):
            self.mensaje = "✅ Usuario registrado correctamente."
            # Limpiar campos
            self.ids.usuario_input.text = ""
            self.ids.contraseña_input.text = ""
        else:
            self.mensaje = "❌ Error al registrar usuario. El nombre de usuario ya existe o es inválido."
    
    def volver(self):
        """
        Vuelve al menú principal.
        
        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Volver al Menú". Simplemente cambiamos la pantalla actual a la pantalla
        de menú.
        """
        self.manager.current = "menu"
