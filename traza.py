"""Árbol de ejecución de DPLL: se arma en memoria y se dibuja al final."""

# DPLL no imprime: si recibe un 'nodo', va colgando ahí el árbol. Con nodo=None
# el trazado se apaga.

SAT = "SAT"                                # rama con solución
UNSAT_VACIA = "UNSAT (clausula vacia)"     # apareció una cláusula sin literales
UNSAT_AGOTADAS = "UNSAT (ramas agotadas)"  # fallaron la rama en V y la rama en F

# Símbolos del dibujo. El cmd viejo de Windows no muestra los de caja ni ¬ □ ∅;
# con ascii=True se usan equivalentes (+ - | ~ []).
_UNICODE = {"rama": "├─ ", "ultima": "└─ ", "tubo": "│  ", "hueco": "   ",
            "neg": "¬", "vacia": "□", "formula_vacia": "∅", "flecha": " -> "}

_ASCII = {"rama": "+- ", "ultima": "\\- ", "tubo": "|  ", "hueco": "   ",
          "neg": "~", "vacia": "[]", "formula_vacia": "{}", "flecha": " -> "}

# Lo mismo para el árbol en cajas (render_cajas).
_CAJA_U = {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│", "t": "┴", "sep": " · "}
_CAJA_A = {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|", "t": "+", "sep": " - "}


def simbolos(ascii=False):
    """Juego de símbolos: ascii puro o Unicode."""
    return _ASCII if ascii else _UNICODE


class Nodo:
    def __init__(self, etiqueta, formula):
        self.etiqueta = etiqueta      # decisión: "p = V" / "p = F" (la raíz no tiene)
        self.formula = formula        # la fórmula ya simplificada
        self.veredicto = None         # SAT / UNSAT; se llena al regresar
        self.asignacion = None        # valores que la cumplen; solo en hojas SAT
        self.hijos = []               # como mucho dos


# Ganchos que usa DPLL para armar el árbol.

def hijo(padre, etiqueta, formula):
    """Cuelga un nodo de 'padre' y lo devuelve. Si 'padre' es None, no hace nada."""
    if padre is None:
        return None
    n = Nodo(etiqueta, formula)
    padre.hijos.append(n)
    return n


def marcar(nodo, veredicto, asignacion=None):
    """Guarda el veredicto (y la asignación si es hoja SAT)."""
    if nodo is None:
        return
    nodo.veredicto = veredicto
    if asignacion is not None:
        nodo.asignacion = dict(asignacion)


# Literales, cláusulas y fórmulas a texto.

def fmt_literal(L, nombres, S=None):
    """'p' si L es positiva, '¬p' si es negativa."""
    S = S or _UNICODE
    nombre = nombres[abs(L)]
    return nombre if L > 0 else S["neg"] + nombre


def _ordenar_clausula(clausula):
    """Literales por variable; a igual variable, la positiva primero."""
    return sorted(clausula, key=lambda l: (abs(l), l < 0))


def _ordenar_formula(formula):
    """Cláusulas por longitud y luego por variables, para que la salida sea estable."""
    return sorted(formula, key=lambda c: (len(c),
                                          tuple(sorted(abs(l) for l in c)),
                                          tuple(_ordenar_clausula(c))))


def fmt_formula(formula, nombres, S=None, max_ancho=60):
    """Fórmula a texto. Vacía → ∅; cláusula vacía → □; muy larga → [n cláusulas, m literales]."""
    S = S or _UNICODE
    if not formula:
        return S["formula_vacia"]
    partes = []
    for clausula in _ordenar_formula(formula):
        if not clausula:
            partes.append(S["vacia"])
        else:
            lits = [fmt_literal(l, nombres, S) for l in _ordenar_clausula(clausula)]
            partes.append("{" + ", ".join(lits) + "}")
    texto = "{" + ", ".join(partes) + "}"
    if len(texto) > max_ancho:
        n_lit = sum(len(c) for c in formula)
        return "[{} clausulas, {} literales]".format(len(formula), n_lit)
    return texto


def fmt_asignacion(asignacion, nombres):
    """A texto, p. ej. {p=V, q=F, r=V}, ordenada por variable."""
    if not asignacion:
        return "{}"
    pares = ["{}={}".format(nombres[v], "V" if val else "F")
             for v, val in sorted(asignacion.items())]
    return "{" + ", ".join(pares) + "}"


# Métricas del árbol: nodos, hojas y profundidad.

def contar(raiz):
    """Recorre el árbol y devuelve nodos, hojas SAT/UNSAT y profundidad máxima."""
    c = {"nodos": 0, "sat": 0, "unsat": 0, "profundidad": 0}

    def rec(n, prof):
        c["nodos"] += 1
        c["profundidad"] = max(c["profundidad"], prof)
        if not n.hijos:
            c["sat" if n.veredicto == SAT else "unsat"] += 1
        for h in n.hijos:
            rec(h, prof + 1)

    rec(raiz, 0)
    return c


def resumen(c):
    return "nodos={nodos}  hojas SAT={sat}  hojas UNSAT={unsat}  profundidad={profundidad}".format(**c)


# Dibujo en texto, con sangría y ramas (├─ └─).

def _sufijo_veredicto(nodo, nombres, S):
    """Veredicto tras la fórmula: siempre en las hojas; en nodos internos solo si es 'ramas agotadas'."""
    if nodo.veredicto is None:
        return ""
    if nodo.hijos and nodo.veredicto != UNSAT_AGOTADAS:
        return ""
    if nodo.veredicto == SAT:
        return "  SAT " + fmt_asignacion(nodo.asignacion, nombres)
    return "  " + nodo.veredicto


def _id(num):
    """Devuelve '[nK] ' y avanza el contador; '' si la numeración está apagada."""
    if num is None:
        return ""
    etiqueta = "[n{}] ".format(num[0])
    num[0] += 1
    return etiqueta


def _lineas_hijos(nodo, prefijo, nombres, S, acc, num):
    total = len(nodo.hijos)
    for i, h in enumerate(nodo.hijos):
        ultimo = (i == total - 1)
        conector = S["ultima"] if ultimo else S["rama"]
        acc.append(prefijo + conector + _id(num) + h.etiqueta + S["flecha"]
                   + fmt_formula(h.formula, nombres, S) + _sufijo_veredicto(h, nombres, S))
        _lineas_hijos(h, prefijo + (S["hueco"] if ultimo else S["tubo"]), nombres, S, acc, num)


def render(raiz, nombres, ascii=False, max_nodos=None, incluir_resumen=True, numerar=False):
    """Árbol como texto indentado. numerar=True antepone [n0], [n1]... en orden de visita."""
    c = contar(raiz)
    if max_nodos is not None and c["nodos"] > max_nodos:
        return "[arbol de {} nodos: se omite el dibujo]".format(c["nodos"])
    S = _ASCII if ascii else _UNICODE
    num = [0] if numerar else None
    acc = [_id(num) + "DPLL" + S["flecha"] + fmt_formula(raiz.formula, nombres, S)
           + _sufijo_veredicto(raiz, nombres, S)]
    _lineas_hijos(raiz, "", nombres, S, acc, num)
    if incluir_resumen:
        acc.append("")
        acc.append(resumen(c))
    return "\n".join(acc)


# Dibujo en cajas, de arriba hacia abajo.

def _veredicto_corto(nodo, S):
    """Veredicto corto para la caja; '' si es un nodo interno que no aporta nada."""
    if nodo.veredicto is None or (nodo.hijos and nodo.veredicto != UNSAT_AGOTADAS):
        return ""
    if nodo.veredicto == SAT:
        return "SAT"
    if nodo.veredicto == UNSAT_VACIA:
        return "UNSAT " + S["vacia"]
    return "UNSAT (ramas)"


def _caja(nodo, idx, nombres, S, C):
    """La caja de un nodo, como lista de líneas del mismo ancho."""
    textos = ["n{}{}{}".format(idx, C["sep"], nodo.etiqueta or "DPLL"),
              fmt_formula(nodo.formula, nombres, S, max_ancho=22)]
    v = _veredicto_corto(nodo, S)
    if v:
        textos.append(v)
    w = max(len(t) for t in textos)
    borde_h = C["h"] * (w + 2)
    cuerpo = [C["v"] + " " + t.ljust(w) + " " + C["v"] for t in textos]
    return [C["tl"] + borde_h + C["tr"]] + cuerpo + [C["bl"] + borde_h + C["br"]]


def _ancho(bloque):
    return len(bloque[0]) if bloque else 0


def _pad_alto(bloque, alto):
    return bloque + [" " * _ancho(bloque)] * (alto - len(bloque))


def _pad_ancho(bloque, ancho):
    return [ln + " " * (ancho - len(ln)) for ln in bloque]


def _bloque(nodo, nombres, S, C, contador):
    """Devuelve (líneas, columna del centro) del subárbol con raíz en 'nodo'."""
    idx = contador[0]
    contador[0] += 1
    caja = _caja(nodo, idx, nombres, S, C)
    cw = _ancho(caja)
    if not nodo.hijos:
        return caja, cw // 2

    hijos = [_bloque(h, nombres, S, C, contador) for h in nodo.hijos]
    GAP = 3
    alto = max(len(b) for b, _ in hijos)
    hijos = [(_pad_alto(b, alto), c) for b, c in hijos]

    if len(hijos) == 1:
        lineas_h, centros = list(hijos[0][0]), [hijos[0][1]]
    else:
        (b1, c1), (b2, c2) = hijos
        lineas_h = [b1[i] + " " * GAP + b2[i] for i in range(alto)]
        centros = [c1, _ancho(b1) + GAP + c2]
    ancho_h = _ancho(lineas_h)
    conn = sum(centros) // len(centros)          # donde el padre se une con los hijos

    # Centra el padre sobre ese punto; si se sale por la izquierda, corre los hijos.
    izq = conn - cw // 2
    if izq < 0:
        corr = -izq
        lineas_h = [" " * corr + ln for ln in lineas_h]
        centros = [c + corr for c in centros]
        conn += corr
        ancho_h += corr
        izq = 0

    total = max(izq + cw, ancho_h)
    caja = _pad_ancho([" " * izq + ln for ln in caja], total)
    lineas_h = _pad_ancho(lineas_h, total)

    v = list(" " * total)
    v[conn] = C["v"]
    conectores = ["".join(v)]
    if len(centros) == 2:
        a, b = centros
        rama = list(" " * total)
        for x in range(a, b + 1):
            rama[x] = C["h"]
        rama[a], rama[b], rama[conn] = C["tl"], C["tr"], C["t"]
        baja = list(" " * total)
        baja[a] = baja[b] = C["v"]
        conectores += ["".join(rama), "".join(baja)]

    return caja + conectores + lineas_h, izq + cw // 2


def render_cajas(raiz, nombres, ascii=False, max_nodos=63):
    """Árbol en cajas. Con más de 'max_nodos' nodos usa render() (el dibujo sería enorme)."""
    if contar(raiz)["nodos"] > max_nodos:
        return render(raiz, nombres, ascii=ascii, incluir_resumen=False, numerar=True)
    S = _ASCII if ascii else _UNICODE
    C = _CAJA_A if ascii else _CAJA_U
    lineas, _ = _bloque(raiz, nombres, S, C, [0])
    return "\n".join(ln.rstrip() for ln in lineas)


# Demo: árbol armado a mano para probar el dibujo. Con dpll.py se arma solo.

if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ascii = "--ascii" in sys.argv

    def fs(*lits):
        return frozenset(lits)

    nombres = {1: "p", 2: "q", 3: "r"}
    raiz = Nodo(None, [fs(-2), fs(1, 2), fs(-1, 3)])    # {{¬q}, {p, q}, {¬p, r}}
    n_p = hijo(raiz, "p = V", [fs(-2), fs(3)])
    n_r = hijo(n_p, "r = V", [fs(-2)])
    n_qv = hijo(n_r, "q = V", [frozenset()])            # cláusula vacía
    marcar(n_qv, UNSAT_VACIA)
    n_qf = hijo(n_r, "q = F", [])                       # fórmula vacía: satisfacible
    marcar(n_qf, SAT, {1: True, 2: False, 3: True})

    print(render(raiz, nombres, ascii=ascii))
