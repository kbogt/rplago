#!/usr/bin/env python2.7

###spi and bmp180 wrapper module for redpitaya to use in python


#base for housing in memory map
base=0x40000000 
#Expansion connector direction addres
ecdp=0x10 #module p 
ecdn=0x14 #module n
#Expansion conector output address
ecop=0x18 #module p
econ=0x1c #module n

import sys
import struct
import os
import time
from ctypes import *

#i2c device info
i2c_device=c_char_p('/dev/i2c-0')
i2c_address=c_int(0x77)

librpSerial=CDLL("./src/libbmp180.so")
#setting return types for preset functions
librpSerial.temperature.restype=c_float
librpSerial.pressure.restype=c_long
librpSerial.altitude.restype=c_float


def rp_open():
    os.system("systemctl start redpitaya_scpi") #opening scpi
    os.system("monitor "+hex(base+ecdn)+" "+hex(1)) #setting n port direction
    time.sleep(0.001)
    os.system("monitor "+hex(base+econ)+" "+hex(1)) #setting ldac on high


def rp_close():
    os.system("systemctl stop redpitaya_scpi")

def rp_loaddac():
    #os.system("monitor "+hex(base+econ)+" "+hex(1))
    #time.sleep(0.001)
    os.system("monitor "+hex(base+econ)+" "+hex(0))
    print "monitor "+hex(base+econ)+" "+hex(0)
    time.sleep(0.00001)
    os.system("monitor "+hex(base+econ)+" "+hex(1))
    
def spi_load(pack):
   # os.system("./a.out "+pack)
    a=librpSerial.spi_load(pack)
    print a
    print pack

class pmt:
    def __init__(self, sfp=773.2):
        self.sfp=sfp

    def vpmt2vdac(self, vpmt):
        return vpmt/self.sfp

    def vdac2vpmt(self, vdac):
        return vdac*self.sfp

class bmp180:
    def __init__(self, address=i2c_address, device=i2c_device):
	self.address=address
	self.device=device

    def temperature(self):
	return librpSerial.temperature(self.address, self.device)
    
    def pressure(self):
	return librpSerial.pressure(self.address, self.device)
    
    def altitude(self):
	return librpSerial.altitude(self.address, self.device)
    
class dac:
    def __init__(self, Ch=2, Vmax=4.68, Vmin=0,  Nbits=12, Nchan=4):
        self.vmax=Vmax
        self.vmin=Vmin
        self.dv=Vmax-Vmin
        self.n=Nbits
        self.span=2**self.n
        self.nchan=Nchan
        self.cheader=self.cHeader(Ch)

    def cHeader(self, ch):
        if ch-1 in range(self.nchan):
            return hex(int(ch-1)<<14)
        else:
            raise IndexError('ch not in value range')
            

    def val2cod(self, val, rad=hex):
        ###return cod for corresponding val
        if val<=self.vmax and val>=self.vmin:
            cod=int((val-self.vmin)/self.dv*(self.span-1))
            return rad(cod+int(self.cheader,16))
        else:
            raise IndexError('val is not between vmax and vmin')

    def cod2val(self, cod):
        ###return val of voltage corresponding to cod (in hex by default)
        if int(cod,16) in range(int(self.cheader,16)+0xfff+1):
            return round(float((int(cod,16)%int(self.cheader,16)))/(self.span-1)*self.dv,3)
        else:
            raise IndexError('cod is not in range')

    def chSelect(self, ch):
        self.cheader=self.cHeader(ch)
        print "Now selected channel "+str(ch)

    def pack(self,cod):
        return struct.pack('>H', int(cod,16))
