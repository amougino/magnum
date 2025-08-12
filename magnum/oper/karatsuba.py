import copy


def karatsuba_add_sub(val1, val2, operation='add'):
    len1 = len(val1)
    len2 = len(val2)

    if len1 > len2:
        val2 = [0 for i in range(len1 - len2)] + val2
        len2 = len1
    else:
        val1 = [0 for i in range(len2 - len1)] + val1
        len1 = len2

    f = []
    if operation == 'add':
        for i in range(len1):
            f.append(val1[i] + val2[i])
    elif operation == 'sub':
        for i in range(len1):
            f.append(val1[i] - val2[i])

    lenf = len(f)
    for i in range(1, lenf):
        idx = lenf - i
        f[idx - 1] += f[idx] // 10
        f[idx] %= 10
    while f[0] // 10 != 0:
        f.insert(0, f[0] // 10)
        f[1] %= 10
    while f[0] == 0 and len(f) > 1:
        f.pop(0)

    return f


def karatsuba(val1, val2):
    copy1 = copy.deepcopy(val1)
    copy2 = copy.deepcopy(val2)

    if len(copy1) == 1:
        len2 = len(copy2)
        for i in range(len2):
            copy2[i] *= copy1[0]
        for i in range(1, len2):
            idx = len2 - i
            copy2[idx - 1] += copy2[idx] // 10
            copy2[idx] %= 10
        while copy2[0] // 10 != 0:
            copy2.insert(0, copy2[0] // 10)
            copy2[1] %= 10
        return copy2

    elif len(copy2) == 1:
        len1 = len(copy1)
        for i in range(len1):
            copy1[i] *= copy2[0]
        for i in range(1, len1):
            idx = len1 - i
            copy1[idx - 1] += copy1[idx] // 10
            copy1[idx] %= 10
        while copy1[0] // 10 != 0:
            copy1.insert(0, copy1[0] // 10)
            copy1[1] %= 10
        return copy1

    else:
        if len(copy1) != len(copy2):
            if len(copy1) > len(copy2):
                copy2 = [0 for i in range(len(copy1)-len(copy2))] + copy2
            else:
                copy1 = [0 for i in range(len(copy2)-len(copy1))] + copy1

    length = len(copy1)
    half = int(length/2)
    high_a = copy1[:half]
    low_a = copy1[half:]
    high_b = copy2[:half]
    low_b = copy2[half:]

    z0 = karatsuba(low_a, low_b)  # ac
    z1 = karatsuba(karatsuba_add_sub(high_a, low_a),
                   karatsuba_add_sub(high_b, low_b))  # (a+b)(c+d)
    z2 = karatsuba(high_a, high_b)  # bd

    k = length - half

    z0pz2 = karatsuba_add_sub(z0, z2)
    z1m_z0pz2 = karatsuba_add_sub(z1, z0pz2, 'sub')

    f = karatsuba_add_sub(z2 + [0 for i in range(2*k)],
                          karatsuba_add_sub(z1m_z0pz2 + [0 for i in range(k)], z0))
    return f
