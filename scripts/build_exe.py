"""
Script para generar ejecutable de Windows del Sistema de Minimización de Polarización

Este script usa PyInstaller para crear un ejecutable independiente (.exe) que incluye
todas las dependencias necesarias.

Requisitos:
- PyInstaller instalado: pip install pyinstaller
- Python 3.8+

Uso:
    python scripts/build_exe.py

El ejecutable se generará en: dist/PolarizacionApp.exe
"""

import sys
import os
from pathlib import Path
import subprocess
import shutil

# Directorio raíz del proyecto
ROOT_DIR = Path(__file__).parent.parent
DIST_DIR = ROOT_DIR / 'dist'
BUILD_DIR = ROOT_DIR / 'build'

def clean_previous_builds():
    """Elimina builds anteriores"""
    print("🧹 Limpiando builds anteriores...")
    
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        print(f"  ✓ Eliminado {DIST_DIR}")
    
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"  ✓ Eliminado {BUILD_DIR}")
    
    spec_file = ROOT_DIR / 'PolarizacionApp.spec'
    if spec_file.exists():
        spec_file.unlink()
        print(f"  ✓ Eliminado {spec_file}")

def build_executable():
    """Construye el ejecutable con PyInstaller"""
    print("\n🔨 Construyendo ejecutable...")
    
    # Opciones de PyInstaller
    cmd = [
        'pyinstaller',
        '--name=PolarizacionApp',
        '--onefile',  # Un solo archivo ejecutable
        '--windowed',  # Sin consola (solo GUI)
        '--icon=assets/logo.ico' if (ROOT_DIR / 'assets' / 'logo.ico').exists() else '',
        '--add-data=model;model',  # Incluir directorio model
        '--add-data=assets;assets',  # Incluir assets
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.scrolledtext',
        '--collect-all=input_output',
        f'--specpath={ROOT_DIR}',
        str(ROOT_DIR / 'main.py')
    ]
    
    # Filtrar argumentos vacíos
    cmd = [arg for arg in cmd if arg]
    
    try:
        result = subprocess.run(cmd, cwd=ROOT_DIR, check=True, capture_output=True, text=True)
        print("  ✓ Ejecutable creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error al crear ejecutable:")
        print(e.stderr)
        return False

def create_readme():
    """Crea un README para el ejecutable"""
    print("\n📝 Creando README para distribución...")
    
    readme_content = """# Sistema de Minimización de Polarización - Ejecutable Windows

## Requisitos
- Windows 10 o superior
- **MiniZinc 2.6+** instalado y en el PATH del sistema
  - Descargar desde: https://www.minizinc.org/
  - Durante la instalación, asegúrate de marcar "Add to PATH"

## Instalación de MiniZinc
1. Visita https://www.minizinc.org/
2. Descarga el instalador para Windows
3. Ejecuta el instalador
4. **IMPORTANTE**: Marca la opción "Add MiniZinc to PATH"
5. Reinicia tu computadora después de la instalación

## Verificar instalación de MiniZinc
Abre PowerShell o CMD y ejecuta:
```
minizinc --version
```
Deberías ver la versión de MiniZinc. Si aparece un error, significa que MiniZinc no está en el PATH.

## Uso del programa
1. Asegúrate de que MiniZinc esté instalado (ver arriba)
2. Ejecuta `PolarizacionApp.exe`
3. La interfaz gráfica se abrirá automáticamente
4. Sigue los pasos en la interfaz para cargar datos y ejecutar optimizaciones

## Solución de problemas

### "MiniZinc no está instalado o no está en el PATH"
- Verifica que MiniZinc esté instalado
- Ejecuta `minizinc --version` en una terminal nueva
- Si no funciona, reinstala MiniZinc marcando "Add to PATH"
- Reinicia tu computadora

### Error al abrir archivos
- Asegúrate de que los archivos .txt tengan el formato correcto
- Consulta la documentación del proyecto para el formato de entrada

## Contacto
Para más información, visita el repositorio del proyecto:
https://github.com/AndreyQuicenoC/ADA_II-Minimizar_Polarizacion

Autores: Andrey Quiceño, Iván, Francesco, Jonathan
Universidad del Valle - 2025
"""
    
    readme_file = DIST_DIR / 'README.txt'
    readme_file.write_text(readme_content, encoding='utf-8')
    print(f"  ✓ README creado en {readme_file}")

def main():
    """Función principal"""
    print("=" * 70)
    print("  BUILD DEL EJECUTABLE - SISTEMA DE MINIMIZACIÓN DE POLARIZACIÓN")
    print("=" * 70)
    
    # Verificar que PyInstaller esté instalado
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', '--version'],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            # Intentar con comando directo
            result = subprocess.run(
                ['pyinstaller', '--version'],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                raise FileNotFoundError("PyInstaller not available")
        print(f"\n✓ PyInstaller detectado: {result.stdout.strip()}")
    except (FileNotFoundError, Exception) as e:
        print("\n❌ Error: PyInstaller no está instalado o no se puede ejecutar")
        print("Instala con: pip install pyinstaller")
        print(f"Detalles: {e}")
        return 1
    
    # Limpiar builds anteriores
    clean_previous_builds()
    
    # Construir ejecutable
    if not build_executable():
        print("\n❌ Falló la construcción del ejecutable")
        return 1
    
    # Crear README
    create_readme()
    
    # Información final
    print("\n" + "=" * 70)
    print("✅ BUILD COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print(f"\nEjecutable creado en: {DIST_DIR / 'PolarizacionApp.exe'}")
    print(f"README incluido en: {DIST_DIR / 'README.txt'}")
    print("\n⚠️  RECORDATORIO IMPORTANTE:")
    print("El usuario DEBE tener MiniZinc instalado y en el PATH del sistema.")
    print("Instrucciones incluidas en el README.txt de la distribución.")
    print("\n" + "=" * 70)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
