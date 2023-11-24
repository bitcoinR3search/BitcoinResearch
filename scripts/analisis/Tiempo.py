    
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


<<<<<<< HEAD
tipo = 'estilo_blanco'
=======
def crear_imagen_total(tipo='estilo_dark'):
    fig, ax = plt.subplots(figsize=(20, 5), dpi=200)
    preferencias = {'color': Estilos[tipo][0], 'fontproperties': prop}
    plt.suptitle("Registro\nTemporal", fontsize=35, x=0.20, y=1.23, **preferencias)
    time_b = leer_data('time_b')
>>>>>>> 682a4ed (Estilos_blancos)

fig, ax = plt.subplots(figsize=(20, 5), dpi=200)

fig.patch.set_facecolor(Estilos[tipo][1])
ax.patch.set_facecolor(Estilos[tipo][1])
preferencias = {'color': Estilos[tipo][0], 'fontproperties': prop}

#plt.suptitle("Timestamp of Bitcoin\nBlock Arrivals",fontsize=45,x=0.25,y=1.4,fontproperties=title,color=Estilos[tipo][0])
time,n_block = leer_data('time_b','n_block')
n_block=n_block[1:]
#time_b = time_data(time)[1:]
diferencias = pd.Series(pd.to_datetime(time)).diff().dt.total_seconds().dropna()/60

A_p = np.where(diferencias.values >= 0)[0]
A_n = np.where(diferencias.values < 0)[0]
A_p = A_p[1:]
A_n = A_n[1:]

<<<<<<< HEAD
d_max = diferencias[diferencias.idxmax()]
d_min = diferencias[diferencias.idxmin()]

ax.xaxis.set_tick_params(labelsize=18, rotation=20,color='black')
ax.yaxis.set_tick_params(labelsize=13, rotation=10,color='black')
ax.tick_params(axis='both', labelcolor='black')

ax.axvline(n_block[210000*1],ymax=.5, color=Estilos[tipo][0], linestyle='--', linewidth=1)
ax.text(n_block[210000*1+50000],-400, '1er\nHalv', ha='right', va='center', size=18,**preferencias)
ax.axvline(n_block[210000*2],ymax=.5,linestyle='--', linewidth=1,color=Estilos[tipo][0])
ax.text(n_block[210000*2+50000],-400, '2do\nHalv',ha='right', va='center', size=18,**preferencias)
ax.axvline(n_block[210000*3],ymax=.5,color=Estilos[tipo][0], linestyle='--', linewidth=1)
ax.text(n_block[210000*3+50000],-400, '3er\nHalv', ha='right', va='center', size=18,**preferencias)

ax.axhline(0,color=Estilos[tipo][0],linewidth=1.5,zorder=3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.spines['bottom'].set_visible(False)

for spine in ax.spines.values():
    spine.set_color(Estilos[tipo][0])


ax.set_ylabel('Tiempo de Llegada de Bloques [min]',fontsize=18,**preferencias)
ax.set_xlabel('\n# Bloque',fontsize=18,**preferencias)
ax.set_ylim(-1400, 1600)
ax.set_yticks(range(-200, 1601, 400)) 

ax.plot(n_block[A_p],diferencias.values[A_p],color=colores[10])
ax.plot(n_block[A_n],diferencias.values[A_n],color=colores[12])  # ,s=0.1)

d_max = diferencias[diferencias.idxmax()]
d_min = diferencias[diferencias.idxmin()]

#ax.scatter(n_block[diferencias.idxmax()], d_max,color=colores[9],s=300)
#ax.scatter(n_block[diferencias.idxmax()], d_max,color=colores[8],s=100)
ax.scatter(n_block[diferencias.idxmax()], d_max,color='black',s=50)

#ax.scatter(n_block[diferencias.idxmin()], d_min,color='w',s=300)
#ax.scatter(n_block[diferencias.idxmin()], d_min,color=colores[8],s=100)
ax.scatter(n_block[diferencias.idxmin()], d_min,color='black',s=50)

# mss = f'Máximo Historico para\nel tiempo de llegada de un bloque\nfue {round(diferencias.max()/60,2)} horas ({round(diferencias.max()/(24*60),2)} día)\nen el bloque {round(n_block[diferencias.idxmax()])}'
# ax.text(200000,1400,mss, color=Estilos[tipo][0], ha='right', va='center',size=15)


# mss = f"Mínimo\nhistorico del tiempo de llegada de un bloque fue\n{round(60*diferencias.min())} segundos en el bloque {round(n_block[diferencias.idxmin()])}\ndebido a problemas en los registros de tiempo"
# ax.text(180000,-800,mss, color=Estilos[tipo][0], ha='right', va='center',size=15)


minutos = round(diferencias[420000:].mean(),2)
segundos = int((minutos-int(minutos)) * 60)  # Convertir la parte decimal a segundos

# mss = f'El tiempo promedio de llegada de un bloque\nsobre los ultimos dos halvins es:\n'
# mss2 = f'{int(minutos)} minutos y {segundos} segundos'
# ax.text(650000,700,mss, color=Estilos[tipo][0], ha='right', va='center',size=18)
# ax.text(650000,400,mss2, color=Estilos[tipo][0], ha='right', va='center',size=22)


# if tipo[7:8] == 'd':
#     tw1 = Image.open('bins/br_w.png')
# else:
#     tw1 = Image.open('bins/br_d.png')
# tw1_resized = tw1.resize((int(tw1.width * 0.4), int(tw1.height * 0.4)))
# tw1_array = np.array(tw1_resized)
    # Reduce el tamaño de la imagen a la mitad
#fig.figimage(tw1_array, xo=2900, yo=1250, alpha=0.55, zorder=1)
plt.savefig('analisis/resultados/timestamp_'+tipo +
                '.png', bbox_inches='tight', pad_inches=0.75)
=======
    # fig, ax = plt.subplots()
#balbalabalblablalbasdasd
    # Configurar los ejes x
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(labelsize=10, rotation=20, color='black')
    ax.tick_params(axis='both', labelcolor='black')

    # Dibujar las líneas horizontales
    # ax.axhline(10, color='black')
    # ax.axhline(np.mean(d), color='g')
    # ============maximos======
    ax.axvline(num_dates[210000*1], color=Estilos[tipo]
               [0], linestyle='--', linewidth=1)
    # date = datetime(2012,11, 28)
    # x_value = mdates.date2num(date)
    ax.text(num_dates[210000*1], 1450, '1er Halving',
            color=Estilos[tipo][0], ha='right', va='center', size=15)
    ##
    ax.axvline(num_dates[210000*2], color=Estilos[tipo]
               [0], linestyle='--', linewidth=1)
    # date = datetime(2016,7, 9)
    # x_value = mdates.date2num(date)
    ax.text(num_dates[210000*2], 1450, '2do Halving',
            color=Estilos[tipo][0], ha='right', va='center', size=15)
    ##
    ax.axvline(num_dates[210000*3], color=Estilos[tipo]
               [0], linestyle='--', linewidth=1)
    # date = datetime(2020,5, 11)
    # x_value = mdates.date2num(date)
    ax.text(num_dates[210000*3], 1450, '3er Halving',
            color=Estilos[tipo][0], ha='right', va='center', size=15)
    # =====
    indice = np.where((d == np.max(d)))[0][0]
    d_max = d[indice]

    # ============minimos=====
    indice2 = np.where((d == np.min(d)))[0][0]
    d_min = d[indice2]
    # print(d_min)
    # Dibujar los puntos
    ax.plot(num_dates, d, label="Datos sin anomalias", color=colores[12])

#     ax.scatter(num_dates[indice], d_max,
#                color=colores[9], label='Máximo', s=100)
    ax.scatter(num_dates[indice], d_max,
               color=colores[1], label='Máximo', s=40)
    #ax.scatter(num_dates[indice], d_max, color='r', label='Máximo', s=10)

    ax.scatter(num_dates[indice2], d_min,
               color=colores[1], label='Minimo', s=40)
#     ax.scatter(num_dates[indice2], d_min,
#                color=colores[8], label='Minimo', s=40)
#     ax.scatter(num_dates[indice2], d_min, color='red', label='Minimo', s=10)

    # ax.scatter(num_dates[indice2], d_min, color ='red',label='Minimo', s=10)
    # =========anomalias=======
    ax.plot(num_dates[:len(A_N)], A_N, label="Anomalias",
            color=colores[10])  # ,s=0.1)

    # Color del fondo dentro la grafica

    # fig.set_facecolor('gray')
    #tw1 = Image.open('bins/br_w.png')
    #tw1_resized = tw1.resize((int(tw1.width * 0.5), int(tw1.height * 0.5)))
    #tw1_array = np.array(tw1_resized)
    #fig.figimage(tw1_array, xo=2300, yo=850, alpha=0.55, zorder=1)
    plt.subplots_adjust(wspace=0.3, hspace=1)
    # color del fondo
    # ax.patch.set_facecolor('white')
    # ===== LEYENDA===
    # scatter.legend_elements(prop="sizes", num=1)[0][0].set_markersize(10)
    # legend_elements=[plt.Line2D([0],[0],marker='o',markersize=10,linewidth=2)]
    # ax.legend(handles=legend_elements)
    ###
    ax.set_title("Análisis de los tiempos de llegada de los bloques",
                 loc='left', **preferencias)
    ax.set_xlabel("Fechas de registros", fontsize=17,**preferencias)
    ax.set_ylabel("Diferencias de tiempo [min]", fontsize=17,**preferencias)
    # cuadricula
    ax.grid(axis='y')
    # ax.legend(loc='upper right',title='Leyenda')
    # plt.show()
    # plt.imshow()
    plt.savefig('analisis/resultados/TIEMPO'+tipo+'.png',
                bbox_inches='tight', pad_inches=0.5)


#crear_imagen_total('estilo_dark')
crear_imagen_total('estilo_blanco')
>>>>>>> 682a4ed (Estilos_blancos)
