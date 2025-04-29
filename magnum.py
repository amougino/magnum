# rotation
import os

def open_file(): ## to do
    pass

def analyse_file(): ## to do
    pass

def file_to_vel_pos(): ## to do
    pass

''' 
to do 4 (decide what to do with this?? maybe save in another file for
another time) -> good for continuing after the '.' for a bit, but nothing
else...
'''
class Num: 

    def __init__(self,value,power,precision):
        self.val = value
        self.pow = power
        self.prec = precision
        self.change_prec_round(precision)

    def change_prec_round(self,new_prec):
        if new_prec > self.pow:
            delta_pow = 10 ** (new_prec - self.pow)
            new_val = self.val // delta_pow
            if self.val % delta_pow >= delta_pow / 2:
                new_val += 1
            self.val = new_val
            self.pow = new_prec

    def change_prec_no_round(self,new_prec):
        if new_prec > self.pow:
            delta_pow = 10 ** (new_prec - self.pow)
            self.val = self.val // delta_pow
            self.pow = new_prec

    def __add__(self,other):
        if other.pow > self.pow:
            delta_pow = 10 ** (other.pow - self.pow)
            self.val += other.val * delta_pow
        else:
            delta_pow = 10 ** (self.pow - other.pow)
            self.val = self.val * delta_pow + other.val
            self.pow = other.pow
        self.change_prec_round(self.prec)
        return(self)

    def __mul__(self,other):
        self.val *= other.val
        self.pow += other.pow
        self.change_prec_round(self.prec)
        return(self)

    def __div__(self,other):
        pass

class MagNum:
    
    def __init__(self,float_val = 0,precision = -8,custom_val_pow_sign = ()):
        if len(custom_val_pow_sign) != 3:
            if float_val < 0:
                self.sign = -1
                float_val *= -1
            else:
                self.sign = 1
            split_float = str(float_val).split('.')
            if len(split_float) == 2 and split_float[1] != '0':
                self.val = [int(char) for char in (split_float[0] + split_float[1])]
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
        #print(self.val,self.pow)

    def change_prec_round(self,new_prec):
        if new_prec > self.pow:
            new_val = self.val[:self.pow - new_prec]
            if self.val[self.pow-new_prec] >= 5:
                new_val[-1] += 1
            self.val = new_val
            self.pow = new_prec
            while self.val[-1] == 0 and self.pow < 0:
                self.val.pop(-1)
                self.pow += 1

    def change_prec_no_round(self,new_prec):
        if new_prec > self.pow:
            self.val = self.val[:self.pow-new_prec]
            self.pow = new_prec
            while self.val[-1] == 0 and self.pow < 0:
                self.val.pop(-1)
                self.pow += 1

    def flatten(self):
        for i in range(1,len(self.val)):
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
            
    def abs_greater(self,other):
        if (self.val,self.pow) == (other.val,other.pow):
            return(False)
        else:
            pos_len_self = len(self.val) + self.pow
            pos_len_other = len(other.val) + other.pow
            if pos_len_self != pos_len_other:
                return(pos_len_self > pos_len_other)
            else:
                idx = 0
                min_len = min(len(self.val),len(other.val))
                while idx < min_len:
                    if self.val[idx] != other.val[idx]:
                        return(self.val[idx] > other.val[idx])
                    else:
                        idx += 1
                return(len(self.val) > len(other.val))

    def __add__(self,other,sign_diff = 1):
        if self.sign == other.sign * sign_diff:
            return(self.add(other))
        else:
            if self.abs_greater(other):
                return(self.sub(other)) #sign = self.sign
            else:
                if (self.val,self.pow) == (other.val,other.pow):
                    return(MagNum(
                        precision = max(self.prec,other.prec),
                        custom_val_pow_sign = ([0],0,1)
                    ))
                else:
                    return((other.sub(self,sign_diff = -1))) #sign = other.sign
            
    def __sub__(self,other):
        return(self.__add__(other,sign_diff = -1))

    def add(self,other):
        if other.pow > self.pow:
            new_other_val = other.val + [0 for i in range(other.pow - self.pow)]
            new_self_val = self.val
            new_pow = self.pow
        else:
            new_self_val = self.val + [0 for i in range(self.pow - other.pow)]
            new_other_val = other.val
            new_pow = other.pow
        len_self = len(new_self_val)
        len_other = len(new_other_val)
        if len_self > len_other:
            new_other_val = [0 for i in range(len_self - len_other)] + new_other_val
        else:
            new_self_val = [0 for i in range(len_other - len_self)] + new_self_val
        new_val = []
        for i in range(len(new_self_val)):
            new_val.append(new_self_val[i] + new_other_val[i])
        new_num = MagNum(precision = max(self.prec,other.prec),
                         custom_val_pow_sign = (new_val,new_pow,self.sign))
        new_num.flatten()
        return(new_num)
    
    def sub(self,other,sign_diff = 1): ## to do 3
        if other.pow > self.pow:
            new_other_val = other.val + [0 for i in range(other.pow - self.pow)]
            new_self_val = self.val
            new_pow = self.pow
        else:
            new_self_val = self.val + [0 for i in range(self.pow - other.pow)]
            new_other_val = other.val
            new_pow = other.pow
        new_other_val = [0 for i in range(len(new_self_val) - len(new_other_val))] + new_other_val
        new_val = []
        for i in range(len(new_self_val)):
            new_val.append(new_self_val[i] - new_other_val[i])
        new_num = MagNum(precision = max(self.prec,other.prec),
                         custom_val_pow_sign = (new_val,new_pow,self.sign * sign_diff))
        new_num.flatten()
        new_num.flatten_horizontal()
        return(new_num)
    
    def __str__(self):
        str_val = ''.join(str(i) for i in self.val)
        if self.pow < 0:
            str_val = (str_val[:len(self.val) + self.pow] + 
            '.' + 
            str_val[len(self.val) + self.pow:])
        else:
            str_val = (str_val + '0'*self.pow)
        if self.sign == 1:
            return(str_val)
        else:
            return('-'+str_val)

class Vector: ## to do
    pass

class Body: ## to do
    pass

class System: ## to do
    pass