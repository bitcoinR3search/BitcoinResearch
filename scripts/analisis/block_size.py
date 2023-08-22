# este script construye la gráfica histórica
# del tamaño de bloques en Bitcoin

# este script construye un gráfico de la evolución del tamaño de bloques
# a lo largo del cada bloque

# librerias a usar
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib import font_manager as fm
from PIL import Image
from datetime import datetime
from app.styles import Estilos, colores
from app.readata import leer_data,time_data,estado_data
from app.readata import leer_data,time_data,estado_data

# Cambiar la tipografia
fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]




def crear_imagen(tipo='estilo_dark'):
        # Color del fondo
    fig, ax = plt.subplots(figsize=(13,5), dpi=200)
    fig.patch.set_facecolor(Estilos[tipo][1])
    ax.patch.set_facecolor(Estilos[tipo][1])

    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}
    plt.suptitle("  Bitcoin: Block Size\nHistory 2009-2023",fontsize=35,x=0.20,y=1.23,**preferencias)
    size,time = leer_data('size','time_b')
    size = np.array(size)/1000000

    time = time_data(time)
    total = np.cumsum(size)

    ax.axhline(1, color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.axhline(4, color=Estilos[tipo][0], linestyle='dashed', linewidth=1)


    ax.plot(time,size,color=colores[3])
    ax.plot(time,total/100000,'-',color=colores[6],linewidth=3.5)
    ax.plot(time,total/100000,'-',color=colores[5],linewidth=2)
    ax.plot(time,total/100000,'-',color=colores[0],linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


    locator = mdates.MonthLocator(interval=17)
    formatter = mdates.DateFormatter('%B\n%Y')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(labelsize=15, rotation=30)
    ax.tick_params(axis='both',colors=Estilos[tipo][0])
    ax.set_ylabel('Size per Block\n', fontsize=23,**preferencias)
    ax.set_yticks([0,1,2,3,4])
    ytick_labels = ['0 MB', '1 MB', '2 MB', '3 MB', '4 MB']
    ax.set_yticklabels(ytick_labels,fontsize=15)
    ax.tick_params(axis='both', length=5,width=3)

    date = datetime(2017, 7, 24)
    x_value = mdates.date2num(date) 
    ax.scatter(x_value,2.5,s=350,color=colores[3])
    ax.scatter(x_value,2.5,s=100,color=colores[4])
    ax.scatter(x_value,2.5,s=5,color=colores[0])
    ax.vlines(x_value,0,2.275, colors=Estilos[tipo][0], linestyles='dashed')
    ax.text(x_value,3.3, 'Segwit\nactivate in\nBlock 481824', color=Estilos[tipo][0], ha='right', va='center',size=15)



    date = datetime(2022, 12, 14)
    x_value = mdates.date2num(date) 
    ax.scatter(x_value,5.5,s=350,color=colores[3])
    ax.scatter(x_value,5.5,s=100,color=colores[4])
    ax.scatter(x_value,5.5,s=5,color=colores[0])
    ax.vlines(x_value,0,5.28, colors=Estilos[tipo][0], linestyles='dashed')
    ax.text(x_value,6.2, 'Ordinals\nBRC-20', color=Estilos[tipo][0], ha='right', va='center',size=15)


    date = datetime(2021, 11, 14)
    x_value = mdates.date2num(date) 
    ax.scatter(x_value,4.5,s=350,color=colores[3])
    ax.scatter(x_value,4.5,s=100,color=colores[4])
    ax.scatter(x_value,4.5,s=5,color=colores[0])
    ax.vlines(x_value,0,4.25, colors=Estilos[tipo][0], linestyles='dashed')
    
    date = datetime(2021, 8, 1)
    x_value = mdates.date2num(date) 
    ax.text(x_value,5, 'Taproot\nactivate in\nBlock 709632', color=Estilos[tipo][0], ha='right', va='center',size=15)

    date = datetime(2010, 5, 22)
    x_value = mdates.date2num(date) 
    ax.scatter(x_value,1.5,s=350,color=colores[3])
    ax.scatter(x_value,1.5,s=100,color=colores[4])
    ax.scatter(x_value,1.5,s=5,color=colores[0])
    ax.vlines(x_value,0,1.28, colors=Estilos[tipo][0], linestyles='dashed')
    ax.text(x_value,2.2,'Bitcoin\nPizza Day', color=Estilos[tipo][0], ha='right', va='center',size=15)
    



# ax.set_yticklabels
    ax2 = ax.twinx()
    # Establecer límites del segundo eje Y
    ax2.set_yticks([0,1,2,3,4])

    last_block = leer_data('n_block')[-1]
    total_bd = 'Through Block '+str(round(last_block))+'\nthe total blockchain\nsize is '+str(round(leer_data('total')/1_000_000_000,2))+' GB\n'
    ytick_labels = ['','','','',total_bd]
    ax2.set_yticklabels(ytick_labels, fontsize=15,color=Estilos[tipo][0])

    for spine in ax2.spines.values():
        spine.set_color(Estilos[tipo][0])

    if tipo[7:8]=='d':
        tw1 = Image.open('bins/br_w.png')
    else:
        tw1 = Image.open('bins/br_d.png')


    tw1_resized = tw1.resize((int(tw1.width * 0.5), int(tw1.height * 0.5)))  # Reduce el tamaño de la imagen a la mitad

# Convierte la imagen de PIL a una matriz de numpy para que matplotlib pueda trabajar con ella
    tw1_array = np.array(tw1_resized)


    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.tick_params(axis='y', length=0)
# Añade la imagen a la figura
    fig.figimage(tw1_array, xo=2400, yo=1000, alpha=0.55, zorder=1)
    plt.savefig('analisis/resultados/block_size_'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)


for a in Estilos.keys():
    crear_imagen(a)
