# este script construye la gráfica histórica
# del tamaño de bloques en Bitcoin

# este script construye un gráfico de la evolución del tamaño de bloques
# a lo largo del cada bloque

# librerias a usar
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib import font_manager as fm, rcParams
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
from app.styles import Estilos, colores
from app.readata import leer_data,time_data,estado_data

# Cambiar la tipografia

current_dir = os.getcwd()
os.chdir(current_dir+'/BitcoinResearch/scripts/')


fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]


# #total = np.cumsum(size)s


def crear_imagen(tipo='estilo_dark'):
        # Color del fondo
    fig, ax = plt.subplots(figsize=(13,5), dpi=200)
<<<<<<< HEAD

=======
    
>>>>>>> dff2b37 (F_4AGO)
    fig.patch.set_facecolor(Estilos[tipo][1])
    ax.patch.set_facecolor(Estilos[tipo][1])

    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}
    plt.suptitle("  Bitcoin: Block Size\nHistory 2009-2023",fontsize=30,x=0.30,y=1.25,**preferencias)
    size,time = leer_data('size','time_b')
<<<<<<< HEAD
    size = np.array(size)/1000000
=======
    #numero_de_bloque,NTX=leer_data('n_block','ntx')

>>>>>>> dff2b37 (F_4AGO)
    time = time_data(time)
    
    ax.plot(time,size)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


    locator = mdates.MonthLocator(interval=17)
    formatter = mdates.DateFormatter('%B\n%Y')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(labelsize=13, rotation=30)
    ax.tick_params(axis='both',colors=Estilos[tipo][0])
    ax.set_ylabel('Size per Block', fontsize=20,**preferencias)

    ax.set_yticks([0,1,2,3,4])
    ytick_labels = ['0 MB', '1 MB', '2 MB', '3 MB', '4 MB']
    ax.set_yticklabels(ytick_labels,fontsize=15)

#    ax.set_yticklabels
    ax2 = ax.twinx()
    # Establecer límites del segundo eje Y
    ax2.set_yticks([0,1,2,3,4])

    last_block = leer_data('n_block')[-1]
    total_bd = 'Through Block '+str(round(last_block))+'\nthe total blockchain\nsize is '+str(round(leer_data('total')/1_000_000_000,2))+' GB\n'
    ytick_labels = ['','','','', total_bd]
    ax2.set_yticklabels(ytick_labels, fontsize=15,color=Estilos[tipo][0])
# ax2.set_ylabel('BTC', fontsize=15, color=tableau20[9])

    # for spine in ax.spines.values():
    #     spine.set_color(Estilos[tipo][0])

    for spine in ax2.spines.values():
        spine.set_color(Estilos[tipo][0])


    plt.savefig('analisis/resultados/1_block_size_'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)




<<<<<<< HEAD


crear_imagen('estilo_dark')
=======
crear_imagen('estilo_blanco')
>>>>>>> dff2b37 (F_4AGO)

# # plt.title(r"$\bf{BITCOIN:\ HISTORIAL\ DEL\ TAMAÑO\ DE\ BLOQUE}$" "\n" r"$\it{Comparación\ del\ size\ y\ strippedsize\ desde:\ bloque\ 1\ a\ }$" +
# #           f"{int(n_block[-1])}", fontsize=40, color=tableau20[6], fontproperties=prop)
# # plt.xlabel('Fecha de Confirmación del Bloque', fontsize=35,
# #            fontproperties=prop, color=tableau20[6])
# # plt.ylabel('Tamaño del Bloque', fontsize=35,
# #            fontproperties=prop, color=tableau20[6])
# # plt.gca().yaxis.grid(linestyle='-', linewidth=2, dashes=(5, 3))
# # plt.xlim(num_dates[0], num_dates[-1])
# # plt.ylim(0, 1.5*max(size))
# # ax.set_yticks([], [])
# # ax.set_xticks([], [])
# # ytick_labels = ['0 MB', '1 MB', '2 MB', '3 MB', '4 MB']
# # plt.yticks([0, 1000, 2000, 3000, 4000], ytick_labels,
# #            fontsize=20, fontproperties=prop, color=tableau20[6])


# # plt.plot_date(num_dates, size, ".", color=tableau20[0], markersize=0.3)
# # plt.plot_date(num_dates, strippedsize, ".", color=tableau20[2], markersize=0.3)

# # plt.plot_date(num_dates, total_b, "--", color=tableau20[10], linewidth=8)


# # plt.fill_between(num_dates, strippedsize,
# #                  facecolor=tableau20[2], alpha=0.7, label='StrippedSize')
# # plt.fill_between(num_dates, size, strippedsize,
# #                  facecolor=tableau20[0], alpha=0.7, label='Size')


# # plt.legend(loc='upper left', fontsize=20)


# # locator = mdates.MonthLocator(interval=11)
# # formatter = mdates.DateFormatter('%B\n%Y')
# # plt.gca().xaxis.set_major_locator(locator)
# # plt.gca().xaxis.set_major_formatter(formatter)
# # plt.gca().xaxis.set_tick_params(labelsize=10, rotation=20)
# # plt.tick_params(axis='x', colors=tableau20[6])

# # plt.axvline(datetime(2012, 11, 28), color="g", label="Min")
# # plt.text(datetime(2012, 12, 28), 4100, '1er Halv',
# #          fontsize=18, fontproperties=prop)
# # plt.axvline(datetime(2016, 7, 9), color="g", label="Min")
# # plt.text(datetime(2016, 8, 9), 4100, '2do Halv',
# #          fontsize=18, fontproperties=prop)
# # plt.axvline(datetime(2020, 5, 11), color="g", label="Min")
# # plt.text(datetime(2020, 6, 11), 4100, '3er Halv',
# #          fontsize=18, fontproperties=prop)

# # plt.annotate('Inicio\nSegWit', xy=(datetime(2017, 1, 24), 0), xytext=(datetime(
# #     2016, 1, 24), 300), fontsize=15, fontproperties=prop, arrowprops=dict(facecolor='red', shrink=0.10))


# # # anotando el acumulado del Blockchain
# # plt.text(datetime(2020, 6, 1), 4600, 'Peso de Bloques\n'+str(round(total[-1]/10000000000, 2))+' GB\nTotal: '+str(
# #     round(total_btc/10000000000, 2))+' GB', fontsize=22, fontproperties=prop, color=tableau20[10])


# # tw1 = mpimg.imread('/home/ghost/BitcoinResearch/scripts/pics/segwit.png')
# # imagebox = OffsetImage(tw1, zoom=0.45)
# # firma = AnnotationBbox(imagebox, (datetime(2011, 12, 8), 1200))
# # plt.gca().add_artist(firma)
# # plt.annotate('Presentación\nSegWit', xy=(datetime(2011, 12, 8), 0), xytext=(datetime(
# #     2010, 11, 1), 200), fontsize=15, fontproperties=prop, arrowprops=dict(facecolor='red', shrink=0.10))


# # tw2 = mpimg.imread('/home/ghost/BitcoinResearch/scripts/pics/ordinals.png')
# # imagebox = OffsetImage(tw2, zoom=0.175)
# # firma2 = AnnotationBbox(imagebox, (datetime(2020, 10, 7), 2600))
# # plt.gca().add_artist(firma2)
# # plt.annotate('Primer\nOrdinal', xy=(datetime(2021, 10, 7), 0), xytext=(datetime(
# #     2020, 10, 8), 300), fontsize=15, fontproperties=prop, arrowprops=dict(facecolor='red', shrink=0.10))

# # tw3 = mpimg.imread('/home/ghost/BitcoinResearch/scripts/pics/satoshi.png')
# # imagebox = OffsetImage(tw3, zoom=0.08)
# # firma3 = AnnotationBbox(imagebox, (datetime(2009, 6, 1), 250))
# # plt.gca().add_artist(firma3)
# # plt.annotate('Lanzamiento de\nBitcoin\n9 de enero de 2009 ', xy=(datetime(2009, 2, 3), 0), xytext=(
# #     datetime(2009, 2, 3), 600), fontsize=15, fontproperties=prop, arrowprops=dict(facecolor='red', shrink=0.10))


# # plt.xticks(fontsize=20, fontproperties=prop)


# # ax2 = ax.twinx()

# # # Establecer límites del segundo eje Y
# # ax2.set_ylim(0, 1.5*max(size))
# # ax2.set_yticks([0, 1000, 2000, 3000, 4000])
# # ytick_labels = ['0 GB', '1 GB', '2 GB', '3 GB', '4 GB']
# # ax2.set_yticklabels(ytick_labels, fontsize=20,
# #                     fontproperties=prop, color=tableau20[6])
# # ax2.set_ylabel('\nTamaño acumulado', fontsize=30,
# #                fontproperties=prop, color=tableau20[6])


# # plt.savefig('/home/ghost/BitcoinResearch/scripts/pics/blocksize.png', bbox_inches='tight')


# # print('hola mundio')
