import numpy as np



aux         =  np.load('bins/database.npz', allow_pickle='TRUE') 
n_block     =  aux['n_block']
time_b        =  aux['time_b']
size        =  aux['size']
ntx         =  aux['ntx']


print('*********************')
print('El total de bloques procesados:',end=' ')
print(int(n_block.shape[0]))
print('Datos del último bloque: ')
print('n_block,time,size,ntx')
print(n_block[-1],time_b[-1],size[-1],ntx[-1])
print('*********************')