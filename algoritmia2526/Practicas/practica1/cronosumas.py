#!/usr/bin/env python3
import time
from sumas import *

for prefix in ["nums","dnums"]:
    for n in [10, 100, 1000, 10000]:
            test = f"nums/{prefix}{n}"
            f = open(test)
            data = read_data(f)
            t0 = time.process_time()
            result = process(data)
            t1 = time.process_time()
            print (f"{test+':':18} {t1-t0:f}")
    print("-"*80)