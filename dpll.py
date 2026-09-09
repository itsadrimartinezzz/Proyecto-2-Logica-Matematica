"""Programa 2: SAT con el algoritmo DPLL sencillo."""

# No imprime; si recibe un 'nodo' arma ahí el árbol.

import traza
from comun import seleccionar_literal, simplificar


def dpll(B, I, nombres, nodo=None):
    """B: fórmula (lista de cláusulas).  I: valores asignados hasta ahora."""
    # No quedan cláusulas: todo se cumplió, es satisfacible.
    if not B:
        traza.marcar(nodo, traza.SAT, I)
        return True, I

    # Hay una cláusula vacía: no se puede cumplir, esta rama falla.
    if frozenset() in B:
        traza.marcar(nodo, traza.UNSAT_VACIA)
        return False, None

    L = seleccionar_literal(B)               # variable a probar (se prueba primero en V)

    B1 = simplificar(B, L)
    n1 = traza.hijo(nodo, nombres[L] + " = V", B1)
    ok, resultado = dpll(B1, {**I, L: True}, nombres, n1)
    if ok:
        traza.marcar(nodo, traza.SAT)         # esta rama encontró solución
        return True, resultado

    B2 = simplificar(B, -L)                  # con V no salió: se prueba en F
    n2 = traza.hijo(nodo, nombres[L] + " = F", B2)
    ok, resultado = dpll(B2, {**I, L: False}, nombres, n2)
    if ok:
        traza.marcar(nodo, traza.SAT)
        return True, resultado

    # Fallaron las dos ramas: esta parte no tiene solución.
    traza.marcar(nodo, traza.UNSAT_AGOTADAS)
    return False, None


def resolver(formula, nombres, trazar=True):
    """Ejecuta DPLL desde la asignación vacía. Devuelve (satisfacible, asignación, raíz)."""
    raiz = traza.Nodo(None, formula) if trazar else None
    ok, asignacion = dpll(formula, {}, nombres, raiz)
    return ok, asignacion, raiz


if __name__ == "__main__":
    import sys

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    from comun import construir

    ascii = "--ascii" in sys.argv

    # (¬q) ∧ (p ∨ q) ∧ (¬p ∨ r)  →  satisfacible
    formula, nombres = construir([["-q"], ["p", "q"], ["-p", "r"]])
    ok, asignacion, raiz = resolver(formula, nombres)
    print(traza.render(raiz, nombres, ascii=ascii))
