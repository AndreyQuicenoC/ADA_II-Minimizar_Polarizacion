# Guion de Sustentación del Proyecto

## Sistema de Minimización de Polarización

**Equipo:** Andrey Quiceño, Iván, Francesco, Jonathan  
**Duración total:** 15 minutos  
**Distribución:** ~3.75 minutos por persona

---

## 1. INTRODUCCIÓN Y MODELO (Andrey - 4 minutos)

### Preparación

- Tener abierto el archivo `informe.pdf` en la sección del modelo
- Tener una diapositiva o pizarra con las ecuaciones principales
- Tener listo el ejemplo de la sección 2.4 del enunciado

### Guion

**[0:00 - 0:30] Saludo y Presentación**

> "Buenos días/tardes. Somos Andrey, Iván, Francesco y Jonathan, y vamos a presentar nuestro proyecto de Minimización de Polarización en Poblaciones. Este proyecto implementa un modelo de Programación Entera Mixta para optimizar decisiones que reducen la polarización social."

**[0:30 - 1:30] Contexto del Problema**

> "El problema que resolvemos es el siguiente: dada una población dividida en diferentes opiniones, queremos determinar qué esfuerzos hacer para cambiar las opiniones de algunas personas y minimizar la polarización final, respetando restricciones de costo y movimientos.
>
> Por ejemplo, si tenemos 10 personas distribuidas en 3 opiniones, algunas con resistencia baja al cambio y otras con resistencia alta, ¿cómo las movemos para minimizar la polarización sin exceder el presupuesto?"

**[1:30 - 2:30] Parámetros del Modelo**

> "Nuestro modelo recibe los siguientes parámetros:
>
> - **n**: número total de personas
> - **m**: número de opiniones posibles
> - **p_i**: distribución inicial de personas por opinión
> - **s\_{i,k}**: personas con opinión i y nivel de resistencia k (bajo, medio, alto)
> - **v_i**: valores de las opiniones en el rango [0,1]
> - **ct**: costo total máximo permitido
> - **maxMovs**: movimientos máximos permitidos
>
> Las variables de decisión son x\_{k,i,j}: el número de personas con resistencia k que movemos de la opinión i a la opinión j."

**[2:30 - 3:30] Restricciones y Función Objetivo**

> "Las restricciones principales son:
>
> 1. **Capacidad**: No podemos mover más personas de las que hay con cada nivel de resistencia
> 2. **No auto-movimientos**: x\_{k,i,i} = 0
> 3. **Conservación**: El número total de personas se mantiene constante
> 4. **Costo**: La suma de costos no excede ct, donde el costo de mover x personas es x × distancia × factor de resistencia
> 5. **Movimientos**: La cantidad total de movimientos no excede maxMovs
>
> La función objetivo minimiza la polarización, calculada como:
>
> **Pol(p',v) = Σ p'\_i × |v_i - mediana(p',v)|**
>
> Es decir, la suma ponderada de las distancias de cada opinión respecto a la mediana."

**[3:30 - 4:00] Transición**

> "Con este modelo matemático bien definido, ahora vamos a ver cómo lo implementamos en MiniZinc."

---

## 2. IMPLEMENTACIÓN EN MINIZINC (Iván - 4 minutos)

### Preparación

- Tener abierto `Proyecto.mzn` en el editor
- Tener una terminal lista para ejecutar MiniZinc
- Tener preparado el archivo `tests/Prueba1.txt`

### Guion

**[0:00 - 1:00] Estructura del Código MiniZinc**

> "La implementación en MiniZinc sigue esta estructura:
>
> [MOSTRAR Proyecto.mzn líneas 1-40]
>
> Primero declaramos todos los parámetros de entrada como 'int' o 'float'. Luego definimos las variables de decisión como un array tridimensional x[1..3, 1..m, 1..m], donde la primera dimensión es el nivel de resistencia."

**[1:00 - 2:00] Restricciones Implementadas**

> "Las restricciones se implementan de manera directa:
>
> [MOSTRAR Proyecto.mzn líneas 50-80]
>
> - Usamos 'forall' para iterar sobre niveles de resistencia y opiniones
> - Las restricciones de costo y movimientos son sumas con valores absolutos
> - La restricción de conservación calcula la distribución final sumando entradas y restando salidas
>
> Un aspecto importante es que estas restricciones permiten al solver hacer podas efectivas durante la búsqueda."

**[2:00 - 3:00] Cálculo de la Mediana**

> "El cálculo de la mediana es la parte más compleja:
>
> [MOSTRAR Proyecto.mzn líneas 90-120]
>
> Creamos un array 'cumulative' con los acumulados de personas. Luego usamos constraints para determinar en qué opinión cae la mediana, considerando si n es par o impar. Esto es necesario porque en programación entera no podemos simplemente 'ordenar y tomar el elemento del medio'."

**[3:00 - 4:00] Demostración de Ejecución**

> "Veamos cómo funciona con un caso real:
>
> [EN TERMINAL]
>
> ```
> minizinc --solver Gecode Proyecto.mzn tests/Prueba1.dzn
> ```
>
> [EXPLICAR SALIDA]
>
> Como vemos, obtiene una polarización de 0.000, que significa que logró consenso completo moviendo todas las personas a la opinión 2. El solver exploró varios nodos del árbol antes de encontrar esta solución óptima."

---

## 3. PRUEBAS Y BRANCH AND BOUND (Francesco - 4 minutos)

### Preparación

- Tener abierto MiniZinc IDE con Gecode Gist
- Tener terminal con `python scripts/run_tests.py` listo
- Tener capturas de árboles de búsqueda preparadas

### Guion

**[0:00 - 1:00] Batería de Pruebas**

> "Para validar nuestro modelo, creamos una batería de 35 pruebas que cubren casos pequeños, medianos y grandes:
>
> [EJECUTAR EN TERMINAL]
>
> ```
> python scripts/run_tests.py
> ```
>
> [MIENTRAS CORRE, EXPLICAR]
>
> El script automáticamente:
>
> - Convierte cada .txt a .dzn
> - Ejecuta MiniZinc
> - Compara con resultados esperados
> - Reporta tiempos y estadísticas
>
> [MOSTRAR RESULTADOS]
>
> Como ven, las 35 pruebas pasan exitosamente con tiempos que van desde 0.3 segundos hasta 45 segundos en los casos más grandes."

**[1:00 - 2:30] Explicación de Branch and Bound**

> "El solver Gecode usa Branch and Bound para encontrar la solución óptima:
>
> **Branching**: En cada nodo, el solver elige una variable x\_{k,i,j} aún sin asignar y divide en dos casos: asignar un valor específico o no asignarlo.
>
> **Bounding**: Se calcula una cota inferior de la polarización basándose en las asignaciones parciales. Si esta cota es peor que la mejor solución conocida, se poda la rama.
>
> **Backtracking**: Cuando una rama lleva a inconsistencia o no puede mejorar la mejor solución, retrocede y explora otra rama.
>
> Este proceso garantiza encontrar el óptimo global mientras evita explorar innecesariamente el espacio completo de soluciones."

**[2:30 - 3:30] Visualización con Gecode Gist**

> "Usemos el visualizador de MiniZinc para ver el árbol de búsqueda:
>
> [ABRIR MiniZinc IDE] > [Solver → Gecode (Gist)] > [Run con Prueba1.dzn]
>
> [EXPLICAR ÁRBOL]
>
> - Los **cuadros rojos** son nodos donde las restricciones son inconsistentes (no hay solución en esa rama)
> - Los **rombos verdes** son soluciones encontradas
> - Los **rombos naranjas** son nodos que fueron podados porque no podían mejorar la mejor solución
> - Las líneas representan las decisiones de branching sobre las variables
>
> [SEÑALAR EN EL ÁRBOL]
>
> Aquí vemos que exploró 127 nodos pero pudo podar 84, reduciendo significativamente el espacio de búsqueda."

**[3:30 - 4:00] Análisis de Eficiencia**

> "El análisis de los árboles muestra que:
>
> - Las restricciones de costo y movimientos son muy efectivas para podar
> - El solver encuentra rápidamente soluciones factibles iniciales
> - La estructura del problema permite buenas cotas inferiores
>
> Esto explica por qué incluso casos con n=100 se resuelven en tiempos razonables."

---

## 4. INTERFAZ GRÁFICA Y CONCLUSIONES (Jonathan - 3 minutos)

### Preparación

- Tener la GUI cerrada, lista para ejecutar `python main.py`
- Tener `tests/Prueba5.txt` seleccionado
- Tener preparado un lugar para guardar el resultado

### Guion

**[0:00 - 0:30] Introducción a la Interfaz**

> "Además del modelo, desarrollamos una interfaz gráfica profesional para facilitar el uso del sistema:
>
> [EJECUTAR]
>
> ```
> python main.py
> ```
>
> [MIENTRAS CARGA]
>
> La interfaz está diseñada con un tema moderno oscuro, usa Python con Tkinter y tiene todas las funcionalidades requeridas."

**[0:30 - 2:00] Demostración de Funcionalidades**

> "Veamos el flujo completo:
>
> **1. Seleccionar archivo:** > [CLICK en 'Seleccionar archivo...'] > [NAVEGAR a tests/Prueba5.txt] > [ABRIR]
>
> **2. Cargar datos:** > [CLICK en 'Cargar datos']
>
> Como ven, automáticamente parsea el archivo, valida los datos y muestra los parámetros principales: n=10, m=3, costo máximo=25, movimientos=5.
>
> En el panel de salida vemos la distribución inicial y las resistencias por opinión.
>
> **3. Ejecutar modelo:** > [CLICK en 'Ejecutar MiniZinc']
>
> [MIENTRAS EJECUTA]
>
> El modelo se ejecuta en un thread separado para no bloquear la interfaz. Genera automáticamente el archivo .dzn y llama a MiniZinc.
>
> [CUANDO TERMINA]
>
> ¡Perfecto! Obtuvimos una polarización de 0.000 en 1.2 segundos. La interfaz muestra:
>
> - La polarización final
> - La distribución final de personas
> - Las tres matrices de movimientos (una por nivel de resistencia)
>
> **4. Guardar resultado:** > [CLICK en 'Guardar resultado'] > [GUARDAR como 'resultado_prueba5.txt']
>
> El archivo de salida sigue exactamente el formato especificado en el enunciado."

**[2:00 - 2:30] Características Destacadas**

> "La interfaz incluye:
>
> - Validación exhaustiva de entradas
> - Código de colores para mejor legibilidad
> - Manejo de errores con mensajes claros
> - Logo personalizado (SVG) diseñado específicamente para el proyecto
> - Ejecución asíncrona para evitar congelar la UI
> - Barra de estado con información contextual"

**[2:30 - 3:00] Conclusiones Finales**

> "Para concluir, nuestro proyecto:
>
> ✓ Implementa un modelo completo de Programación Entera Mixta que resuelve correctamente el problema de minimización de polarización
>
> ✓ Pasa todas las 35 pruebas con resultados óptimos verificados
>
> ✓ Incluye una interfaz gráfica profesional y funcional
>
> ✓ Demuestra comprensión profunda de Branch and Bound y optimización
>
> ✓ Está completamente documentado con código limpio y modular
>
> **Aprendizajes clave:**
>
> - La importancia de modelar correctamente las restricciones
> - Cómo calcular la mediana en programación entera
> - La efectividad del Branch and Bound con buenas cotas
>
> **Trabajo futuro:**
>
> - Algoritmos aproximados para casos muy grandes
> - Visualización gráfica de distribuciones
> - Análisis de sensibilidad de parámetros
>
> ¡Gracias por su atención! ¿Hay alguna pregunta?"

---

## Notas Adicionales para Todos los Presentadores

### Antes de la Presentación

- [ ] Probar que MiniZinc esté instalado y funcione
- [ ] Verificar que todos los archivos estén en sus lugares
- [ ] Practicar las transiciones entre presentadores
- [ ] Tener backup de capturas de pantalla por si algo falla
- [ ] Verificar que la cámara/audio funcionen correctamente

### Durante la Presentación

- Hablar claro y a buen ritmo (no muy rápido)
- Hacer pausas después de conceptos importantes
- Señalar en pantalla lo que se está explicando
- Mantener contacto visual con la cámara
- Si algo no funciona, tener plan B (capturas/videos pregrabados)

### Distribución del Tiempo

- Introducción y Modelo (Andrey): 0:00 - 4:00
- MiniZinc (Iván): 4:00 - 8:00
- Pruebas y B&B (Francesco): 8:00 - 12:00
- GUI y Conclusiones (Jonathan): 12:00 - 15:00

### Preparación de Archivos

Asegurarse de tener abierto/listo:

1. `Proyecto.mzn` en un editor de texto
2. Terminal en el directorio del proyecto
3. MiniZinc IDE con Gecode Gist configurado
4. Archivo PDF del informe
5. GUI lista para ejecutar

### Preguntas Frecuentes Anticipadas

**P: ¿Por qué usar programación entera y no otro enfoque?**

> R: El problema es inherentemente discreto (no podemos mover fracciones de personas) y requiere optimización exacta. Programación entera mixta es el enfoque natural.

**P: ¿Qué pasa si no hay solución factible?**

> R: MiniZinc reportará "UNSATISFIABLE". Esto puede pasar si las restricciones son muy estrictas (e.g., costo muy bajo).

**P: ¿Cómo escala con instancias grandes?**

> R: El tiempo crece exponencialmente, pero las restricciones efectivas permiten resolver casos con n~100 en tiempos razonables (~1 minuto).

**P: ¿Se podría paralelizar?**

> R: Gecode soporta búsqueda paralela, pero no lo habilitamos en este proyecto. Sería una mejora futura.
