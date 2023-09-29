'''
Este script calcula y muestra el hashrate de la red Bitcoin

El hashrate es una variable que indica la potencia de trabajo de la red Bitcoin
La potencia de trabajo es la cantidad de hashes que se pueden realizar en un segundo
y depende del poder de hash de cada minero que esta en la red.

Este valor no se puede conocer con precision pues depende de factores externos 
a la red como el precio de la energia, la cantidad de hashpower de cada minero 
y maquina, etc.

sin embargo se puede inferir este valor a partir del trabajo de la red 
y el tiempo de llegada de cada bloque.

'''

# importamos librerias a usar

import numpy as np
import pandas as pd
from app.readata import read_data, time_data, last_block



# tomamos los valores de la red

chainw, timestamp = read_data('chainwork','timestamp')
