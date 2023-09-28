import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from app.styles import Estilos, colores
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from PIL import Image
#print(os.getcwd())
os.chdir('/home/richard/TRABAJO/BitcoinResearch/scripts/')
print(os.getcwd())

aux = np.load('/home/richard/Escritorio/datos/database.npz', allow_pickle='TRUE')
n_block = aux['n_block']
time_b = aux['time_b']
size = aux['size']
ntx = aux['ntx']
bits = aux['bits']
chainwork = aux['chainwork']
strippedsize = aux['strippedsize']
weight = aux['weight']
total = aux['total']


fpath = os.path.join('/home/richard/TRABAJO/BitcoinResearch/scripts/bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]

#=======NTX VS N_BLOCKS
def crear_imagen_total(tipo='estilo_dark'):
    fig, ax = plt.subplots(1,2,figsize=(20,5), dpi=200)
    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}
    indice=np.where((ntx==np.max(ntx)))[0][0]
    ntx_max=ntx[indice]

    fig.patch.set_facecolor(Estilos[tipo][1])
    ax[0].patch.set_facecolor(Estilos[tipo][1])
    ax[1].patch.set_facecolor(Estilos[tipo][1])

    for spine in ax[0].spines.values():
        spine.set_color(Estilos[tipo][0])
    for spine in ax[1].spines.values():
        spine.set_color(Estilos[tipo][0])


    plt.suptitle("Bitcoin\n   Difficulty",fontsize=50,y=1.5,x=0.1,**preferencias)


    ax[0].scatter(n_block[indice], ntx_max, color ='red',label='Máximo', s=20)
    ax[0].annotate(f'Max: {ntx_max}', (n_block[indice], ntx_max), xytext=(20, 20), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=12, color='red')
        
    ax[0].plot(n_block,ntx ,label="number of transactions per block",alpha=0.8,color=colores[3])
    ax[0].set_ylabel('Number of transactions\n', fontsize=23,**preferencias)
    ax[0].set_xlabel('Number of Blocks\n', fontsize=23,**preferencias)
    ax[0].axvline(x=210000, color=Estilos[tipo][0], linestyle='--', linewidth=1)
    ax[0].axvline(x=210000*2, color=Estilos[tipo][0], linestyle='--', linewidth=1)
    ax[0].axvline(x=210000*3, color=Estilos[tipo][0], linestyle='--', linewidth=1)
    ax[0].tick_params(axis='both',colors=Estilos[tipo][0])
    #ax[0].axvline(x=210000*3, color='red', linestyle='--', linewidth=1)


    ax[1].scatter(n_block[indice], np.log(ntx_max), color ='red',label='Máximo', s=20)
    ax[1].annotate(f'Max: {np.log(ntx_max)}', (n_block[indice], np.log(ntx_max)), xytext=(20, 20), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=12, color='red')

    ax[1].plot(n_block,np.log(ntx) ,label="number of transactions per block",alpha=0.8,color=colores[3])
    ax[1].set_ylabel('Number of transactions \n', fontsize=23,**preferencias)
    ax[1].set_xlabel('Number of Blocks\n', fontsize=23,**preferencias)
    ax[1].scatter(n_block[indice], np.log(ntx_max), color ='red',label='Máximo', s=20)
    ax[1].axvline(x=210000, color=Estilos[tipo][0], linestyle='--', linewidth=1)
    ax[1].axvline(x=210000*2, color=Estilos[tipo][0], linestyle='--', linewidth=1)
    ax[1].axvline(x=210000*3, color=Estilos[tipo][0], linestyle='--', linewidth=1)
    ax[1].tick_params(axis='both',colors=Estilos[tipo][0])

    tw1 = Image.open('/home/richard/TRABAJO/BitcoinResearch/scripts/bins/br_w.png')
    # tw1 = Image.open('bins/br_w.png')
    tw1_resized = tw1.resize((int(tw1.width * 0.65), int(tw1.height * 0.65)))
    tw1_array = np.array(tw1_resized)
    fig.figimage(tw1_array, xo=2800, yo=1000, alpha=0.55, zorder=1)
    plt.subplots_adjust(wspace=0.25)
    plt.savefig('analisis/resultados/Numero_de_transacciones_'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)
    #plt.show()

crear_imagen_total(tipo='estilo_dark')


def crear_imagen_h(tipo='estilo_dark'):

    fig, ax = plt.subplots(2,2,figsize=(13,6), dpi=200)

    fig.patch.set_facecolor(Estilos[tipo][1])
    ax[0,0].patch.set_facecolor(Estilos[tipo][1])
    ax[0,1].patch.set_facecolor(Estilos[tipo][1])
    ax[1,0].patch.set_facecolor(Estilos[tipo][1])
    ax[1,1].patch.set_facecolor(Estilos[tipo][1])


    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}

    plt.suptitle("Number of blocks\nper Halving",fontsize=35,x=0.20,y=1.23,**preferencias)
    #ntx,n_block = leer_data('ntx','n_block')


    for spine in ax[0,0].spines.values():
        spine.set_color(Estilos[tipo][0])
    for spine in ax[0,1].spines.values():
        spine.set_color(Estilos[tipo][0])
    for spine in ax[1,0].spines.values():
        spine.set_color(Estilos[tipo][0])
    for spine in ax[1,1].spines.values():
        spine.set_color(Estilos[tipo][0])
############################
    ########
    hist, edges = np.histogram(ntx[:210000],bins=50)
    
    top_10_indices = np.argpartition(hist, -5)[-5:]
    
    ax[0, 0].bar(range(0,10), hist[:10], color=Estilos[tipo][0], edgecolor='black', width=0.4, align='edge')
    
    for i in top_10_indices:
        freq = hist[i]
        label = f'{(freq / np.sum(hist)) * 100:.2f}%'
        ax[0, 0].text(i, freq, label, ha='center', va='bottom', fontsize=9, color=Estilos[tipo][0], rotation=0)

    
    xticks_positions = [i for i in range(0, 10)] 
    interval_labels = [f'{int(edges[i])} - {int(edges[i+1])}' for i in range(len(edges)-1)]
    ax[0, 0].set_xticks(xticks_positions)
    ax[0, 0].set_xticklabels([interval_labels[i] for i in xticks_positions], color=Estilos[tipo][0], rotation=45)
    ax[0, 0].tick_params(axis='y', colors=Estilos[tipo][0])
    ax[0, 0].set_ylim(0, 185000)
#________________________
    hist, edges = np.histogram(ntx[210000:2*210000],bins=50)
    
    top_10_indices = np.argpartition(hist, -5)[-5:]
    
    ax[0, 1].bar(range(0,15), hist[:15], color=Estilos[tipo][0], edgecolor='black', width=0.4, align='edge')
    
    for i in top_10_indices:
        freq = hist[i]
        label = f'{(freq / np.sum(hist)) * 100:.2f}%'
        ax[0, 1].text(i, freq, label, ha='center', va='bottom', fontsize=9, color=Estilos[tipo][0], rotation=45)

    xticks_positions = [i for i in range(0, 15)] 
    interval_labels = [f'{int(edges[i])} - {int(edges[i+1])}' for i in range(len(edges)-1)]
    ax[0, 1].set_xticks(xticks_positions)
    ax[0, 1].set_xticklabels([interval_labels[i] for i in xticks_positions], color=Estilos[tipo][0], rotation=45)
    ax[0, 1].tick_params(axis='y', colors=Estilos[tipo][0])
    ax[0, 1].set_ylim(0, 98000)
#_______________________
    hist, edges = np.histogram(ntx[2*210000:3*210000],bins=50)
    
    top_10_indices = np.argpartition(hist, -5)[-5:]
    
    ax[1, 0].bar(range(0, 35), hist[:35], color=Estilos[tipo][0], edgecolor='black', width=0.4, align='edge')

    for i in top_10_indices:
        freq = hist[i]
        label = f'{(freq / np.sum(hist)) * 100:.2f}%'
        ax[1, 0].text(i, freq, label, ha='center', va='bottom', fontsize=9, color=Estilos[tipo][0], rotation=75)

    
    xticks_positions = [i for i in range(0, 35, 2)]  
    interval_labels = [f'{int(edges[i])} - {int(edges[i+1])}' for i in range(len(edges)-1)]
    ax[1, 0].set_xticks(xticks_positions)
    ax[1, 0].set_xticklabels([interval_labels[i] for i in xticks_positions], color=Estilos[tipo][0], rotation=45)
    ax[1, 0].tick_params(axis='y', colors=Estilos[tipo][0])
    ax[1, 0].set_ylim(0, 15000)
    #=================================
    hist, edges = np.histogram(ntx[3*210000:], bins=50)
    
    top_10_indices = np.argpartition(hist, -5)[-5:]
    
    ax[1, 1].bar(range(0,35), hist[:35], color=Estilos[tipo][0], edgecolor='black', width=0.4, align='edge')

    for i in top_10_indices:
        freq = hist[i]
        label = f'{(freq / np.sum(hist)) * 100:.2f}%'
        ax[1, 1].text(i, freq, label, ha='center', va='bottom', fontsize=9, color=Estilos[tipo][0], rotation=75)

    xticks_positions = [i for i in range(0, 35, 2)]  
    interval_labels = [f'{int(edges[i])} - {int(edges[i+1])}' for i in range(len(edges)-1)]
    ax[1, 1].set_xticks(xticks_positions)
    ax[1, 1].set_xticklabels([interval_labels[i] for i in xticks_positions], color=Estilos[tipo][0], rotation=45)
    ax[1, 1].tick_params(axis='y', colors=Estilos[tipo][0])
    ax[1, 1].set_ylim(0, 16500)
    #====================================
    
    ax[0,0].set_title("1st Halving\n2009-2012",fontsize=25,loc='left', **preferencias)
    ax[0,1].set_title("2nd Halving\n2012-2016",fontsize=25,loc='left', **preferencias)
    ax[1,0].set_title("3rd Halving\n2016-2020",fontsize=25,loc='left', **preferencias)
    ax[1,1].set_title("4th Halving\n2020-2024",fontsize=25,loc='left', **preferencias)

    
    #tw1 = Image.open('/home/richard/TRABAJO/BitcoinResearch/scripts/bins/br_d.png')
    tw1 = Image.open('/home/richard/TRABAJO/BitcoinResearch/scripts/bins/br_w.png')


    tw1_resized = tw1.resize((int(tw1.width * 0.5), int(tw1.height * 0.5)))  # Reduce el tamaño de la imagen a la mitad
 # Convierte la imagen de PIL a una matriz de numpy para que matplotlib pueda trabajar con ella
    tw1_array = np.array(tw1_resized)




    fig.figimage(tw1_array, xo=1500, yo=1000, alpha=0.55, zorder=1)
    plt.subplots_adjust(wspace=0.3, hspace=1)
    
    plt.savefig('analisis/resultados/Numero_de_transacciones_halv_'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)
    #plt.show()



for a in Estilos.keys():
#    crear_imagen_h(a)    
    crear_imagen_h(a)    