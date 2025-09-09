import sys
from typing import TextIO

type Data = list[int]
type Result = list[int]


def read_data(f: TextIO) -> Data:
# Leer del fichero f
    lines = f.readlines()
    return [int(line) for line in lines]


#show_results lee la lista
def show_results(result : Result):
    for numero in result :
        print(numero) 


if __name__ == "__main__":
    data = read_data(sys.stdin)
    show_results(data)