import heapq #cola de prioridad 

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        lineas = [line.strip() for line in f if line.strip()]
    inicio = [list(map(int, lineas[i].split())) for i in range(3)]
    meta = [list(map(int, lineas[i+3].split())) for i in range(3)]

    #print("Estado inicial:", inicio)
    #print("Estado meta:", meta)

    return tuple(sum(inicio, [])), tuple(sum(meta, []))

def manhattan(estado, meta):
    distancia = 0
    for num in range(1, 9):
        i, j = divmod(estado.index(num), 3)
        x, y = divmod(meta.index(num), 3)
        distancia += abs(i - x) + abs(j - y)
    #print("Distancia: ", distancia)
    return distancia

def mover(estado, direccion):
    pos = estado.index(0)
    fila, col = divmod(pos, 3)
    #print("Posición del espacio vacío:", (fila, col))
    movimientos = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    df, dc = movimientos[direccion]
    nf, nc = fila + df, col + dc
    if 0 <= nf < 3 and 0 <= nc < 3:
        nuevo = list(estado)
        nuevo[pos], nuevo[nf * 3 + nc] = nuevo[nf * 3 + nc], nuevo[pos]
        return tuple(nuevo)
    return None

def obtener_vecinos(estado):
    vecinos = []
    for d in ['up', 'down', 'left', 'right']:
        nuevo = mover(estado, d)
        if nuevo:
            vecinos.append((nuevo, d))
    #print("Vecinos generados:", vecinos)
    return vecinos

def best_first_search(inicio, meta):
    frontera = []
    heapq.heappush(frontera, (manhattan(inicio, meta), inicio, []))
    visitados = set()
    
    while frontera:
        costo, actual, camino = heapq.heappop(frontera)
        if actual == meta:
            return camino
        if actual in visitados:
            continue
        visitados.add(actual)
        for vecino, mov in obtener_vecinos(actual):
            if vecino not in visitados:
                nuevo_camino = camino + [mov]
                heuristica = manhattan(vecino, meta)
                heapq.heappush(frontera, (heuristica, vecino, nuevo_camino))
    return None

def main():
    inicio, meta = leer_archivo('Act3-PuzzlePrimeroElMejor/puzzle.txt')
    camino = best_first_search(inicio, meta)
    if camino:
        print("Solución encontrada en", len(camino), "movimientos:")
        print(" → ".join(camino))
    else:
        print("No es resolvible o no se encontró solución.")

if __name__ == "__main__":
    main()
