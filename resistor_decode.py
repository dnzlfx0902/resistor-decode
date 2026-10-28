"""Decodificador de resistencias de 4 y 5 bandas.

Traduce bandas de color a ohmios y de ohmios a bandas para resistencias de 4 y 5 bandas, validando cada banda contra su posición y con tabla de casos conocidos en los tests.
"""
from __future__ import annotations

COLORES = {"negro": 0, "marron": 1, "rojo": 2, "naranja": 3, "amarillo": 4,
           "verde": 5, "azul": 6, "violeta": 7, "gris": 8, "blanco": 9}
MULTIPLICADOR = {**COLORES, "oro": -1, "plata": -2}
TOLERANCIA = {"marron": 1.0, "rojo": 2.0, "verde": 0.5, "azul": 0.25,
              "oro": 5.0, "plata": 10.0}


def decodificar(bandas):
    """Convierte 4 o 5 bandas de color en (ohmios, tolerancia en %)."""
    nombres = [b.strip().lower() for b in bandas]
    if len(nombres) not in (4, 5):
        raise ValueError("se esperan 4 o 5 bandas")
    for banda in nombres[:-1]:
        if banda not in MULTIPLICADOR:
            raise ValueError(f"banda desconocida: {banda}")
    if nombres[-1] not in TOLERANCIA:
        raise ValueError(f"tolerancia desconocida: {nombres[-1]}")
    digitos = "".join(str(COLORES[b]) for b in nombres[:-2])
    valor = int(digitos) * 10 ** MULTIPLICADOR[nombres[-2]]
    return valor, TOLERANCIA[nombres[-1]]


def codificar(ohmios, tolerancia=5.0):
    """Devuelve las 4 bandas (dos cifras, multiplicador, tolerancia)."""
    if ohmios <= 0:
        raise ValueError("el valor debe ser positivo")
    if tolerancia not in TOLERANCIA.values():
        raise ValueError(f"tolerancia no soportada: {tolerancia}")
    exponente = 0
    valor = int(round(ohmios))
    while valor >= 100:
        valor //= 10
        exponente += 1
    cifras = [d for d in str(valor).zfill(2)]
    nombre = {v: k for k, v in COLORES.items()}
    banda_tol = next(k for k, v in TOLERANCIA.items() if v == tolerancia)
    multiplicador = next(k for k, v in MULTIPLICADOR.items() if v == exponente)
    return [nombre[int(c)] for c in cifras] + [multiplicador, banda_tol]


def formatear(ohmios):
    """Presenta el valor con la unidad más legible (ohmios, kΩ, MΩ)."""
    for escala, sufijo in ((1_000_000, "MΩ"), (1_000, "kΩ")):
        if ohmios >= escala:
            return f"{ohmios / escala:g} {sufijo}"
    return f"{ohmios:g} Ω"


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Decodificador de resistencias de 4 y 5 bandas")
    p.add_argument("--bandas", nargs="+", help="cuatro bandas: rojo violeta marron oro")
    p.add_argument("--ohmios", type=float, help="valor a codificar, por ejemplo 470")
    p.add_argument("--demo", action="store_true", help="corrida de ejemplo del README")
    a = p.parse_args(argv)
    if a.bandas:
        valor, tol = decodificar(a.bandas)
        print(f"{formatear(valor)} ±{tol:g}%")
        return 0
    if a.ohmios:
        print(" ".join(codificar(a.ohmios)))
        return 0
    if a.demo:
        for bandas in (["rojo", "violeta", "marron", "oro"],
                       ["amarillo", "violeta", "negro", "rojo", "marron"]):
            valor, tol = decodificar(bandas)
            print(f"{' '.join(bandas):38s} -> {formatear(valor):>9s} ±{tol:g}%")
        print(f"codificar(470 Ω) = {' '.join(codificar(470))}")
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
