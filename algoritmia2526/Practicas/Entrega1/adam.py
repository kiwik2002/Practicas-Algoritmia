import sys
from typing import TextIO


# --- Comprobamos las versiones de Python y algoritmia ---

def _check_environment(min_py: tuple[int, ...], min_alg: tuple[int, ...]):
    # Comprueba la versión de Python
    if sys.version_info < min_py:
        print(f"Error: Se requiere Python {'.'.join(map(str, min_py))} o superior (detectado {sys.version.split()[0]})")
        sys.exit(1)
    # Comprueba la versión de algoritmia
    try:
        from algoritmia import TVERSION
    except ModuleNotFoundError:
        print("La biblioteca algoritmia no está instalada.")
        sys.exit(1)
    except ImportError:
        TVERSION = (0, 0, 0)
    if TVERSION < min_alg:
        print(f"Error: Se requiere algoritmia >= {'.'.join(map(str, min_alg))}")
        sys.exit(1)

_check_environment((3, 12), (3, 1, 4))  # Versiones mínimas: python 3.12 y algoritmia 3.1.4

# ---- Importamos de la biblioteca algoritmia ---

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo
from collections import deque

# --- Tipos ----

type Vertex = tuple[int, int]
type Edge = tuple[Vertex, Vertex]
type Path = list[Vertex]

# Tipo para las instancias (ver apartado 2.2 del enunciado)
type Data = tuple[int, int, int, int, UndirectedGraph[Vertex]]

# Tipo para los resultados (ver apartado 2.2 del enunciado)
type Result = tuple[Vertex, int, Path, Path]

# --- Funciones auxiliares ---

# Convierte un camino (lista de vértices) en un string con el formato indicado en
# el apartado 2.2 del enunciado.
def _path2str(path: list[Vertex]) -> str:
    return ' # '.join(f'{t[0]} {t[1]}' for t in path)

# --- Funciones ---

def traverse_bf(graph: UndirectedGraph[Vertex], start: Vertex) -> dict[Vertex, Vertex]:
    res: dict[Vertex, Vertex] = {}
    cola: Deque[Vertex] = deque()
    seen: set[Vertex] = set()
    cola.append(start)
    seen.add(start)

    while len(cola) > 0:
        u = cola.popleft()

        for v in graph.succs(u):
            if v not in seen:
                res[v] = u
                seen.add(v)
                cola.append(v)
    return res


def distancias_vertices(graph: UndirectedGraph, start: Vertex) -> dict[Vertex, int]:
    seen: set[Vertex] = set()
    res: dict[Vertex, int] = {}
    cola: Deque[Vertex] = deque()
    cola.append(start)
    seen.add(start)
    res[start] = 0

    while len(cola) > 0:
        u = cola.popleft()
        for v in graph.succs(u):
            if v not in seen:
                res[v] = res[u] + 1
                seen.add(v)
                cola.append(v)
    return res

def calcular_path(bp: dict[Vertex, Vertex], start: Vertex, end: Vertex) -> Path:

    res: Path = []

    v = end
    while v != start:
        res.append(v)
        v = bp[v]
    res.append(start)
    res.reverse()
    return res

def bfs_distancias_y_bp(graph: UndirectedGraph, start: Vertex) -> tuple[dict[Vertex, int], dict[Vertex, Vertex]]:
    seen: set[Vertex] = set()
    distancias: dict[Vertex, int] = {}
    bp: dict[Vertex, Vertex] = {}
    cola: Deque[Vertex] = deque()

    cola.append(start)
    seen.add(start)
    distancias[start] = 0

    while len(cola) > 0:
        u = cola.popleft()
        for v in graph.succs(u):
            if v not in seen:
                distancias[v] = distancias[u] + 1
                bp[v] = u
                seen.add(v)
                cola.append(v)

    return distancias, bp



# - Recibe un descriptor de fichero de texto que contiene una instancia del problema
#   en el formato descrito en el apartado 1.2 del enunciado.
# - Devuelve la instancia como un objeto de tipo Data.
def read_data(f: TextIO) -> Data:
    caloriasX, caloriasY = (int(s) for s in f.readline().split())
    rows, cols = (int(s) for s in f.readline().split())
    #Esta línea de código para cada linea que representa una arista en el archivo
    #lo convierte en una lista de aristas en una sola línea de código
    edges: list[Edge] = [((int(num1), int(num2)), (int(num3), int(num4))) for num1, num2, num3, num4 in (line.split() for line in f.readlines())]

    grafo: UndirectedGraph[Vertex] = UndirectedGraph(E=edges)

    return caloriasX, caloriasY, rows, cols, grafo

# - Recibe un objeto de tipo Data con la instancia del problema.
# - Devuelve el resultado como un objeto de tipo Result.
def process(data: Data) -> Result:

    caloriasX, caloriasY, rows, cols, grafo = data

    distancias_start, bp_start = bfs_distancias_y_bp(grafo, (0, 0))
    distancias_end, bp_end = bfs_distancias_y_bp(grafo, (rows-1, cols-1))

    max = -1
    tesoro: Vertex = (0, 0)
    for v in grafo.V:
        if v in distancias_start and v in distancias_end:
            score = caloriasX*distancias_start[v] + caloriasY*distancias_end[v]
            if score > max:
                max = score
                tesoro = v

    path_tesoro: Path = calcular_path(bp_start, (0, 0), tesoro)
    path_salida: Path = calcular_path(bp_end, (rows-1, cols-1), tesoro)
    path_salida.reverse()

    calorias_total = caloriasX*(len(path_tesoro)-1) + caloriasY*(len(path_salida)-1)

    return tesoro, calorias_total, path_tesoro, path_salida


# - Recibe un objeto de tipo Result con el resultado del problema.
# - Muestra la salida en el formato que se indica en el apartado 1.3 del enunciado
def show_results(result: Result):
    (row, col), total_cal, path1, path2 = result
    print(row, col)
    print(total_cal)
    print(_path2str(path1))
    print(_path2str(path2))

# --- Programa principal ---

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_results(result0)