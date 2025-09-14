import sys
from typing import TextIO

type Data = list[int]
type Result = bool


def read_data(f: TextIO) -> Data:
# Leer del fichero f
    lines = f.readlines()
    return [int(line) for line in lines]
def average(nums: list[int]) -> float:
    return sum(nums)/len(nums)
def process(data: Data) -> Result:
    seen = set()
    for n in data:
        if n in seen:
            return True
        seen.add(n)
    return False
#show_results lee la lista
def show_result(result: Result):
    print("No hay repetidos" if not result
    else "Hay repetidos")

if __name__ == "__main__":
    data = read_data(sys.stdin)
    result = process(data)
    show_result(result)