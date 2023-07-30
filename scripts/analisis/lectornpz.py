"""
Este script es para verificar que los datos almacenados
por recopilador.py son correctos
"""


import numpy as np
import matplotlib as plt
import pandas as pd
from datetime import datetime, timedelta

aux = np.load('/home/richard/Escritorio/datos/database.npz', allow_pickle='TRUE')
n_block = aux['n_block']
time_b = aux['time_b']
size = aux['size']
ntx = aux['ntx']
bits = aux['bits']
chainwork = aux['chainwork']
strippedsize = aux['strippedsize']
weight = aux['weight']
total = aux['total']

print(type(time_b))
print(type(time_b[100]))



#############################
#a=time_b.copy()

#crea un arreglo que empieza en 1 sube hasta 798268, sube de 1 en 1 
a=np.copy(time_b)
c=np.linspace(1,len(a),len(a))
#copia el contenido del arreglo time_b
i=0
z=len(a)
diferencias=[]
for i in range(1,len(a)):
    fecha_anterior=datetime.strptime(a[i-1], "%Y-%m-%d %H:%M:%S")
    fecha_actual = datetime.strptime(a[i], "%Y-%m-%d %H:%M:%S")
    diferencia = (fecha_actual - fecha_anterior).total_seconds()
    diferencias.append(diferencia)

print(diferencias[0],diferencias[1])
print(len(diferencias))

#fig,ax=plt.subplots()
#crea un objeto graficable del tipo fig
#ax.scatter(c,diferencias)
#crea una grafica de sipersion y toma como eje x al arreglo "c", eje y a "b"




# print('*********************')
# print('El total de bloques procesados:', end=' ')
# print(len(n_block), end=' ')
# print('Total: ', total)
# print('Datos del último bloque: ')
# print('n_block,time,size,ntx')
# print(n_block[-1], time_b[-1], size[-1], ntx[-1])
# print('*********************')
# print(n_block.shape, size.shape, strippedsize.shape)
