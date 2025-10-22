import heapq

def leer_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        lineas = [line.strip() for line in f.readlines() if line.strip()]

    # Extraemos el tamaño del tablero
    M, N = map(int, lineas[0].split())

    # Extraemos coordenadas iniciales y finales
    x_ini, y_ini, x_fin, y_fin = map(int, lineas[1].split())

    # Extraemos las matrices
    des = 2 # ponemos un desplazamiento de 2
    transito = [list(map(int, lineas[i].split())) for i in range(des, des + M)]
    seguridad = [list(map(int, lineas[i].split())) for i in range(des + M, des + 2 * M)]
    trafico = [list(map(int, lineas[i].split())) for i in range(des + 2 * M, des + 3 * M)]

    return M, N, (x_ini, y_ini), (x_fin, y_fin), transito, seguridad, trafico


def vecinos(x, y, M, N): #metodo para las siguientes posiciones
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < M and 0 <= ny < N:
            yield nx, ny


def costo_celda(seguridad, trafico, x, y):
    return (10 - seguridad[x][y]) + trafico[x][y]


def a_estrella(M, N, inicio, fin, transito, seguridad, trafico): #algoritmo a estrella
    (x_ini, y_ini), (x_fin, y_fin) = inicio, fin
    open_set = [(0, x_ini, y_ini, [])]  # (costo, x, y, ruta)
    heapq.heapify(open_set)

    visitados = set()
    rutas = []

    while open_set:
        costo_actual, x, y, ruta = heapq.heappop(open_set)
        if (x, y) in visitados:
            continue
        visitados.add((x, y))
        ruta = ruta + [(x, y)]

        # Si llegamos al final
        if (x, y) == (x_fin, y_fin):
            rutas.append((ruta, costo_actual))
            continue

        for nx, ny in vecinos(x, y, M, N):
            if transito[nx][ny] == 1 and (nx, ny) not in visitados:
                nuevo_costo = costo_actual + costo_celda(seguridad, trafico, nx, ny)
                heapq.heappush(open_set, (nuevo_costo, nx, ny, ruta))

    rutas.sort(key=lambda x: x[1])
    return rutas


def main():
    archivo = "mapa.txt"
    M, N, inicio, fin, transito, seguridad, trafico = leer_archivo(archivo)
    rutas = a_estrella(M, N, inicio, fin, transito, seguridad, trafico)

    if not rutas:
        print("No se encontró ruta posible.")
        return

    print("Ruta óptima:")
    print(" -> ".join([str(p) for p in rutas[0][0]]))
    print(f"Costo total: {rutas[0][1]}")

if __name__ == "__main__":
    main()
