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
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg
from matplotlib import font_manager as fm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from app.styles import Estilos, colores


os.chdir('D:\proyectos\BitcoinResearch\BitcoinResearch\scripts')


PRIZE = 50*10**8  # premio inicial expresedo en satoshis

# un halv ocurre cada 210 000 bloques
LIM = 210_000  # limite de division
BTC = 0  # se inicia con cero bitcoin
HALV = 0  # contador de halvings
BLOCKS = 0  # contador de bloques
DATE = datetime(2009, 1, 8, 22, 00)  # fecha inicio Bloques

# los datos se almacenan en una lista
H = [0,]  # Halv
Y = [0,]  # btc emitido
YN = []  # normalizado


H_D = [DATE,]  # halv date estimated

# para detalles de la grafica mas precisos

A = [0,]    # graf por bloque
B = [DATE,]  # graf por bloque


while PRIZE > 0:
    aux = [(BTC := BTC+PRIZE, BLOCKS := BLOCKS+1, A.append(BTC),
            B.append(B[-1]+timedelta(minutes=10))) for i in range(0, LIM)]
    print('Halv:', HALV, end='|')
    print('Prize(sats):', PRIZE/10**8, end='|')
    print('Supply(btc):', BTC/10**8, end='|')
    print('Block:', BLOCKS, end='|')
    print('Date:'+(H_D[-1]+timedelta(minutes=10*LIM)
                   ).strftime('%Y (estimate)'))
    PRIZE //= 2
    HALV += 1
    H.append(HALV)
    H_D.append(H_D[-1]+timedelta(minutes=10*LIM))
    Y.append(BTC)

# Correccion de fechas: La fecha del Halv es estimada pues
# se calcula tomando el promedio de salida de bloque 10 min
# por la cantidad de bloques 210 000 en cada halving
# Se toman las fechas reales en vez del dato estimado.
H_D[1] = datetime(2012, 11, 28)
H_D[2] = datetime(2016, 7, 9)
H_D[3] = datetime(2020, 5, 11)
YN = [(100*a/10**8)/(BTC/10**8) for a in Y]
A1 = [(100*a/10**8)/(BTC/10**8) for a in A]
B1 = [b.date() for b in B]
# Creamos la imagen


def crear_imagen(tipo='estilo_dark'):

    fig, ax = plt.subplots(figsize=(13,5), dpi=200)

    fig.patch.set_facecolor(Estilos[tipo][1])
    ax.patch.set_facecolor(Estilos[tipo][1])
    preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}
    plt.suptitle("Bitcoin Supply\n2009 - 2140", fontsize=23,x=0.20,y=1.23,**preferencias)
    ax
plt.ylabel('BTC Supply %', fontsize=15,
           color=tableau20[6])
plt.xlabel('\nYear', fontsize=15,
           color=tableau20[6])

plt.gca().yaxis.grid(linestyle='-', linewidth=0.75, dashes=(3, 1))

plt.xlim(H_D[0], H_D[8])
plt.ylim(0, 100)
ax.set_yticks([], [])
ax.set_xticks([], [])


btc = mpimg.imread(path_actual+'/Onchain/scripts/pics/btc.png')
imagebox = OffsetImage(btc, zoom=0.01)
hoy = datetime.now()
firma = AnnotationBbox(imagebox, (hoy, 92))
plt.gca().add_artist(firma)

hoy_txt = hoy.date().strftime('%Y-%m')

plt.annotate('You are Here!\n'+hoy_txt,
             xy=(hoy.date() + timedelta(weeks=36), 88),
             xytext=(hoy.date() + timedelta(weeks=180), 68),
             fontsize=12, color='black', arrowprops=dict(facecolor='red',
                                                         shrink=0.005))


plt.plot_date(H_D[4:], YN[4:], "-",
              color=tableau20[2], linewidth=0.25)
plt.plot_date(H_D[4:], YN[4:], ".",
              color=tableau20[2], markersize=6)
index = B1.index(hoy.date())

plt.plot_date(B1[:index:2016], A1[:index:2016], '-',
              color=tableau20[9], linewidth=4)

locator = mdates.MonthLocator(interval=50)
formatter = mdates.DateFormatter('%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().xaxis.set_tick_params(labelsize=10, rotation=15)
plt.tick_params(axis='x', colors=tableau20[6])

ytick_labels = ['0%', '50%', '75%', '87.5%', '100%']
plt.yticks([0, 50, 75, 87.5, 100], ytick_labels,
           fontsize=10, color=tableau20[6])


plt.axvline(datetime(2012, 11, 28), color=tableau20[16])
plt.text(datetime(2013, 1, 28), 10, '1er Halv\n28/12/2012', fontsize=8)

plt.axvline(datetime(2016, 7, 9), color=tableau20[17])
plt.text(datetime(2016, 9, 9), 10, '2do Halv\n9/8/2016', fontsize=8)

plt.axvline(datetime(2020, 5, 11), color=tableau20[18])
plt.text(datetime(2020, 7, 11), 10, '3er Halv\n11/6/2020', fontsize=8)

plt.axvline(H_D[4], color=tableau20[18])
plt.text(H_D[4]+timedelta(weeks=15), 7,
         '4er Halv\nEstimated:\n24/12/2024', fontsize=8)

plt.text(datetime(2010, 1, 1), 90, 'Reward\n50 $btc', fontsize=7)
plt.text(datetime(2014, 1, 1), 78, 'Reward\n25 $btc', fontsize=7)
plt.text(datetime(2017, 1, 1), 65, 'Reward\n12.5 $btc', fontsize=7)
plt.text(datetime(2021, 1, 1), 60, 'Reward\n6.25 $btc', fontsize=7)
plt.text(datetime(2025, 5, 1), 55, 'Reward\n3.125 $btc', fontsize=7)


ax2 = ax.twinx()

# Establecer límites del segundo eje Y
ax2.set_yticks([50, 75, 87.5, 100])
ytick_labels = ['10500000.0', '15750000.0', '18375000.0', '20999999.9769']
ax2.set_yticklabels(ytick_labels, fontsize=10, color=tableau20[6])
ax2.set_ylabel('BTC', fontsize=15, color=tableau20[9])
plt.tight_layout()

plt.savefig(path_actual+'/Onchain/scripts/pics/btcsupply.png')
