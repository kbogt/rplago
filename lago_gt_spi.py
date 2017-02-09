###spi control module for redpitaya

#base for housing in memory map
base=0x400000000
#Expansion connector direction addres
ecdp=0x10 #module p
ecdn=0x14 #module n
#Expansion conector output address
ecop=0x18
econ=0x1c

import sys
import struct
import os
import time

def rp_open():
    os.system("systemctl start redpitaya_scpi")
    os.system("monitor "+hex(base+ecdn)+" "+hex(1))

def rp_close():
    os.system("systemctl stop redpitaya_scpi")

def rp_loaddac():
    os.system("monitor "+hex(base+econ)+" "+hex(1))
    time.sleep(0.001)
    os.system("monitor "+hex(base+econ)+" "+hex(0))
    
def spi_load(pack):
    os.system("./a.out "+pack)

class pmt:
    def __init__(self, sfp=773.2):
        self.sfp=sfp

    def vpmt2vdac(self, vpmt):
        return vpmt/self.sfp

    def vdac2vpmt(self, vdac):
        return vdac*self.sfp
    
class dac:
    def __init__(self, Ch=4, Vmax=4.68, Vmin=0,  Nbits=12, Nchan=4):
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
