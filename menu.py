"""Menú del proyecto. Se ejecuta con: python menu.py  (--ascii para el cmd de Windows)."""

import sys

from comun import construir
from dpll import resolver
from ejemplos import EJEMPLOS
from reporte import ANCHO, habilitar_ansi, informe


def _glifos(ascii):
    """Caracteres para dibujar el recuadro del título."""
    return {"bar": "-", "esq_tl": "+", "esq_tr": "+", "esq_bl": "+", "esq_br": "+", "vert": "|"} if ascii \
        else {"bar": "═", "esq_tl": "╔", "esq_tr": "╗", "esq_bl": "╚", "esq_br": "╝", "vert": "║"}


def portada(ascii):
    G = _glifos(ascii)
    titulo = "PROYECTO 2"
    print()
    print(G["esq_tl"] + G["bar"] * (ANCHO - 2) + G["esq_tr"])
    print(G["vert"] + titulo.center(ANCHO - 2) + G["vert"])
    print(G["esq_bl"] + G["bar"] * (ANCHO - 2) + G["esq_br"])


def menu_principal():
    print()
    print("   1   Resolver los ejemplos del enunciado")
    print("   2   Exportar los árboles a PNG")
    print("   3   Salir")
    print()
    return input("   Elige una opción > ").strip()


def correr_ejemplos(ascii):
    total = len(EJEMPLOS)
    for i, (expresion, clausulas) in enumerate(EJEMPLOS, start=1):
        formula, nombres = construir(clausulas)
        informe(formula, nombres, ascii=ascii,
                titulo="EJEMPLO {} DE {}".format(i, total), expresion=expresion)
        if i < total:
            if input("   [Enter] siguiente  ·  [m] volver al menú > ").strip().lower() == "m":
                return


def exportar_pngs():
    """Guarda el árbol de cada ejemplo como imagen PNG en la carpeta arboles/."""
    try:
        from arbol_png import exportar_png
    except ImportError:
        print("\n   >> Falta matplotlib.  Instalalo con:  pip install matplotlib\n")
        return
    print()
    for i, (expresion, clausulas) in enumerate(EJEMPLOS, start=1):
        formula, nombres = construir(clausulas)
        _, _, raiz = resolver(formula, nombres)
        ruta = exportar_png(raiz, nombres, "arboles/ejemplo_{}.png".format(i),
                            titulo="Ejemplo {}:  {}".format(i, expresion))
        print("   guardado  {}".format(ruta))
    print("\n   {} imágenes en la carpeta 'arboles/'.".format(len(EJEMPLOS)))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    habilitar_ansi()

    ascii = "--ascii" in sys.argv
    portada(ascii)

    while True:
        opcion = menu_principal()
        if opcion == "1":
            correr_ejemplos(ascii)
        elif opcion == "2":
            exportar_pngs()
        elif opcion in ("3", "q", ""):
            print("\n   Listo.\n")
            return
        else:
            print("   >> Opción no válida.")


if __name__ == "__main__":
    main()
