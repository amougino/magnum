import copy
from magnum.oper.basic_func import flatten_horizontal, abs_greater, add_sub
from magnum.oper.long_div import long_div

# constants can change
_SQRT_PREC_MULTIPLIER = 1.1
_SQRT_PREC_SHIFT = -2


def _extra_prec(prec, multiplier=_SQRT_PREC_MULTIPLIER, shift=_SQRT_PREC_SHIFT):
    prec = (prec*multiplier) + shift
    return int(prec)


def _nr_sqrt_start(val, pow):
    n_pos = len(val) + pow - 1
    start_pow = n_pos//2
    if n_pos % 2 == 1:
        start_val = [3]
    else:
        start_val = [1]
    return (start_val, start_pow)


def _next_nr_sqrt(x0v, x0p, orig_v, orig_p, prec):
    x1v, x1p = long_div(orig_v, orig_p, x0v, x0p, prec)
    x1v, x1p = add_sub(x1v, x1p, x0v, x0p)
    x1v, x1p = long_div(x1v, x1p, [2], 0, prec)
    return (x1v, x1p)


def nr_sqrt(val, pow, sign, prec):
    adapted_prec = _extra_prec(prec)
    if sign == -1:
        raise Exception(
            'mag error : cannot obtain the square root of a negative number')
    x0v, x0p = _nr_sqrt_start(val, pow)
    x1v, x1p = _next_nr_sqrt(x0v, x0p, val, pow, adapted_prec)
    while True:
        if abs_greater(x0v, x0p, x1v, x1p):
            delta_v, delta_p = add_sub(x0v, x0p, x1v, x1p, operation=-1)
        else:
            delta_v, delta_p = add_sub(x1v, x1p, x0v, x0p, operation=-1)
        delta_v, delta_p = flatten_horizontal(delta_v, delta_p)
        if abs_greater([1], prec, delta_v, delta_p) or delta_v == [0]:
            return (x1v, x1p)
        else:
            x0v = copy.deepcopy(x1v)
            x0p = copy.deepcopy(x1p)
            x1v, x1p = _next_nr_sqrt(x0v, x0p, val, pow, adapted_prec)
