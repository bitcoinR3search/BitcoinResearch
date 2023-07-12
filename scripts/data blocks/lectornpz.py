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

a=pd.to_datetime(a,format='%Y%m%d %H:%M:%s')
#convierte los datos de fecha en 
#a=datetime.strptime("%Y%m%d , %H:%M:%s ").timestamp()
while i<z-1:
     b=((a[i]-a[i+1])**2)**(1/2)
     i=i+1
print(a[0],a[1])
#print(b[2])
#print(z)
#print(type(z))

fig,ax=plt.subplots()
#crea un objeto graficable del tipo fig
ax.scatter(c,b)
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
