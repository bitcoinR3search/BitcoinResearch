import os
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

os.chdir('/home/richard/TRABAJO/BitcoinResearch/scripts')



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


if __name__ == '__main__':
    a = leer_data('time_b')
    print(time_data(a))


