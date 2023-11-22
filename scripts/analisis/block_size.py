# este script construye la gráfica histórica
# del tamaño de bloques en Bitcoin

# este script construye un gráfico de la evolución del tamaño de bloques
# a lo largo del cada bloque

# librerias a usar
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from PIL import Image
from app.styles import Estilos, colores
from app.readata import leer_data, time_data
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Cambiar la tipografia
fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fpatht = os.path.join('bins/BigBlueTerm437NerdFont-Regular.ttf')
title = fm.FontProperties(fname=fpatht)
fname = os.path.split(fpath)[1]


def crear_imagen(tipo='estilo_dark'):
    # Color del fondo
    fig, ax = plt.subplots(figsize=(13, 5), dpi=200)
    fig.patch.set_facecolor(Estilos[tipo][1])
    ax.patch.set_facecolor(Estilos[tipo][1])

    preferencias = {'color': Estilos[tipo][0], 'fontproperties': prop}
    # plt.suptitle("Bitcoin Block Size\nHistory 2009-2023", fontsize=40,
    #              x=0.2, y=1.3, fontproperties=title, color=Estilos[tipo][0])
    size, time = leer_data('size', 'time_b')
    size = np.array(size)/1000000

    time = time_data(time)
    total = np.cumsum(size)

    ax.axhline(1, color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.axhline(4, color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ##
    ax.plot(time, size, color=colores[10])
    ##
    #ax.plot(time, total/100000, '-', color=colores[6], linewidth=5)
    ax.plot(time, total/100000, '-', color=colores[3], linewidth=2.5)
    #ax.plot(time, total/100000, '-', color=colores[0], linewidth=.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    #locator = mdates.MonthLocator(interval=10)
    #formatter = mdates.DateFormatter('%B\ndel %Y')
    
    locator = mdates.MonthLocator(interval=17)
    formatter = mdates.DateFormatter('%b\n%Y')

    formatter.locale = locale.getlocale()

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(labelsize=15, rotation=30)
    ax.tick_params(axis='both', colors=Estilos[tipo][0])
    ax.set_ylabel('Tamaño por bloque\n', fontsize=20, **preferencias)
    ax.set_xlabel('Fecha\n', fontsize=20, **preferencias)
    ax.set_yticks([0, 1, 2, 3, 4])
    ytick_labels = ['0 MB', '1 MB', '2 MB', '3 MB', '4 MB']
    ax.set_yticklabels(ytick_labels, fontsize=18)
    ax.tick_params(axis='both', length=5, width=3)

    date = datetime(2017, 7, 24)
    x_value = mdates.date2num(date)
    #ax.scatter(x_value, 2.5, s=350, color=colores[3])
    ax.scatter(x_value, 2.5, s=100, color=colores[1])
    #ax.scatter(x_value, 2.5, s=5, color=colores[5])
    ax.vlines(x_value, 0, 2.275, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2017, 1, 24)
    x_value = mdates.date2num(date)
    ax.text(x_value, 3.2, 'Segwit\nactivado en el \nBloque 481824',
            color=Estilos[tipo][0], ha='right', va='center', size=18)

    date = datetime(2022, 12, 14)
    x_value = mdates.date2num(date)
    #ax.scatter(x_value, 5.5, s=350, color=colores[3])
    ax.scatter(x_value, 5.5, s=100, color=colores[1])
    #ax.scatter(x_value, 5.5, s=5, color=colores[5])
    ax.vlines(x_value, 0, 5.28, colors=Estilos[tipo][0], linestyles='dashed')
    ax.text(x_value, 6.25, 'Ordinals\nBRC-20',
            color=Estilos[tipo][0], ha='right', va='center', size=18)

    date = datetime(2021, 11, 14)
    x_value = mdates.date2num(date)
    #ax.scatter(x_value, 4.5, s=350, color=colores[3])
    ax.scatter(x_value, 4.5, s=100, color=colores[1])
    #ax.scatter(x_value, 4.5, s=5, color=colores[5])
    ax.vlines(x_value, 0, 4.25, colors=Estilos[tipo][0], linestyles='dashed')

    date = datetime(2021, 3, 1)
    x_value = mdates.date2num(date)
    ax.text(x_value, 5, 'Taproot\nactivo en el\nBloque 709632',
            color=Estilos[tipo][0], ha='right', va='center', size=18)

    date = datetime(2010, 5, 22)
    x_value = mdates.date2num(date)
    #ax.scatter(x_value, 1.5, s=350, color=colores[3])
    ax.scatter(x_value, 1.5, s=100, color=colores[1])
    #ax.scatter(x_value, 1.5, s=5, color=colores[5])
    ax.vlines(x_value, 0, 1.28, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2011, 1, 22)
    x_value = mdates.date2num(date)
    ax.text(x_value, 2.25, 'Bitcoin\nDía de Pizza',
            color=Estilos[tipo][0], ha='right', va='center', size=18)


# ax.set_yticklabels
    #ax2 = ax.twinx()
    # Establecer límites del segundo eje Y
    #ax2.set_yticks([0, 1, 2, 3, 4])

    #last_block = leer_data('n_block')[-1]
    # total_bd = 'Through Block '+str(round(last_block))+'\nthe total blockchain\nsize is '+str(
    #     round(leer_data('total')/1_000_000_000, 2))+' GB\n'
    #ytick_labels = ['', '', '', '', total_bd]
    #ax2.set_yticklabels(ytick_labels, fontsize=18, color=Estilos[tipo][0])

    # for spine in ax2.spines.values():
    #     spine.set_color(Estilos[tipo][0])

#     if tipo[7:8] == 'd':
#         tw1 = Image.open('bins/br_w.png')
#     else:
#         tw1 = Image.open('bins/br_d.png')

#     # Reduce el tamaño de la imagen a la mitad
#     tw1_resized = tw1.resize((int(tw1.width * 0.4), int(tw1.height * 0.4)))

# # Convierte la imagen de PIL a una matriz de numpy para que matplotlib pueda trabajar con ella
#     tw1_array = np.array(tw1_resized)

    # ax2.spines['top'].set_visible(False)
    # ax2.spines['right'].set_visible(False)
    # ax2.tick_params(axis='y', length=0)
# Añade la imagen a la figura
    #fig.figimage(tw1_array, xo=2600, yo=1100, alpha=0.55, zorder=1)
    plt.savefig('analisis/resultados/blocksize_'+tipo +
                '.png', bbox_inches='tight', pad_inches=0.75)


#crear_imagen('estilo_dark')
crear_imagen('estilo_blanco')
# for a in Estilos.keys():
#     crear_imagen(a)
