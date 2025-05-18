import json
import os
from datetime import datetime

class JSONStorage:
    def __init__(self, json_dir='datos'):
        self.json_dir = json_dir
        self.jugadores_file = os.path.join(json_dir, 'jugadores.json')
        self.puntuaciones_file = os.path.join(json_dir, 'puntuaciones.json')
        
        # Crear directorio si no existe
        os.makedirs(json_dir, exist_ok=True)
        
        # Inicializar archivos JSON si no existen
        if not os.path.exists(self.jugadores_file):
            self._guardar_jugadores([])
        
        if not os.path.exists(self.puntuaciones_file):
            self._guardar_puntuaciones([])
    
    def _cargar_jugadores(self):
        try:
            with open(self.jugadores_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _guardar_jugadores(self, jugadores):
        with open(self.jugadores_file, 'w') as f:
            json.dump(jugadores, f, indent=4)
    
    def _cargar_puntuaciones(self):
        try:
            with open(self.puntuaciones_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _guardar_puntuaciones(self, puntuaciones):
        with open(self.puntuaciones_file, 'w') as f:
            json.dump(puntuaciones, f, indent=4)
    
    def registrar_jugador(self, nombre_usuario, contraseña):
        jugadores = self._cargar_jugadores()
        
        # Verificar si el jugador ya existe
        for jugador in jugadores:
            if jugador['nombre_usuario'] == nombre_usuario:
                return False
        
        # Crear nuevo jugador
        nuevo_jugador = {
            'id': len(jugadores) + 1,
            'nombre_usuario': nombre_usuario,
            'contraseña': contraseña
        }
        
        jugadores.append(nuevo_jugador)
        self._guardar_jugadores(jugadores)
        return True
    
    def iniciar_sesion(self, nombre_usuario, contraseña):
        jugadores = self._cargar_jugadores()
        
        for jugador in jugadores:
            if jugador['nombre_usuario'] == nombre_usuario and jugador['contraseña'] == contraseña:
                return jugador
        
        return None
    
    def actualizar_puntuacion(self, id_jugador, puntos):
        puntuaciones = self._cargar_puntuaciones()
        
        nueva_puntuacion = {
            'id': len(puntuaciones) + 1,
            'id_jugador': id_jugador,
            'puntos': puntos,
            'fecha': datetime.now().isoformat()
        }
        
        puntuaciones.append(nueva_puntuacion)
        self._guardar_puntuaciones(puntuaciones)
        return puntos
    
    def obtener_puntuaciones(self, limite=10):
        puntuaciones = self._cargar_puntuaciones()
        jugadores = self._cargar_jugadores()
        
        # Crear un diccionario para buscar nombres de jugadores por ID
        jugadores_dict = {j['id']: j['nombre_usuario'] for j in jugadores}
        
        # Formatear puntuaciones con nombres de jugadores
        resultado = []
        for p in puntuaciones:
            nombre_usuario = jugadores_dict.get(p['id_jugador'], 'Desconocido')
            resultado.append({
                'nombre_usuario': nombre_usuario,
                'puntaje': p['puntos'],
                'fecha': p['fecha']
            })
        
        # Ordenar por puntaje (de mayor a menor)
        resultado.sort(key=lambda x: x['puntaje'], reverse=True)
        
        # Limitar resultados
        return resultado[:limite]
