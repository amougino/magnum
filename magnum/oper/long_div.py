import copy
from oper.basic_func import *


def short_mul(val, digit):
    length = len(val)
    for i in range(length):
        val[i] *= digit
    for i in range(1, length):
        idx = length - i
        val[idx - 1] += val[idx] // 10
        val[idx] %= 10
    while val[0] // 10 != 0:
        val.insert(0, val[0] // 10)
        val[1] %= 10
    return val


def long_div(numer_val, numer_pow, denom_val, denom_pow, prec):
    modifier = 0
    if len(numer_val) > len(denom_val) + denom_pow:
        while abs_greater(numer_val, 0, denom_val, denom_pow + modifier + 1) == True:
            modifier += 1
    else:
        while abs_greater(numer_val, 0, denom_val, denom_pow + modifier) == False:
            modifier -= 1
    r = copy.deepcopy(numer_val)
    r_pow = 0
    div_pow = denom_pow + modifier
    q = []
    while r.count(0) != len(r):
        if len(r) == 1:
            r.append(0)
            r_pow -= 1
        digit = 0
        current_div = [0]
        next_div = copy.deepcopy(denom_val)
        while abs_greater(next_div, div_pow, r, r_pow) == False:
            digit += 1
            current_div = copy.deepcopy(next_div)
            next_div = short_mul(copy.deepcopy(denom_val), digit + 1)
        q.append(digit)
        r, r_pow = add_sub(r, r_pow, current_div, div_pow, operation=-1)
        div_pow -= 1
        if r_pow <= prec:
            break
    return (q, div_pow + 1 - denom_pow + numer_pow)
