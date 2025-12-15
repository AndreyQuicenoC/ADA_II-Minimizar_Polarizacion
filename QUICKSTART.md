# GUÍA RÁPIDA DE INICIO - Sistema de Minimización de Polarización

## Para Usuarios Nuevos (Instalación desde Cero)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/AndreyQuicenoC/ADA_II-Minimizar_Polarizacion.git
cd ADA_II-Minimizar_Polarizacion
```

### Paso 2: Instalar Python

- Descargar Python 3.8 o superior desde: https://www.python.org/
- Durante la instalación, **marcar "Add Python to PATH"**
- Verificar: `python --version`

### Paso 3: Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

### Paso 4: Instalar MiniZinc (⚠️ OBLIGATORIO)

1. Ir a: https://www.minizinc.org/
2. Descargar el instalador para Windows
3. Ejecutar el instalador
4. **MUY IMPORTANTE**: Marcar la opción "Add MiniZinc to PATH"
5. Reiniciar la computadora

### Paso 5: Verificar Instalación de MiniZinc

Abrir una terminal NUEVA (después de reiniciar) y ejecutar:

```bash
minizinc --version
```

**Si ves la versión de MiniZinc**: ✅ ¡Todo listo!
**Si ves un error**: ❌ MiniZinc no está en el PATH. Reinstala marcando la opción "Add to PATH".

### Paso 6: Ejecutar la Aplicación

```bash
python main.py
```

## Problemas Comunes

### "MiniZinc no está instalado o no está en el PATH"

**Solución:**

1. Verifica que MiniZinc esté instalado
2. Abre una terminal NUEVA (PowerShell o CMD)
3. Ejecuta: `minizinc --version`
4. Si no funciona:
   - Reinstala MiniZinc
   - Asegúrate de marcar "Add to PATH"
   - **Reinicia tu computadora** (importante)
   - Prueba de nuevo en una terminal nueva

### "python: command not found"

**Solución:**

- Reinstala Python marcando "Add Python to PATH"
- Reinicia la terminal

### La GUI no se abre

**Solución:**

- Verifica que Python esté instalado: `python --version`
- Asegúrate de estar en el directorio del proyecto
- Intenta: `python main.py`

## Uso Rápido

1. Ejecuta: `python main.py`
2. Click en "Seleccionar archivo..." y elige un archivo de prueba (tests/Prueba1.txt)
3. Click en "Cargar datos"
4. Click en "Ejecutar MiniZinc"
5. Espera los resultados (puede tomar unos segundos)
6. Opcional: "Guardar resultado" para exportar

## Generar Ejecutable Windows (.exe)

Si quieres un archivo .exe que no requiera abrir Python:

```bash
python scripts/build_exe.py
```

El ejecutable estará en: `dist/PolarizacionApp.exe`

**Nota**: El .exe SIGUE REQUIRIENDO que MiniZinc esté instalado en el sistema.

## Ejecutar Pruebas Automatizadas

```bash
python scripts/run_tests.py
```

Esto ejecutará las 35 pruebas y comparará con los resultados esperados.

## Soporte

Para problemas o preguntas:

- Revisa el README.md principal
- Consulta la documentación en docs/
- Abre un issue en GitHub

---

**Autores**: Andrey Quiceño, Iván, Francesco, Jonathan  
**Universidad del Valle** - Análisis de Algoritmos II - 2025
