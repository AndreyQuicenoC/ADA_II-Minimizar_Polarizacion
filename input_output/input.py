"""
Módulo para procesar archivos de entrada del problema de Minimizar Polarización.

Este módulo lee archivos .txt con el formato especificado en el enunciado
y genera archivos .dzn para MiniZinc.

Autores: Andrey Quiceño, Iván, Francesco, Jonathan
Fecha: Diciembre 2025
"""

import os
from typing import Dict, List, Tuple


def parse_input_file(filepath: str) -> Dict:
    """
    Lee un archivo de entrada y extrae los parámetros del problema.
    
    Formato del archivo:
    - Línea 1: n (número de personas)
    - Línea 2: m (número de opiniones)
    - Línea 3: distribución de personas por opinión (p[i])
    - Línea 4: valores de las opiniones (v[i])
    - Líneas 5 a 4+m: resistencias por opinión (bajo, medio, alto)
    - Línea 5+m: costo total máximo (ct)
    - Línea 6+m: movimientos máximos (maxMovs)
    
    Args:
        filepath: Ruta al archivo de entrada
        
    Returns:
        Diccionario con los parámetros del problema
        
    Raises:
        ValueError: Si el formato del archivo es inválido
        FileNotFoundError: Si el archivo no existe
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if len(lines) < 7:
            raise ValueError("El archivo debe tener al menos 7 líneas no vacías")
        
        # Línea 1: número de personas
        n = int(lines[0])
        if n <= 0:
            raise ValueError("El número de personas debe ser positivo")
        
        # Línea 2: número de opiniones
        m = int(lines[1])
        if m <= 0:
            raise ValueError("El número de opiniones debe ser positivo")
        
        # Línea 3: distribución de personas por opinión
        p = [int(x) for x in lines[2].split(',')]
        if len(p) != m:
            raise ValueError(f"Se esperaban {m} valores en la distribución de personas, se encontraron {len(p)}")
        
        if sum(p) != n:
            raise ValueError(f"La suma de personas por opinión ({sum(p)}) no coincide con n ({n})")
        
        # Línea 4: valores de las opiniones
        v = [float(x) for x in lines[3].split(',')]
        if len(v) != m:
            raise ValueError(f"Se esperaban {m} valores de opiniones, se encontraron {len(v)}")
        
        # Validar que los valores estén en [0,1]
        for i, val in enumerate(v):
            if not (0 <= val <= 1):
                raise ValueError(f"El valor de la opinión {i+1} ({val}) debe estar en [0,1]")
        
        # Líneas 5 a 4+m: resistencias por opinión
        if len(lines) < 4 + m:
            raise ValueError(f"Se esperaban {m} líneas de resistencias")
        
        s = []
        total_by_resistance = [0, 0, 0]  # bajo, medio, alto
        
        for i in range(m):
            resistance_line = lines[4 + i].split(',')
            if len(resistance_line) != 3:
                raise ValueError(f"La línea de resistencia {i+1} debe tener 3 valores")
            
            resistances = [int(x) for x in resistance_line]
            s.append(resistances)
            
            # Verificar que la suma de resistencias coincida con p[i]
            if sum(resistances) != p[i]:
                raise ValueError(
                    f"La suma de resistencias para opinión {i+1} ({sum(resistances)}) "
                    f"no coincide con p[{i+1}] ({p[i]})"
                )
            
            for j, r in enumerate(resistances):
                total_by_resistance[j] += r
        
        # Línea 5+m: costo total máximo
        ct = float(lines[4 + m])
        if ct < 0:
            raise ValueError("El costo total máximo debe ser no negativo")
        
        # Línea 6+m: movimientos máximos
        maxMovs = float(lines[5 + m])
        if maxMovs < 0:
            raise ValueError("Los movimientos máximos deben ser no negativos")
        
        return {
            'n': n,
            'm': m,
            'p': p,
            'v': v,
            's': s,
            'ct': ct,
            'maxMovs': maxMovs
        }
        
    except (IndexError, ValueError) as e:
        raise ValueError(f"Error al parsear el archivo: {str(e)}")


def generate_dzn_file(params: Dict, output_path: str):
    """
    Genera un archivo .dzn para MiniZinc a partir de los parámetros.
    
    Args:
        params: Diccionario con los parámetros del problema
        output_path: Ruta donde guardar el archivo .dzn
    """
    n = params['n']
    m = params['m']
    p = params['p']
    v = params['v']
    s = params['s']
    ct = params['ct']
    maxMovs = params['maxMovs']
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"% Datos generados automáticamente\n")
        f.write(f"% Problema de Minimizar Polarización\n\n")
        
        f.write(f"n = {n};\n")
        f.write(f"m = {m};\n\n")
        
        # Array p
        f.write(f"p = [{', '.join(map(str, p))}];\n\n")
        
        # Array v con formato de decimales
        v_str = ', '.join([f"{val:.3f}" for val in v])
        f.write(f"v = [{v_str}];\n\n")
        
        # Matriz s (m x 3)
        # Formato MiniZinc: usar | para separar filas
        f.write(f"s = [|\n")
        for i, resistances in enumerate(s):
            f.write(f"  {', '.join(map(str, resistances))}")
            if i < len(s) - 1:
                f.write(" |\n")  # pipe para separar filas
            else:
                f.write("\n")
        f.write(f"|];\n\n")
        
        f.write(f"ct = {ct};\n")
        f.write(f"maxMovs = {maxMovs};\n")


def txt_to_dzn(input_txt_path: str, output_dzn_path: str = None) -> str:
    """
    Convierte un archivo .txt de entrada a un archivo .dzn.
    
    Args:
        input_txt_path: Ruta al archivo .txt de entrada
        output_dzn_path: Ruta donde guardar el .dzn (opcional)
        
    Returns:
        Ruta al archivo .dzn generado
    """
    if output_dzn_path is None:
        base_name = os.path.splitext(input_txt_path)[0]
        output_dzn_path = f"{base_name}.dzn"
    
    params = parse_input_file(input_txt_path)
    generate_dzn_file(params, output_dzn_path)
    
    return output_dzn_path


if __name__ == "__main__":
    # Prueba del módulo
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        try:
            result = txt_to_dzn(input_file, output_file)
            print(f"✓ Archivo .dzn generado: {result}")
        except Exception as e:
            print(f"✗ Error: {e}")
            sys.exit(1)
    else:
        print("Uso: python input.py <archivo_entrada.txt> [archivo_salida.dzn]")
