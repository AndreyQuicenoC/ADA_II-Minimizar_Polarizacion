# Sistema de Minimización de Polarización

## Descripción

Este proyecto implementa un modelo de optimización para minimizar la polarización en poblaciones utilizando Programación Entera Mixta con MiniZinc. El sistema permite decidir qué esfuerzos realizar para cambiar opiniones de personas, minimizando la polarización final respetando restricciones de costo y movimientos.

## Autores

- Andrey 
- Iván
- Francesco  
- Jonathan

**Universidad del Valle** - Análisis de Algoritmos II  
Diciembre 2025

## Características

- 🎯 Modelo completo en MiniZinc con Branch and Bound
- 🖥️ Interfaz gráfica moderna y profesional en Python/Tkinter
- 📊 Procesamiento automático de entradas/salidas
- ✅ Batería de 35 pruebas automatizadas
- 📈 Visualización detallada de resultados
- 💾 Exportación de soluciones en formato especificado

## Requisitos del Sistema

### Software Necesario

1. **Python 3.8+**
2. **MiniZinc 2.6+**
   - Descargar desde: https://www.minizinc.org/
   - Asegurarse de que `minizinc` esté en el PATH del sistema

### Dependencias de Python

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
ADA_II-Minimizar_Polarizacion/
├── model/                    # Modelo de optimización
│   └── Proyecto.mzn         # Modelo MiniZinc
├── main.py                   # Punto de entrada de la aplicación
├── gui.py                    # Interfaz gráfica
├── gui_styles.py             # Estilos y temas de la GUI
├── input_output/             # Módulos de procesamiento I/O
│   ├── input.py             # Parser de archivos .txt a .dzn
│   ├── output.py            # Procesador de salida de MiniZinc
│   └── __init__.py
├── scripts/                  # Scripts de utilidad
│   ├── run_tests.py         # Ejecutor de batería de pruebas
│   ├── validate_system.py   # Validación del sistema
│   └── build_exe.py         # Generador de ejecutable Windows
├── tests/                    # Archivos de prueba
│   ├── Prueba1.txt - Prueba35.txt
│   └── resultados.txt       # Resultados esperados
├── assets/                   # Recursos gráficos
│   └── logo.svg             # Logo de la aplicación
├── docs/                     # Documentación
│   ├── Enunciado.tex        # Enunciado del proyecto
│   ├── informe.tex          # Informe del proyecto
│   ├── informe.pdf          # Informe compilado
│   └── guion_sustentacion.md
└── README.md
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/AndreyQuicenoC/ADA_II-Minimizar_Polarizacion.git
cd ADA_II-Minimizar_Polarizacion
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota**: La aplicación usa principalmente módulos estándar de Python (tkinter, subprocess, etc.). El único requisito adicional es PyInstaller si deseas generar el ejecutable.

### 3. Instalar MiniZinc

**⚠️ IMPORTANTE**: MiniZinc es OBLIGATORIO para que el proyecto funcione.

#### Windows:
1. Descargar desde: https://www.minizinc.org/
2. Ejecutar el instalador
3. **Marcar la opción "Add MiniZinc to PATH"** durante la instalación
4. Reiniciar la computadora

#### Verificar instalación:
```bash
minizinc --version
```

Deberías ver algo como: `MiniZinc to FlatZinc converter, version 2.x.x`

Si ves un error como `'minizinc' is not recognized`, significa que:
- MiniZinc no está instalado, O
- No está en el PATH del sistema

**Solución**: Reinstala MiniZinc asegurándote de marcar "Add to PATH" y reinicia tu computadora.

## Uso

### Interfaz Gráfica

```bash
python main.py
```

#### Pasos para usar la interfaz:

1. **Seleccionar archivo**: Click en "Seleccionar archivo..." y elegir un archivo .txt de entrada
2. **Cargar datos**: Click en "Cargar datos" para parsear y visualizar los parámetros
3. **Ejecutar**: Click en "Ejecutar MiniZinc" para resolver el problema
4. **Ver resultados**: Los resultados se muestran en el panel derecho
5. **Guardar**: Click en "Guardar resultado" para exportar la solución

### Ejecutar Batería de Pruebas

```bash
python scripts/run_tests.py
```

Este script:
- Ejecuta las 35 pruebas automáticamente
- Compara con resultados esperados
- Muestra estadísticas de éxito/fallo
- Reporta tiempos de ejecución

### Uso Manual del Modelo

```bash
# Convertir entrada .txt a .dzn
python input_output/input.py tests/Prueba1.txt temp/datos.dzn

# Ejecutar MiniZinc
minizinc --solver Gecode model/Proyecto.mzn temp/datos.dzn
```

## Generar Ejecutable para Windows

Para crear un ejecutable independiente (.exe):

```bash
# Instalar PyInstaller (si no está instalado)
pip install pyinstaller

# Ejecutar script de build
python scripts/build_exe.py
```

El ejecutable se generará en `dist/PolarizacionApp.exe`

**⚠️ NOTA**: El ejecutable sigue requiriendo que MiniZinc esté instalado en el sistema del usuario.

## Formato de Entrada

Archivo `.txt` con la siguiente estructura:

```
n                           # Número de personas
m                           # Número de opiniones
p1,p2,...,pm               # Distribución de personas
v1,v2,...,vm               # Valores de opiniones
s1_bajo,s1_medio,s1_alto   # Resistencias opinión 1
s2_bajo,s2_medio,s2_alto   # Resistencias opinión 2
...
sm_bajo,sm_medio,sm_alto   # Resistencias opinión m
ct                         # Costo total máximo
maxMovs                    # Movimientos máximos
```

### Ejemplo:

```
10
3
3,3,4
0.297,0.673,0.809
1,2,0
0,3,0
2,1,1
25
5
```

## Formato de Salida

Archivo `.txt` con:

```
polarización
1                          # Nivel resistencia baja
matriz_movimientos_k1      # m×m movimientos
2                          # Nivel resistencia media
matriz_movimientos_k2      # m×m movimientos
3                          # Nivel resistencia alta
matriz_movimientos_k3      # m×m movimientos
```

## Modelo MiniZinc

El modelo implementa:

- **Parámetros**: n, m, p, v, s, ct, maxMovs
- **Variables**: x[k,i,j] (movimientos por nivel de resistencia)
- **Restricciones**:
  - No superar personas disponibles por resistencia
  - Conservación de población total
  - Límite de costo total
  - Límite de movimientos
- **Objetivo**: Minimizar Pol(p,v) = Σ pᵢ|vᵢ - mediana(p,v)|

## Pruebas

El proyecto incluye 35 casos de prueba con resultados validados:

- Pruebas 1-10: Casos pequeños (n ≤ 20)
- Pruebas 11-20: Casos medianos (n ≤ 50)
- Pruebas 21-35: Casos grandes (n > 50)

Para verificar todos los tests:

```bash
python scripts/run_tests.py
```

## Documentación

- **Enunciado**: [`docs/Enunciado.tex`](docs/Enunciado.tex)
- **Informe**: [`docs/informe.tex`](docs/informe.tex)
- **Guion de Sustentación**: [`docs/guion_sustentacion.md`](docs/guion_sustentacion.md)

## Licencia

Este proyecto es un trabajo académico para el curso de Análisis de Algoritmos II de la Universidad del Valle.

## Contacto

Para preguntas o comentarios sobre el proyecto, contactar a los autores a través del repositorio de GitHub.