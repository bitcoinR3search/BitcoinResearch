import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime, timedelta
from app.styles import Estilos, colores
from app.readata import leer_data, last_block
from matplotlib import font_manager as fm
from PIL import Image


fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fpatht = os.path.join('bins/BigBlueTerm437NerdFont-Regular.ttf')
title = fm.FontProperties(fname=fpatht)

fname = os.path.split(fpath)[1]



#=======NTX VS N_BLOCKS
def crear_imagen_total(tipo='estilo_blanco'):
    fig, ax = plt.subplots(1,2,figsize=(20,5), dpi=200)
    preferencias = {'color':Estilos[tipo][1],'fontproperties':prop}
    ntx,n_block = leer_data('ntx','n_block')
    indice=np.where((ntx==np.max(ntx)))[0][0]
    ntx_max=int(ntx[indice])
    fig.patch.set_facecolor(Estilos[tipo][0])
    ax[0].patch.set_facecolor(Estilos[tipo][0])
    ax[1].patch.set_facecolor(Estilos[tipo][0])

    for spine in ax[0].spines.values():
        spine.set_color(Estilos[tipo][1])
    for spine in ax[1].spines.values():
        spine.set_color(Estilos[tipo][1])


    #plt.suptitle("Number of\n    Transactions",fontsize=50,y=1.5,x=0.25,color=Estilos[tipo][0],fontproperties=title)
    if tipo[7:8]=='d':        
        ax[0].plot(n_block,ntx,alpha=0.8,color=colores[3])
        ax[0].scatter(n_block[indice], ntx_max, color ='white',s=180)
        ax[0].scatter(n_block[indice], ntx_max, color ='red',s=50)
        ax[0].text(n_block[indice]+100000,ntx_max+2000,f'ATH: {ntx_max} Tx\en el Bloque {round(n_block[indice])}',color='black', ha='right', va='center',size=18)

        ax[0].spines['top'].set_visible(False)
        ax[0].spines['right'].set_visible(False)
        
        ax[1].spines['top'].set_visible(False)
        ax[1].spines['right'].set_visible(False)

        a_np = np.array(ntx)
        b_np = np.cumsum(a_np)
        ax[1].plot(n_block,b_np,label="# de tx por bloque",alpha=0.8,color='black')
        ax[1].fill_between(n_block,b_np, color='lightblue', alpha=0.5)
    else:        
        ax[0].plot(n_block,ntx ,label="number of transactions per block",alpha=0.8,color=colores[10])
        ax[0].scatter(n_block[indice], ntx_max, color ='black',label='Máximo', s=40)
        ax[0].annotate(f'Max: {int(ntx_max)}', (n_block[indice], ntx_max), xytext=(20, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='black', linewidth=3), fontsize=18, color='black')

        #VALOR_MAX="{:.2f}".format(np.log(ntx.max))
        
        ax[1].plot(n_block,np.log(ntx) ,label="number of transactions per block",alpha=0.8,color=colores[10])
        ax[1].scatter(n_block[indice], np.log(ntx_max), color ='black',label='Máximo', s=40)        
        ax[1].annotate(f'Max: {np.log(float(ntx_max)):.2f}', (n_block[indice], np.log(ntx_max)), xytext=(20, 30), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='black', linewidth=3), fontsize=18, color='black')
        

    
        
    ax[0].text(n_block[210000*1]+1.2e5,8000,'1er\nHalv', color='black', ha='right', va='center',size=18)
    ax[0].text(n_block[210000*2]+1.2e5,8000,'2do\nHalv', color='black', ha='right', va='center',size=18)
    ax[0].text(n_block[210000*3]+1.2e5,8000,'3er\nHalv', color='black', ha='right', va='center',size=18)
    

    sentence = f"Hasta el Bloque {last_block()} \nfueron un total \nde "+'{:,}'.format(round(max(b_np))).replace(",", "'")+" tx"
    ax[1].text(max(n_block)*.8,max(b_np)*1.1,sentence, color='black', ha='right', va='center',size=18)
    ax[1].scatter(n_block[-1],b_np[-1], color ='white',s=180)
    ax[1].scatter(n_block[-1],b_np[-1], color ='red',s=50)

    ax[0].set_ylabel('# Tx\n', fontsize=25,**preferencias)
    ax[0].set_xlabel('# Bloque\n', fontsize=25,**preferencias,labelpad=20)
    ax[0].axvline(x=210000,ymax=0.75, color='black', linestyle='--', linewidth=1, zorder=0)
    ax[0].axvline(x=210000*2,ymax=0.75,color='black', linestyle='--', linewidth=1)
    ax[0].axvline(x=210000*3,ymax=0.75,color='black', linestyle='--', linewidth=1)
    ax[0].tick_params(axis='both',colors='black',labelsize=14)
    
    ax[0].set_xticks([0,1e5,2e5,3e5,4e5,5e5,6e5,7e5,8e5])
    ytick_labels = ['0','100k','200k','300k','400k','500k','600k','700k','800k']
    ax[0].set_xticklabels(ytick_labels,fontsize=18)
    ax[0].tick_params(axis='both', length=5,width=3)
    

    
    ax[1].set_ylabel('Tx Acumuladas\n', fontsize=23,**preferencias)
    ax[1].set_xlabel('# Bloque\n', fontsize=23,**preferencias,labelpad=20)

    ax[1].set_xticks([0,1e5,2e5,3e5,4e5,5e5,6e5,7e5,8e5])
    ytick_labels = ['0','100k','200k','300k','400k','500k','600k','700k','800k']
    ax[1].set_xticklabels(ytick_labels,fontsize=18)
    ax[1].tick_params(axis='both',colors='black',labelsize=14)

    


    #if tipo[7:8]=='d':
    #    tw1 = Image.open('bins/br_w.png')
    #else:
    #    tw1 = Image.open('bins/br_d.png')
    #tw1_resized = tw1.resize((int(tw1.width * 0.4), int(tw1.height * 0.4)))
    #tw1_array = np.array(tw1_resized)
    #fig.figimage(tw1_array, xo=2750, yo=1300, alpha=0.55, zorder=1)
    plt.subplots_adjust(wspace=0.4)

    plt.savefig('analisis/resultados/Numero_de_transacciones_'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)
    #plt.show()


def crear_imagen_h(tipo='estilo_blanco'):

    fig, ax = plt.subplots(2,2,figsize=(13,6), dpi=200)
    ntx,n_block = leer_data('ntx','n_block')
    fig.patch.set_facecolor(Estilos[tipo][0])
    ax[0,0].patch.set_facecolor(Estilos[tipo][0])
    ax[0,1].patch.set_facecolor(Estilos[tipo][0])
    ax[1,0].patch.set_facecolor(Estilos[tipo][0])
    ax[1,1].patch.set_facecolor(Estilos[tipo][0])


    preferencias = {'color':Estilos[tipo][1],'fontproperties':prop}

    #plt.suptitle("Number of blocks\nper Halving",fontsize=35,x=0.20,y=1.23,**preferencias)
    #ntx,n_block = leer_data('ntx','n_block')


    for spine in ax[0,0].spines.values():
        spine.set_color(Estilos[tipo][1])
    for spine in ax[0,1].spines.values():
        spine.set_color(Estilos[tipo][1])
    for spine in ax[1,0].spines.values():
        spine.set_color(Estilos[tipo][1])
    for spine in ax[1,1].spines.values():
        spine.set_color(Estilos[tipo][1])
############################
    ########
    hist, edges = np.histogram(ntx[:210000],bins=50)
    
    top_10_indices = np.argpartition(hist, -5)[-5:]
    
    ax[0, 0].bar(range(0,10), hist[:10], color=Estilos[tipo][1], edgecolor='black', width=0.4, align='edge')
    
    for i in top_10_indices:
        freq = hist[i]
        label = f'{(freq / np.sum(hist)) * 100:.2f}%'
        ax[0, 0].text(i, freq, label, ha='center', va='bottom', fontsize=9, color=Estilos[tipo][1], rotation=0)

    
    xticks_positions = [i for i in range(0, 10)] 
    interval_labels = [f'{int(edges[i])} - {int(edges[i+1])}' for i in range(len(edges)-1)]
    ax[0, 0].set_xticks(xticks_positions)
    ax[0, 0].set_xticklabels([interval_labels[i] for i in xticks_positions], color=Estilos[tipo][1], rotation=45)
    ax[0, 0].tick_params(axis='y', colors=Estilos[tipo][1])
    ax[0, 0].set_ylim(0, 185000)
#________________________
    hist, edges = np.histogram(ntx[210000:2*210000],bins=50)
    
    top_10_indices = np.argpartition(hist, -5)[-5:]
    
    ax[0, 1].bar(range(0,15), hist[:15], color=Estilos[tipo][1], edgecolor='black', width=0.4, align='edge')
    
    for i in top_10_indices:
        freq = hist[i]
        label = f'{(freq / np.sum(hist)) * 100:.2f}%'
        ax[0, 1].text(i, freq, label, ha='center', va='bottom', fontsize=9, color=Estilos[tipo][1], rotation=45)

    xticks_positions = [i for i in range(0, 15)] 
    interval_labels = [f'{int(edges[i])} - {int(edges[i+1])}' for i in range(len(edges)-1)]
    ax[0, 1].set_xticks(xticks_positions)
    ax[0, 1].set_xticklabels([interval_labels[i] for i in xticks_positions], color=Estilos[tipo][1], rotation=45)
    ax[0, 1].tick_params(axis='y', colors=Estilos[tipo][1])
    ax[0, 1].set_ylim(0, 98000)
#_______________________
    hist, edges = np.histogram(ntx[2*210000:3*210000],bins=50)
    
    top_10_indices = np.argpartition(hist, -5)[-5:]
    
    ax[1, 0].bar(range(0, 35), hist[:35], color=Estilos[tipo][1], edgecolor='black', width=0.4, align='edge')

    for i in top_10_indices:
        freq = hist[i]
        label = f'{(freq / np.sum(hist)) * 100:.2f}%'
        ax[1, 0].text(i, freq, label, ha='center', va='bottom', fontsize=9, color=Estilos[tipo][1], rotation=75)

    
    xticks_positions = [i for i in range(0, 35, 2)]  
    interval_labels = [f'{int(edges[i])} - {int(edges[i+1])}' for i in range(len(edges)-1)]
    ax[1, 0].set_xticks(xticks_positions)
    ax[1, 0].set_xticklabels([interval_labels[i] for i in xticks_positions], color=Estilos[tipo][1], rotation=45)
    ax[1, 0].tick_params(axis='y', colors=Estilos[tipo][1])
    ax[1, 0].set_ylim(0, 15000)
    #=================================
    hist, edges = np.histogram(ntx[3*210000:], bins=50)
    
    top_10_indices = np.argpartition(hist, -5)[-5:]
    
    ax[1, 1].bar(range(0,35), hist[:35], color=Estilos[tipo][1], edgecolor='black', width=0.4, align='edge')

    for i in top_10_indices:
        freq = hist[i]
        label = f'{(freq / np.sum(hist)) * 100:.2f}%'
        ax[1, 1].text(i, freq, label, ha='center', va='bottom', fontsize=9, color=Estilos[tipo][1], rotation=75)

    xticks_positions = [i for i in range(0, 35, 2)]  
    interval_labels = [f'{int(edges[i])} - {int(edges[i+1])}' for i in range(len(edges)-1)]
    ax[1, 1].set_xticks(xticks_positions)
    ax[1, 1].set_xticklabels([interval_labels[i] for i in xticks_positions], color=Estilos[tipo][1], rotation=45)
    ax[1, 1].tick_params(axis='y', colors=Estilos[tipo][0])
    ax[1, 1].set_ylim(0, 16500)
    #====================================
    
    ax[0,0].set_title("1st Halving\n2009-2012",fontsize=25,loc='left', **preferencias)
    ax[0,1].set_title("2nd Halving\n2012-2016",fontsize=25,loc='left', **preferencias)
    ax[1,0].set_title("3rd Halving\n2016-2020",fontsize=25,loc='left', **preferencias)
    ax[1,1].set_title("4th Halving\n2020-2024",fontsize=25,loc='left', **preferencias)

    
    #if tipo[7:8]=='d':
    #    tw1 = Image.open('bins/br_w.png')
    #else:
    #   tw1 = Image.open('bins/br_d.png')

    #tw1_resized = tw1.resize((int(tw1.width * 0.5), int(tw1.height * 0.5)))  # Reduce el tamaño de la imagen a la mitad
 # Convierte la imagen de PIL a una matriz de numpy para que matplotlib pueda trabajar con ella
    #tw1_array = np.array(tw1_resized)

    #fig.figimage(tw1_array, xo=1500, yo=1150, alpha=0.55, zorder=1)
    plt.subplots_adjust(wspace=0.3, hspace=1)
    plt.savefig('analisis/resultados/Numero_de_transacciones_halv_'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)


# for a in Estilos.keys():
#     crear_imagen_h(a)
#     crear_imagen_total(a)
crear_imagen_total('estilo_dark')
crear_imagen_h('estilo_dark')