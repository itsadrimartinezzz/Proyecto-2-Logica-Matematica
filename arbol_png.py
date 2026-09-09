"""Exporta el árbol de DPLL a una imagen PNG (requiere matplotlib)."""

import os

import matplotlib
matplotlib.use("Agg")                     # backend sin ventana: solo genera el archivo
import matplotlib.pyplot as plt

from traza import (SAT, UNSAT_AGOTADAS, UNSAT_VACIA,
                   contar, fmt_asignacion, fmt_formula)


def _posiciones(raiz):
    """Calcula (x, y) de cada nodo: x = punto medio de sus hijos, y = -profundidad."""
    pos = {}
    hoja = [0]

    def rec(n, prof):
        for h in n.hijos:
            rec(h, prof + 1)
        if n.hijos:
            x = sum(pos[h][0] for h in n.hijos) / len(n.hijos)
        else:
            x, hoja[0] = hoja[0], hoja[0] + 1
        pos[n] = (x, -prof)

    rec(raiz, 0)
    return pos


def _ids(raiz):
    """Numera los nodos en orden de visita (n0 = raíz), devolviendo {id(nodo): número}."""
    orden = {}
    cont = [0]

    def rec(n):
        orden[id(n)] = cont[0]
        cont[0] += 1
        for h in n.hijos:
            rec(h)

    rec(raiz)
    return orden


def _texto(n, idx, nombres):
    """Texto que va dentro de la caja: número de nodo, decisión, fórmula y veredicto."""
    lineas = ["n{}   {}".format(idx, n.etiqueta or "DPLL"),
              fmt_formula(n.formula, nombres, max_ancho=40)]
    if n.veredicto and (not n.hijos or n.veredicto == UNSAT_AGOTADAS):
        if n.veredicto == SAT:
            lineas.append("SAT  " + fmt_asignacion(n.asignacion, nombres))
        else:
            lineas.append(n.veredicto)
    return "\n".join(lineas)


def _colores(n):
    """Devuelve (color de relleno, color de borde) según cómo terminó el nodo."""
    if n.veredicto == SAT:
        return "#e6f4ea", "#2e7d32"                     # verde: parte del camino solución
    if n.veredicto in (UNSAT_VACIA, UNSAT_AGOTADAS):
        return "#fdecea", "#c62828"                     # rojo: rama sin solución
    return "#eef1f6", "#5c6b8a"                         # gris: decisión que no llegó a un resultado


def exportar_png(raiz, nombres, ruta, titulo=""):
    """Dibuja el árbol y lo guarda en 'ruta'. Devuelve la ruta."""
    pos = _posiciones(raiz)
    idx = _ids(raiz)
    c = contar(raiz)
    hojas = max(1, sum(1 for n in pos if not n.hijos))

    fig, ax = plt.subplots(figsize=(max(6, hojas * 2.6),
                                    max(3, (c["profundidad"] + 1) * 1.8)))

    for n, (x0, y0) in pos.items():                     # primero las líneas entre nodos
        for h in n.hijos:
            x1, y1 = pos[h]
            ax.plot([x0, x1], [y0, y1], color="#9aa4b8", lw=1.1, zorder=1)

    for n, (x, y) in pos.items():                       # y encima, las cajas
        relleno, borde = _colores(n)
        ax.text(x, y, _texto(n, idx[id(n)], nombres),
                ha="center", va="center", fontsize=8, family="monospace", zorder=2,
                bbox=dict(boxstyle="round,pad=0.45", fc=relleno, ec=borde, lw=1.3))

    ax.set_axis_off()
    ax.margins(x=0.20, y=0.16)
    if titulo:
        ax.set_title(titulo, fontsize=11, fontweight="bold", pad=12)
    fig.tight_layout()

    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    fig.savefig(ruta, dpi=150, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    return ruta
