#!/usr/bin/env python

# Homework 3, work with classmates Krishna Saharsh Mamidipalli, and Abhishek Dhande
# Copyright 2023 Yuqi Jin yuqijin8@bu.edu
# Copyright 2023 abhishek dhande abhi86@bu.edu
# Copyright 2023 Krishna Saharsh Mamidipalli mkrishna@bu.edu

class Polynomial():
    
    # implement a constructor which takes a sequence and assigns the coefficients in the natural 
    # (descending order). 
    # for example: p = Polynomial([4,-9,5.6]), 4 has x^2, -9 has x^1, 5.6 has x^0
    # {2: 4, 1: -9, 0: 5.6}
    def __init__(self, input = []):
        self.input_raw = input
        # create a dictionary/map called polynomial
        self.polynomial = {}
        # iterate from large exponent to smaller
        index = len(input) - 1
        for coeff in input:
            self.polynomial[index] = coeff
            index = index - 1
        self.keys = list(self.polynomial.keys()) # ex: 2,1,0 -> exponent
        
    # implement the add method
    # they have only with same exponent degrees can sum together self polynomial + other Polynomial
    def __add__(self, other):       
        sum_result = Polynomial()
        
        for exponent in self.polynomial.keys():
            # case 1: If both polynomials have a term with the same exponent, add their coefficients.
            if exponent in other.polynomial.keys():
                sum_result[exponent] = self.polynomial[exponent] + other.polynomial[exponent]
        
            # case 2: If the other polynomial doesn't have a term with the same exponent, use the coefficient from self.
            else:
                sum_result[exponent] = self.polynomial[exponent] 
                
        # post-processing
        # check the exponent in other poly without adding yet
        for exponent in other.polynomial.keys(): 
            try:
                if exponent not in self.polynomial.keys(): 
                    sum_result[exponent] = other.polynomial[exponent]
            except: 
            # if exponent does not exist, give 0 value 
                if exponent not in self.polynomial.keys(): 
                    sum_result[exponent] = 0
        return sum_result # return a new instance of class Polynomial 
        
    # implement the substract method
    # they have only with same exponent degrees can substract together
    # return: self polynomial - other Polynomial
    def __sub__(self, other):
        sub_result = Polynomial()
        for exponent in self.polynomial.keys():
            # case 1: If both polynomials have a term with the same exponent, substract their coefficients.
            if exponent in other.polynomial.keys():
                sub_result[exponent] = self.polynomial[exponent] - other.polynomial[exponent]
        
            # case 2: If the other polynomial doesn't have a term with the same exponent, use the coefficient from self.
            else:
                sub_result[exponent] = self.polynomial[exponent] 
                
        # post-processing
        # check the exponent in other poly without adding yet
        for exponent in other.polynomial.keys(): 
            try:
                if exponent not in self.polynomial.keys(): 
                    sub_result[exponent] = other.polynomial[exponent]
            except: 
            # if exponent does not exist, give 0 value 
                if exponent not in self.polynomial.keys(): 
                    sub_result[exponent] = 0
        return sub_result # return new instance of class Polynomial
    
    # implement the multiplication method
    # for-for loop, iterate both polynomials
    # update the new exponents and their coeffs
    def __mul__(self, other):
        mul_result = {}
        for exponent_one in self.polynomial.keys():
            for exponent_two in other.polynomial.keys():
                # case 1: If both polynomials' coefficients are not mult yet, multiply it and update the key in the mul_result
                if mul_result.get(exponent_one + exponent_two) == None:
                    mul_result[exponent_one + exponent_two] = self.polynomial[exponent_one] * other.polynomial[exponent_two]
                # case 2: If this exponent is already exists when poly1 & poly2, update the result into mul_result by add previous again
                else:
                    mul_result[exponent_one + exponent_two] = mul_result[exponent_one + exponent_two] + (self.polynomial[exponent_one] * other.polynomial[exponent_two])
        # solve the negative power cases
        negative_polynomial = self.negative(mul_result)
        return negative_polynomial
    
    # need to compare each polynomial's key: exponent and value: coeff
    def __eq__(self, other):
        # case 1: If the exponents are the same
        if self.polynomial.keys() == other.polynomial.keys():
            # then check their coeffs corsponding with the exponent
            for exponent in self.polynomial.keys():
                if self.polynomial[exponent] == other.polynomial[exponent]:
                    result = True
                else:
                    result = False
                    break
        # case 2: if the exponents are not the same, return False directly
        else: 
            result = False
        return result
    
    # implement a derivative method p.deriv() which returns the derivative of the polynomial.
    # derivate a power with 0 (which is constant) is 0
    # ex: 2*x^2 = 2*2*x^(2-1).... if d(2)/dx, the result is 0
    def deriv(self):
        deriv_result = {}
        for exponent in self.polynomial.keys():
            if exponent != 0:
                deriv_result[exponent - 1] = exponent * self.polynomial[exponent]
        # deal with negative power case
        negative_polynomial = negative(deriv_result)
        return negative_polynomial
    
    # implement the eval method, such as p.eval(2.1)
    # input number into a polynomial to evaluate 
    def eval(self, input):
        result = 0
        for exponent in self.polynomial.keys():
            result += polynomial[exponent] * (input ** exponent)
        return result
    
    # implement negative powers in the polynomial
    # to handle the negative power of x, it is time to create a dictionary which is converted from old dict
    # add some negitive numbers into the dictionary with corresponding value coeff
    def negative(self, with_negative_dict):
        negative_polynomial = Polynomial([])
        for exponent in with_negative_dict.keys():
            negative_polynomial.__setitem__(exponent, with_negative_dict[exponent])
        negative_polynomial.keys = list(with_negative_dict.keys())
        return negative_polynomial
        
        
    def __setitem__(self, key, value):
        # set this key (exponent) from the map corresponding with value (coefficient)
        self.polynomial[key] = value
        # list of keys append new key
        self.keys.append(key)
    
    def __getitem__(self, key):
        # from the map to get the value (coefficient) with the corresponding Key(exponent)
        map = self.polynomial
        if map.get(key) == None:
            return 0
        return map[key]


class Complex():
    "Complex(real,[imag]) -> a complex number"

    def __init__(self,real=0,imag=0):
        self.real=real
        self.imag=imag

    def __abs__(self):
        "abs(self)"
        return (self.real**2 +self.imag**2)**0.5

    def __add__(self,value):
        "Return self+value."
        if hasattr(value,'imag'):
            return Complex(self.real+value.real,self.imag+value.imag)
        else:
            return Complex(self.real+value,self.imag)

    def __mul__(s,v):
        "Return s*v."
        if hasattr(v,'imag'):
            x = s.real * v.real - s.imag * v.imag
            y = s.real * v.imag + v.real * s.imag
            return Complex(x,y)
        else:
            return Complex(v*s.real,v*s.imag)

    def __rmul__(s,v):
        "Return s*v"
        if hasattr(v,'imag'):
            x = s.real * v.real - s.imag * v.imag
            y = s.real * v.imag + v.real * s.imag
            return Complex(x,y)
        else:
            return Complex(v*s.real,v*s.imag)

    def __radd__(self,value):
        "Return self+value"
        if hasattr(value,'imag'):
            return Complex(self.real+value.real,self.imag+value.imag)
        else:
            return Complex(self.real+value,self.imag)            

    def __str__(self):
        if self.real==0:
            return "{}j".format(self.imag)
        else:
            sign="-" if self.imag<0 else "+"
            return "({}{}{}j)".format(self.real,sign,abs(self.imag))

    def __repr__(self):
        return str(self)

    def __pow__(self,value):
        "Return self ** value"
        raise NotImplementedError('not done yet')
            
if __name__=="__main__":
    main()
#---------------------------------------------------------------------------------

        
   