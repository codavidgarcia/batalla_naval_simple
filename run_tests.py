"""
Script para ejecutar todas las pruebas unitarias.

Este script descubre y ejecuta todas las pruebas unitarias
en el directorio 'tests' y sus subdirectorios.

Autor: Juan David
"""

import unittest
import sys
import os

def run_tests():
    """
    Descubre y ejecuta todas las pruebas unitarias.
    
    Returns:
        bool: True si todas las pruebas pasaron, False en caso contrario.
    """
    # Añadir el directorio actual al path para que Python pueda encontrar los módulos
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Descubrir todas las pruebas
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    
    # Ejecutar las pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Imprimir un resumen
    print("\n" + "=" * 70)
    print(f"Total de pruebas: {result.testsRun}")
    print(f"Pruebas exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Pruebas fallidas: {len(result.failures)}")
    print(f"Pruebas con errores: {len(result.errors)}")
    print("=" * 70)
    
    # Retornar True si todas las pruebas pasaron
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
