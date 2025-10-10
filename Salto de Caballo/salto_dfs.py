import datetime

N = 8 # Tamaño del tablero

# Movimientos posibles del caballo
movFila = [1, 2, 2, 1, -1, -2, -2, -1]
movCol = [2, 1, -1, -2, -2, -1, 1, 2]


# Verifica si la posición se encuentra dentro del tablero y no ha sido visitada
def es_valido(x, y, tablero):
    return 0 <= x < N and 0 <= y < N and tablero[x][y] == -1

def imprimir_tablero(tablero):
    for fila in tablero:
        print(fila)

def resolver_dfs(x, y, mov, tablero):
    # Si el movimiento actual es igual a NxN, hemos completado el recorrido
    if mov == N * N:
        return True

    # Intenta todos los movimientos posibles del caballo
    for i in range(8):
        nuevo_x = x + movFila[i]
        nuevo_y = y + movCol[i]
        # Verifica si el nuevo movimiento es válido
        if es_valido(nuevo_x, nuevo_y, tablero):
            tablero[nuevo_x][nuevo_y] = mov # Marca el movimiento en el tablero
            # Llama recursivamente para el siguiente movimiento
            if resolver_dfs(nuevo_x, nuevo_y, mov + 1, tablero):
                return True
            tablero[nuevo_x][nuevo_y] = -1  # Backtrack si no se llego a la solución
    return False

def main():
    print("Solución del problema del salto del caballo usando DFS:")
    # Inicializar el tablero de NxN con -1 en todas las casillas
    tablero = [[-1 for _ in range(N)] for _ in range(N)]

    # Dar posición inicial
    inicio_x, inicio_y = 0, 0 # posición inicial del caballo
    tablero[inicio_x][inicio_y] = 0
    # Muestra la hora de inicio
    print(datetime.datetime.now())
    if resolver_dfs(inicio_x, inicio_y, 1, tablero):
        imprimir_tablero(tablero)
        # Muestra la hora de finalización
        print(datetime.datetime.now())
    else:
        print("No existe solución.")
        # Muestra la hora de finalización
        print(datetime.datetime.now())

    # Intentar desde todas las posiciones del tablero
    # for inicio_x in range(N):
    #     for inicio_y in range(N):
    #         # Limpiar el tablero con -1
    #         for i in range(N):
    #             for j in range(N):
    #                 tablero[i][j] = -1
            
    #         tablero[inicio_x][inicio_y] = 0

    #         print(f"Probando posición inicial: ({inicio_x}, {inicio_y})")
    #         # Muestra la hora de inicio
    #         print(datetime.datetime.now())

    #         if resolver_dfs(inicio_x, inicio_y, 1, tablero):
    #             print("Solución encontrada:")
    #             imprimir_tablero(tablero)
    #             # Muestra la hora de finalización
    #             print(datetime.datetime.now())
    #             return  # Salir al encontrar la primera solución
    #         else:
    #             print("No hay solución desde esta posición.")
    #             # Muestra la hora de finalización
    #             print(datetime.datetime.now())
    # print("No existe ninguna solución posible desde ninguna posición.")
    # print(datetime.datetime.now())

if __name__ == "__main__":
    main()
