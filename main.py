"""Ejecuta los 6 ejemplos uno tras otro. Opciones: --ascii, --png. Para el menú: python menu.py."""

import sys

from comun import construir
from dpll import resolver
from ejemplos import EJEMPLOS
from reporte import habilitar_ansi, informe


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    habilitar_ansi()

    ascii = "--ascii" in sys.argv
    png = "--png" in sys.argv
    exportar_png = None
    if png:
        from arbol_png import exportar_png

    total = len(EJEMPLOS)
    for i, (expresion, clausulas) in enumerate(EJEMPLOS, start=1):
        formula, nombres = construir(clausulas)
        informe(formula, nombres, ascii=ascii,
                titulo="EJEMPLO {} DE {}".format(i, total), expresion=expresion)
        if png:
            _, _, raiz = resolver(formula, nombres)
            ruta = exportar_png(raiz, nombres, "arboles/ejemplo_{}.png".format(i),
                                titulo="Ejemplo {}:  {}".format(i, expresion))
            print("   PNG: {}\n".format(ruta))


if __name__ == "__main__":
    main()
