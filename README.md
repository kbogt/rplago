# rplago
Archivos para controlar la redpitaya a utilizar en LAGO.

Existen cuatro archivos los cuales se detallan de la siguiente manera:

**RPPMTwTSens.pdf** Archivo PDF de los esquemáticos de la tarjeta de polarización. 

**lago_gt_spi.py**  Librería para controlar la tarjeta.

**spi.py**  Archivo de ejemplo para controlar el PMT

**spi.c** Archivo .c editado del ejemplo original de Red Pitaya para adecuarse al TLV5614

El archivo spi.c debe ser compilado utilizando gcc previo a ejecutar el ejemplo spi.py, el ejecutable por defecto se llama a.out, si se cambia el nombre debe ser editado el nombre en el *lago_gt_spi.py* 

Una ejecución típica es:

<code>:~$./spi.py voltage opciones</code>

**voltage** El valor del voltaje es un entero de 0 a 2000 voltios

**opciones** Opciónes de cambio la única ejecutada actualmente es *v* la cuál despliega lo que se está ejecutando en cada momento, (para debugging)

**PENDIENTE**

Agregar en la librería el control i2c para el sensor de temperatura/presión
