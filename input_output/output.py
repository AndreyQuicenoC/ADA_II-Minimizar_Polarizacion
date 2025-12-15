"""
Módulo para procesar la salida de MiniZinc y generar archivos de salida.

Este módulo parsea la salida de MiniZinc y genera archivos .txt con el formato
especificado en el enunciado del proyecto.

Autores: Andrey Quiceño, Iván, Francesco, Jonathan
Fecha: Diciembre 2025
"""

import re
from typing import Dict, List, Tuple


def parse_minizinc_output(output_str: str) -> Dict:
    """
    Parsea la salida de MiniZinc y extrae los valores relevantes.
    
    Args:
        output_str: String con la salida de MiniZinc
        
    Returns:
        Diccionario con polarización, distribución final y matrices de movimientos
        
    Raises:
        ValueError: Si no se puede parsear la salida
    """
    result = {}
    
    try:
        # Extraer polarización (incluye negativos y notación científica)
        pol_match = re.search(r'polarization=(-?[\d.]+(?:[eE][+-]?\d+)?)', output_str)
        if pol_match:
            result['polarization'] = float(pol_match.group(1))
        else:
            raise ValueError("No se encontró el valor de polarización")
        
        # Extraer distribución final
        dist_match = re.search(r'final_distribution=\[([\d, ]+)\]', output_str)
        if dist_match:
            result['final_distribution'] = [int(x.strip()) for x in dist_match.group(1).split(',')]
        
        # Extraer mediana
        median_match = re.search(r'median_value=([\d.]+)', output_str)
        if median_match:
            result['median_value'] = float(median_match.group(1))
        
        # Extraer matrices de movimientos
        for k in range(1, 4):
            pattern = rf'movements_k{k}=\[([\d,\s\n]+)\]'
            matrix_match = re.search(pattern, output_str)
            
            if matrix_match:
                matrix_str = matrix_match.group(1).strip()
                rows = matrix_str.split('\n')
                matrix = []
                
                for row in rows:
                    row = row.strip()
                    if row:
                        values = [int(x.strip()) for x in row.split(',') if x.strip()]
                        matrix.append(values)
                
                result[f'movements_k{k}'] = matrix
        
        return result
        
    except Exception as e:
        raise ValueError(f"Error al parsear la salida de MiniZinc: {str(e)}")


def generate_output_file(minizinc_output: str, output_path: str, m: int):
    """
    Genera un archivo de salida .txt según el formato especificado.
    
    Formato de salida:
    - Línea 1: Polarización final
    - Línea 2: Nivel de resistencia (1)
    - Siguientes m líneas: Matriz de movimientos para resistencia baja
    - Línea: Nivel de resistencia (2)
    - Siguientes m líneas: Matriz de movimientos para resistencia media
    - Línea: Nivel de resistencia (3)
    - Siguientes m líneas: Matriz de movimientos para resistencia alta
    
    Args:
        minizinc_output: String con la salida de MiniZinc
        output_path: Ruta donde guardar el archivo de salida
        m: Número de opiniones
    """
    try:
        parsed = parse_minizinc_output(minizinc_output)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Línea 1: Polarización (redondeada a 3 decimales)
            # Convertir -0.0 a 0.0 para evitar valores negativos en cero
            pol = parsed['polarization']
            pol = abs(pol) if abs(pol) < 0.0001 else pol
            f.write(f"{pol:.3f}\n")
            
            # Para cada nivel de resistencia
            for k in range(1, 4):
                # Línea: nivel de resistencia
                f.write(f"{k}\n")
                
                # Matriz de movimientos
                matrix = parsed.get(f'movements_k{k}', [])
                
                # Si la matriz no existe, crear una matriz de ceros
                if not matrix or len(matrix) != m:
                    matrix = [[0] * m for _ in range(m)]
                
                # Escribir cada fila de la matriz
                for row in matrix:
                    # Asegurarse de que la fila tenga m elementos
                    while len(row) < m:
                        row.append(0)
                    
                    row_str = ','.join(map(str, row[:m]))
                    f.write(f"{row_str}\n")
        
        return True
        
    except Exception as e:
        print(f"Error al generar archivo de salida: {e}")
        return False


def format_polarization(value: float) -> str:
    """
    Formatea el valor de polarización según el formato esperado.
    
    Args:
        value: Valor de polarización
        
    Returns:
        String formateado (con coma decimal y 3 decimales)
    """
    # Formato: 3 decimales, usando coma como separador decimal
    formatted = f"{value:.3f}"
    # Reemplazar punto por coma si es necesario
    formatted = formatted.replace('.', ',')
    return formatted


def read_output_file(filepath: str) -> Dict:
    """
    Lee un archivo de salida y extrae la información.
    
    Args:
        filepath: Ruta al archivo de salida
        
    Returns:
        Diccionario con polarización y matrices de movimientos
    """
    result = {
        'polarization': 0.0,
        'movements': {}
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if not lines:
            raise ValueError("El archivo está vacío")
        
        # Primera línea: polarización
        pol_str = lines[0].replace(',', '.')
        result['polarization'] = float(pol_str)
        
        # Leer las tres matrices
        idx = 1
        for k in range(1, 4):
            if idx >= len(lines):
                break
            
            # Leer nivel de resistencia
            level = int(lines[idx])
            idx += 1
            
            # Leer matriz (inferir m del número de líneas)
            matrix = []
            start_idx = idx
            
            # Leer hasta encontrar el siguiente nivel o fin de archivo
            while idx < len(lines):
                line = lines[idx]
                # Si es un número solo (1, 2, o 3), es el siguiente nivel
                if line in ['1', '2', '3'] and idx > start_idx:
                    break
                
                # Parsear fila de la matriz
                try:
                    row = [int(x) for x in line.split(',')]
                    matrix.append(row)
                    idx += 1
                except ValueError:
                    break
            
            result['movements'][level] = matrix
        
        return result
        
    except Exception as e:
        raise ValueError(f"Error al leer archivo de salida: {str(e)}")


if __name__ == "__main__":
    # Prueba del módulo
    import sys
    
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
        
        try:
            data = read_output_file(output_file)
            print(f"Polarización: {data['polarization']}")
            print(f"Movimientos por nivel: {list(data['movements'].keys())}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Uso: python output.py <archivo_salida.txt>")
