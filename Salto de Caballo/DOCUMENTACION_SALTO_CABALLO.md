# ♟️ Problema del Salto del Caballo (Knight's Tour)

## 📝 Descripción

Este códifo contiene una implementación en **Python** para resolver el clásico **Problema del Salto del Caballo** (Knight's Tour) en un tablero de ajedrez de $N \times N$. El objetivo es encontrar una secuencia de movimientos legales del caballo que visite cada casilla del tablero exactamente una vez.

La solución utiliza el algoritmo de búsqueda en profundidad (**Depth-First Search - DFS**) con **Backtracking**.



---

## ⚙️ Configuración y Variables Globales

| Variable | Valor Predeterminado | Descripción |
| :--- | :--- | :--- |
| `N` | `8` | Tamaño del tablero de ajedrez ($N \times N$). Se puede modificar para tableros de distinto tamaño. |
| `movFila` | `[1, 2, 2, 1, -1, -2, -2, -1]` | Componentes de desplazamiento en la fila (eje X) para los 8 movimientos posibles del caballo. |
| `movCol` | `[2, 1, -1, -2, -2, -1, 1, 2]` | Componentes de desplazamiento en la columna (eje Y) para los 8 movimientos posibles del caballo. |

---

## 🛠️ Funciones Principales

### `es_valido(x, y, tablero)`

* **Descripción:** Verifica si una posición $(x, y)$ es un movimiento legal.
* **Parámetros:**
    * `x` (int): Coordenada de la fila.
    * `y` (int): Coordenada de la columna.
    * `tablero` (list[list[int]]): El estado actual del tablero.
* **Retorna:** `True` si la posición está dentro de los límites del tablero ($0 \le x < N$ y $0 \le y < N$) y no ha sido visitada (`tablero[x][y] == -1`), de lo contrario `False`.

### `imprimir_tablero(tablero)`

* **Descripción:** Imprime el estado actual del tablero en la consola.

### `resolver_dfs(x, y, mov, tablero)`

* **Descripción:** Implementa el algoritmo **DFS con Backtracking** para encontrar un recorrido del caballo.
* **Parámetros:**
    * `x` (int): Fila actual del caballo.
    * `y` (int): Columna actual del caballo.
    * `mov` (int): El número de movimiento actual (comenzando en 1).
    * `tablero` (list[list[int]]): El estado actual del tablero.
* **Lógica:**
    1.  **Caso Base:** Si `mov` es igual a $N \times N$ (todas las casillas visitadas), retorna `True`.
    2.  Itera sobre los 8 movimientos posibles del caballo.
    3.  Para un movimiento válido:
        * Marca la nueva posición en el tablero con el número de movimiento actual (`tablero[nuevo_x][nuevo_y] = mov`).
        * Llama recursivamente a `resolver_dfs` para el siguiente movimiento (`mov + 1`).
        * Si la llamada recursiva retorna `True`, se ha encontrado una solución, y retorna `True`.
        * Si no se encuentra solución, realiza **Backtrack**: Desmarca la casilla (`tablero[nuevo_x][nuevo_y] = -1`) y continúa con el siguiente movimiento posible.
* **Retorna:** `True` si se encuentra un recorrido completo, `False` en caso contrario.

### `main()`

* **Descripción:** Función principal que inicializa el tablero, establece la posición de inicio, y ejecuta el proceso de búsqueda de la solución.
* **Proceso:**
    1.  Inicializa el tablero $N \times N$ con todas las casillas a `-1`.
    2.  Establece la posición inicial del caballo en `(0, 0)` y la marca con el movimiento `0`.
    3.  Muestra la hora de inicio y llama a `resolver_dfs`.
    4.  Si se encuentra una solución, imprime el tablero final y la hora de finalización.
    5.  Si no se encuentra solución, imprime un mensaje indicando que no existe solución y la hora de finalización.
    * *(El código también incluye secciones comentadas para intentar la búsqueda desde todas las posibles posiciones iniciales).*

---

## 🏃 Ejecución

Para ejecutar el programa, simplemente corre el archivo Python:

```bash
python salto_dfs.py