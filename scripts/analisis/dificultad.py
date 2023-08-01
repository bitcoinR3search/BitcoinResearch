'''
Este script realiza el analisis de la serie de tiempo de la 
dificultad de la red.
'''

#usar comandos del sistema
import os
#manejo numerico
import numpy as np
#graficar
import matplotlib.pyplot as plt
#libreria manejo de tipografia
from matplotlib import font_manager as fm, rcParams
from app.styles import *

#cambiar la typografia
fpath = os.path.join(r'MonoLisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]






def crear_imagen(estilo='estilo_dark'):
    fig, ax = plt.subplots(figsize=(10,7),dpi=200)
    fig.patch.set_facecolor(Estilos[estilo][1])
    ax.set_facecolor(Estilos[estilo][2])
    
    
    plt.show()



crear_imagen()