"""Formato de la salida: informe() imprime los datos, ambos métodos, el árbol y la comparación."""

import os
import sys
import textwrap

from comun import variables
from dpll import resolver
from fuerza_bruta import fuerza_bruta
from traza import contar, fmt_asignacion, fmt_formula, render_cajas, simbolos

ANCHO = 66
ETIQUETA = 13                       # ancho de la columna de las etiquetas
_SUPER = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def habilitar_ansi():
    """En Windows 10 o superior, habilita los colores ANSI en la consola."""
    if os.name == "nt":
        os.system("")


def _tema(ascii):
    """Códigos de color a usar; van vacíos en modo ascii o si la salida no es una terminal."""
    if ascii or not sys.stdout.isatty():
        return {k: "" for k in ("b", "d", "ok", "no", "ac", "z")}
    return {"b": "\033[1m", "d": "\033[2m", "ok": "\033[32m",
            "no": "\033[31m", "ac": "\033[36m", "z": "\033[0m"}


def _glifos(ascii):
    """Símbolos decorativos, con su versión en ascii puro."""
    if ascii:
        return {"bar": "-", "punto": "*", "flecha": ">", "check": "OK", "cruz": "X"}
    return {"bar": "─", "punto": "·", "flecha": "▸", "check": "✓", "cruz": "✗"}


def _campo(etiqueta, valor, T):
    """Devuelve una línea 'etiqueta   valor', con la etiqueta en gris y alineada."""
    return "    {}{}{}{}".format(T["d"], etiqueta.ljust(ETIQUETA), T["z"], valor)


def _seccion(texto, T, G):
    print()
    print("  {}{} {}{}".format(T["b"], G["flecha"], texto, T["z"]))


def _veredicto(ok, T):
    return (T["ok"] + "SATISFACIBLE" + T["z"]) if ok else (T["no"] + "INSATISFACIBLE" + T["z"])


def informe(formula, nombres, ascii=False, titulo=None, expresion=None):
    """Imprime el bloque completo de resultados de una fórmula."""
    T = _tema(ascii)
    G = _glifos(ascii)
    S = simbolos(ascii)

    vs = sorted(variables(formula))
    n = len(vs)
    combinaciones = 2 ** n

    # Encabezado: título, fórmula y cantidad de variables.
    print()
    print(T["ac"] + G["bar"] * ANCHO + T["z"])
    if titulo:
        print("  " + T["b"] + titulo + T["z"])
        print(T["ac"] + G["bar"] * ANCHO + T["z"])

    if expresion:
        if ascii:
            expresion = expresion.translate(str.maketrans("∧∨¬", "&|~"))
        print(_campo("Fórmula", expresion, T))
    print(_campo("Cláusulas", fmt_formula(formula, nombres, S, max_ancho=ANCHO - ETIQUETA), T))
    if vs:
        vars_txt = ", ".join(nombres[v] for v in vs)
        pot = "2^{}".format(n) if ascii else "2{}".format(str(n).translate(_SUPER))
        combos = "{} = {} combinaciones".format(pot, combinaciones)
        print(_campo("Variables", "{}   {}   {}".format(vars_txt, G["punto"], combos), T))
    else:
        print(_campo("Variables", "(ninguna)", T))

    # Resolver con fuerza bruta y mostrar su resultado.
    fb_ok, fb_asig, fb_intentos = fuerza_bruta(formula)
    _seccion("FUERZA BRUTA", T, G)
    print(_campo("Resultado", _veredicto(fb_ok, T), T))
    print(_campo("Asignación", fmt_asignacion(fb_asig, nombres) if fb_ok else "nula", T))
    print(_campo("Esfuerzo", "{} de {} asignaciones evaluadas".format(fb_intentos, combinaciones), T))

    # Resolver con DPLL y mostrar su resultado.
    dp_ok, dp_asig, raiz = resolver(formula, nombres)
    c = contar(raiz)
    hojas = c["sat"] + c["unsat"]
    hojas_txt = "{} hoja{}".format(hojas, "" if hojas == 1 else "s")
    _seccion("DPLL", T, G)
    print(_campo("Resultado", _veredicto(dp_ok, T), T))
    print(_campo("Asignación", fmt_asignacion(dp_asig, nombres) if dp_ok else "nula", T))
    print(_campo("Esfuerzo", "{} nodos {} {} {} profundidad {}".format(
        c["nodos"], G["punto"], hojas_txt, G["punto"], c["profundidad"]), T))

    # Dibujar el árbol de decisiones que siguió DPLL.
    _seccion("ÁRBOL DE EJECUCIÓN (DPLL)", T, G)
    print(textwrap.indent(render_cajas(raiz, nombres, ascii=ascii), "    "))

    # Comparar cuánto trabajo hizo cada método.
    _seccion("COMPARACIÓN", T, G)
    if fb_ok:
        fb_txt = "probó {} de {} hasta hallar una asignación".format(fb_intentos, combinaciones)
    else:
        fb_txt = "probó las {} (todas)".format(fb_intentos)
    print(_campo("Espacio", "{} asignaciones posibles".format(combinaciones), T))
    print(_campo("Fuerza bruta", fb_txt, T))
    print(_campo("DPLL", "recorrió {} nodos del árbol ({})".format(c["nodos"], hojas_txt), T))
    iguales = fb_ok == dp_ok
    marca = (T["ok"] + G["check"] + T["z"]) if iguales else (T["no"] + G["cruz"] + T["z"])
    estado = "SATISFACIBLE" if dp_ok else "INSATISFACIBLE"
    print(_campo("Coinciden", "{}  {}".format(marca, estado if iguales else "DISCREPAN"), T))
    print()
