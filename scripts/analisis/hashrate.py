'''
Este script calcula y muestra el hashrate de la red Bitcoin

El hashrate es una variable que indica la potencia de trabajo de la red Bitcoin
La potencia de trabajo es la cantidad de hashes que se pueden realizar en un segundo
y depende del poder de hash de cada minero que esta en la red.

Este valor no se puede conocer con precision pues depende de factores externos 
a la red como el precio de la energia, la cantidad de hashpower de cada minero 
y maquina, etc.

sin embargo se puede inferir este valor a partir del trabajo de la red 
y el tiempo de llegada de cada bloque.

'''

# importamos librerias a usar

import numpy as np
import pandas as pd
import os
from app.readata import leer_data, time_data, last_block
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from PIL import Image
from datetime import datetime
from app.styles import Estilos, colores


# tomamos los valores de la red
chainw, timestamp = leer_data('chainwork','time_b')

# procesamos los datos del tiempo para obtener en segundos 
time = time_data(timestamp[1:])
time_block = pd.Series(pd.to_datetime(timestamp)).diff().dt.total_seconds().dropna().replace(0, 1)

window=4*2016
chainwork = pd.Series([int(a,16) for a in chainw]).diff().dropna()

hashrate  = pd.Series([(chainwork[a]/1e18)/time_block[a] for a in range(1,len(time_block)+1)])
hashrate_smoothed = hashrate.rolling(window).median().fillna(np.mean(hashrate[:window]))


# Cambiar la tipografia
fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fpatht = os.path.join('bins/BigBlueTerm437NerdFont-Regular.ttf')
title = fm.FontProperties(fname=fpatht)
fname = os.path.split(fpath)[1]

def crear_imagen_total(tipo='estilo_dark'):
        # Color del fondo
    fig, ax = plt.subplots(1,2,figsize=(20,5), dpi=200)
    fig.patch.set_facecolor(Estilos[tipo][1])
    ax[0].patch.set_facecolor(Estilos[tipo][1])
    ax[1].patch.set_facecolor(Estilos[tipo][1])

    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}

    plt.suptitle("Bitcoin\n  Hashrate",fontsize=50,y=1.5,x=0.15,fontproperties=title,color=Estilos[tipo][0])


    ax[0].plot(time,hashrate_smoothed,color=colores[1],zorder=1,linewidth=7)
    ax[0].plot(time,hashrate_smoothed,color=colores[2],zorder=1,linewidth=2)
    ax[0].plot(time,hashrate_smoothed,color=colores[3],zorder=1,linewidth=0.5)
    


    #ax[0].set_yscale('log')
    locator = mdates.MonthLocator(interval=23)
    formatter = mdates.DateFormatter('%b\n%Y')
    ax[0].xaxis.set_major_locator(locator)
    ax[0].xaxis.set_major_formatter(formatter)
    ax[0].xaxis.set_tick_params(labelsize=15, rotation=30,length=5,width=3)
    ax[0].tick_params(axis='both',colors=Estilos[tipo][0])
    ax[0].set_ylabel('Hashrate\n', fontsize=25,**preferencias)
    ax[0].set_title("Scale:'linear'",loc='right',fontsize=12,color='white')
    
    ax[0].axhline(hashrate_smoothed.max(),linestyle='dashed',color='red',linewidth=2)
    ax[1].axhline(1e18*hashrate_smoothed.max(),linestyle='dashed',color='red',linewidth=1)

    ax[0].axhline(hashrate_smoothed.iloc[-1],linestyle='dashed',color='green',linewidth=2)
    ax[1].axhline(1e18*hashrate_smoothed.iloc[-1],linestyle='dashed',color='green',linewidth=1.5)


    ax[1].plot(time,hashrate_smoothed*1e18,color=colores[1],zorder=1,linewidth=7)
    ax[1].plot(time,hashrate_smoothed*1e18,color=colores[2],zorder=1,linewidth=2)
    ax[1].plot(time,hashrate_smoothed*1e18,color=colores[3],zorder=1,linewidth=0.5)
    


    ax[1].set_yscale('log')
    locator = mdates.MonthLocator(interval=23)
    formatter = mdates.DateFormatter('%b\n%Y')
    ax[1].xaxis.set_major_locator(locator)
    ax[1].xaxis.set_major_formatter(formatter)
    ax[1].xaxis.set_tick_params(labelsize=15, rotation=30,length=5,width=3)
    ax[1].tick_params(axis='both',colors=Estilos[tipo][0])
    ax[1].set_ylabel('Hashrate\n', fontsize=25,**preferencias)

    ax[1].set_title("Scale:'logy'",loc='right',fontsize=15,color='white')
       
    ax[0].set_yticks([0,1e2,2e2,3e2,4e2,5e2])
    ytick_labels = ['0 EH\\s','100 EH\\s','200 EH\\s','300 EH\\s','400 EH\\s','500 EH\\s']
    ax[0].set_yticklabels(ytick_labels,rotation=23,**preferencias)
    ax[0].yaxis.set_tick_params(labelsize=15)
    ax[0].tick_params(axis='y',labelsize=15,rotation=25)  # Cambia 20 al tamaño que prefieras
       

    ax[1].yaxis.set_tick_params(labelsize=23,rotation=20)
    ax[1].tick_params(axis='y',labelsize=15,rotation=20)  # Cambia 20 al tamaño que prefieras

    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)

    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)

    plt.subplots_adjust(wspace=2, hspace=1)


    for spine in ax[0].spines.values():
        spine.set_color(Estilos[tipo][0])
    for spine in ax[1].spines.values():
        spine.set_color(Estilos[tipo][0])

    if tipo[7:8]=='d':
        tw1 = Image.open('bins/br_w.png')
    else:
        tw1 = Image.open('bins/br_d.png')


    tw1_resized = tw1.resize((int(tw1.width * 0.4), int(tw1.height * 0.4)))  # Reduce el tamaño de la imagen a la mitad
# Convierte la imagen de PIL a una matriz de numpy para que matplotlib pueda trabajar con ella
    tw1_array = np.array(tw1_resized)

    date = datetime(2021,5,21)
    x_value = mdates.date2num(date) 
    ax[0].scatter(x_value,350,s=100,color=colores[3])
    ax[0].vlines(x_value,-10,350,colors=Estilos[tipo][0], linestyles='dashed')
    
    date = datetime(2020,5,21)
    x_value = mdates.date2num(date)
    mss = 'China ban\nBitcoin mining' 
    ax[0].text(x_value,400, mss, color=Estilos[tipo][0], ha='right', va='center',size=18)
    
    date = datetime(2023,10,1)
    x_value = mdates.date2num(date)
    mss = f'The Hashrate is estimated\nbased on variables such as\ndifficulty and chainwork.\n\nAs of block {round(last_block())} the \nvalue of chainwork is\n' 
    mss2= r'$2.39\times10^{23}$'+' Hashes'
    ax[1].text(x_value,1e12,mss+mss2, color=Estilos[tipo][0], ha='right', va='center',size=18)


 

# Usa el índice para obtener la fecha correspondiente
    fecha_datetime = datetime.strptime(timestamp[np.argmax(hashrate)][:10],'%Y-%m-%d')
    formatted_date = fecha_datetime.strftime('%d of %B %Y')
    mss1 = '*Up to block ' + str(last_block())+'\nthe All-Time High\nwas '
    mss2 = str(round(hashrate_smoothed.max(),2))+' TH/s on\n'+str(formatted_date)

    fig.text(0.5,1.15,mss1+mss2, ha='center', va='center', fontsize=20,**preferencias)

    fig.figimage(tw1_array, xo=2800, yo=1200, alpha=0.55, zorder=1)
    plt.subplots_adjust(wspace=0.25)
    plt.savefig('analisis/resultados/hashrate_'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)

crear_imagen_total('estilo_dark')
