import sys
from typing import TextIO

type Data = list[int]
type Result = int


def read_data(f: TextIO) -> Data:
# Leer del fichero f
    lines = f.readlines()
    return [int(line) for line in lines]

def process(data: Data) -> Result:
    menor = data[0]
    for dato in data :
        if dato < menor:
            menor = dato
    return menor

#show_results lee la lista
def show_results(result : Result):
    print(result)


if __name__ == "__main__":
    data = read_data(sys.stdin)
    result = process(data)
    show_results(result)