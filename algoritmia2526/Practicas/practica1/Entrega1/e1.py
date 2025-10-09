import sys
from typing import TextIO

from algoritmia.datastructures.queues import Fifo


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

# - Recibe un descriptor de fichero de texto que contiene una instancia del problema
#   en el formato descrito en el apartado 1.2 del enunciado.
# - Devuelve la instancia como un objeto de tipo Data.
def read_data(f: TextIO) -> Data:
    calorias_x , calorias_y = (int(s) for s in f.readline().split())
    rows , cols = (int(s) for s in f.readline().split())
    aristas : list[Edge] = []
    #Extraigo las aristas y las convierto
    for line in f:
        for stru , strv , stra ,strb in line.split():
            u,v,a,b = int(stru), int(strv), int(stra), int(strb)
            aristas.append(((u,v),(a,b)))
    grafo : UndirectedGraph[Vertex]  = UndirectedGraph(E=aristas)
    return calorias_x, calorias_y, rows, cols,grafo

# - Recibe un objeto de tipo Data con la instancia del problema.
# - Devuelve el resultado como un objeto de tipo Result.
def process(data: Data) -> Result:
    calorias_x, calorias_y, rows, cols,grafo = data

    #obtener la habitacion del tesoro
    tesoro_room : Vertex = habitacion_tesoro(grafo, (0,0))
    #ir a la habitacion del tesoro
    camino = traverse_bf(grafo, (0,0),tesoro_room)
    pasossintesoro , pathtesoro = reconstructor(camino,tesoro_room)
    #me voy a la  salida con el tesoro
    camino = traverse_bf(grafo, tesoro_room,(rows-1,cols-1))
    pasoscontesoro , pathcontesoro = reconstructor(camino,(rows-1,cols-1))

    #preparo los resultados
    caloria = cal_calorias(calorias_x, calorias_y,pasossintesoro,pasoscontesoro)
    return ((rows, cols),caloria ,pathtesoro,pathcontesoro)

# - Recibe un objeto de tipo Result con el resultado del problema.
# - Muestra la salida en el formato que se indica en el apartado 1.3 del enunciado
def cal_calorias(cal_x : int , cal_y : int,pasossintesoro : int , pasoscontesoro : int) -> int:
    return cal_x*pasossintesoro + cal_y*pasoscontesoro
def show_results(result: Result):
    (row, col), total_cal, path1, path2 = result
    print(row, col)
    print(total_cal)
    print(_path2str(path1))
    print(_path2str(path2))

def traverse_bf (graph: UndirectedGraph[Vertex],inicio : Vertex , destino : Vertex) -> dict[Vertex, Vertex]:
    queue : Fifo[Edge] = Fifo[Edge]()
    queue.push((inicio,inicio))
    vistos : set[Vertex] = set()
    vistos.add(inicio)
    bp: dict[Vertex, Vertex] = {}
    while len(queue) > 0:
        u,v = queue.pop()
        bp[v] = u
        for suc in graph.succs(v):
            if suc not in vistos:
                vistos.add(suc)
                if suc == destino:
                    bp[suc]=v
                    return bp
                else:
                    queue.push((v,suc))
    return bp
def reconstructor(bp: dict[Vertex,Vertex],fin:Vertex) -> tuple[int , list[Vertex]]:
    #re haces el camino
    path = [fin]
    cont = 0
    while fin != bp[fin]:
        cont += 1
        fin = bp[fin]
        path.append(fin)
    path.reverse()
    return cont, path

def habitacion_tesoro(graph: UndirectedGraph[Vertex],inicio : Vertex)-> Vertex:
    #esto es lo mas importante
    queue: Fifo[tuple[Vertex,int]] = Fifo[tuple[Vertex,int]]()
    queue.push((inicio,0))
    vistos: set[Vertex] = set()
    vistos.add(inicio)
    maxpasos = 0
    tesoro = inicio
    while len(queue) > 0:
        v, pasos= queue.pop()

        for suc in graph.succs(v):
            if suc not in vistos:
                vistos.add(suc)
                nextpasos = pasos + 1
                if nextpasos > maxpasos:
                    maxpasos = nextpasos
                    tesoro  = suc
                queue.push((suc, nextpasos))

    return  tesoro

    return 0 , inicio


#usaremos este metodo cuando tengamos varios camino y saber cual es el mas calorico


#Esta funcion coje 2 vertices distintos y te compara si si te has movido
#en el eje x o en y en funcion de eso te devolvera un numero que sera
#lo que has consumido
def cal_calorias(u: Vertex,v : Vertex ,cal_x , cal_y) -> int:
    a, b = u
    c, d = v
    if a == c:
        # te has movido en el eje Y
        return cal_y
    else :
        # te has movido en el eje X
        return  cal_x


    return 0
# --- Programa principal ---


if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_results(result0)
