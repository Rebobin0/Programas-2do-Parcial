# 🧩 Solucionador del Puzzle de 8 (Eight Puzzle Solver)

## 📝 Descripción

Este programa implementa una solución para el clásico **Puzzle de 8** (un tablero deslizable de $3 \times 3$) utilizando el algoritmo de **Búsqueda Primero el Mejor (Best-First Search)**.

El algoritmo emplea la **Distancia Manhattan** como función heurística para priorizar la exploración de estados que están más cerca de la meta, lo que lo hace más eficiente que una búsqueda ciegamente.



---

## ⚙️ Estructuras de Datos y Librerías

| Componente | Uso | Descripción |
| :--- | :--- | :--- |
| `heapq` | Cola de Prioridad | Se utiliza para implementar la frontera del algoritmo Best-First Search, priorizando los nodos con el menor valor heurístico (Distancia Manhattan). |
| Estado del Puzzle | Tupla de 9 enteros | Cada estado del tablero se representa como una **tupla inmutable** de 9 elementos (las fichas de 1 a 8 y el espacio vacío 0). La inmutabilidad es clave para usar los estados como claves en conjuntos (`set`) y diccionarios, y para almacenarlos en la cola de prioridad. |

---

## 🛠️ Funciones Principales

### `leer_archivo(nombre_archivo)`

* **Descripción:** Lee los estados inicial y meta del puzzle desde un archivo de texto.
* **Proceso:**
    1.  Lee las primeras tres líneas como el estado inicial.
    2.  Lee las siguientes tres líneas como el estado meta.
    3.  Convierte ambas estructuras de listas de listas a una **tupla aplanada** de 9 elementos.
* **Retorna:** `(inicio, meta)` donde ambos son tuplas que representan los estados.

### `manhattan(estado, meta)`

* **Descripción:** Calcula la **Distancia Manhattan** (heurística $h(n)$) entre el estado actual y el estado meta.
* **Fórmula:** La suma de la distancia horizontal y vertical de cada ficha (1 a 8) hasta su posición correcta en el estado meta.
    $$
    h(n) = \sum_{i=1}^{8} \left(|r_i - r'_i| + |c_i - c'_i|\right)
    $$
    Donde $(r_i, c_i)$ es la posición actual de la ficha $i$ y $(r'_i, c'_i)$ es su posición en el estado meta.
* **Retorna:** La distancia Manhattan total (entero).

### `mover(estado, direccion)`

* **Descripción:** Genera un nuevo estado del puzzle moviendo el espacio vacío (`0`) en una dirección específica.
* **Parámetros:**
    * `estado` (tuple): El estado actual.
    * `direccion` (str): `'up'`, `'down'`, `'left'`, o `'right'`.
* **Proceso:**
    1.  Encuentra la posición (`pos`) del `0`.
    2.  Calcula la nueva posición del `0` basada en la `direccion`.
    3.  Si la nueva posición es válida (dentro del tablero $3 \times 3$), intercambia el `0` con la ficha adyacente.
* **Retorna:** El nuevo estado del puzzle (tuple), o `None` si el movimiento es ilegal.

### `obtener_vecinos(estado)`

* **Descripción:** Genera todos los estados válidos alcanzables desde el estado actual con un solo movimiento.
* **Retorna:** Una lista de tuplas `(nuevo_estado, movimiento_realizado)`.

### `best_first_search(inicio, meta)`

* **Descripción:** Algoritmo de Búsqueda Primero el Mejor.
* **Implementación:**
    1.  Inicializa una **cola de prioridad (`frontera`)** con el estado inicial. Cada elemento es `(heuristica, estado, camino)`.
    2.  Inicializa un **conjunto (`visitados`)** para evitar ciclos y estados repetidos.
    3.  Mientras la frontera no esté vacía:
        * Extrae el estado con la **menor heurística** (Distancia Manhattan).
        * Si el estado actual es el **meta**, retorna el camino.
        * Marca el estado como visitado.
        * Para cada vecino:
            * Si el vecino no ha sido visitado, calcula su heurística y lo añade a la frontera.
* **Retorna:** Una lista de movimientos (`['up', 'left', ...]`) que resuelven el puzzle, o `None` si no se encuentra solución.

---

## 🚀 Ejecución

La función `main()` lee los estados de `puzzle.txt` y ejecuta la búsqueda.
Para ejecutar el programa, asegúrate de tener un archivo llamado puzzle.txt en la ubicación correcta con el siguiente formato:
```txt
2 0 3
1 8 4
7 6 5
1 2 3
8 0 4
7 6 5
```

Simplemente corre el archivo Python:

```bash
python puzzle.py