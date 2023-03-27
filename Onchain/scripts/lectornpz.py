import numpy as np



aux         =  np.load('bins/database.npz', allow_pickle='TRUE') 
n_block     =  aux['n_block']
time_b        =  aux['time_b']
size        =  aux['size']
ntx         =  aux['ntx']
bits        =  aux['bits']
chainwork = aux['chainwork']
strippedsize = aux['strippedsize']
weight = aux['weight']
total = aux['total']

print('*********************')
print('El total de bloques procesados:',end=' ')
print(int(n_block.shape[0]),end=' ')
print('Total: ',total)
print('Datos del último bloque: ')
print('n_block,time,size,ntx')
print(n_block[-1],time_b[-1],size[-1],ntx[-1])
print('*********************')
print(n_block.shape,size.shape,strippedsize.shape)
# for a in n_block:
#    print(a)