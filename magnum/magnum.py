# rotation


import oper


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

    def change_prec_no_round(self, new_prec):
        if new_prec > self.pow:
            self.val = self.val[:self.pow-new_prec]
            self.pow = new_prec
            while self.val[-1] == 0 and self.pow < 0:
                self.val.pop(-1)
                self.pow += 1

    def flatten(self, f_flatten=oper.flatten):
        self.val = f_flatten(self.val)

    def flatten_horizontal(self, f_flatten_horizontal=oper.flatten_horizontal):
        self.val, self.pow = f_flatten_horizontal(self.val, self.pow)

    def abs_greater(self, other, f_abs_greater=oper.abs_greater):
        return f_abs_greater(self.val, self.pow, other.val, other.pow)

    def __add__(self, other, sign_diff=1, f_add_sub=oper.add_sub):
        if self.sign == other.sign * sign_diff:
            new_val, new_pow = f_add_sub(
                self.val, self.pow, other.val, other.pow)
            sign_diff = 1
        else:
            if self.abs_greater(other):
                new_val, new_pow = f_add_sub(
                    self.val, self.pow, other.val, other.pow, operation=-1)
                sign_diff = 1
            else:
                if (self.val, self.pow) == (other.val, other.pow):
                    return MagNum(
                        precision=max(self.prec, other.prec),
                        custom_val_pow_sign=([0], 0, 1)
                    )
                else:
                    new_val, new_pow = f_add_sub(
                        other.val, other.pow, self.val, self.pow, operation=-1)
                    sign_diff = -1
        new_num = MagNum(precision=max(self.prec, other.prec),
                         custom_val_pow_sign=(
                             new_val,
                             new_pow,
                             self.sign * sign_diff
        ))
        return new_num

    def __sub__(self, other):
        return self.__add__(other, sign_diff=-1)

    def __mul__(self, other, f_mul=oper.karatsuba):
        new_prec = max(self.prec, other.prec)
        new_val = f_mul(self.val, other.val)
        new_pow = self.pow + other.pow
        new_sign = self.sign * other.sign
        new_num = MagNum(precision=new_prec, custom_val_pow_sign=(
            new_val, new_pow, new_sign))
        return new_num

    def __truediv__(self, other, f_div=oper.long_div):
        new_prec = min(self.prec, other.prec)
        new_val, new_pow = f_div(
            self.val, self.pow, other.val, other.pow, new_prec)
        new_sign = self.sign * other.sign
        return MagNum(precision=new_prec, custom_val_pow_sign=(new_val, new_pow, new_sign))

    def __str__(self):
        str_val = ''.join(str(i) for i in self.val)
        if self.pow < 0:
            if len(self.val) <= self.pow*-1:
                str_val = '0.' + '0'*((self.pow+len(self.val))*-1) + str_val
            else:
                str_val = (str_val[:len(self.val) + self.pow] +
                           '.' + str_val[len(self.val) + self.pow:])
        else:
            str_val = (str_val + '0'*self.pow)
        if self.sign == 1:
            return str_val
        else:
            return ('-'+str_val)

# division
# check __str__... shit seems weird
# powers / fractional powers ?

# _ in front of func = not supposed to be used by user
# all caps = constant
# add descriptions of each function (description, args, arg type, return, return type)
