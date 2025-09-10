import oper


class MagNum:

    def __init__(self, float_val=0, precision=-8, custom_val_pow_sign=()):
        '''
        float_val : float
        precision : int
        custom_val_pow_sign : ([int,int,...] with int between 0 and 9, int, 1 or -1)
        '''
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

    def __str__(self):
        '''
        turns self into a string (useful for a print)
        '''
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

    def __float__(self, length=10):
        '''
        length : int
        returns a float that is a rounded value of self, of length digits long
        '''
        if length > 16:
            length = 16
        len_val = len(self.val)
        if len_val > length:
            str_val = ''.join(str(i) for i in self.val[:length-1])
            if self.val[length] >= 5:
                str_val += str(self.val[length - 1] + 1)
            else:
                str_val += str(self.val[length - 1])
        else:
            str_val = ''.join(str(i) for i in self.val)
        if self.sign == -1:
            str_val = '-'+str_val
        str_val += 'E'+str(self.pow + len(self.val) - length)
        return (float(str_val))

    def change_prec_round(self, new_prec):
        '''
        new_prec : int
        change the precision to new_prec, with rounding
        '''
        if new_prec > self.pow:
            new_val = self.val[:self.pow - new_prec]
            if new_val != []:
                if self.val[self.pow - new_prec] >= 5:
                    new_val[-1] += 1
            else:
                new_val = [0]
            self.val = new_val
            self.pow = new_prec
            self.flatten()

    def change_prec_no_round(self, new_prec):
        '''
        new_prec : int
        change the precision to new_prec, without rounding
        truncates
        '''
        if new_prec > self.pow:
            self.val = self.val[:self.pow-new_prec]
            self.pow = new_prec
        self.flatten_horizontal()

    def flatten(self, f_flatten=oper.flatten):
        '''
        f_flatten : func
        flattens using the f_flatten function
        if there are non digits or non positive integers, self.val is adapted
        '''
        self.val = f_flatten(self.val)

    def flatten_horizontal(self, f_flatten_horizontal=oper.flatten_horizontal):
        '''
        f_flatten_horizontal : func
        removes extra 0s at beginning and end using f_flatten_horizontal function
        '''
        self.val, self.pow = f_flatten_horizontal(self.val, self.pow)

    def abs_greater(self, other, f_abs_greater=oper.abs_greater):
        '''
        other : MagNum
        f_abs_greater : func
        return : bool
        checks if the absolute value of self is greater than the absolute value of other
        '''
        return f_abs_greater(self.val, self.pow, other.val, other.pow)

    def __add__(self, other, sign_diff=1, f_add_sub=oper.add_sub):
        '''
        other : MagNum
        sign_diff : 1 or -1 (not used by user)
        f_add_sub : func
        return : MagNum
        adds self and other*sign_diff
        '''
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
        '''
        other : MagNum
        return : MagNum
        subtracts self and other
        '''
        return self.__add__(other, sign_diff=-1)

    def __mul__(self, other, f_mul=oper.karatsuba):
        '''
        other : MagNum
        f_mul : func
        return : MagNum
        multiplies self and other
        '''
        new_prec = max(self.prec, other.prec)
        new_val = f_mul(self.val, other.val)
        new_pow = self.pow + other.pow
        new_sign = self.sign * other.sign
        new_num = MagNum(precision=new_prec, custom_val_pow_sign=(
            new_val, new_pow, new_sign))
        return new_num

    def __truediv__(self, other, f_div=oper.long_div):
        '''
        other : MagNum
        f_div : func
        return : MagNum
        divides self and other
        '''
        new_prec = min(self.prec, other.prec)
        new_val, new_pow = f_div(
            self.val, self.pow, other.val, other.pow, new_prec)
        new_sign = self.sign * other.sign
        return MagNum(precision=new_prec, custom_val_pow_sign=(new_val, new_pow, new_sign))

    def sqrt(self, f_sqrt=oper.nr_sqrt):
        '''
        f_sqrt : func
        return : MagNum
        finds the square root of self
        '''
        new_val, new_pow = f_sqrt(self.val, self.pow, self.sign, self.prec)
        return MagNum(precision=self.prec, custom_val_pow_sign=(new_val, new_pow, self.sign))

# _ in front of func = not supposed to be used by user
# all caps = constant
# add descriptions of each function (description, args, arg type, return, return type)
