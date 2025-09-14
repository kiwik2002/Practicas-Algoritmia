import sys
from typing import TextIO

type Data = list[int]
type Result = int


def read_data(f: TextIO) -> Data:
# Leer del fichero f
    lines = f.readlines()
    return [int(line) for line in lines]

def process(data: Data) -> Result:
    dic = {}
    for dato in data:
        if dato not in dic:
            dic[dato] = 1
        else:
            dic[dato] += 1
    keys = dic.keys()
    max = 0
    maxkey = None
    for key in keys:
        if max < dic[key]:
            maxkey = key
            max = dic[key]

    return maxkey
#show_results lee la lista
def show_results(result : Result):
        print(result)


if __name__ == "__main__":
    data = read_data(sys.stdin)
    result = process(data)
    show_results(result)