# 🤖 Programas del Semestre de IA

Este repositorio contiene las implementaciones en Python de varios problemas y actividades relacionadas con algoritmos de búsqueda, heurísticas y técnicas básicas de Inteligencia Artificial.

---

## 📂 Estructura del Repositorio

La documentación detallada de cada proyecto se encuentra dentro de su respectiva carpeta, en archivos con extensión `.md`.

* **`README.md`**: Este archivo (resumen general).
* **`Act3-PuzzlePrimeroElMejor/`**: Solucionador del Puzzle de 8 (Eight Puzzle).
* **`actividad4/`**: Solucionador de la ruta óptima en un laberinto con costos.
* **`DetectorNumeros/`**: Sistema de detección o reconocimiento de números.
* **`Salto De Caballo/`**: Solución al problema clásico del Salto del Caballo.

---

## 🧩 1. Act3-PuzzlePrimeroElMejor: Solucionador del Puzzle de 8

| Archivo | Descripción |
| :--- | :--- |
| **[`DOCUMENTACION_PUZZLE.md`](./Act3-PuzzlePrimeroElMejor/DOCUMENTACION_PUZZLE.md)** | Documentación detallada del código, la heurística y el algoritmo utilizado. |
| `puzzle.py` | Implementación del algoritmo **Búsqueda Primero el Mejor (Best-First Search)**. |
| `puzzle.txt` | Archivo de entrada con el estado inicial y el estado meta del puzzle. |

> **Algoritmo Clave:** Búsqueda Primero el Mejor (Best-First Search).
> **Heurística:** Distancia Manhattan.

---

## 🗺️ 2. Actividad 4: Búsqueda de Ruta Óptima en Laberinto

| Archivo | Descripción |
| :--- | :--- |
| **[`DOCUMENTACION_LABERINTO_....md`](./actividad4/DOCUMENTACION_LABERINTO_....md)** | Documentación del algoritmo A\* y la función de costo personalizada. |
| `actividad4.py` | Implementación del algoritmo **A\* (A-estrella)** para encontrar la ruta de menor costo. |
| `mapa.txt` | Archivo de entrada con las dimensiones, coordenadas, y las matrices de Tránsito, Seguridad y Tráfico. |

> **Algoritmo Clave:** Algoritmo A\* (A-estrella).
> **Costo:** Basado en Seguridad y Tráfico.

---

## 🐎 3. Salto De Caballo (Knight's Tour)

| Archivo | Descripción |
| :--- | :--- |
| **[`DOCUMENTACION_SALTO_CABALLO.md`](./Salto%20De%20Caballo/DOCUMENTACION_SALTO_CABALLO.md)** | Documentación del problema, la estrategia de movimientos y la implementación. |
| `salto_dfs.py` | Implementación de la solución utilizando **Búsqueda en Profundidad (DFS)** con **Backtracking**. |

> **Algoritmo Clave:** Búsqueda en Profundidad (DFS) con Backtracking.
> **Problema:** Encontrar un camino que visite cada casilla de un tablero $N \times N$ una sola vez.

---

## 🔢 4. DetectorNumeros: Detección de Patrones

| Archivo | Descripción |
| :--- | :--- |
| **[`DOCUMENTACION_DETECTA.md`](./DetectorNumeros/DOCUMENTACION_DETECTA.md)** | Documentación del proceso de detección, los patrones y el código. |
| `detecta.py` | Script principal para el proceso de detección. |
| `frecuencias/`, `input/`, `patrones/` | Carpetas con los archivos necesarios para la ejecución del detector. |

> **Técnica Clave:** Distancia euclidiana que nos permite ver que tanto se parece una mtriz de entrada a los patrones que se tienen

---

*Nota: Para revisar los detalles de cada implementación, por favor diríjase al archivo `.md` correspondiente dentro de cada subdirectorio.*