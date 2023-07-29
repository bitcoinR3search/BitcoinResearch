
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
import locale
#locale.setlocale(locale.LC_TIME, 'es')


fpath = os.path.join(r'/home/ghost/BitcoinResearch/scripts/bins/MonoLisaSimpson-Regular.ttf')
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

aux = np.load('/home/ghost/BitcoinResearch/scripts/bins/database.npz', allow_pickle='TRUE')
n_block = aux['n_block']
time_b = aux['time_b']
size = aux['size']
ntx = aux['ntx']
bits = aux['bits']
chainwork = aux['chainwork']
strippedsize = aux['strippedsize']
weight = aux['weight']
total_btc = aux['total']
# Las fechas tienen un tratamiento especial.
# la mejor forma de hacerlo es pasarlos como objetos
# que matplot interpreta como fechas.

time_b = pd.to_datetime(time_b)  # time_b es un array con fechas en str
# las convertimos a datetime y solo guardamos la fecha (no la hora)
time_b = time_b.date

# un nuevo array contendra los valores para q matplotlib maneje fechas.
# estos valores son números. No se rescatan.
num_dates = mdates.date2num(time_b)


# para la grafica del total acumulado

total = np.cumsum(size)


# La gráfica deberia reunir a todos los puntos.
# sin embargo para facilidad tomamos el primero valor
# de cada corrección de dificultad

num_dates = num_dates[::2016]
# se dividen enter mil para mostrar el dato en KB
size = size[::2016]/1000
strippedsize = strippedsize[::2016]/1000
total_b = total[::2016]/100_000_000


# GENERANDO LA IMAGEN

fig, ax = plt.subplots(figsize=(66, 11), dpi=300)

# Color del fondo
fig.patch.set_facecolor(tableau20[4])
plt.axes().patch.set_facecolor(tableau20[5])

plt.title(r"$\bf{BITCOIN:\ HISTORIAL\ DEL\ TAMAÑO\ DE\ BLOQUE}$" "\n" r"$\it{Comparación\ del\ size\ y\ strippedsize\ desde:\ bloque\ 1\ a\ }$" +
          f"{int(n_block[-1])}", fontsize=40, color=tableau20[6], fontproperties=prop)
plt.xlabel('Fecha de Confirmación del Bloque', fontsize=35,
           fontproperties=prop, color=tableau20[6])
plt.ylabel('Tamaño del Bloque', fontsize=35,
           fontproperties=prop, color=tableau20[6])
plt.gca().yaxis.grid(linestyle='-', linewidth=2, dashes=(5, 3))
plt.xlim(num_dates[0], num_dates[-1])
plt.ylim(0, 1.5*max(size))
ax.set_yticks([], [])
ax.set_xticks([], [])
ytick_labels = ['0 MB', '1 MB', '2 MB', '3 MB', '4 MB']
plt.yticks([0, 1000, 2000, 3000, 4000], ytick_labels,
           fontsize=20, fontproperties=prop, color=tableau20[6])


plt.plot_date(num_dates, size, ".", color=tableau20[0], markersize=0.3)
plt.plot_date(num_dates, strippedsize, ".", color=tableau20[2], markersize=0.3)

plt.plot_date(num_dates, total_b, "--", color=tableau20[10], linewidth=8)


plt.fill_between(num_dates, strippedsize,
                 facecolor=tableau20[2], alpha=0.7, label='StrippedSize')
plt.fill_between(num_dates, size, strippedsize,
                 facecolor=tableau20[0], alpha=0.7, label='Size')


plt.legend(loc='upper left', fontsize=20)


locator = mdates.MonthLocator(interval=11)
formatter = mdates.DateFormatter('%B\n%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_tick_params(labelsize=10, rotation=20)
plt.tick_params(axis='x', colors=tableau20[6])

plt.axvline(datetime(2012, 11, 28), color="g", label="Min")
plt.text(datetime(2012, 12, 28), 4100, '1er Halv',
         fontsize=18, fontproperties=prop)
plt.axvline(datetime(2016, 7, 9), color="g", label="Min")
plt.text(datetime(2016, 8, 9), 4100, '2do Halv',
         fontsize=18, fontproperties=prop)
plt.axvline(datetime(2020, 5, 11), color="g", label="Min")
plt.text(datetime(2020, 6, 11), 4100, '3er Halv',
         fontsize=18, fontproperties=prop)

plt.annotate('Inicio\nSegWit', xy=(datetime(2017, 1, 24), 0), xytext=(datetime(
    2016, 1, 24), 300), fontsize=15, fontproperties=prop, arrowprops=dict(facecolor='red', shrink=0.10))


# anotando el acumulado del Blockchain
plt.text(datetime(2020, 6, 1), 4600, 'Peso de Bloques\n'+str(round(total[-1]/10000000000, 2))+' GB\nTotal: '+str(
    round(total_btc/10000000000, 2))+' GB', fontsize=22, fontproperties=prop, color=tableau20[10])


tw1 = mpimg.imread('/home/ghost/BitcoinResearch/scripts/pics/segwit.png')
imagebox = OffsetImage(tw1, zoom=0.45)
firma = AnnotationBbox(imagebox, (datetime(2011, 12, 8), 1200))
plt.gca().add_artist(firma)
plt.annotate('Presentación\nSegWit', xy=(datetime(2011, 12, 8), 0), xytext=(datetime(
    2010, 11, 1), 200), fontsize=15, fontproperties=prop, arrowprops=dict(facecolor='red', shrink=0.10))


tw2 = mpimg.imread('/home/ghost/BitcoinResearch/scripts/pics/ordinals.png')
imagebox = OffsetImage(tw2, zoom=0.175)
firma2 = AnnotationBbox(imagebox, (datetime(2020, 10, 7), 2600))
plt.gca().add_artist(firma2)
plt.annotate('Primer\nOrdinal', xy=(datetime(2021, 10, 7), 0), xytext=(datetime(
    2020, 10, 8), 300), fontsize=15, fontproperties=prop, arrowprops=dict(facecolor='red', shrink=0.10))

tw3 = mpimg.imread('/home/ghost/BitcoinResearch/scripts/pics/satoshi.png')
imagebox = OffsetImage(tw3, zoom=0.08)
firma3 = AnnotationBbox(imagebox, (datetime(2009, 6, 1), 250))
plt.gca().add_artist(firma3)
plt.annotate('Lanzamiento de\nBitcoin\n9 de enero de 2009 ', xy=(datetime(2009, 2, 3), 0), xytext=(
    datetime(2009, 2, 3), 600), fontsize=15, fontproperties=prop, arrowprops=dict(facecolor='red', shrink=0.10))


plt.xticks(fontsize=20, fontproperties=prop)


ax2 = ax.twinx()

# Establecer límites del segundo eje Y
ax2.set_ylim(0, 1.5*max(size))
ax2.set_yticks([0, 1000, 2000, 3000, 4000])
ytick_labels = ['0 GB', '1 GB', '2 GB', '3 GB', '4 GB']
ax2.set_yticklabels(ytick_labels, fontsize=20,
                    fontproperties=prop, color=tableau20[6])
ax2.set_ylabel('\nTamaño acumulado', fontsize=30,
               fontproperties=prop, color=tableau20[6])


plt.savefig('/home/ghost/BitcoinResearch/scripts/pics/blocksize.png', bbox_inches='tight')


print('hola mundio')
