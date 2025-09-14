import sys
from typing import TextIO

type Data = list[int]
type Result = list[int]


def read_data(f: TextIO) -> Data:
# Leer del fichero f
    lines = f.readlines()
    #funcion generatriz  es un truquito que lo que hace es
    #coje una linea y esa linea lo transforma en entero
    #y se almacena en la lista
    return [int(line) for line in lines]
#show_results lee la lista
def show_results(result: Result):
    for num in result:
        print(num)


if __name__ == "__main__":
    result = read_data(sys.stdin)
    show_results(result)