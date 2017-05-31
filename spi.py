#!/usr/bin/env python2.7
from lago_gt_spi import *
#####Constantes del sistema
##DAC
Ch=2
Vmax=4.68
Vmin=0
Nbits=12
##PMT
fep=807.23 #Factor de escala del pmt 1 vin == <fep> vpmt

verbose=False

val=int(sys.argv[1])
if len(sys.argv)>2:
	if  sys.argv[2]=='v':
		verbose=True
	else:
		verbose=False

if val>2000 or val<0:
	raise IndexError('El voltaje debe ser un valor entre 0 y 2000')
if val%256==0: #correccion de 00 bits
    val=val+1
    
pmt0=pmt(fep)
dac0=dac(Ch, Vmax, Vmin, Nbits)
vdac=pmt0.vpmt2vdac(val)
pack=dac0.pack(dac0.val2cod(vdac))

rp_open()
if verbose: print "scpi abierto"
spi_load(pack)
if verbose: print "enviando spi"
rp_loaddac()
if verbose: print "loaddac cargado"
#rp_close()
#print "cerrando scpi"
bmp=bmp180()

print "PMT polarizado a "+str(val)+" voltios."
print "Temperatura: "+str(round(bmp.temperature(),2))+ " C"+" Presion: "+str(bmp.pressure())+" Pa"" Altitud: "+str(round(bmp.altitude(),2))+" msnm"



