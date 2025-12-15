"""
Script para ejecutar la batería completa de pruebas del proyecto.

Este script ejecuta todas las pruebas disponibles, compara con los resultados
esperados y muestra un reporte profesional en consola.

Autores: Andrey Quiceño, Iván, Francesco, Jonathan
Fecha: Diciembre 2025
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple
import re

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from input_output.input import txt_to_dzn
from input_output.output import parse_minizinc_output


# Colores ANSI para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Imprime un encabezado decorado."""
    width = 80
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * width}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(width)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * width}{Colors.ENDC}\n")


def print_subheader(text: str):
    """Imprime un sub-encabezado."""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'-' * len(text)}{Colors.ENDC}")


def print_success(text: str):
    """Imprime mensaje de éxito."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Imprime mensaje de error."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Imprime mensaje de advertencia."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_info(text: str):
    """Imprime mensaje informativo."""
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")


def load_expected_results(results_file: Path) -> Dict[int, float]:
    """
    Carga los resultados esperados desde el archivo resultados.txt
    
    Args:
        results_file: Ruta al archivo de resultados
        
    Returns:
        Diccionario {número_prueba: polarización_esperada}
    """
    results = {}
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Saltar la cabecera
        for line in lines[2:]:  # Las primeras 2 líneas son cabecera
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) >= 2:
                try:
                    test_num = int(parts[0])
                    # Reemplazar coma por punto para conversión
                    pol_str = parts[1].replace(',', '.')
                    polarization = float(pol_str)
                    results[test_num] = polarization
                except (ValueError, IndexError):
                    continue
        
        return results
        
    except Exception as e:
        print_error(f"Error al cargar resultados esperados: {e}")
        return {}


def run_minizinc(mzn_file: Path, dzn_file: Path, timeout: int = 300) -> Tuple[bool, str, float]:
    """
    Ejecuta MiniZinc con un modelo y datos.
    
    Args:
        mzn_file: Ruta al archivo .mzn
        dzn_file: Ruta al archivo .dzn
        timeout: Tiempo máximo de ejecución en segundos
        
    Returns:
        Tupla (éxito, salida, tiempo_ejecución)
    """
    start_time = time.time()
    
    try:
        # Comando para ejecutar MiniZinc
        cmd = [
            'minizinc',
            '--solver', 'Gecode',
            '--output-mode', 'json',
            '--time-limit', str(timeout * 1000),  # en milisegundos
            str(mzn_file),
            str(dzn_file)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            return True, result.stdout, elapsed_time
        else:
            return False, result.stderr, elapsed_time
            
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        return False, "TIMEOUT", elapsed_time
    except FileNotFoundError:
        return False, "MiniZinc no encontrado. Asegúrese de que esté instalado y en el PATH.", 0
    except Exception as e:
        return False, str(e), 0


def extract_polarization(minizinc_output: str) -> float:
    """
    Extrae el valor de polarización de la salida de MiniZinc.
    
    Args:
        minizinc_output: Salida de MiniZinc
        
    Returns:
        Valor de polarización
    """
    try:
        parsed = parse_minizinc_output(minizinc_output)
        return parsed.get('polarization', None)
    except:
        # Intentar extraer directamente
        match = re.search(r'polarization=([\d.]+)', minizinc_output)
        if match:
            return float(match.group(1))
        return None


def compare_results(obtained: float, expected: float, tolerance: float = 0.001) -> bool:
    """
    Compara dos valores de polarización.
    
    Args:
        obtained: Valor obtenido
        expected: Valor esperado
        tolerance: Tolerancia para la comparación
        
    Returns:
        True si los valores son iguales dentro de la tolerancia
    """
    if obtained is None:
        return False
    return abs(obtained - expected) <= tolerance


def run_test(test_num: int, tests_dir: Path, mzn_file: Path, 
             expected_pol: float, temp_dir: Path) -> Dict:
    """
    Ejecuta una prueba individual.
    
    Args:
        test_num: Número de la prueba
        tests_dir: Directorio de pruebas
        mzn_file: Archivo .mzn del modelo
        expected_pol: Polarización esperada
        temp_dir: Directorio temporal para archivos .dzn
        
    Returns:
        Diccionario con los resultados de la prueba
    """
    test_file = tests_dir / f"Prueba{test_num}.txt"
    
    if not test_file.exists():
        return {
            'test_num': test_num,
            'status': 'NOT_FOUND',
            'message': f"Archivo {test_file.name} no encontrado"
        }
    
    # Generar archivo .dzn
    dzn_file = temp_dir / f"Prueba{test_num}.dzn"
    
    try:
        txt_to_dzn(str(test_file), str(dzn_file))
    except Exception as e:
        return {
            'test_num': test_num,
            'status': 'PARSE_ERROR',
            'message': f"Error al parsear entrada: {str(e)}"
        }
    
    # Ejecutar MiniZinc
    success, output, exec_time = run_minizinc(mzn_file, dzn_file)
    
    if not success:
        return {
            'test_num': test_num,
            'status': 'EXECUTION_ERROR',
            'message': output,
            'time': exec_time
        }
    
    # Extraer polarización
    obtained_pol = extract_polarization(output)
    
    if obtained_pol is None:
        return {
            'test_num': test_num,
            'status': 'OUTPUT_ERROR',
            'message': "No se pudo extraer la polarización de la salida",
            'time': exec_time
        }
    
    # Comparar resultados
    matches = compare_results(obtained_pol, expected_pol)
    
    return {
        'test_num': test_num,
        'status': 'PASS' if matches else 'FAIL',
        'expected': expected_pol,
        'obtained': obtained_pol,
        'diff': abs(obtained_pol - expected_pol),
        'time': exec_time,
        'message': 'OK' if matches else f"Diferencia: {abs(obtained_pol - expected_pol):.6f}"
    }


def print_test_result(result: Dict):
    """Imprime el resultado de una prueba de forma estética."""
    test_num = result['test_num']
    status = result['status']
    
    prefix = f"Prueba {test_num:2d}"
    
    if status == 'PASS':
        pol = result['obtained']
        time_str = f"{result['time']:.3f}s"
        print_success(f"{prefix}: Polarización = {pol:.3f} | Tiempo = {time_str}")
    elif status == 'FAIL':
        exp = result['expected']
        obt = result['obtained']
        diff = result['diff']
        print_error(f"{prefix}: Esperado = {exp:.3f}, Obtenido = {obt:.3f}, Diff = {diff:.6f}")
    elif status == 'NOT_FOUND':
        print_warning(f"{prefix}: {result['message']}")
    elif status == 'EXECUTION_ERROR':
        if result['message'] == 'TIMEOUT':
            print_error(f"{prefix}: TIMEOUT (>{result['time']:.1f}s)")
        else:
            print_error(f"{prefix}: Error de ejecución")
    else:
        print_error(f"{prefix}: {result['message']}")


def print_summary(results: List[Dict]):
    """Imprime un resumen de todos los resultados."""
    print_subheader("RESUMEN DE RESULTADOS")
    
    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] not in ['PASS', 'FAIL'])
    
    print(f"\n{Colors.BOLD}Total de pruebas:{Colors.ENDC} {total}")
    print(f"{Colors.OKGREEN}{Colors.BOLD}Pasadas:{Colors.ENDC} {passed} ({100*passed/total:.1f}%)")
    print(f"{Colors.FAIL}{Colors.BOLD}Fallidas:{Colors.ENDC} {failed} ({100*failed/total:.1f}%)")
    print(f"{Colors.WARNING}{Colors.BOLD}Errores:{Colors.ENDC} {errors} ({100*errors/total:.1f}%)")
    
    # Estadísticas de tiempo
    times = [r['time'] for r in results if 'time' in r and r['time'] > 0]
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        print(f"\n{Colors.BOLD}Tiempo de ejecución:{Colors.ENDC}")
        print(f"  Promedio: {avg_time:.3f}s")
        print(f"  Mínimo:   {min_time:.3f}s")
        print(f"  Máximo:   {max_time:.3f}s")


def main():
    """Función principal del script de pruebas."""
    print_header("BATERÍA DE PRUEBAS - MINIMIZAR POLARIZACIÓN")
    
    # Rutas
    tests_dir = ROOT_DIR / 'tests'
    results_file = tests_dir / 'resultados.txt'
    mzn_file = ROOT_DIR / 'model' / 'Proyecto.mzn'
    temp_dir = ROOT_DIR / 'temp'
    
    # Crear directorio temporal
    temp_dir.mkdir(exist_ok=True)
    
    # Verificar archivos
    if not mzn_file.exists():
        print_error(f"Archivo de modelo no encontrado: {mzn_file}")
        return 1
    
    if not results_file.exists():
        print_error(f"Archivo de resultados no encontrado: {results_file}")
        return 1
    
    # Cargar resultados esperados
    print_info("Cargando resultados esperados...")
    expected_results = load_expected_results(results_file)
    print_success(f"Cargados {len(expected_results)} resultados esperados")
    
    # Ejecutar pruebas
    print_subheader("EJECUTANDO PRUEBAS")
    
    results = []
    for test_num in sorted(expected_results.keys()):
        expected_pol = expected_results[test_num]
        result = run_test(test_num, tests_dir, mzn_file, expected_pol, temp_dir)
        results.append(result)
        print_test_result(result)
    
    # Mostrar resumen
    print_summary(results)
    
    # Retornar código de salida
    failed_count = sum(1 for r in results if r['status'] != 'PASS')
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
