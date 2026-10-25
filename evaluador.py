"""
Evaluador de expresiones aritméticas en notación POSFIJA y PREFIJA usando una PILA.

Reutiliza la clase Pila del archivo pila.py (deben estar en la misma carpeta).

Posfija (el operador va DESPUÉS):  3 4 + 2 *   = (3 + 4) * 2 = 14
  - Se lee de IZQUIERDA a DERECHA.
  - Número   -> se inserta en la pila.
  - Operador -> se sacan dos valores (b y luego a), se calcula a op b
                y el resultado se inserta de nuevo.

Prefija (el operador va ANTES):    * + 3 4 2   = (3 + 4) * 2 = 14
  - Se lee de DERECHA a IZQUIERDA.
  - Número   -> se inserta en la pila.
  - Operador -> se sacan dos valores (a y luego b), se calcula a op b
                y el resultado se inserta de nuevo.

Al final, la pila debe tener EXACTAMENTE un valor: el resultado.

Los símbolos se separan con espacios. Operadores: + - * / ^
"""

import math
import sys

from pila import (Pila, Subdesbordamiento, pintar,
                  NEGRITA, TENUE, ROJO, VERDE, AMARILLO, AZUL, CYAN)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OPERADORES = {"+", "-", "*", "/", "^"}


class ErrorExpresion(Exception):
    """La expresión es inválida o no se puede calcular."""


# ----------------------------------------------------------------------------
# Utilidades de cálculo
# ----------------------------------------------------------------------------
def a_numero(simbolo):
    """Convierte un símbolo a número; si no es válido lanza ErrorExpresion."""
    try:
        return int(simbolo)
    except ValueError:
        pass
    try:
        valor = float(simbolo)
    except ValueError:
        raise ErrorExpresion(f"Símbolo inválido: '{simbolo}'.")
    if not math.isfinite(valor):
        raise ErrorExpresion(f"Símbolo inválido: '{simbolo}'.")
    return valor


def aplicar(op, a, b):
    """Calcula a op b."""
    try:
        if op == "+":
            r = a + b
        elif op == "-":
            r = a - b
        elif op == "*":
            r = a * b
        elif op == "/":
            if b == 0:
                raise ErrorExpresion("División entre cero.")
            r = a / b
        else:  # "^"
            r = a ** b
    except OverflowError:
        raise ErrorExpresion("El resultado es demasiado grande.")
    if isinstance(r, complex):
        raise ErrorExpresion("El resultado no es un número real.")
    return r


def fmt(n):
    """Muestra enteros sin '.0' y limita los decimales."""
    if isinstance(n, float):
        return str(int(n)) if n.is_integer() else str(round(n, 6))
    return str(n)


# ----------------------------------------------------------------------------
# Evaluación con pila
# ----------------------------------------------------------------------------
def evaluar(expresion, modo, pasos):
    """
    Evalúa la expresión ('posfija' o 'prefija') usando una Pila.
    Cada paso se guarda en la lista 'pasos' para poder mostrar la tabla,
    incluso si más adelante ocurre un error.
    """
    tokens = expresion.split()
    if not tokens:
        raise ErrorExpresion("La expresión está vacía.")

    # Posfija: izquierda -> derecha.  Prefija: derecha -> izquierda.
    orden = tokens if modo == "posfija" else list(reversed(tokens))
    pila = Pila(len(tokens))

    for n, simbolo in enumerate(orden, start=1):
        if simbolo in OPERADORES:
            try:
                if modo == "posfija":
                    b = pila.eliminar()   # primero sale el operando derecho
                    a = pila.eliminar()
                else:
                    a = pila.eliminar()   # primero sale el operando izquierdo
                    b = pila.eliminar()
            except Subdesbordamiento:
                pasos.append((n, simbolo, "Faltan operandos", pila.contenido(), pila.tope))
                raise ErrorExpresion(
                    f"Faltan operandos para el operador '{simbolo}' (la pila se vació)."
                )
            try:
                r = aplicar(simbolo, a, b)
            except ErrorExpresion:
                pasos.append((n, simbolo, f"{fmt(a)} {simbolo} {fmt(b)} → ERROR", pila.contenido(), pila.tope))
                raise
            pila.insertar(r)
            accion = f"Sacar {fmt(b if modo == 'posfija' else a)} y "\
                     f"{fmt(a if modo == 'posfija' else b)}: {fmt(a)} {simbolo} {fmt(b)} = {fmt(r)}"
        else:
            try:
                valor = a_numero(simbolo)
            except ErrorExpresion:
                pasos.append((n, simbolo, "Símbolo inválido", pila.contenido(), pila.tope))
                raise
            pila.insertar(valor)
            accion = f"Insertar {fmt(valor)}"
        pasos.append((n, simbolo, accion, pila.contenido(), pila.tope))

    if pila.tope != 1:
        raise ErrorExpresion(
            f"Expresión mal formada: sobraron {pila.tope - 1} valor(es) en la pila "
            f"(faltan operadores)."
        )
    return pila.eliminar()


# ----------------------------------------------------------------------------
# Presentación
# ----------------------------------------------------------------------------
def titulo(texto):
    linea = "═" * 70
    print(pintar(linea, AZUL))
    print(pintar(f"  {texto}", NEGRITA, AZUL))
    print(pintar(linea, AZUL))


def tabla(pasos):
    cols = ["Paso", "Símbolo", "Acción", "Pila (base → cima)", "TOPE"]
    filas = [
        [str(n), s, a, "[" + ", ".join(fmt(x) for x in p) + "]", str(t)]
        for n, s, a, p, t in pasos
    ]
    anchos = [max(len(c), *(len(f[i]) for f in filas)) for i, c in enumerate(cols)]

    def linea(izq, med, der):
        return izq + med.join("─" * (a + 2) for a in anchos) + der

    print(linea("┌", "┬", "┐"))
    print("│" + "│".join(pintar(f" {c:<{a}} ", NEGRITA, CYAN) for c, a in zip(cols, anchos)) + "│")
    print(linea("├", "┼", "┤"))
    for f in filas:
        celdas = [f" {txt:<{a}} " for txt, a in zip(f, anchos)]
        if "ERROR" in f[2] or f[2] in ("Faltan operandos", "Símbolo inválido"):
            celdas[2] = pintar(celdas[2], ROJO)
        elif f[2].startswith("Insertar"):
            celdas[2] = pintar(celdas[2], VERDE)
        else:
            celdas[2] = pintar(celdas[2], AMARILLO)
        print("│" + "│".join(celdas) + "│")
    print(linea("└", "┴", "┘"))


def resolver(expresion, modo):
    sentido = "izquierda → derecha" if modo == "posfija" else "derecha → izquierda"
    print()
    titulo(f"Notación {modo.upper()}  ·  se lee de {sentido}")
    print(f"  Expresión: {pintar(expresion, NEGRITA)}\n")
    pasos = []
    try:
        resultado = evaluar(expresion, modo, pasos)
    except ErrorExpresion as e:
        if pasos:
            tabla(pasos)
        print(pintar(f"\n  ✘ ERROR: {e}", NEGRITA, ROJO))
        return
    tabla(pasos)
    print(pintar(f"\n  ✔ Resultado = {fmt(resultado)}", NEGRITA, VERDE))


EJEMPLOS = [
    ("posfija", "3 4 + 2 *"),
    ("posfija", "5 1 2 + 4 * + 3 -"),
    ("prefija", "* + 3 4 2"),
    ("prefija", "- * 2 3 4"),
    ("posfija", "4 0 /"),       # error: división entre cero
    ("posfija", "3 +"),         # error: faltan operandos
    ("posfija", "3 4"),         # error: faltan operadores
    ("prefija", "+ 3 x"),       # error: símbolo inválido
]


def menu():
    print()
    titulo("EVALUADOR DE EXPRESIONES CON PILA")
    print("  1) Evaluar expresión POSFIJA   (ej. 3 4 + 2 *)")
    print("  2) Evaluar expresión PREFIJA   (ej. * + 3 4 2)")
    print("  3) Ejecutar ejemplos automáticos (incluye casos de error)")
    print("  0) Salir")
    return input(pintar("\n  Elige una opción: ", NEGRITA)).strip()


def main():
    while True:
        try:
            opcion = menu()
            if opcion in ("1", "2"):
                modo = "posfija" if opcion == "1" else "prefija"
                expr = input(pintar("  Escribe la expresión (símbolos separados por espacio): ", NEGRITA))
                resolver(expr, modo)
            elif opcion == "3":
                for modo, expr in EJEMPLOS:
                    resolver(expr, modo)
            elif opcion == "0":
                print(pintar("\n  ¡Hasta luego!\n", CYAN))
                break
            else:
                print(pintar("  Opción no válida.", ROJO))
        except (EOFError, KeyboardInterrupt):
            print(pintar("\n\n  ¡Hasta luego!\n", CYAN))
            break


if __name__ == "__main__":
    main()
