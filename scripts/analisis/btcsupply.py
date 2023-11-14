"""    INFO
Para calcular cuanto bitcoin será emitido con precisión
usamos la regla:
-Recompensa Inicial > 50 btc
-Cada 210 000 bloques se reduce a la mitad
-La mínima unidad es satoshi 1 btc = 100 000 000 sats
la recompensa inicial son 50*10^8 sats (50 btc)
"""

# librerias a usar
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg
from matplotlib import font_manager as fm
#from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from app.styles import Estilos, colores
from app.readata import bitcoins_emitidos,punto_halv, last_block

#os.chdir('D:\proyectos\BitcoinResearch\BitcoinResearch\scripts')
# Cambiar la tipografia
fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)

fpatht = os.path.join('bins/BigBlueTerm437NerdFont-Regular.ttf')
title = fm.FontProperties(fname=fpatht)

fname = os.path.split(fpath)[1]





# Se va a calcular la cantidad de bitcoin que se va a emitir
# por cada halving hasta que la recompensa sea 1 satoshi

#Al inicio, el premio era de 50 btc, se convierten a satoshis 
#reward = 50e8

#el halving se da cada 210k bloques
# limit = 210_000
# halv = []
# supply = []

# btc = 0
# h=0
# rew=[]
# while reward >= 1:
#     cnt = 1 
#     while cnt<=limit:
#         #print(limit)
#         cnt+=1
#         btc+=reward
#     h+=1
#     rew.append(reward)
#     reward//=2
#     halv.append(h)
#     supply.append(btc/1e8)


#el método anterior se puede resumir en tres lineas

rewards = [50e8 // (2**i) for i in range(50) if 50e8 // (2**i) >= 1]
halvings = list(range(1, len(rewards) + 1))
supply = [sum(rewards[:i+1]) * 210_000 / 1e8 for i in range(len(rewards))]


def crear_imagen(tipo='estilo_dark'):
    fig, ax = plt.subplots(figsize=(13,5), dpi=200)
    fig.patch.set_facecolor(Estilos[tipo][1])
    ax.patch.set_facecolor(Estilos[tipo][1])
    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}
    #plt.suptitle("Bitcoin Supply\n2009 - 2140", fontsize=45,x=0.1,y=1.4,fontproperties=title,color=Estilos[tipo][0])
    ax.set_ylabel('BTC Minados', fontsize=25,**preferencias)
    ax.set_xlabel('Halving', fontsize=25,**preferencias)
    ax.tick_params(axis='both',colors=Estilos[tipo][0])


    ax.plot(halvings[:],supply[:],color=colores[10],linewidth=6)
    ax.plot([0,1,2,3,punto_halv()],[0,supply[0],supply[1],supply[2],bitcoins_emitidos()],color=colores[10],linewidth=5)
    #ax.plot([0,1,2,3,punto_halv()],[0,supply[0],supply[1],supply[2],bitcoins_emitidos()],color=colores[0],linewidth=1)
    

       
    ax.set_yticks(supply[:5]+[supply[-1]])
    ytick_labels = ['50% ','75% ','87.5% ','','','100% ']   
    ax.set_yticklabels(ytick_labels,fontsize=15)


    ax.set_xticks([1,2,3,4])
    xtick_labels = ['1er Halv\n28/12/2012','2do Halv\n9/8/2016','3er Halv\n11/6/2020','4to Halv\nEstimado:\n~24/12/2024']   
    ax.set_xticklabels(xtick_labels,fontsize=15)
    
    ax.tick_params(axis='y', length=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    
    #ax.text(3,23e6,"For Block "+str(last_block())+" we've reached\n"+str(round(100*(punto_halv()%1),2))+"% completion of the 4th\nhalving cicle, emitting\n"+str(round(bitcoins_emitidos(),5))+' $btc', fontsize=15, **preferencias)
    
    #ax.text(4.5,11e6,"As of Block 6'930'000 a\ntotal of "+str(supply[-1])+" $btc\nwill have been issued (~21M $btc)\nduring 33 halvings until the\nestimated year of 2140.", fontsize=15, **preferencias)


    for spine in ax.spines.values():
        spine.set_color(Estilos[tipo][0])

    ax.plot([0, 1], [supply[0],supply[0]], color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.plot([0, 2], [supply[1],supply[1]], color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.plot([0, 3], [supply[2],supply[2]], color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.plot([0, 6], [supply[-1],supply[-1]], color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.plot([1, 1], [0,supply[0]], color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.plot([2, 2], [0,supply[1]], color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.plot([3, 3], [0,supply[2]], color=Estilos[tipo][0], linestyle='dashed', linewidth=1)
    ax.plot([4, 4], [0,supply[3]], color=Estilos[tipo][0], linestyle='dashed', linewidth=1)  

    
    ax.scatter([1,2,3,4],supply[:4],color=colores[6],s=100,zorder= 2)
    ax.scatter([1,2,3,4],supply[:4],color=colores[6],s=30,zorder = 2)
    ax.scatter([1,2,3,4],supply[:4],color=colores[6],s=10,zorder = 2)

    ax.scatter([punto_halv()],[bitcoins_emitidos()],color=colores[2],s=200,zorder= 2)
    ax.scatter([punto_halv()],[bitcoins_emitidos()],color=colores[0],s=50,zorder = 2)
    ax.scatter([punto_halv()],[bitcoins_emitidos()],color=colores[1],s=15,zorder = 2)
    
    ax.set_xlim(0,6)
    ax.set_ylim(0,21e6)
    
    #if tipo[7:8]=='d':
   #     tw1 = Image.open('bins/br_w.png')
   # else:
   #     tw1 = Image.open('bins/br_d.png')


    #tw1_resized = tw1.resize((int(tw1.width * 0.40), int(tw1.height * 0.40)))  # Reduce el tamaño de la imagen a la mitad

# Convierte la imagen de PIL a una matriz de numpy para que matplotlib pueda trabajar con ella
    #tw1_array = np.array(tw1_resized)



    #fig.figimage(tw1_array, xo=2600, yo=1250, alpha=0.55, zorder=2)



    plt.savefig('analisis/resultados/supply_btc_'+tipo+'.png',bbox_inches='tight',pad_inches=0.75)

# for a in Estilos.keys():
#     crear_imagen(a)
crear_imagen('estilo_blanco')