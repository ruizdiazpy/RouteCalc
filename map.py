import heapq

# Definir direcciones posibles: arriba, abajo, izquierda, derecha
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Función para calcular la distancia heurística (en este caso, la distancia Manhattan)
def distancia_manhattan(pos_actual, pos_fin):
    return abs(pos_actual[0] - pos_fin[0]) + abs(pos_actual[1] - pos_fin[1])

# Función para crear una matriz 4x6 con letras del alfabeto en inglés
def crear_matriz():
    
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWX'
    
    # Crear matriz vacía
    matriz = []
    
    # Llenar la matriz con letras del alfabeto en inglés
    for i in range(4):
        fila = []
        for j in range(6):
            fila.append(alfabeto[i * 6 + j])
        matriz.append(fila)
    
    return matriz

# Función para imprimir la matriz
def imprimir_matriz(matriz):
    for fila in matriz:
        for letra in fila:
            if letra in obstaculos:
                print('\033[1;34m' + letra + '\033[0m', end=' ')  # Imprime en azul si es un obstáculo
            else:
                print(letra, end=' ')
        print()

# Función para manejar la entrada de letras para los obstáculos por parte del usuario
def obtener_obstaculos():
    while True:
        obstaculos = input("\nIngrese las letras para los obstáculos (máximo 8): ").strip().upper()
        
        if len(obstaculos) <= 8 and all(letra.isalpha() for letra in obstaculos):
            return set(obstaculos)  # Devuelve un conjunto de letras de obstáculos
        else:
            print("Entrada inválida. Ingrese hasta 8 letras del alfabeto en inglés.")
            continue

# Función para manejar la entrada de puntos de inicio y fin por parte del usuario
def obtener_puntos_usuario(matriz):
    while True:
        imprimir_matriz(matriz)
        inicio = input("\nIngrese la letra de inicio: ").strip().upper()
        fin = input("Ingrese la letra de fin: ").strip().upper()
        
        if len(inicio) == 1 and len(fin) == 1 and inicio.isalpha() and fin.isalpha():
            if inicio != 'Y' and fin != 'Y' and inicio != 'Z' and fin != 'Z':
                # Encontrar las posiciones de inicio y fin en la matriz
                pos_inicio = None
                pos_fin = None
                for i in range(len(matriz)):
                    for j in range(len(matriz[0])):
                        if matriz[i][j] == inicio:
                            pos_inicio = (i, j)
                        elif matriz[i][j] == fin:
                            pos_fin = (i, j)
                
                if pos_inicio is not None and pos_fin is not None:
                    return pos_inicio, pos_fin
                else:
                    print("Las letras ingresadas no fueron encontradas en la matriz. Intente de nuevo.")
                    continue
            else:
                print("Las letras 'Y Z' no pueden ser ni el inicio ni el fin. Intente de nuevo.")
                continue
        else:
            print("Entrada inválida. Ingrese una única letra del alfabeto en inglés.")
            continue

# Función para encontrar el camino utilizando el algoritmo A*
def encontrar_camino_A_estrella(matriz, inicio, fin, obstaculos):
    fila_inicio, col_inicio = inicio
    fila_fin, col_fin = fin
    
    # Conjuntos para nodos visitados y por visitar
    nodos_visitados = set()
    nodos_por_visitar = []
    
    # Inicializar la cola de prioridad con el nodo de inicio
    heapq.heappush(nodos_por_visitar, (0, inicio, None))
    
    # Diccionarios para mantener el costo acumulado y los padres de cada nodo
    costo_acumulado = {inicio: 0}
    padre = {inicio: None}
    
    while nodos_por_visitar:
        _, pos_actual, _ = heapq.heappop(nodos_por_visitar)
        
        if pos_actual in nodos_visitados:
            continue
        
        nodos_visitados.add(pos_actual)
        
        if pos_actual == fin:
            # Reconstruir el camino desde el punto final hasta el inicio
            camino = []
            while pos_actual:
                camino.append(pos_actual)
                pos_actual = padre[pos_actual]
            camino.reverse()
            return camino
        
        for direccion in direcciones:
            fila_nueva = pos_actual[0] + direccion[0]
            col_nueva = pos_actual[1] + direccion[1]
            nueva_pos = (fila_nueva, col_nueva)
            
            if not (0 <= fila_nueva < len(matriz) and 0 <= col_nueva < len(matriz[0])):
                continue
            
            if matriz[fila_nueva][col_nueva] in obstaculos or nueva_pos in nodos_visitados:
                continue
            
            costo_nuevo = costo_acumulado[pos_actual] + 1
            
            if nueva_pos not in costo_acumulado or costo_nuevo < costo_acumulado[nueva_pos]:
                costo_acumulado[nueva_pos] = costo_nuevo
                prioridad = costo_nuevo + distancia_manhattan(nueva_pos, fin)
                heapq.heappush(nodos_por_visitar, (prioridad, nueva_pos, pos_actual))
                padre[nueva_pos] = pos_actual
    
    return None

# Función para imprimir la matriz con el camino resaltado en amarillo
def imprimir_matriz_con_camino(matriz, camino):
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if (i, j) == camino[0]:
                print('\033[1;32m' + matriz[i][j] + '\033[0m', end=' ')  # Imprime en verde el punto de inicio
            elif (i, j) == camino[-1]:
                print('\033[1;31m' + matriz[i][j] + '\033[0m', end=' ')  # Imprime en rojo el punto final
            elif (i, j) in camino:
                print('\033[1;33m' + matriz[i][j] + '\033[0m', end=' ')  # Imprime en amarillo el camino
            elif matriz[i][j] in obstaculos:
                print('\033[1;34m' + matriz[i][j] + '\033[0m', end=' ')  # Imprime en azul los obstáculos
            else:
                print(matriz[i][j], end=' ')
        print()

# Crear la matriz
matriz = crear_matriz()

# Obtener letras para los obstáculos del usuario
obstaculos = obtener_obstaculos()

# Obtener puntos de inicio y fin del usuario
inicio, fin = obtener_puntos_usuario(matriz)

# Encontrar el camino utilizando A*
camino = encontrar_camino_A_estrella(matriz, inicio, fin, obstaculos)

if camino:
    # Imprimir la matriz con el camino resaltado en amarillo y los obstáculos en azul
    print("\nMatriz 4x6 con camino resaltado y obstáculos:")
    imprimir_matriz_con_camino(matriz, camino)
else:
    print("No se encontró un camino válido.")