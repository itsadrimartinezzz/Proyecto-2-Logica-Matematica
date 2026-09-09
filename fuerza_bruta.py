"""Programa 1: SAT por fuerza bruta. Prueba las 2^n asignaciones posibles."""

import itertools

from comun import variables


def evaluar(formula, asignacion):
    """La fórmula es verdadera si cada cláusula tiene al menos una literal verdadera."""
    for clausula in formula:
        if not any(asignacion[abs(l)] if l > 0 else not asignacion[abs(l)]
                   for l in clausula):
            return False
    return True


def fuerza_bruta(formula):
    """Prueba todas las combinaciones. Devuelve (satisfacible, asignación, intentos)."""
    vs = sorted(variables(formula))
    intentos = 0
    # itertools.product recorre todas las combinaciones de V/F para las variables.
    for combinacion in itertools.product((False, True), repeat=len(vs)):
        intentos += 1
        asignacion = dict(zip(vs, combinacion))
        if evaluar(formula, asignacion):
            return True, asignacion, intentos      # la primera combinación que funciona
    return False, None, intentos                   # ninguna funcionó → insatisfacible


if __name__ == "__main__":
    import sys

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    from comun import construir
    from traza import fmt_asignacion, fmt_formula

    # r ∧ (¬q ∨ ¬r) ∧ (¬p ∨ q ∨ ¬r) ∧ q  →  insatisfacible
    formula, nombres = construir([["r"], ["-q", "-r"], ["-p", "q", "-r"], ["q"]])
    ok, asignacion, intentos = fuerza_bruta(formula)
    print("Formula:", fmt_formula(formula, nombres))
    if ok:
        print("SAT  ", fmt_asignacion(asignacion, nombres), " intentos:", intentos)
    else:
        print("UNSAT  (asignacion nula)  intentos:", intentos)
