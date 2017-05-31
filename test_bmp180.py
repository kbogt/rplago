#!/usr/bin/env python2.7

from ctypes import *

#defining address and i2c channel
i2c_device=c_char_p('/dev/i2c-0')
address=c_int(0x77)

#opening shared object
bmp180=CDLL("./libbmp180.so")

#setting return types for arguments

bmp180.temperature.restype=c_float
bmp180.pressure.restype=c_long
bmp180.altitude.restype=c_float

a=(bmp180.temperature(address, i2c_device),bmp180.pressure(address, i2c_device),bmp180.altitude(address, i2c_device))
print type(a)
print a
