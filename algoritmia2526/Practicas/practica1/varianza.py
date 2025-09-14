import sys
from typing import TextIO

type Data = list[int]
type Result = float


def read_data(f: TextIO) -> Data:
# Leer del fichero f
    lines = f.readlines()
    return [int(line) for line in lines]
#calcula la media
def average(nums: list[int]) -> float:
    return sum(nums)/len(nums)
def process(data: Data) -> Result:
    s = 0
    media = average(data)
    for num in data:
        s += (num - media) ** 2
    return s/len(data)

#show_results lee la lista
def show_results(result : Result):
        print(result)

if __name__ == "__main__":
    data = read_data(sys.stdin)
    result = process(data)
    show_results(result)