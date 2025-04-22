import os
import numpy as np
import pandas as pd
import matplotlib.dates as mdates


#os.chdir('D:/proyectos/BitcoinResearch/BitcoinResearch/scripts/')
os.chdir('~/BitcoinResearch/scripts/')
#os.chdir('/home/richard/TRABAJO/BitcoinResearch/scripts/')


def leer_data(*args):
    aux = np.load('bins/database.npz', allow_pickle='TRUE')
    if len(args) == 1:
        return aux[args[0]]
    else:
        return [aux[arg] for arg in args]

def estado_data():
    aux = np.load('bins/database.npz', allow_pickle='TRUE')
    last_n_block = aux['n_block'][-1]
    variables = list(aux.files)
    return print('Last block: '+str(int(last_n_block))+'\nVariables :'+', '.join(variables))

def time_data(time_b):
    time_b = mdates.date2num(pd.to_datetime(time_b).date)
    return time_b


def bitcoins_emitidos(num=np.load('bins/database.npz', allow_pickle='TRUE')['n_block'][-1]):
    num_bloque=int(num)
    # Recompensa inicial por bloque
    recompensa_inicial = 50
    # Número de bloques entre halvings
    bloques_por_halving = 210000
    
    # Determinar cuántos halvings han ocurrido
    num_halvings = num_bloque // bloques_por_halving
    
    # Calcular la recompensa actual por bloque
    recompensa_actual = recompensa_inicial / (2 ** num_halvings)
    
    # Calcular el total de bitcoins emitidos hasta el bloque dado
    bitcoins_total = 0
    for i in range(num_halvings + 1):
        bloques_en_este_periodo = min(bloques_por_halving, num_bloque - bloques_por_halving * i)
        bitcoins_total += bloques_en_este_periodo * (recompensa_inicial / (2 ** i))    
    return bitcoins_total

def punto_halv(b=np.load('bins/database.npz', allow_pickle='TRUE')['n_block'][-1]):
    bloque = int(b)
    bloques_por_halving = 210000
    halving_completos = bloque // bloques_por_halving  
    residuo = bloque % bloques_por_halving
    fraccion = residuo / bloques_por_halving
    return halving_completos + fraccion

def last_block():
    aux = np.load('bins/database.npz', allow_pickle='TRUE')
    last_b = aux['n_block'][-1]
    return int(last_b)

if __name__ == '__main__':
    print(last_block())
