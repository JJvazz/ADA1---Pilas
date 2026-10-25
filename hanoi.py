"""
Torres de Hanoi con la clase Pila (3 o más discos).

Reutiliza la clase Pila del archivo pila.py (deben estar en la misma carpeta).

Reglas:
  1. Solo se mueve un disco a la vez (el que está en la cima de una torre).
  2. Nunca se puede poner un disco grande sobre uno más pequeño.
  3. Objetivo: pasar todos los discos de la torre A a la torre C.

Cada torre es una Pila de capacidad n:
  - Mover un disco = eliminar() de la torre origen + insertar() en la destino.
  - El TOPE de cada pila indica cuántos discos tiene la torre.

Solución recursiva para n discos:
  1. Mover n-1 discos de origen a auxiliar.
  2. Mover el disco más grande de origen a destino.
  3. Mover los n-1 discos de auxiliar a destino.
  Total de movimientos: 2^n - 1.

Uso:
    python hanoi.py            # pregunta cuántos discos
    python hanoi.py 4          # 4 discos
    python hanoi.py 4 --pausa  # avanza con Enter en cada movimiento
"""

import sys

from pila import Pila, pintar, NEGRITA, TENUE, ROJO, VERDE, AMARILLO, AZUL, CYAN

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Colores (ANSI 256) para los discos, del más pequeño al más grande
PALETA = [51, 48, 46, 190, 220, 208, 205, 171, 99, 75]


class MovimientoInvalido(Exception):
    """Se intentó poner un disco grande sobre uno pequeño o mover de una torre vacía."""


def cima(pila):
    """Disco que está en la cima (sin sacarlo), o None si la torre está vacía."""
    return pila.datos[pila.tope - 1] if pila.tope > 0 else None


class Hanoi:
    def __init__(self, n, pausa=False):
        self.n = n
        self.pausa = pausa
        self.detallado = n <= 5 or pausa   # con muchos discos solo se muestra el estado final
        self.movimientos = 0
        # Tres pilas: A, B y C. Cada una puede contener hasta n discos.
        self.torres = {"A": Pila(n), "B": Pila(n), "C": Pila(n)}
        # Discos n, n-1, ..., 1 en A (el 1 es el más pequeño y queda arriba)
        for disco in range(n, 0, -1):
            self.torres["A"].insertar(disco)

    # ------------------------------------------------------------------
    def mover(self, origen, destino):
        """Mueve el disco de la cima de 'origen' a 'destino' validando las reglas."""
        disco = cima(self.torres[origen])
        if disco is None:
            raise MovimientoInvalido(f"La torre {origen} está vacía.")
        tope_destino = cima(self.torres[destino])
        if tope_destino is not None and tope_destino < disco:
            raise MovimientoInvalido(
                f"No se puede poner el disco {disco} sobre el disco {tope_destino}."
            )
        self.torres[origen].eliminar()
        self.torres[destino].insertar(disco)
        self.movimientos += 1

        if self.detallado:
            print(pintar(f"▶ Movimiento {self.movimientos}: ", NEGRITA)
                  + f"disco {self.disco_color(disco)} de {origen} → {destino}")
            self.dibujar()
            if self.pausa:
                input(pintar("  [Enter para continuar]", TENUE))
                print()

    def resolver(self, n, origen, destino, auxiliar):
        """Algoritmo recursivo de las Torres de Hanoi."""
        if n == 0:
            return
        self.resolver(n - 1, origen, auxiliar, destino)   # 1) n-1 discos a auxiliar
        self.mover(origen, destino)                        # 2) el más grande a destino
        self.resolver(n - 1, auxiliar, destino, origen)   # 3) n-1 discos a destino

    # ------------------------------------------------------------------
    def disco_color(self, d):
        return pintar(d, NEGRITA, f"\033[38;5;{PALETA[(d - 1) % len(PALETA)]}m")

    def dibujar(self):
        """Dibuja las tres torres lado a lado, con el TOPE de cada pila."""
        n = self.n
        ancho = 2 * n + 1
        for nivel in range(n - 1, -1, -1):
            partes = []
            for nombre in "ABC":
                torre = self.torres[nombre]
                if nivel < torre.tope:
                    d = torre.datos[nivel]
                    bloque = "█" * (2 * d + 1)
                    relleno = " " * (n - d)
                    color = f"\033[38;5;{PALETA[(d - 1) % len(PALETA)]}m"
                    partes.append(relleno + pintar(bloque, color) + relleno)
                else:
                    partes.append(" " * n + pintar("│", TENUE) + " " * n)
            print("   " + "    ".join(partes))
        print("   " + "    ".join(pintar("━" * ancho, AZUL) for _ in "ABC"))
        print("   " + "    ".join(pintar(f"{'Torre ' + t:^{ancho}}", NEGRITA, CYAN) for t in "ABC"))
        print("   " + "    ".join(f"{'TOPE=' + str(self.torres[t].tope):^{ancho}}" for t in "ABC"))
        print()


# ----------------------------------------------------------------------------
def titulo(texto):
    linea = "═" * 56
    print(pintar(linea, AZUL))
    print(pintar(f"  {texto}", NEGRITA, AZUL))
    print(pintar(linea, AZUL))


def pedir_discos():
    """Obtiene n desde la línea de comandos o preguntando (mínimo 3, máximo 10)."""
    for arg in sys.argv[1:]:
        if arg.isdigit():
            n = int(arg)
            if 3 <= n <= 10:
                return n
            print(pintar("El número de discos debe estar entre 3 y 10.", ROJO))
            sys.exit(1)
    while True:
        try:
            texto = input(pintar("¿Cuántos discos? (3 a 10, Enter = 3): ", NEGRITA)).strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if texto == "":
            return 3
        if texto.isdigit() and 3 <= int(texto) <= 10:
            return int(texto)
        print(pintar("  Escribe un número entre 3 y 10.", ROJO))


def main():
    n = pedir_discos()
    juego = Hanoi(n, pausa="--pausa" in sys.argv)

    print()
    titulo(f"TORRES DE HANOI  ·  {n} discos  ·  A → C")
    print("  Cada torre es una Pila: mover = eliminar() + insertar().\n")
    print(pintar("Estado inicial", NEGRITA))
    juego.dibujar()

    juego.resolver(n, "A", "C", "B")

    if not juego.detallado:
        print(pintar("(Con más de 5 discos solo se muestra el estado final; "
                     "usa --pausa para ver cada movimiento.)\n", TENUE))

    titulo("RESULTADO")
    juego.dibujar()
    esperado = 2 ** n - 1
    ok = (juego.torres["C"].contenido() == list(range(n, 0, -1))
          and juego.torres["A"].tope == 0 and juego.torres["B"].tope == 0)
    print(f"  Movimientos realizados: {pintar(juego.movimientos, NEGRITA, VERDE)}")
    print(f"  Movimientos esperados (2^{n} - 1): {esperado}")
    if ok and juego.movimientos == esperado:
        print(pintar("  ✔ ¡Resuelto! Todos los discos están en la torre C, en orden.\n", NEGRITA, VERDE))
    else:
        print(pintar("  ✘ Algo salió mal.\n", NEGRITA, ROJO))


if __name__ == "__main__":
    main()
