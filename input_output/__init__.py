"""
Módulo de entrada/salida para el problema de Minimizar Polarización.
"""

from .input import parse_input_file, generate_dzn_file, txt_to_dzn
from .output import parse_minizinc_output, generate_output_file, read_output_file, format_polarization

__all__ = [
    'parse_input_file',
    'generate_dzn_file',
    'txt_to_dzn',
    'parse_minizinc_output',
    'generate_output_file',
    'read_output_file',
    'format_polarization'
]
