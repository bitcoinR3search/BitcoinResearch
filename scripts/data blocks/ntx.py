# este script construye la gráfica histórica
# con el número de transacciones por cada bloque
# asi como el acumulado


#librerias a usar
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib import font_manager as fm, rcParams
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
#import locale
#locale.setlocale(locale.LC_TIME, 'es')


fpath = os.path.join(r'bins/MonoLisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]


# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
    (44, 44, 44), (255, 255, 248), (255, 255, 255), (255, 152, 150),  
    (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
    (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
    (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)] 

for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)   



# Cargamos los datos a usar como arrays

aux         =  np.load('bins/database.npz', allow_pickle='TRUE') 
n_block     =  aux['n_block']
time_b        =  aux['time_b']
size        =  aux['size']
ntx         =  aux['ntx']
bits        =  aux['bits']
chainwork = aux['chainwork']
strippedsize = aux['strippedsize']
weight = aux['weight']

# Las fechas tienen un tratamiento especial.
# la mejor forma de hacerlo es pasarlos como objetos
# que matplot interpreta como fechas.

time_b = pd.to_datetime(time_b) #time_b es un array con fechas en str
#las convertimos a datetime y solo guardamos la fecha (no la hora)
time_b = time_b.date 

# un nuevo array contendra los valores para q matplotlib maneje fechas.
# estos valores son números. No se rescatan. 
num_dates = mdates.date2num(time_b)

#La gráfica deberia reunir a todos los puntos.
#sin embargo para facilidad tomamos el primero valor 
#de cada corrección de dificultad

num_dates=num_dates[::2016]
# se dividen enter mil para mostrar el dato en KB
ntx=ntx[::2016]


### GENERANDO LA IMAGEN

fig, ax = plt.subplots(figsize=(33,11),dpi=300)

#Color del fondo
fig.patch.set_facecolor(tableau20[4])
plt.axes().patch.set_facecolor(tableau20[5])

plt.title(r"$\bf{BITCOIN:\ HISTORIAL\ DEL\ NÚMERO\ DE\ TX}$" "\n" r"$\it{Comparación\ por\ bloque\ y\ por\ acumulado}$",fontsize=40,color=tableau20[6],fontproperties=prop)
plt.xlabel('Fecha Confirmación del Bloque',fontsize=35,fontproperties=prop,color=tableau20[6])
plt.ylabel('Número de Tx',fontsize=35,fontproperties=prop,color=tableau20[6])
plt.gca().yaxis.grid(linestyle='-',linewidth=2,dashes=(5,3))
plt.xlim(num_dates[0],num_dates[-1])
plt.ylim(0,1.1*max(ntx))
ax.set_yticks([], [])
ax.set_xticks([], [])
#ytick_labels = ['0 MB','1 MB','2 MB','3 MB','4 MB']
#plt.yticks([0, 1000, 2000, 3000, 4000],ytick_labels,fontsize=20,fontproperties=prop,color=tableau20[6]);

plt.plot_date(num_dates, ntx, "--", color=tableau20[0], linewidth=1)
plt.fill_between(num_dates, ntx, facecolor =tableau20[2], alpha = 0.7)

plt.plot_date(num_dates, np.cumsum(ntx)/100, "--", color=tableau20[10], linewidth=8)




locator = mdates.MonthLocator(interval=11)
formatter = mdates.DateFormatter('%B\n%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_tick_params(labelsize=10,rotation=20)
plt.tick_params(axis='x', colors=tableau20[6])

plt.xticks(fontsize=20,fontproperties=prop);
plt.yticks(fontsize=20,fontproperties=prop,color=tableau20[6]);


tw3 = mpimg.imread('pics/satoshi.png')
imagebox = OffsetImage(tw3,zoom=0.08)
firma3 = AnnotationBbox(imagebox,(datetime(2009, 6, 1),250))
plt.gca().add_artist(firma3)
plt.annotate('Lanzamiento de\nBitcoin\n9 de enero de 2009 ', xy=(datetime(2009, 2, 3),0),xytext=(datetime(2009, 2, 3),500),fontsize=15,fontproperties=prop,arrowprops=dict(facecolor='red', shrink=0.10))



plt.savefig('pics/ntx.png',bbox_inches='tight')
