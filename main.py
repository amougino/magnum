from peristrofi_lib import *
import random
import time

settings = [
    {
        'mass_unit' : 'kg',
        'mass_prec' : -8
    }
]

if __name__ == '__main__':
    l = []
    iterations = 100000
    start = time.time()
    for i in range(iterations):
        l.append(MagNum(i))
    t = time.time()-start
    print(t/iterations*1000)