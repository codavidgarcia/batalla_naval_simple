"""
Módulo que define la pantalla de inicio de sesión para el juego Batalla Naval.

Este módulo contiene la implementación de la pantalla de inicio de sesión
que permite a los usuarios acceder a su cuenta.

Autor: Juan David
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from src.controller.controlador import Controlador
import os

# Cargar el archivo KV que define la interfaz
kv_path = os.path.join(os.path.dirname(__file__), 'kv', 'login.kv')
Builder.load_file(os.path.abspath(kv_path))

class LoginScreen(Screen):
    """
    Pantalla de inicio de sesión.
    
    Esta pantalla permite a los usuarios iniciar sesión con su cuenta
    proporcionando su nombre de usuario y contraseña.
    
    Atributos:
        mensaje (StringProperty): Mensaje para el usuario (éxito, error, etc.).
        controlador (Controlador): Instancia del controlador que gestiona la lógica del juego.
    
    Métodos:
        iniciar_sesion(): Inicia sesión con las credenciales proporcionadas.
        volver(): Vuelve al menú principal.
    
    Hola Jona: Esta clase representa la pantalla de inicio de sesión.
    Aquí definimos la propiedad mensaje que se mostrará en la interfaz y
    los métodos que responden a las acciones del usuario (iniciar sesión, volver).
    """
    
    # Propiedad que se actualiza en la interfaz
    mensaje = StringProperty("")
    
    def __init__(self, **kwargs):
        """
        Inicializa la pantalla de inicio de sesión.
        
        Hola Jona: Aquí inicializamos la pantalla de inicio de sesión. Creamos una instancia
        del controlador que gestionará la lógica del inicio de sesión. La propiedad mensaje
        se actualizará durante el proceso de inicio de sesión y se mostrará en la interfaz.
        """
        super(LoginScreen, self).__init__(**kwargs)
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
    
    def iniciar_sesion(self):
        """
        Inicia sesión con las credenciales proporcionadas.
        
        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Iniciar Sesión". Obtenemos el nombre de usuario y la contraseña de los campos
        de entrada, validamos que no estén vacíos e iniciamos sesión usando el controlador.
        Si el inicio de sesión es exitoso, navegamos a la pantalla de juego.
        Si no, mostramos un mensaje de error.
        """
        # Obtener datos de entrada
        usuario = self.ids.usuario_input.text.strip()
        contraseña = self.ids.contraseña_input.text.strip()
        
        # Validar datos
        if not usuario or not contraseña:
            self.mensaje = "❌ Todos los campos son obligatorios."
            return
        
        # Iniciar sesión
        if self.controlador.iniciar_sesion(usuario, contraseña):
            self.mensaje = "✅ Inicio de sesión exitoso."
            # Compartir el controlador con la pantalla de juego
            juego_screen = self.manager.get_screen("juego")
            juego_screen.controlador = self.controlador
            # Navegar a la pantalla de juego
            self.manager.current = "juego"
        else:
            self.mensaje = "❌ Credenciales incorrectas."
    
    def volver(self):
        """
        Vuelve al menú principal.
        
        Hola Jona: Este método se llama cuando el usuario hace clic en el botón
        "Volver al Menú". Simplemente cambiamos la pantalla actual a la pantalla
        de menú.
        """
        self.manager.current = "menu"
