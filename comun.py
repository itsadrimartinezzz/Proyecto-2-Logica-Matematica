"""Representación de fórmulas y utilidades comunes a los dos solucionadores."""

# Variable: entero ≥ 1.  Literal: ese entero con signo (p → 1, ¬p → -1).
# Cláusula: frozenset de literales (un OR).  Fórmula: lista de cláusulas (un AND).
# Cláusula vacía = frozenset() (falsa).  Fórmula vacía = [] (verdadera).


def _parsear_literal(texto):
    """'p' → (1, 'p') ;  '-p' o '¬p' → (-1, 'p')."""
    texto = str(texto).strip()
    negativo = False
    for prefijo in ("-", "¬", "~", "!", "not "):
        if texto.startswith(prefijo):
            negativo = True
            texto = texto[len(prefijo):].strip()
            break
    return (-1 if negativo else 1), texto


def construir(clausulas):
    """Cláusulas de texto → (fórmula interna, nombres). Numera las variables por aparición."""
    nombres = {}
    indice = {}
    formula = []
    for clausula in clausulas:
        literales = set()
        for lit in clausula:
            signo, nombre = _parsear_literal(lit)
            if nombre not in indice:                 # variable nueva
                indice[nombre] = len(indice) + 1
                nombres[indice[nombre]] = nombre
            literales.add(signo * indice[nombre])
        formula.append(frozenset(literales))
    return formula, nombres


def variables(formula):
    """Números de las variables que aparecen en la fórmula."""
    return {abs(l) for clausula in formula for l in clausula}


def simplificar(formula, L):
    """Simplifica la fórmula dando L por verdadera."""
    nueva = []
    for clausula in formula:
        if L in clausula:
            continue                                       # cláusula ya cumplida: se elimina
        nueva.append(clausula - {-L} if -L in clausula else clausula)   # -L no puede cumplirla
    return nueva


def seleccionar_literal(formula):
    """Variable a probar: la menor de la cláusula más corta (prioriza las unitarias)."""
    clausula_corta = min(formula, key=len)
    return min(abs(l) for l in clausula_corta)
