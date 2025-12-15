"""
Punto de entrada principal para el Sistema de Minimización de Polarización

Este módulo lanza la interfaz gráfica de usuario.

Autores: Andrey Quiceño, Iván, Francesco, Jonathan
Fecha: Diciembre 2025
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Importar y ejecutar la GUI
from gui import main

if __name__ == "__main__":
    main()
