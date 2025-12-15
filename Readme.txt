# Readme.txt - Sistema de Minimización de Polarización

## DESCRIPCIÓN DEL PROYECTO

Este proyecto implementa un sistema completo de optimización para minimizar
la polarización en poblaciones mediante Programación Entera Mixta con MiniZinc.

Autores: Andrey Quiceño, Iván, Francesco, Jonathan
Universidad del Valle - Análisis de Algoritmos II
Diciembre 2025

## CONTENIDO DEL PAQUETE

1. **Proyecto.mzn** - Modelo de optimización en MiniZinc
2. **main.py** - Punto de entrada de la aplicación GUI
3. **gui.py** - Interfaz gráfica de usuario
4. **gui_styles.py** - Estilos y configuración visual
5. **input_output/** - Módulos de procesamiento de archivos
   - input.py - Conversión de .txt a .dzn
   - output.py - Procesamiento de salida de MiniZinc
6. **scripts/** - Scripts de utilidad
   - run_tests.py - Ejecutor de batería de pruebas
7. **tests/** - 35 casos de prueba con resultados esperados
8. **docs/** - Documentación completa
   - Enunciado.tex - Especificación del problema
   - informe.tex - Informe del proyecto
   - guion_sustentacion.md - Guion para la presentación
9. **assets/** - Recursos gráficos
   - logo.svg - Logo de la aplicación
10. **README.md** - Documentación completa en Markdown

## REQUISITOS DEL SISTEMA

### Software Obligatorio

1. **Python 3.8 o superior**
   - Descargar de: https://www.python.org/downloads/
   - IMPORTANTE: Marcar "Add Python to PATH" durante instalación

2. **MiniZinc 2.6 o superior**
   - Descargar de: https://www.minizinc.org/
   - IMPORTANTE: Agregar minizinc al PATH del sistema
   - Verificar con: minizinc --version

3. **LaTeX (opcional, para compilar el informe)**
   - Windows: MiKTeX (https://miktex.org/)
   - Linux: texlive-full
   - Mac: MacTeX (https://www.tug.org/mactex/)

### Dependencias

El proyecto solo usa bibliotecas estándar de Python:
- tkinter (incluido con Python)
- subprocess, threading, pathlib, typing, re (estándar)

## INSTALACIÓN

### Paso 1: Verificar Python

Abrir terminal/PowerShell y ejecutar:
```
python --version
```
Debe mostrar Python 3.8 o superior.

### Paso 2: Verificar MiniZinc

Ejecutar:
```
minizinc --version
```
Debe mostrar la versión de MiniZinc instalada.

Si no funciona, asegurarse de que MiniZinc esté en el PATH:
- Windows: Agregar C:\Program Files\MiniZinc a las variables de entorno
- Linux/Mac: Verificar que el binario esté en /usr/local/bin

### Paso 3: Descomprimir el proyecto

Extraer el archivo .zip en una carpeta de su elección.

## INSTRUCCIONES DE EJECUCIÓN

### Opción 1: Interfaz Gráfica (Recomendado)

1. Abrir terminal en el directorio del proyecto
2. Ejecutar:
   ```
   python main.py
   ```
3. En la interfaz:
   a) Click en "Seleccionar archivo..." y elegir un .txt de tests/
   b) Click en "Cargar datos" para visualizar parámetros
   c) Click en "Ejecutar MiniZinc" para resolver
   d) Click en "Guardar resultado" para exportar solución

### Opción 2: Línea de Comandos

#### Convertir entrada .txt a .dzn:
```
python input_output/input.py tests/Prueba1.txt temp/datos.dzn
```

#### Ejecutar MiniZinc:
```
minizinc --solver Gecode Proyecto.mzn temp/datos.dzn
```

### Opción 3: Ejecutar Batería de Pruebas

Para validar todas las 35 pruebas automáticamente:
```
python scripts/run_tests.py
```

Este script:
- Convierte cada prueba a .dzn
- Ejecuta MiniZinc
- Compara con resultados esperados
- Muestra estadísticas y tiempos

## FORMATO DE ARCHIVOS

### Archivo de Entrada (.txt)

```
n                           # Línea 1: Número de personas
m                           # Línea 2: Número de opiniones
p1,p2,...,pm               # Línea 3: Distribución de personas
v1,v2,...,vm               # Línea 4: Valores de opiniones [0,1]
s1_bajo,s1_medio,s1_alto   # Línea 5: Resistencias opinión 1
s2_bajo,s2_medio,s2_alto   # Línea 6: Resistencias opinión 2
...
sm_bajo,sm_medio,sm_alto   # Línea 4+m: Resistencias opinión m
ct                         # Línea 5+m: Costo total máximo
maxMovs                    # Línea 6+m: Movimientos máximos
```

Ejemplo (tests/Prueba1.txt):
```
10
3
1,8,1
0.345,0.394,0.5
0,1,0
3,3,2
0,1,0
25
5
```

### Archivo de Salida (.txt)

```
polarización               # Línea 1: Valor de polarización final
1                         # Línea 2: Nivel resistencia baja
matriz m×m                # Líneas 3 a 2+m: Movimientos k=1
2                         # Nivel resistencia media
matriz m×m                # Movimientos k=2
3                         # Nivel resistencia alta
matriz m×m                # Movimientos k=3
```

## COMPILAR DOCUMENTACIÓN

### Compilar informe.pdf:

```
cd docs
pdflatex informe.tex
pdflatex informe.tex
```
(Ejecutar dos veces para referencias cruzadas)

### Compilar Enunciado.pdf:

```
cd docs
pdflatex Enunciado.tex
```

## ESTRUCTURA DE DIRECTORIOS

```
Proyecto/
├── Proyecto.mzn              # Modelo MiniZinc
├── main.py                   # Launcher GUI
├── gui.py                    # Código GUI
├── gui_styles.py             # Estilos
├── README.md                 # Documentación
├── Readme.txt                # Este archivo
├── requirements.txt          # Dependencias
├── input_output/             # Módulos I/O
│   ├── __init__.py
│   ├── input.py
│   └── output.py
├── scripts/                  # Scripts útiles
│   └── run_tests.py
├── tests/                    # Casos de prueba
│   ├── Prueba1.txt - Prueba35.txt
│   └── resultados.txt
├── docs/                     # Documentación
│   ├── Enunciado.tex
│   ├── informe.tex
│   └── guion_sustentacion.md
├── assets/                   # Recursos
│   └── logo.svg
└── temp/                     # Archivos temporales (creado automáticamente)
```

## RESOLUCIÓN DE PROBLEMAS

### Error: "minizinc no se reconoce como comando"
- Solución: Agregar MiniZinc al PATH del sistema
- Windows: Panel de Control → Sistema → Variables de entorno
- Agregar la ruta de instalación de MiniZinc (ej: C:\Program Files\MiniZinc)

### Error: "No module named 'tkinter'"
- Solución en Ubuntu/Debian:
  ```
  sudo apt-get install python3-tk
  ```
- Solución en macOS:
  ```
  brew install python-tk
  ```

### La GUI no muestra correctamente
- Verificar que tkinter esté instalado correctamente
- En algunos sistemas Linux puede requerir:
  ```
  sudo apt-get install python3-tk python3-pil python3-pil.imagetk
  ```

### MiniZinc es muy lento
- Normal para casos grandes (n > 100)
- Reducir el time-limit en la GUI o usar --time-limit en CLI
- Considerar solvers más rápidos (Gurobi, CPLEX) si están disponibles

### Error al compilar LaTeX
- Verificar que todos los paquetes necesarios estén instalados
- En MiKTeX, permitir instalación automática de paquetes
- Ejecutar pdflatex dos veces para resolver referencias

## INFORMACIÓN ADICIONAL

### Video de Sustentación
El video está disponible en el enlace proporcionado en el informe.pdf

### Contacto
Para dudas o comentarios:
- Repositorio: https://github.com/AndreyQuicenoC/ADA_II-Minimizar_Polarizacion
- Correo: [Información de contacto de los autores]

### Licencia
Este proyecto es un trabajo académico para el curso de Análisis de Algoritmos II
de la Universidad del Valle. Todos los derechos reservados.

## NOTAS IMPORTANTES

1. **Tiempo de Ejecución**: Los casos grandes pueden tomar varios minutos.
   Es normal. La interfaz mostrará una barra de progreso.

2. **Archivos Temporales**: El sistema genera archivos .dzn en la carpeta temp/.
   Pueden eliminarse manualmente si se desea.

3. **Validación de Entrada**: El sistema valida exhaustivamente los archivos
   de entrada. Mensajes de error detallados guiarán en caso de problemas.

4. **Resultados Óptimos**: El solver garantiza encontrar la solución óptima.
   Si el problema es infactible, MiniZinc lo reportará.

5. **Formato de Números**: Los resultados usan punto decimal (0.123) pero
   pueden configurarse para usar coma si es necesario.

## AGRADECIMIENTOS

Agradecemos al profesor Jesús Alexander Aranda y al monitor Mauricio Muñoz
por su guía durante el desarrollo de este proyecto.

---
Fin del archivo Readme.txt
