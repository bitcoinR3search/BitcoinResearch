import numpy as np

aux         =  np.load('database.npz', allow_pickle='TRUE') 
n_block     =  aux['n_block']
time        =  aux['time']
size        =  aux['size']
ntx         =  aux['ntx']
print('*********************')
print('El total de bloques procesados:',end=' ')
print(len(n_block))
print('Datos del último bloque: ')
print('n_block,time,size,ntx')
print(n_block[-1],time[-1],size[-1],ntx[-1])
