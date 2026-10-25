# Pilas en Python: Pila, Evaluador de expresiones y Torres de Hanoi

**Alumno:** Johan Alexander Coot Vázquez
**Materia:** Estructuras de Datos
**Grupo:** 3ZA

Este repositorio reúne tres programas en Python que usan una misma estructura: la pila. Además incluye la página web (`Frutiger_Aero`) donde se pueden ver funcionando los tres programas y consultar su código.

> Ver la página en línea: https://TU-USUARIO.github.io/TU-REPOSITORIO/
> (también se puede abrir descargando el repositorio y dando doble clic en `Frutiger_Aero`)
---

## Qué es una pila

Una pila es una estructura LIFO (_Last In, First Out_): el último elemento que entra es el primero que sale, como una pila de platos.

- TOPE es el número que indica cuántos elementos hay y dónde está la cima.
- `TOPE = 0` significa pila vacía.
- Si se intenta insertar con la pila llena ocurre un **desbordamiento** (_overflow_).
- Si se intenta eliminar con la pila vacía ocurre un **subdesbordamiento** (_underflow_).

---

## Contenido del repositorio

| Archivo | Para qué sirve |
|---|---|
| `pila.py` | Clase `Pila` (capacidad 8, con TOPE) y solución de la actividad de la pila. Los otros dos programas la reutilizan. |
| `evaluador.py` | Evalúa expresiones aritméticas en notación posfija y prefija usando una pila. |
| `hanoi.py` | Resuelve las Torres de Hanoi con tres o más discos usando tres pilas. |
| `index.html` | Página interactiva (estilo Frutiger Aero) para ejecutar y explicar los tres programas. |
| `README.md` | Esta documentación. |

> `evaluador.py` y `hanoi.py` importan la clase `Pila` de `pila.py`, por lo que los tres archivos deben estar en la misma carpeta.

---

## Actividad 1: La pila (TOPE y capacidad 8)

Se simulan estas operaciones sobre una pila vacía (`TOPE = 0`) de capacidad 8:

| Paso | Operación | Pila (base → cima) | TOPE |
|:---:|---|---|:---:|
| a | Insertar (PILA, X) | X | 1 |
| b | Insertar (PILA, Y) | X, Y | 2 |
| c | Eliminar (PILA, Z), sale Y | X | 1 |
| d | Eliminar (PILA, T), sale X | (vacía) | 0 |
| e | Eliminar (PILA, U) | **ERROR: subdesbordamiento** | 0 |
| f | Insertar (PILA, V) | V | 1 |
| g | Insertar (PILA, W) | V, W | 2 |
| h | Eliminar (PILA, p), sale W | V | 1 |
| i | Insertar (PILA, R) | V, R | 2 |

¿Con cuántos elementos quedó la pila? Con 2 elementos: `V` en la base y `R` en la cima (`TOPE = 2`).

¿Hubo algún error? Sí, un subdesbordamiento en el paso e). Los pasos c) y d) ya habían sacado todos los elementos, así que al intentar eliminar de nuevo no había nada que retirar. La operación no se realiza y la pila sigue vacía. No hubo desbordamiento, porque la pila nunca pasó de 2 elementos y su capacidad es 8.

Ejecutar: `python pila.py` (o `python pila.py --pausa` para avanzar con Enter).
---

## Actividad 2: Evaluador de expresiones posfijas y prefijas

Una computadora no necesita paréntesis si el operador se escribe antes o después de los números:

| Notación | Ejemplo | Equivale a |
|---|---|---|
| Posfija (operador después) | `3 4 + 2 *` | (3 + 4) × 2 = 14 |
| Prefija (operador antes) | `* + 3 4 2` | (3 + 4) × 2 = 14 |

Cómo funciona con la pila:

1. Se leen los símbolos uno por uno (posfija: de izquierda a derecha; prefija: de derecha a izquierda).
2. Si es un número, se inserta en la pila.
3. Si es un operador se sacan los dos números de arriba, se opera y se inserta el resultado.
4. Al final queda un solo valor en la pila: el resultado.

Ejemplo `3 4 + 2 *`:

| Símbolo | Acción | Pila |
|---|---|---|
| 3 | Insertar | [3] |
| 4 | Insertar | [3, 4] |
| + | Sacar 4 y 3, calcular 3 + 4 = 7 | [7] |
| 2 | Insertar | [7, 2] |
| * | Sacar 2 y 7, calcular 7 × 2 = 14 | [14] |

Errores que detecta: división entre cero (`4 0 /`), faltan operandos (`3 +`), sobran números (`3 4`) y símbolos inválidos (`+ 3 x`). Operadores admitidos: `+ - * / ^`.

Ejecutar: `python evaluador.py` y elegir una opción del menú (la opción 3 corre ejemplos automáticos).

---

## Actividad 3: Torres de Hanoi con pilas

Hay tres torres (A, B y C) y varios discos de distinto tamaño apilados en A. El objetivo es pasarlos todos a C cumpliendo dos reglas:

1. Se mueve un solo disco a la vez (el de arriba de una torre).
2. Nunca se puede poner un disco grande sobre uno más pequeño.

Cómo se usa la pila: cada torre es una pila. Mover un disco es eliminar el disco de arriba de una torre e insertarlo en otra. El TOPE de cada torre indica cuántos discos tiene.

Idea de la solución (recursiva): para mover _n_ discos de A a C, primero se mueven _n-1_ discos a B, luego el disco más grande pasa a C y finalmente los _n-1_ discos de B pasan a C.

| Discos | Movimientos mínimos (2ⁿ − 1) |
|:---:|:---:|
| 3 | 7 |
| 4 | 15 |
| 5 | 31 |
| 6 | 63 |
| 7 | 127 |

Ejecutar: `hanoi.py`. El programa comprueba al final que todos los discos quedaron en la torre C, en orden, y que el número de movimientos coincide con 2ⁿ − 1.

---

## Página interactiva (`index.html`)

La página muestra cada actividad con dos vistas:

- Ejecutar:la pila con botones de insertar y eliminar y el problema paso a paso; el evaluador con ejemplos (incluidos casos de error) y una tabla de cada paso; y las Torres de Hanoi, que se pueden resolver a mano haciendo clic en las torres o ver resueltas automáticamente.
  *Código: el código de cada programa, con botón para copiarlo y para cargar el archivo `.py` completo.

La página funciona sin internet. Aunque está hecha en HTML y JavaScript para mostrar el funcionamiento de forma visual, la lógica es la misma que la de los programas en Python.

