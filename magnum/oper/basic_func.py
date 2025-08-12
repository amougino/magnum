def abs_greater(val1, pow1, val2, pow2):
    if (val1, pow1) == (val2, pow2):
        return False
    else:
        len1 = len(val1)
        len2 = len(val2)
        pos_len1 = len1 + pow1
        pos_len2 = len2 + pow2
        if pos_len1 != pos_len2:
            return (pos_len1 > pos_len2)
        else:
            idx = 0
            min_len = min(len1, len2)
            while idx < min_len:
                if val1[idx] != val2[idx]:
                    return (val1[idx] > val2[idx])
                else:
                    idx += 1
            return (len1 > len2)


def add_sub(val1, pow1, val2, pow2, operation=1):
    if pow2 > pow1:
        new_val2 = val2 + \
            [0 for i in range(pow2 - pow1)]
        new_val1 = val1
        new_pow = pow1
    else:
        new_val1 = val1 + \
            [0 for i in range(pow1 - pow2)]
        new_val2 = val2
        new_pow = pow2
    len_val1 = len(new_val1)
    len_val2 = len(new_val2)
    if len_val1 > len_val2:
        new_val2 = [0 for i in range(
            len_val1 - len_val2)] + new_val2
    else:
        new_val1 = [0 for i in range(
            len_val2 - len_val1)] + new_val1
    new_val = []
    for i in range(len(new_val1)):
        new_val.append(new_val1[i] + new_val2[i] * operation)
    return (new_val, new_pow)
