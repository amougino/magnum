# rotation

class MagNum:

    def __init__(self, float_val=0, precision=-8, custom_val_pow_sign=()):
        if custom_val_pow_sign == ():
            if float_val < 0:
                self.sign = -1
                float_val *= -1
            else:
                self.sign = 1
            split_float = str(float_val).split('.')
            if len(split_float) == 2 and split_float[1] != '0':
                self.val = [int(char)
                            for char in (split_float[0] + split_float[1])]
                self.pow = -len(split_float[1])
            else:
                self.pow = 0
                while split_float[0][-1] == '0' and len(split_float[0]) > 1:
                    self.pow += 1
                    split_float[0] = split_float[0][:-1]
                self.val = [int(char) for char in split_float[0]]
        else:
            self.val = custom_val_pow_sign[0]
            self.pow = custom_val_pow_sign[1]
            self.sign = custom_val_pow_sign[2]
        self.prec = precision
        self.change_prec_round(precision)
        self.flatten_horizontal()

    def change_prec_round(self, new_prec):
        if new_prec > self.pow:
            new_val = self.val[:self.pow - new_prec]
            if self.val[self.pow-new_prec] >= 5:
                new_val[-1] += 1
            self.val = new_val
            self.pow = new_prec
            self.flatten()
            '''while self.val[-1] == 0 and self.pow < 0:
                self.val.pop(-1)
                self.pow += 1'''  # re-add if seen that necessary

    def change_prec_no_round(self, new_prec):
        if new_prec > self.pow:
            self.val = self.val[:self.pow-new_prec]
            self.pow = new_prec
            while self.val[-1] == 0 and self.pow < 0:
                self.val.pop(-1)
                self.pow += 1

    def flatten(self):
        for i in range(1, len(self.val)):
            idx = len(self.val) - i
            self.val[idx - 1] += self.val[idx] // 10
            self.val[idx] %= 10
        while self.val[0] // 10 != 0:
            self.val.insert(0, self.val[0] // 10)
            self.val[1] %= 10

    def flatten_horizontal(self):
        if self.val != [0]:
            while self.val[-1] == 0:
                self.val.pop(-1)
                self.pow += 1
            while self.val[0] == 0:
                self.val.pop(0)

    def abs_greater(self, other):
        if (self.val, self.pow) == (other.val, other.pow):
            return (False)
        else:
            pos_len_self = len(self.val) + self.pow
            pos_len_other = len(other.val) + other.pow
            if pos_len_self != pos_len_other:
                return (pos_len_self > pos_len_other)
            else:
                idx = 0
                min_len = min(len(self.val), len(other.val))
                while idx < min_len:
                    if self.val[idx] != other.val[idx]:
                        return (self.val[idx] > other.val[idx])
                    else:
                        idx += 1
                return (len(self.val) > len(other.val))

    def __add__(self, other, sign_diff=1):
        if self.sign == other.sign * sign_diff:
            return (self.add_sub(other))
        else:
            if self.abs_greater(other):
                return (self.add_sub(other, operation=-1))
            else:
                if (self.val, self.pow) == (other.val, other.pow):
                    return (MagNum(
                        precision=max(self.prec, other.prec),
                        custom_val_pow_sign=([0], 0, 1)
                    ))
                else:
                    return ((other.add_sub(self, operation=-1, sign_diff=-1)))

    def __sub__(self, other):
        return (self.__add__(other, sign_diff=-1))

    def add_sub(self, other, operation=1, sign_diff=1):
        if other.pow > self.pow:
            new_other_val = other.val + \
                [0 for i in range(other.pow - self.pow)]
            new_self_val = self.val
            new_pow = self.pow
        else:
            new_self_val = self.val + \
                [0 for i in range(self.pow - other.pow)]
            new_other_val = other.val
            new_pow = other.pow
        len_self = len(new_self_val)
        len_other = len(new_other_val)
        if len_self > len_other:
            new_other_val = [0 for i in range(
                len_self - len_other)] + new_other_val
        else:
            new_self_val = [0 for i in range(
                len_other - len_self)] + new_self_val
        new_val = []
        for i in range(len(new_self_val)):
            new_val.append(new_self_val[i] + new_other_val[i] * operation)
        new_num = MagNum(precision=max(self.prec, other.prec),
                         custom_val_pow_sign=(new_val, new_pow, self.sign * sign_diff))
        new_num.flatten()
        new_num.flatten_horizontal()
        return (new_num)

    def __mul__(self, other):
        # collect both powers
        # add both powers
        # calculate val multiplication
        # re-add the powers
        # return

        return ('Work in progress...')

    def karatsuba(self, other):
        # make copies of self and other

        # 1 DIGIT NUMBER

        # if len self == 1
        # for every item in other, multiply by the only object in self
        # flatten
        # flatten horizontal ?
        # return result

        # do the same for len other == 1 with an "elif"

        # MULTIPLE DIGIT NUMBER

        # if self and other are not of the same length
        # set them to the same length

        # length : length of self and other (now the same length)
        # half : int(length/2)
        # split them in half (create high_a, low_a, high_b, low_b)

        # calculate z0 : low_a * low_b
        # calculate z1 : (high_a + low_a) * (high_b + low_b)
        # calculate z2 : high_a * high_b
        # k : 10^(length - half)
        # calculate f : z2 * k^2 + (z1 - (z2 + z0)) * k + z0
        # return f

        pass

    def __str__(self):
        str_val = ''.join(str(i) for i in self.val)
        if self.pow < 0:
            str_val = (str_val[:len(self.val) + self.pow] +
                       '.' +
                       str_val[len(self.val) + self.pow:])
        else:
            str_val = (str_val + '0'*self.pow)
        if self.sign == 1:
            return (str_val)
        else:
            return ('-'+str_val)

# karatsuba
# division
# powers / fractional powers ?
