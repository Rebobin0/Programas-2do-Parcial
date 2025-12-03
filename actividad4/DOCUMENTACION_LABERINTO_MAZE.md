# 🗺️ Solucionador de Rutas en Laberintos (Maze Solver) con Algoritmo A\*

## 📝 Descripción

Este programa implementa el algoritmo de búsqueda **A\* (A-estrella)** para encontrar la **ruta óptima** (de menor costo) entre un punto de inicio y un punto final en un laberinto con costos dinámicos.

El laberinto se representa como una cuadrícula $M \times N$, donde el costo de moverse a través de cada celda se calcula a partir de los niveles de **Seguridad** y **Tráfico** definidos en los datos de entrada. La ruta óptima es aquella que minimiza la suma de estos costos a lo largo del camino. 

---

## ⚙️ Estructuras de Datos y Entrada

La información del laberinto se lee de un archivo de texto, como el especificado `./actividad4/mapa.txt`. El archivo debe contener la siguiente información en orden:

1.  **Línea 1:** Dimensiones $M$ (filas) y $N$ (columnas).
2.  **Línea 2:** Coordenadas de inicio $(x_{\text{ini}}, y_{\text{ini}})$ y de fin $(x_{\text{fin}}, y_{\text{fin}})$.
3.  **Matriz de Tránsito:** $M$ líneas de $N$ números.
4.  **Matriz de Seguridad:** $M$ líneas de $N$ números.
5.  **Matriz de Tráfico:** $M$ líneas de $N$ números.

| Componente | Tipo | Propósito |
| :--- | :--- | :--- |
| `heapq` | Cola de Prioridad | Utilizada para la **Cola de Prioridad (`open_set`)** del algoritmo A\*, siempre extrayendo el nodo con el **menor costo acumulado**. |
| `visitados` | `set` | Almacena las coordenadas $(x, y)$ ya procesadas para evitar ciclos y caminos ineficientes. |
| `transito` | Matriz | Indica si la celda es **transitable (`1`)** o un obstáculo (`0`). |
| `seguridad` | Matriz | Nivel de seguridad de 1 (peor) a 10 (mejor). |
| `trafico` | Matriz | Nivel de congestión o tráfico (impacto negativo en el costo). |

---

## 🧮 Función de Costo de Paso (`costo_celda`)

El costo de un paso $g(n)$ hacia una celda específica se calcula buscando **maximizar la seguridad** y **minimizar el tráfico**, según la siguiente fórmula:

$$
\text{Costo Paso} = (10 - \text{Seguridad}[x][y]) + \text{Tráfico}[x][y]
$$

* **Seguridad (Inversa):** El término $(10 - \text{Seguridad}[x][y])$ garantiza que un valor de seguridad alto (10) resulte en un costo bajo (0), incentivando rutas seguras.
* **Tráfico (Directo):** El término $\text{Tráfico}[x][y]$ se añade directamente al costo, reflejando su impacto negativo.

### Algoritmo A\* (Costo Acumulado)

En esta implementación, el algoritmo A\* se enfoca en minimizar el **costo acumulado** ($g(n)$), priorizando los nodos con el menor costo real desde el inicio.

---

## 🛠️ Funciones Clave

### `leer_archivo(ruta_archivo)`

* **Descripción:** Procesa el archivo de entrada, extrayendo dimensiones, coordenadas y las tres matrices de costos.
* **Retorna:** $M, N$, las coordenadas `inicio` y `fin`, y las matrices `transito`, `seguridad`, y `trafico`.

### `vecinos(x, y, M, N)`

* **Descripción:** Genera las coordenadas de las celdas **adyacentes** (arriba, abajo, izquierda, derecha) que se encuentran **dentro de los límites** del laberinto.
* **Retorna:** Un generador de tuplas `(nx, ny)`.

### `a_estrella(M, N, inicio, fin, transito, seguridad, trafico)`

* **Descripción:** Implementación principal del algoritmo A\*. Utiliza la cola de prioridad para buscar eficientemente la ruta de menor costo.
* **Lógica Clave:** Solo explora los vecinos si son **transitables** (`transito[nx][ny] == 1`) y si no han sido visitados previamente.
* **Retorna:** Una lista de rutas `(ruta_coordenadas, costo_total)`, ordenada de la mejor (menor costo) a la peor.

---

## 🚀 Ejecución

Para ejecutar, asegúrate de tener el archivo de mapa configurado y ejecuta el script de Python.

```bash
python actividad4.py