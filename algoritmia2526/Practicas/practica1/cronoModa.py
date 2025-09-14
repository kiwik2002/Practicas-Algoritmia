#!/usr/bin/env python3
import time
from moda import *

carpeta = "nums"
for prefix in ["nums"]:
    for n in [10, 100, 1000, 10000]:
            test = f"{carpeta}/{prefix}{n}"
            f = open(test)
            data = read_data(f)
            t0 = time.process_time()
            result = process(data)
            t1 = time.process_time()
            print (f"{test+':':18} {t1-t0:f}")
    print("-"*80)