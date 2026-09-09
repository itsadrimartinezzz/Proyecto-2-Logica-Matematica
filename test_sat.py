"""Verificación: compara DPLL con fuerza bruta en miles de fórmulas y revisa el árbol."""

import random

from comun import construir, variables
from dpll import resolver
from fuerza_bruta import evaluar, fuerza_bruta
from traza import SAT, UNSAT_AGOTADAS, UNSAT_VACIA, contar


def _formula_aleatoria(rng):
    """Genera una fórmula al azar: 1 a 6 variables, 1 a 12 cláusulas de 1 a 3 literales."""
    n_vars = rng.randint(1, 6)
    nombres = ["x{}".format(i) for i in range(1, n_vars + 1)]
    clausulas = []
    for _ in range(rng.randint(1, 12)):
        k = rng.randint(1, min(3, n_vars))
        elegidas = rng.sample(nombres, k)
        clausulas.append([("-" if rng.random() < 0.5 else "") + v for v in elegidas])
    return clausulas


def _satisface(formula, asignacion_parcial):
    """Rellena con F las variables que falten y comprueba que la fórmula sea verdadera."""
    completa = {v: asignacion_parcial.get(v, False) for v in variables(formula)}
    return evaluar(formula, completa)


def _revisar_arbol(raiz):
    """Comprueba que el árbol sea coherente: numeración 0..n-1, toda hoja con veredicto, SAT solo en ramas válidas."""
    ids = []
    c = contar(raiz)

    def rec(n, idx, prof, en_rama_ok):
        ids.append(idx)
        if not n.hijos:
            assert n.veredicto in (SAT, UNSAT_VACIA), "hay una hoja sin veredicto válido"
        if n.veredicto == SAT:
            assert en_rama_ok, "un nodo SAT cuelga de una rama que ya había fallado"
        hijo_ok = n.veredicto != UNSAT_AGOTADAS and n.veredicto != UNSAT_VACIA
        sig = idx + 1
        for h in n.hijos:
            sig = rec(h, sig, prof + 1, hijo_ok)
        return sig

    total = rec(raiz, 0, 0, True)
    assert total == c["nodos"], "la numeración de nodos no cuadra"
    assert max(ids) + 1 == c["nodos"], "los números de nodo no cubren 0..n-1"


def _casos_fijos():
    """Casos difíciles a propósito: tautologías, literales repetidos y los 6 del enunciado."""
    from ejemplos import EJEMPLOS

    fijos = [
        ([["p", "-p"]], True),                       # tautología: siempre verdadera
        ([["p"], ["p"], ["p"]], True),               # la misma cláusula repetida
        ([["p", "p", "-q"]], True),                   # una literal repetida dentro de la cláusula
        ([["p"], ["-p"], ["q"]], False),             # p y ¬p a la vez: contradicción
        ([["a", "b"], ["-a", "b"], ["a", "-b"], ["-a", "-b"]], False),
    ]
    esperado = [False, True, True, True, True, False]  # resultado esperado de cada ejemplo del enunciado
    fijos += [(cl, ok) for (_, cl), ok in zip(EJEMPLOS, esperado)]

    for clausulas, sat_esperado in fijos:
        formula, nombres = construir(clausulas)
        fb_ok, _, _ = fuerza_bruta(formula)
        dp_ok, dp_asig, raiz = resolver(formula, nombres)
        assert fb_ok == dp_ok == sat_esperado, ("caso fijo", clausulas, fb_ok, dp_ok, sat_esperado)
        if dp_ok:
            assert _satisface(formula, dp_asig), ("caso fijo asignacion", clausulas, dp_asig)
        _revisar_arbol(raiz)
    print("OK: {} casos fijos (tautologias, repetidos, enunciado).".format(len(fijos)))


def main():
    _casos_fijos()

    rng = random.Random(20260908)
    n = 4000
    for _ in range(n):
        clausulas = _formula_aleatoria(rng)
        formula, nombres = construir(clausulas)

        fb_ok, _, _ = fuerza_bruta(formula)
        dp_ok, dp_asig, raiz = resolver(formula, nombres)

        assert fb_ok == dp_ok, ("veredicto distinto", clausulas, fb_ok, dp_ok)
        if dp_ok:
            assert _satisface(formula, dp_asig), ("asignacion no satisface", clausulas, dp_asig)
        _revisar_arbol(raiz)

    print("OK: {} formulas aleatorias.".format(n))
    print("   - DPLL y fuerza bruta coinciden en SAT/UNSAT")
    print("   - las asignaciones de DPLL satisfacen la formula")
    print("   - el arbol (nodos, ids, veredictos) es consistente")


if __name__ == "__main__":
    main()
