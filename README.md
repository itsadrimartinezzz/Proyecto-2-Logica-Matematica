# Proyecto 2: SAT con fuerza bruta y DPLL Logica Matematica
# Prof. Paulo Mejia

Implementación en Python de dos métodos para resolver el problema de satisfacibilidad booleana (SAT) para fórmulas en forma normal conjuntiva (CNF): fuerza bruta y DPLL sencillo.

El programa determina si una fórmula es satisfacible. Si lo es, devuelve una asignación de valores de verdad; de lo contrario, informa que es insatisfacible y devuelve una asignación nula. También genera y visualiza el árbol de decisiones de DPLL.

## Requisitos

- Python 3.10 o superior.
- `matplotlib` únicamente para exportar los árboles a PNG.

Instala las dependencias desde la raíz del proyecto:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

### Ejecutar los seis ejemplos

```bash
python main.py
```

En terminales que no muestran correctamente caracteres Unicode, usa:

```bash
python main.py --ascii
```

### Exportar árboles a PNG

```bash
python main.py --png
```

Las imágenes se guardan en la carpeta `arboles/` con los nombres `ejemplo_1.png` a `ejemplo_6.png`.

### Usar el menú interactivo

```bash
python menu.py
```

El menú permite resolver los ejemplos uno por uno o volver a generar los árboles PNG.

### Ejecutar las pruebas

```bash
python test_sat.py
```

La prueba compara DPLL con fuerza bruta en casos fijos y fórmulas aleatorias, verifica que las asignaciones encontradas satisfagan cada fórmula y revisa la consistencia de los árboles generados.

## Representación de fórmulas

Una fórmula es una lista de cláusulas y cada cláusula es una lista de literales de texto:

```python
[["p", "q"], ["-p", "r"], ["-q"]]
```

La representación anterior equivale a:

```text
(p ∨ q) ∧ (¬p ∨ r) ∧ ¬q
```

Se puede usar `-`, `¬`, `~` o `!` para indicar la negación de una variable.

## Algoritmos implementados

### Fuerza bruta

Prueba todas las asignaciones posibles para las variables de la fórmula. Si hay `n` variables, examina como máximo `2^n` combinaciones.

### DPLL sencillo

El algoritmo DPLL se implementa de forma recursiva:

1. Si no quedan cláusulas, la fórmula es satisfacible.
2. Si aparece una cláusula vacía, la rama es insatisfacible.
3. Se selecciona una variable no asignada.
4. Se prueba primero su valor verdadero y se simplifica la fórmula.
5. Si esa rama falla, se prueba el valor falso.

El árbol de ejecución muestra cada decisión, las fórmulas simplificadas y el resultado de cada rama.

## Estructura del proyecto

```text
.
├── main.py            # Ejecuta los seis ejemplos
├── menu.py            # Menú interactivo
├── fuerza_bruta.py    # Solucionador por fuerza bruta
├── dpll.py            # Solucionador DPLL recursivo
├── comun.py           # Representación y simplificación de fórmulas
├── traza.py           # Construcción y presentación del árbol DPLL
├── arbol_png.py       # Exportación de árboles a PNG
├── reporte.py         # Informe en terminal y comparación de resultados
├── ejemplos.py        # Fórmulas de ejemplo
├── test_sat.py        # Pruebas de validación
├── requirements.txt   # Dependencias
└── arboles/           # Árboles PNG generados
```

## Ejemplos incluidos

El proyecto incluye seis fórmulas del enunciado, entre ellas fórmulas satisfacibles, insatisfacibles y tautológicas. Para cada una se muestra:

- La fórmula booleana y su forma clausal.
- El resultado y la asignación obtenidos por fuerza bruta.
- El resultado y la asignación obtenidos por DPLL.
- El árbol de decisiones de DPLL.
- Una comparación del trabajo realizado por ambos enfoques.

## Autores

- Adriana Martínez -- 24086
- Daniel Sandoval -- 24885
- Diego Sandoval -- 231977
- Saúl Castillo -- 24915
- Diego Gudiel -- 24451
- Luis Alejandro Hernández -- 241424
