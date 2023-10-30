#!/usr/bin/env python


import numpy as np
import time
import struct

# Homework 2, work with classmates Krishna Saharsh Mamidipalli, and Abhishek Dhande
# Copyright 2023 Yuqi Jin yuqijin8@bu.edu
# Copyright 2023 abhishek dhande abhi86@bu.edu
# Copyright 2023 Krishna Saharsh Mamidipalli mkrishna@bu.edu
 
# 3.1
def show_integer_properties():
    # prints out the capability of integers using 1 to 8 bytes of storage
    Table = "{:<6} {:<22} {:<22} {:<22}"
    print(Table.format("Bytes","Largest Unsigned Int","Minimum Signed Int","Maximum Signed Int"))
    
    for i in range(1, 9):
        Bytes = i
        bits = 2**(8*i)
        Largest_Unsigned_Int = bits - 1
        Minimum_Signed_Int = -1 * (bits/2)
        Maximum_Signed_Int = (bits/2) - 1
        print(Table.format(Bytes,int(Largest_Unsigned_Int),int(Minimum_Signed_Int),int(Maximum_Signed_Int)))

show_integer_properties()

# # 3.2
# wrap around
# import numpy
# m = numpy.array([1],dtype= numpy.int16)

# while m[0]>0:
#     m[0] += 1
#     print(m)
    
# m = numpy.int16(1)
# while m>0:
#       m = m + 1
# because the 1 is not int16, it will eventually overflow

def estimate_wrap_around():
    int_16 = np.array([1],dtype = np.int16)
    start_time = time.time()
    while int_16[0] > 0:
        int_16[0] += 1
    end_time = time.time()
    measured_time = (end_time - start_time) # in seconds
    
    measured_time_16 = measured_time * 1e6
    print(f"Measured {'16-bit'} time (microseconds): {measured_time_16:.0f}")
    # the output of 16-bit is 65741 microSeconds
    
    estimate_time_8 = (measured_time / 256) * 1e9  # microsecond to nanosecond
    print(f"Estimated {'8-bit'} time (nanoseconds): {estimate_time_8:.1f}")

    estimate_time_32 = measured_time * 2**16 # microseconds to seconds
    print(f"Estimated {'32-bit'} time (seconds): {estimate_time_32:.5f}")
    
    estimate_time_64 = (estimate_time_32 * 2**32) / (365*60*60*24) # microsec to year
    print(f"Estimated {'64-bit'} time (years): {estimate_time_64:.3f}") 

estimate_wrap_around()


# 3.3
# Floating point representation of numbers is superior to integer representation in that numbers “close to zero” like 0.01213 can be represented and used for calculations. 
# It also allows for the representation of very large numbers.
# The tradeoff, however, is that floating point numbers cannot represent as many integers accurately (i.e. without round off error) as the integer of the same size.
# Write a function maximum_consecutive_int_value(float_type) that returns an integer N defined such all integers 1,2,3,…,N can be represented without loss of accuracy by a float of this size.
# The input argument is one of numpy.float16 numpy.float32 numpy.float64 numpy.float128

def maximum_consecutive_int_value(float_type):

    roundoff_error = np.finfo(float_type).eps
    max_conse_int_Value = int(1.0 / roundoff_error)
    return max_conse_int_Value

# Test the function with different float types
print("float16:", maximum_consecutive_int_value(np.float16))
print("float32:", maximum_consecutive_int_value(np.float32))
print("float64:", maximum_consecutive_int_value(np.float64))
print("float128:", maximum_consecutive_int_value(np.float128))


# 3.4
# Using your knowledge of floating-point number representations,
# write four functions that will calculate the following values

# 1. the largest possible double-precision number (not infinity): largest_double()
# 2. the smallest double-precision number greater than zero: smallest_double()
# 3. the largest possible single-precision number (not infinity): largest_single()
# 4. the smallest single-precision number greater than zero: smallest_single()
# In this problem, you should include the denormal/subnormal numbers.

# The greatest real number that can be represented exactly as a double-precision real is 2**1024 – 2**971, 
# and the least positive real that can be so represented is 2**-1074.
def largest_double():
    # the binary representation: 0 11111111110 1111111111111111111111111111111111111111111111111111
    binary_representation = "0b0111111111101111111111111111111111111111111111111111111111111111"
    return struct.unpack('d', struct.pack('Q', int(binary_representation, 2)))[0]

def smallest_double():
    binary_representation = "0b0000000000000000000000000000000000000000000000000000000000000001"
    return struct.unpack('d', struct.pack('Q', int(binary_representation, 2)))[0]

def largest_single():
    # it can be represented by 0 11111110 11111111111111111111111
    binary_representation = "0b01111111011111111111111111111111"
    
    return struct.unpack('f', struct.pack('I', int(binary_representation, 2)))[0]

def smallest_single():
    # it can be represented by 0 00000000 00000000000000000000001
    binary_representation = "0b00000000000000000000000000000001"
    
    return struct.unpack('f', struct.pack('I', int(binary_representation, 2)))[0]
    
print("the largest possible double-precision number (not infinity)", largest_double())
print("the smallest double-precision number greater than zero", smallest_double())
print("the largest possible single-precision number (not infinity)", largest_single())
print("the smallest single-precision number greater than zero", smallest_single())


# 3.5
# Write a function breakdown_float(f) that returns a dictionary of its sign, exponent, and fraction,
# all integers and a boolean flag “subnormal” which indicates whether the subnormal state was required to represent this number.
# For example,
# >>> m = numpy.float64(2.5)
# >>> d = breakdown_float(m)
# >>> print(d)
# {'sign': 0, 'fraction': 1125899906842624, 'exponent': 1024, 'subnormal': False}
# The argument should be positional-only

def breakdown_float(f):
    string = str(type(f))
    string = string[:-2]

    sign = 1 if f<0 else 0
    if (string.endswith('64')):
        hex_value = struct.unpack('>Q', struct.pack('>d', f))[0]
        hex_string = hex(hex_value)
        int_val = int(hex_string, 16)
        bin_val = bin(int_val)
        bin_val = bin_val[2:]

        if (len(bin_val) < 64):
            bin_val = '0'* (64-len(bin_val)) + bin_val


        exponent = int(bin_val[1:12], 2)
        fraction = int(bin_val[12:], 2)

        if (exponent == 0 and fraction >= 1):
            subnormal = True
        else:
            subnormal = False

    elif (string.endswith('32')):
        hex_value = struct.unpack('>I', struct.pack('>f', f))[0]
        hex_string = hex(hex_value)
        int_val = int(hex_string, 16)
        bin_val = bin(int_val)
        bin_val = bin_val[2:]
    
        if (len(bin_val) < 32):
            bin_val = '0'* (32-len(bin_val)) + bin_val

        exponent = int(bin_val[1:9], 2)
        fraction = int(bin_val[9:], 2)
        if (exponent == 0 and fraction >= 1):
            subnormal = True
        else:
            subnormal = False
    elif (string.endswith('16')):
        hex_value = struct.unpack('>H', struct.pack('>e', f))[0]
        hex_string = hex(hex_value)
        int_val = int(hex_string, 16)
        bin_val = bin(int_val)
        bin_val = bin_val[2:]

        if (len(bin_val) < 16):
            bin_val = '0'* (16-len(bin_val)) + bin_val


        exponent = int(bin_val[1:6], 2)
        fraction = int(bin_val[6:], 2)
        if (exponent == 0 and fraction >= 1):
            subnormal = True
        else:
            subnormal = False
    return {
    "sign": sign,
    "exponent": exponent,
    "fraction": fraction,
    "subnormal": subnormal,
    }

f64 = np.float64(-23874.384579)
f32 = np.float32(4)
f16= np.float16(291.45)
print(breakdown_float(f64))
print(breakdown_float(f32))
print(breakdown_float(f16))
# test case
# m = np.float64(2.5)
# d = breakdown_float(m)
# print(d)


# 3.6
# Write a function construct_float(float_parms,float_type) that uses a dictionary of its sign, exponent, and fraction, all integers) 
# to produce a value of type float_type which should be one of numpy.float16 numpy.float32 numpy.float64 numpy.float128

# If it is not possible to make such a float, raise a ValueError exception.
# The function should also have an optional keyword-only parameter subnormal with default value False.
# If subnormal is True, then a subnormal float with the specified float parameters should be created.
# The first parameter, float_parms, should be positional only, and the second parameter should be keyword only with default value float

def construct_float(float_params, float_type=float, *, subnormal=False):
    sign = float_params.get('sign', 0)
    exponent = float_params.get('exponent', 0)
    fraction = float_params.get('fraction', 0)

    if not (0 <= sign <= 1):
        raise ValueError("Sign must be 0 or 1")
    if not isinstance(float_parms, dict):
        raise ValueError("float_parms must be a dictionary.")

    if not all(key in float_parms for key in ["sign", "exponent", "fraction"]):
        raise ValueError("float_parms must contain the keys 'sign', 'exponent', and 'fraction'.")

    if not all(isinstance(value, int) for value in float_parms.values()):
        raise ValueError("All values in float_parms must be integers.")

    if float_type not in [np.float16, np.float32, np.float64, np.float128]:
        raise ValueError("float_type must be one of numpy.float16, numpy.float32, numpy.float64, or numpy.float128.")
    
    #Float128
    if float_type == np.float128:
        e = (exponent - 16383) - 112
        two_power = 2**e

        hex_of_fraction = hex(fraction)
        hex_of_fraction = hex_of_fraction[2:]

        if fraction == 0:
            e = (exponent - 16383)
            two_power = 2**e
            float_value = two_power
            return float_value

        elif len(hex_of_fraction) < 28 and not subnormal:
            hex_of_fraction = ('1'* (28 - (len(hex_of_fraction)))) + hex_of_fraction

        elif len(hex_of_fraction) < 28 and subnormal:
            e = (- 16382) - 112
            two_power = 2**e
            hex_of_fraction = ('0'* (28 - (len(hex_of_fraction)))) + hex_of_fraction

        float_value = ((-1)**sign)*(int(hex_of_fraction, 16)) * two_power
    #Float64
    if float_type == np.float64:
        e = (exponent - 1023) - 52
        two_power = 2**e

        hex_of_fraction = hex(fraction)
        hex_of_fraction = hex_of_fraction[2:]

        if fraction == 0:
            e = (exponent - 1023)
            two_power = 2**e
            float_value = two_power
            return float_value

        elif len(hex_of_fraction) < 14 and not subnormal:
            hex_of_fraction = ('1'* (14 - (len(hex_of_fraction)))) + hex_of_fraction

        elif len(hex_of_fraction) < 14 and subnormal:
            e = (- 1022) - 52
            two_power = 2**e
            hex_of_fraction = ('0'* (14 - (len(hex_of_fraction)))) + hex_of_fraction

        float_value = ((-1)**sign)*(int(hex_of_fraction, 16)) * two_power
        
    #Float32
    if float_type == np.float32:
        e = (exponent - 127) - 23
        two_power = 2**e

        bin_of_fraction = bin(fraction)
        bin_of_fraction = bin_of_fraction[2:]

        if fraction == 0:
            e = (exponent - 127)
            two_power = 2**e
            float_value = two_power
            return float_value

        elif len(bin_of_fraction) < 24 and not subnormal:
            bin_of_fraction = ('1'* (24 - (len(bin_of_fraction)))) + bin_of_fraction

        elif len(bin_of_fraction) < 24 and subnormal:
            e = (- 126) - 23
            two_power = 2**e
            bin_of_fraction = ('0'* (24 - (len(bin_of_fraction)))) + bin_of_fraction

        float_value = ((-1)**sign)*(int(bin_of_fraction, 2)) * two_power
        
    #Float16
    if float_type == np.float16:
        e = (exponent - 15) - 10
        two_power = 2**e

        bin_of_fraction = bin(fraction)
        bin_of_fraction = bin_of_fraction[2:]

        if fraction == 0:
            e = (exponent - 15)
            two_power = 2**e
            float_value = two_power
            return float_value

        elif len(bin_of_fraction) < 11 and not subnormal:
            bin_of_fraction = ('0'* (11 - (len(bin_of_fraction)))) + bin_of_fraction
            bin_of_fraction = '1' + bin_of_fraction[1:]
        elif len(bin_of_fraction) < 11 and subnormal:
            e = (-14) - 10
            two_power = 2**e
            bin_of_fraction = ('0'*(11 - (len(bin_of_fraction)))) + bin_of_fraction

        float_value = ((-1)**sign)* (int(bin_of_fraction, 2)) * two_power

    if not np.isfinite(float_value):
        raise ValueError("The float parameters are not valid for the specified float type.")

    return float_value
# Example usage:
# float_params = {'sign': 0, 'exponent': 1023, 'fraction': 1125899906842624}
# result = construct_float(float_params, float_type=np.float64, subnormal=False)
# print(result)


# 3.7
# In this section, we are going to write a function that generates a specific floating point number, 
# according to the following input parameters:
# 1. start_float: required positional-only parameter
# 2. index: optional keyword-only parameter with default value of 1. The value of index is used to determine the index-th next float in the sequence of possible floating point numbers.
# 3. The name of the function should be get_next_float
# Other requirements:
# 1. the type of start_float must be one of numpy.float16 numpy.float32 numpy.float64 numpy.float128 or simply float. 
# If it is not one of these, the function should raise an exception of type TypeError
# 2. the value of index must be positive. If it is not, the function should raise an exception of type ‘ValueError’
# 3. the return value must be the same type as start_float
# 4. if there is no floating-point number, then positive infinity should be returned (again, in the same type as start_float)
# 5. the type of index must be an integer (numpy.intx or int). If it is not, the function should raise an exception of type TypeError

def get_next_float(start_float, *, index=1):
    #1
    if type(start_float) not in (float, np.float16, np.float32, np.float64, np.float128):
        raise TypeError("The float type is not correct")
    
    #2
    if index <= 0:
        raise ValueError("The value type in is not correct")
    
    #5
    if not isinstance(index, (int, np.int_)):
        raise TypeError("The index is not integer")
    
    if isinstance(start_float, float):
        step = np.nextafter(start_float, np.inf) - start_float
    else:
        step = np.nextafter(start_float.item(), np.inf) - start_float.item()
    
    next_float = start_float + index * step
    
    #4
    if np.isposinf(next_float):
        return type(start_float)(next_float)
    
    # 3
    return type(start_float)(next_float)

# try:
#     result = get_next_float(np.float64(1.0), index=2)
#     print(result)
# except (TypeError, ValueError) as e:
#     print(f"Error: {e}")

