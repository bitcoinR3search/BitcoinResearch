# este script construye la gráfica histórica
# del tamaño de bloques en Bitcoin

# este script construye un gráfico de la evolución del tamaño de bloques
# a lo largo del cada bloque

# librerias a usar
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from PIL import Image
from datetime import datetime
from app.styles import Estilos, colores
from app.readata import leer_data,time_data,estado_data,last_block


# Cambiar la tipografia
fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)

fpatht = os.path.join('bins/BigBlueTerm437NerdFont-Regular.ttf')
title = fm.FontProperties(fname=fpatht)

fname = os.path.split(fpath)[1]

def bits_to_difficulty(bits):
   bits = int(bits, 16)
   # Convertir bits a un número de 256 bits en formato big-endian
   target = (bits & 0x007fffff) * 2 ** (8 * ((bits >> 24) - 3)) 
   # Calcular la dificultad como el cociente entre el objetivo máximo y el objetivo actual
   max_target = 0xffff * 2 ** (8 * (0x1d - 3))
   difficulty = max_target / target
   return difficulty

def crear_imagen_total(tipo='estilo_dark'):
        # Color del fondo
    fig, ax = plt.subplots(1,2,figsize=(20,5), dpi=200)
    fig.patch.set_facecolor(Estilos[tipo][1])
    ax[0].patch.set_facecolor(Estilos[tipo][1])
    ax[1].patch.set_facecolor(Estilos[tipo][1])

    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}

    plt.suptitle("Bitcoin\n   Difficulty",fontsize=50,y=1.5,x=0.18,color=Estilos[tipo][0],fontproperties=title)
    bits,time_s = leer_data('bits','time_b')
    difficulty = np.array([bits_to_difficulty(a) for a in bits])
    time = time_data(time_s)    

    if tipo[7:8]=='d':
        ax[0].plot(time,difficulty,color=colores[3],zorder=1,linewidth=3)
    else:
        ax[0].plot(time,difficulty,color=colores[10],zorder=1,linewidth=3)

    ##ax[0].plot(time,difficulty,color=colores[8],zorder=1,linewidth=7)
    #ax[0].plot(time,difficulty,color=colores[2],zorder=1,linewidth=3)
    #ax[0].plot(time,difficulty,color=colores[1],zorder=1,linewidth=0.5)
    


    #ax[0].set_yscale('log')
    locator = mdates.MonthLocator(interval=23)
    formatter = mdates.DateFormatter('%b\n%Y')
    ax[0].xaxis.set_major_locator(locator)
    ax[0].xaxis.set_major_formatter(formatter)
    ax[0].xaxis.set_tick_params(labelsize=18, rotation=30,length=5,width=3)
    ax[0].tick_params(axis='both',colors=Estilos[tipo][0])
    ax[0].set_ylabel('Difficulty\n', fontsize=23,**preferencias)
    ax[0].set_title("Scale:'linear'",loc='right',fontsize=15,color='white')
    ax[0].axhline(difficulty.max(),linestyle='dashed',color='red',linewidth=1)
    ax[1].axhline(difficulty.max(),linestyle='dashed',color='red',linewidth=1)

    #ax[1].plot(time,difficulty,color=colores[3],zorder=1,linewidth=7)

    if tipo[7:8]=='d':
        ax[1].plot(time,difficulty,color=colores[3],zorder=1,linewidth=3)
    else:
        ax[1].plot(time,difficulty,color=colores[10],zorder=1,linewidth=3)
    #ax[1].plot(time,difficulty,color=colores[8],zorder=1,linewidth=7)
    #ax[1].plot(time,difficulty,color=colores[2],zorder=1,linewidth=3)
    #ax[1].plot(time,difficulty,color=colores[1],zorder=1,linewidth=0.5)
    


    ax[1].set_yscale('log')
    locator = mdates.MonthLocator(interval=23)
    formatter = mdates.DateFormatter('%b\n%Y')
    ax[1].xaxis.set_major_locator(locator)
    ax[1].xaxis.set_major_formatter(formatter)
    ax[1].xaxis.set_tick_params(labelsize=18, rotation=30,length=5,width=3)
    ax[1].tick_params(axis='both',colors=Estilos[tipo][0])
    ax[1].set_ylabel('Difficulty log\n', fontsize=23,**preferencias)

    ax[1].set_title("Scale:'logy'",loc='right',fontsize=15,color='white')
       
    ax[0].set_yticks([0,1e13,2e13,3e13,4e13,5e13])
    ytick_labels = ['0',r"$1\times10^{13}$",r"$2\times10^{13}$",r"$3\times10^{13}$",r"$4\times10^{13}$",r"$5\times10^{13}$"]
    ax[0].set_yticklabels(ytick_labels,rotation=23,**preferencias)
    ax[0].yaxis.set_tick_params(labelsize=18)
    ax[1].tick_params(axis='y',labelsize=18,rotation=25)  # Cambia 20 al tamaño que prefieras

    ax[0].grid(axis='y', linewidth=.5,linestyle='--')
    ax[1].grid(axis='y', linewidth=.5,linestyle='--')


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


# Usa el índice para obtener la fecha correspondiente
    fecha_datetime = datetime.strptime(time_s[np.argmax(difficulty)][:10],'%Y-%m-%d')
    formatted_date = fecha_datetime.strftime('%d of %B %Y')
    mss1 = '*Up to block ' + str(last_block())+'\nthe All-Time High\nwas '
    mss2 = str(round(difficulty.max()/1e12,2))+' T on\n'+str(formatted_date)

    fig.text(0.5,1.15,mss1+mss2, ha='center', va='center', fontsize=20,**preferencias)

    fig.figimage(tw1_array, xo=3100, yo=1250, alpha=0.55, zorder=1)
    plt.subplots_adjust(wspace=0.25)
    plt.savefig('analisis/resultados/dificultad_total_'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)





def crear_imagen_h(tipo='estilo_dark'):
#         # Color del fondo
    fig, ax = plt.subplots(2,2,figsize=(13,6), dpi=200)

    fig.patch.set_facecolor(Estilos[tipo][1])
    ax[0,0].patch.set_facecolor(Estilos[tipo][1])
    ax[0,1].patch.set_facecolor(Estilos[tipo][1])
    ax[1,0].patch.set_facecolor(Estilos[tipo][1])
    ax[1,1].patch.set_facecolor(Estilos[tipo][1])


    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}

    plt.suptitle("Difficulty\nper Halving",fontsize=45,x=0.28,y=1.4,fontproperties=title,color=Estilos[tipo][0])
    bits,time = leer_data('bits','time_b')

    difficulty_1 = np.array([bits_to_difficulty(a) for a in bits[:210000-1]])
    time_1 = time_data(time[:210000-1])

    difficulty_2 = np.array([bits_to_difficulty(a) for a in bits[210000:2*210000-1]])
    time_2 = time_data(time[210000:2*210000-1])

    difficulty_3 = np.array([bits_to_difficulty(a)/10**12 for a in bits[2*210000:3*210000-1]])
    time_3 = time_data(time[210000*2:3*210000-1])

    difficulty_4 = np.array([bits_to_difficulty(a)/10**12 for a in bits[3*210000:]])
    time_4 = time_data(time[3*210000:])


    


    for spine in ax[0,0].spines.values():
        spine.set_color(Estilos[tipo][0])
    for spine in ax[0,1].spines.values():
        spine.set_color(Estilos[tipo][0])
    for spine in ax[1,0].spines.values():
        spine.set_color(Estilos[tipo][0])
    for spine in ax[1,1].spines.values():
        spine.set_color(Estilos[tipo][0])



    locator1 = mdates.MonthLocator(interval=9)
    formatter1 = mdates.DateFormatter('%b\n%Y')
    ax[0,0].xaxis.set_major_locator(locator1)
    ax[0,0].xaxis.set_major_formatter(formatter1)
    ax[0,0].xaxis.set_tick_params(labelsize=12, rotation=30,length=5,width=3)
    ax[0,0].tick_params(axis='both',colors=Estilos[tipo][0])
    ax[0,0].set_ylabel('Difficulty\n', fontsize=13,**preferencias)
    

    date = datetime(2010, 7, 18)
    x_value = mdates.date2num(date) 
    ax[0,0].scatter(x_value,5e1,s=300,color=colores[3])
    ax[0,0].scatter(x_value,5e1,s=75,color=colores[8])
    ax[0,0].scatter(x_value,5e1,s=5,color=colores[5])
    ax[0,0].vlines(x_value,0,1e1, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2010,4,1)
    x_value = mdates.date2num(date) 
    ax[0,0].text(x_value,1e3, 'GPU Art Fozt\nOpenCL GPU', color=Estilos[tipo][0], ha='right', va='center',size=13)


    date = datetime(2011, 5, 20)
    x_value = mdates.date2num(date) 
    ax[0,0].scatter(x_value,5e5,s=300,color=colores[3], zorder=0)
    ax[0,0].scatter(x_value,5e5,s=75,color=colores[8], zorder=0)
    ax[0,0].scatter(x_value,5e5,s=5,color=colores[5], zorder=0)
    ax[0,0].vlines(x_value,0,1e5, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2012,1, 20)
    x_value = mdates.date2num(date) 
    ax[0,0].text(x_value,1e4, 'FPGA\nMiner', color=Estilos[tipo][0], ha='right', va='center',size=13)
    

    locator2 = mdates.MonthLocator(interval=8)
    formatter2 = mdates.DateFormatter('%b\n%Y')
    ax[0,1].xaxis.set_major_locator(locator2)
    ax[0,1].xaxis.set_major_formatter(formatter2)
    ax[0,1].xaxis.set_tick_params(labelsize=12, rotation=30,length=5,width=3)
    ax[0,1].tick_params(axis='both',colors=Estilos[tipo][0])
    ax[0,1].set_ylabel('Difficulty\n', fontsize=13,**preferencias)
    

    date = datetime(2013, 5, 1)
    x_value = mdates.date2num(date) 
    ax[0,1].scatter(x_value,1e7,s=300,color=colores[3])
    ax[0,1].scatter(x_value,1e7,s=75,color=colores[8])
    ax[0,1].scatter(x_value,1e7,s=5,color=colores[5])
    ax[0,1].vlines(x_value,0,1e7, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2013,12, 1)
    x_value = mdates.date2num(date) 
    ax[0,1].text(x_value,9e9, 'First ASIC\nCannan miner\nChip 130nm', color=Estilos[tipo][0], ha='right', va='center',size=12)



    date = datetime(2015, 1, 1)
    x_value = mdates.date2num(date) 
    ax[0,1].scatter(x_value,5e10,s=300,color=colores[3])
    ax[0,1].scatter(x_value,5e10,s=75,color=colores[8])
    ax[0,1].scatter(x_value,5e10,s=5,color=colores[5])
    ax[0,1].vlines(x_value,0,5e10, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2015,9, 1)
    x_value = mdates.date2num(date) 
    ax[0,1].text(x_value,1e9, 'ASIC\n16nm', color=Estilos[tipo][0], ha='right', va='center',size=13)


    locator3 = mdates.MonthLocator(interval=9)
    formatter3 = mdates.DateFormatter('%b\n%Y')
    ax[1,0].xaxis.set_major_locator(locator3)
    ax[1,0].xaxis.set_major_formatter(formatter3)
    ax[1,0].xaxis.set_tick_params(labelsize=12, rotation=30,length=5,width=3)
    ax[1,0].tick_params(axis='both',colors=Estilos[tipo][0])
    ax[1,0].set_ylabel('Difficulty\n', fontsize=13,**preferencias)
    
    ax[1,0].set_yticks([0,5,10,15])
    ytick_labels = ['0.1T','5T','10T','15T']
    ax[1,0].set_yticklabels(ytick_labels,**preferencias)
    ax[1,0].yaxis.set_tick_params(labelsize=12)


    date = datetime(2017, 1, 1)
    x_value = mdates.date2num(date) 
    ax[1,0].scatter(x_value,.21,s=100,color=colores[3])
    ax[1,0].scatter(x_value,.21,s=50,color=colores[8])
    ax[1,0].scatter(x_value,.21,s=5,color=colores[5])
    ax[1,0].vlines(x_value,0,.21, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2017,3,1)
    x_value = mdates.date2num(date) 
    ax[1,0].text(x_value,4, 'ASIC\n14nm', color=Estilos[tipo][0], ha='right', va='center',size=13)

    date = datetime(2019, 1, 1)
    x_value = mdates.date2num(date) 
    ax[1,0].scatter(x_value,5,s=300,color=colores[3])
    ax[1,0].scatter(x_value,5,s=75,color=colores[8])
    ax[1,0].scatter(x_value,5,s=5,color=colores[5])
    ax[1,0].vlines(x_value,0,5, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2019,3, 1)
    x_value = mdates.date2num(date) 
    ax[1,0].text(x_value,10, 'ASIC\n7nm', color=Estilos[tipo][0], ha='right', va='center',size=13)


    locator4 = mdates.MonthLocator(interval=7)
    formatter4 = mdates.DateFormatter('%b\n%Y')
    ax[1,1].xaxis.set_major_locator(locator4)
    ax[1,1].xaxis.set_major_formatter(formatter4)
    ax[1,1].xaxis.set_tick_params(labelsize=12, rotation=30,length=5,width=3)
    ax[1,1].tick_params(axis='both',colors=Estilos[tipo][0])
    ax[1,1].set_ylabel('Difficulty\n', fontsize=13,**preferencias)
    
    ax[1,1].set_yticks([10,20,30,40,50])
    ytick_labels = ['10T','20T','30T','40T','50T']
    ax[1,1].set_yticklabels(ytick_labels,**preferencias)
    ax[1,1].yaxis.set_tick_params(labelsize=12)

    date = datetime(2023, 1, 1)
    x_value = mdates.date2num(date) 
    ax[1,1].scatter(x_value,38,s=300,color=colores[3])
    ax[1,1].scatter(x_value,38,s=75,color=colores[8])
    ax[1,1].scatter(x_value,38,s=5,color=colores[5])
    ax[1,1].vlines(x_value,0,38, colors=Estilos[tipo][0], linestyles='dashed')
    date = datetime(2023,7, 1)
    x_value = mdates.date2num(date) 
    ax[1,1].text(x_value,20,'ASIC\n5nm', color=Estilos[tipo][0], ha='right', va='center',size=13)

    if tipo[7:8]=='d':
        ax[0,0].plot(time_1,difficulty_1,color=colores[3],zorder=1)#,linewidth=1)
        ax[0,1].plot(time_2,difficulty_2,color=colores[3])
        ax[1,0].plot(time_3,difficulty_3,color=colores[3])
        ax[1,1].plot(time_4,difficulty_4,color=colores[3])
    else:
        ax[0,0].plot(time_1,difficulty_1,color=colores[10],zorder=1)#,linewidth=1)
        ax[0,1].plot(time_2,difficulty_2,color=colores[10])
        ax[1,0].plot(time_3,difficulty_3,color=colores[10])
        ax[1,1].plot(time_4,difficulty_4,color=colores[10])

    #ax[0,0].plot(time_1,difficulty_1,color=colores[3],zorder=1,linewidth=3)
    #ax[0,0].plot(time_1,difficulty_1,color=colores[2],zorder=1,linewidth=2)
    #ax[0,0].plot(time_1,difficulty_1,color=colores[1],zorder=1,linewidth=0.5)
    
    
    ax[0,0].set_yscale('log')
    ####ax[0,1].plot(time_2,difficulty_2,color=colores[3])
    ax[0,1].set_yscale('log')
    ####ax[1,0].plot(time_3,difficulty_3,color=colores[3])
    #ax[1,0].set_yscale('log')
    ####ax[1,1].plot(time_4,difficulty_4,color=colores[3])
    #ax[1,1].set_yscale('log')

    ax[0,0].set_title("1st Halving\n2009-2012                       scale:'logy'",fontsize=25,loc='left', **preferencias)
    ax[0,1].set_title("2nd Halving\n2012-2016                       scale:'logy'",fontsize=25,loc='left', **preferencias)
    ax[1,0].set_title("3rd Halving\n2016-2020",fontsize=25,loc='left', **preferencias)
    ax[1,1].set_title("4th Halving\n2020-2024",fontsize=25,loc='left', **preferencias)

    if tipo[7:8]=='d':
        tw1 = Image.open('bins/br_w.png')
    else:
        tw1 = Image.open('bins/br_d.png')

    total_diff = np.array([bits_to_difficulty(a)/10**12 for a in bits])
    me1 = 'All-time High: '+str(round(total_diff.max(),2))+' T'
    me2 = '\nLast Block '+str(last_block())+' : '+str(round(total_diff[-1],2))+' T'


    
    date = datetime(2013, 1, 1)
    x_value = mdates.date2num(date) 
    ax[0,0].text(x_value,1e10,me1+me2, color=Estilos[tipo][0], ha='right', va='center',size=13)


    tw1_resized = tw1.resize((int(tw1.width * 0.3), int(tw1.height * 0.3)))  # Reduce el tamaño de la imagen a la mitad
# Convierte la imagen de PIL a una matriz de numpy para que matplotlib pueda trabajar con ella
    tw1_array = np.array(tw1_resized)




    fig.figimage(tw1_array, xo=1800, yo=1550, alpha=0.55, zorder=1)
    plt.subplots_adjust(wspace=0.3, hspace=1)
    plt.savefig('analisis/resultados/dificultad_halv_'+tipo+'.png',bbox_inches='tight',pad_inches=0.75)



# for a in Estilos.keys():
#     crear_imagen_h(a)
#     crear_imagen_total(a)
crear_imagen_h('estilo_dark')
crear_imagen_total('estilo_dark')
