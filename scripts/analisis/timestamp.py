    
import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm

from PIL import Image
from datetime import datetime
from app.styles import Estilos, colores
from app.readata import leer_data, time_data

fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fpatht = os.path.join('bins/BigBlueTerm437NerdFont-Regular.ttf')
title = fm.FontProperties(fname=fpatht)
fname = os.path.split(fpath)[1]


tipo = 'estilo_dark'

fig, ax = plt.subplots(figsize=(20, 5), dpi=200)

fig.patch.set_facecolor(Estilos[tipo][1])
ax.patch.set_facecolor(Estilos[tipo][1])
preferencias = {'color': Estilos[tipo][0], 'fontproperties': prop}

plt.suptitle("Timestamp of Bitcoin\nBlock Arrivals",fontsize=45,x=0.25,y=1.4,fontproperties=title,color=Estilos[tipo][0])
time,n_block = leer_data('time_b','n_block')
n_block=n_block[1:]
#time_b = time_data(time)[1:]
diferencias = pd.Series(pd.to_datetime(time)).diff().dt.total_seconds().dropna()/60

A_p = np.where(diferencias.values >= 0)[0]
A_n = np.where(diferencias.values < 0)[0]
A_p = A_p[1:]
A_n = A_n[1:]

d_max = diferencias[diferencias.idxmax()]
d_min = diferencias[diferencias.idxmin()]

ax.xaxis.set_tick_params(labelsize=18, rotation=20,color='w')
ax.yaxis.set_tick_params(labelsize=13, rotation=10,color='w')
ax.tick_params(axis='both', labelcolor='w')

ax.axvline(n_block[210000*1],ymax=.5, color=Estilos[tipo][0], linestyle='--', linewidth=1)
ax.text(n_block[210000*1+50000],-400, '1st\nHalv', ha='right', va='center', size=18,**preferencias)
ax.axvline(n_block[210000*2],ymax=.5,linestyle='--', linewidth=1,color=Estilos[tipo][0])
ax.text(n_block[210000*2+50000],-400, '2nd\nHalv',ha='right', va='center', size=18,**preferencias)
ax.axvline(n_block[210000*3],ymax=.5,color=Estilos[tipo][0], linestyle='--', linewidth=1)
ax.text(n_block[210000*3+50000],-400, '3rd\nHalv', ha='right', va='center', size=18,**preferencias)

ax.axhline(0,color=Estilos[tipo][0],linewidth=1.5,zorder=3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.spines['bottom'].set_visible(False)

for spine in ax.spines.values():
    spine.set_color(Estilos[tipo][0])


ax.set_ylabel('Block arrival times [min]',fontsize=18,**preferencias)
ax.set_xlabel('\n# Block',fontsize=18,**preferencias)
ax.set_ylim(-1400, 1600)
ax.set_yticks(range(-200, 1601, 400)) 

ax.plot(n_block[A_p],diferencias.values[A_p],color=colores[9])
ax.plot(n_block[A_n],diferencias.values[A_n],color=colores[7])  # ,s=0.1)

d_max = diferencias[diferencias.idxmax()]
d_min = diferencias[diferencias.idxmin()]

ax.scatter(n_block[diferencias.idxmax()], d_max,color=colores[9],s=300)
ax.scatter(n_block[diferencias.idxmax()], d_max,color=colores[8],s=100)
ax.scatter(n_block[diferencias.idxmax()], d_max,color='r',s=50)

ax.scatter(n_block[diferencias.idxmin()], d_min,color='w',s=300)
ax.scatter(n_block[diferencias.idxmin()], d_min,color=colores[8],s=100)
ax.scatter(n_block[diferencias.idxmin()], d_min,color='r',s=50)

mss = f'The ATH (All-Time High) for\nthe arrival time of a block\nwas {round(diferencias.max()/60,2)} hours ({round(diferencias.max()/(24*60),2)} day)\nin block {round(n_block[diferencias.idxmax()])}'
ax.text(200000,1400,mss, color=Estilos[tipo][0], ha='right', va='center',size=15)


mss = f"The ATL (All-Time Low) for\nthe block arrival time was\n{round(60*diferencias.min())} seconds in block {round(n_block[diferencias.idxmin()])}\ndue to timestamp issues"
ax.text(180000,-800,mss, color=Estilos[tipo][0], ha='right', va='center',size=15)


minutos = round(diferencias[420000:].mean(),2)
segundos = int((minutos-int(minutos)) * 60)  # Convertir la parte decimal a segundos

mss = f'The average block arrival time\nover the last two halvings is:\n'
mss2 = f'{int(minutos)} minutes and {segundos} seconds'
ax.text(650000,700,mss, color=Estilos[tipo][0], ha='right', va='center',size=18)
ax.text(650000,400,mss2, color=Estilos[tipo][0], ha='right', va='center',size=22)

minutos = round(diferencias.mean(),2)
segundos = int((minutos-int(minutos)) * 60) 

mss = f'And the total average\nblock arrival time\n'
mss2 = f'{int(minutos)} minutes\nand {segundos} seconds'
ax.text(850000,-200,mss, color=Estilos[tipo][0], ha='right', va='center',size=15)
ax.text(850000,-100,mss2, color=Estilos[tipo][0], ha='right', va='center',size=18)


if tipo[7:8] == 'd':
    tw1 = Image.open('bins/br_w.png')
else:
    tw1 = Image.open('bins/br_d.png')
tw1_resized = tw1.resize((int(tw1.width * 0.4), int(tw1.height * 0.4)))
tw1_array = np.array(tw1_resized)
    # Reduce el tamaño de la imagen a la mitad
fig.figimage(tw1_array, xo=2900, yo=1250, alpha=0.55, zorder=1)
plt.savefig('analisis/resultados/timestamp_'+tipo +
                '.png', bbox_inches='tight', pad_inches=0.75)
