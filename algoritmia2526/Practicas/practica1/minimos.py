import sys
from typing import TextIO

type Data = list[int] # introduce el tipo de dato de entrada
type Result = int # introduce  el tipo de resultado


# lees el fichero de datos
def read_data(f: TextIO) -> Data:
    lines = f.readlines()
    return [int(line) for line in lines ]

# haces el procesamiento de los datos aqui
def process(data: Data) -> Result:
    minimo = data [0]
    for dato in data:
        if dato < minimo:
            minimo = dato
    return  minimo

# show_results funcion de resultados
def show_results(result: Result):
    print(f"el numero mas pequeño es {result}")

# Esto siempre igual  llamas a las funciones
if __name__ == "__main__":
    data = read_data(sys.stdin)
    result = process(data)
    show_results(result)