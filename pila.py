"""
Simulación de una PILA (stack) con TOPE y capacidad máxima de 8 elementos.

Problema: dibujar los estados de la pila al ejecutar 9 operaciones
(Insertar / Eliminar), mostrando el TOPE en cada paso, e indicar con cuántos
elementos queda la pila y si hubo desbordamiento o subdesbordamiento.

Conceptos:
  - TOPE = 0  -> pila vacía.
  - TOPE = capacidad -> pila llena.
  - Insertar con la pila llena  -> DESBORDAMIENTO (overflow).
  - Eliminar con la pila vacía  -> SUBDESBORDAMIENTO (underflow).

Uso:
    python pila.py            # ejecución completa
    python pila.py --pausa    # avanza paso a paso con Enter
"""

import os
import sys

os.system("")  # habilita colores ANSI en la consola de Windows

# ----------------------------------------------------------------------------
# Colores
# ----------------------------------------------------------------------------
RESET, NEGRITA, TENUE = "\033[0m", "\033[1m", "\033[2m"
ROJO, VERDE, AMARILLO = "\033[91m", "\033[92m", "\033[93m"
AZUL, CYAN = "\033[94m", "\033[96m"


def pintar(texto, *estilos):
    return "".join(estilos) + str(texto) + RESET


# ----------------------------------------------------------------------------
# Errores propios de la pila
# ----------------------------------------------------------------------------
class Desbordamiento(Exception):
    """Se intentó insertar con la pila llena (TOPE == capacidad)."""


class Subdesbordamiento(Exception):
    """Se intentó eliminar con la pila vacía (TOPE == 0)."""


# ----------------------------------------------------------------------------
# Estructura de datos
# ----------------------------------------------------------------------------
class Pila:
    def __init__(self, capacidad=8):
        self.capacidad = capacidad
        self.datos = [None] * capacidad  # arreglo de tamaño fijo
        self.tope = 0                    # TOPE = 0 -> pila vacía

    def insertar(self, x):
        """Insertar (PILA, X): coloca X en la cima y aumenta TOPE."""
        if self.tope == self.capacidad:
            raise Desbordamiento(
                f"No se puede insertar '{x}': la pila está llena "
                f"(TOPE = {self.tope} = capacidad)."
            )
        self.datos[self.tope] = x
        self.tope += 1

    def eliminar(self):
        """Eliminar (PILA, V): disminuye TOPE y devuelve el elemento de la cima."""
        if self.tope == 0:
            raise Subdesbordamiento(
                "No se puede eliminar: la pila está vacía (TOPE = 0)."
            )
        self.tope -= 1
        valor = self.datos[self.tope]
        self.datos[self.tope] = None
        return valor

    def contenido(self):
        """Lista de elementos de la base a la cima."""
        return self.datos[: self.tope]

    def dibujar(self):
        """Dibuja la pila de la posición más alta a la 1, marcando el TOPE."""
        ancho = 9
        borde = "─" * ancho
        print(f"      ┌{borde}┐")
        for i in range(self.capacidad - 1, -1, -1):
            valor = self.datos[i]
            if valor is None:
                celda = pintar(f"{'·':^{ancho}}", TENUE)
            else:
                celda = pintar(f"{valor:^{ancho}}", NEGRITA, VERDE)
            marca = pintar("  ◄── TOPE", NEGRITA, AMARILLO) if i == self.tope - 1 else ""
            print(f"  {i + 1:>2}  │{celda}│{marca}")
            if i > 0:
                print(f"      ├{borde}┤")
        print(f"      └{borde}┘")
        print(pintar(f"      TOPE = {self.tope}", NEGRITA, CYAN))
        if self.tope == 0:
            print(pintar("      (pila vacía)", TENUE))
        elif self.tope == self.capacidad:
            print(pintar("      (pila llena)", TENUE))
        print()


# ----------------------------------------------------------------------------
# Presentación
# ----------------------------------------------------------------------------
def titulo(texto):
    linea = "═" * 56
    print(pintar(linea, AZUL))
    print(pintar(f"  {texto}", NEGRITA, AZUL))
    print(pintar(linea, AZUL))


def tabla_resumen(bitacora):
    cols = ["Paso", "Operación", "Resultado", "TOPE", "Pila (base → cima)"]
    filas = [
        [b["paso"], b["operacion"], b["resultado"], str(b["tope"]), b["pila"]]
        for b in bitacora
    ]
    anchos = [max(len(c), *(len(f[i]) for f in filas)) for i, c in enumerate(cols)]

    def linea(izq, med, der):
        return izq + med.join("─" * (a + 2) for a in anchos) + der

    print(linea("┌", "┬", "┐"))
    print("│" + "│".join(f" {c:<{a}} " for c, a in zip(cols, anchos)) + "│")
    print(linea("├", "┼", "┤"))
    for f, b in zip(filas, bitacora):
        celdas = []
        for i, (txt, a) in enumerate(zip(f, anchos)):
            relleno = f" {txt:<{a}} "
            if i == 2:  # columna Resultado
                relleno = pintar(relleno, ROJO if b["error"] else VERDE)
            celdas.append(relleno)
        print("│" + "│".join(celdas) + "│")
    print(linea("└", "┴", "┘"))


# ----------------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------------
def main():
    pausa = "--pausa" in sys.argv
    pila = Pila(8)

    # (etiqueta, tipo, variable)  I = Insertar, E = Eliminar
    operaciones = [
        ("a", "I", "X"), ("b", "I", "Y"), ("c", "E", "Z"),
        ("d", "E", "T"), ("e", "E", "U"), ("f", "I", "V"),
        ("g", "I", "W"), ("h", "E", "p"), ("i", "I", "R"),
    ]

    titulo("PILA  ·  capacidad = 8  ·  estado inicial (TOPE = 0)")
    pila.dibujar()

    bitacora, errores = [], []

    for letra, tipo, var in operaciones:
        nombre = "Insertar" if tipo == "I" else "Eliminar"
        operacion = f"{nombre} (PILA, {var})"
        print(pintar(f"▶ Paso {letra})  {operacion}", NEGRITA))

        error = None
        try:
            if tipo == "I":
                pila.insertar(var)
                print(pintar(f"  ✔ '{var}' se colocó en la cima.", VERDE))
                resultado = f"Se insertó {var}"
            else:
                valor = pila.eliminar()
                print(pintar(f"  ✔ Se retiró '{valor}' y se guardó en {var}.", VERDE))
                resultado = f"Salió {valor} → {var}"
        except Desbordamiento as e:
            error = ("DESBORDAMIENTO (overflow)", str(e))
        except Subdesbordamiento as e:
            error = ("SUBDESBORDAMIENTO (underflow)", str(e))

        if error:
            print(pintar(f"  ✘ ERROR: {error[0]}", NEGRITA, ROJO))
            print(pintar(f"    {error[1]}", ROJO))
            resultado = "ERROR: " + ("underflow" if "SUB" in error[0] else "overflow")
            errores.append((letra, operacion, error[0], error[1]))

        print()
        pila.dibujar()
        bitacora.append({
            "paso": letra, "operacion": operacion, "resultado": resultado,
            "tope": pila.tope, "error": error is not None,
            "pila": ", ".join(pila.contenido()) or "(vacía)",
        })
        if pausa:
            input(pintar("  [Enter para continuar]", TENUE))
            print()

    # ---------------- Resumen y respuestas ----------------
    titulo("RESUMEN DE ESTADOS")
    tabla_resumen(bitacora)
    print()

    titulo("RESPUESTAS")
    print(pintar("¿Con cuántos elementos quedó la pila?", NEGRITA))
    print(f"  Quedó con {pintar(pila.tope, NEGRITA, VERDE)} elemento(s): "
          f"{', '.join(pila.contenido())}  (TOPE = {pila.tope}).\n")

    print(pintar("¿Hubo algún caso de error?", NEGRITA))
    if errores:
        for letra, operacion, tipo_error, detalle in errores:
            print(pintar(f"  Sí: {tipo_error} en el paso {letra}) {operacion}.", ROJO))
            print(f"  {detalle}")
            if "SUB" in tipo_error:
                print("  Los pasos c) y d) ya habían sacado todos los elementos, así que")
                print("  en e) no había nada que retirar. La operación no se realiza y")
                print("  la pila sigue vacía.")
        if not any("DES" == t[2][:3] for t in errores):
            print("  No hubo desbordamiento: nunca se superaron los 8 elementos.")
    else:
        print(pintar("  No hubo errores.", VERDE))


if __name__ == "__main__":
    main()
