#######################################################################
#********Script Bot Telegram Nodo Btc*********************************#
#######################################################################


# La primera versión solo tiene tres acciones:
# /start - Inicia el bot, realiza un saludo y guarda usuario en log.
# send_ip - manda el ip con que el rpi se conecta.        solo admins
# terminal - Abre una terminal en el rpi por mensajes.    solo admins

# importación de librerias
import telebot, json, time, os, sys
import numpy as np
#from telebot import types
from dotenv import load_dotenv

#donde se guardan los tokens como variables de entorno
path = '/home/ghost/rpibots/'
load_dotenv(path+'.env')

# autenrtificación y cuenta maestra
token = os.getenv('token_telegram')
master = float(os.getenv('master_id'))

#comandos que ingresas al bot ej /start
commands = {'start'  :   'Inicia el bot',}

# /start es un comando, 'send_ip' y 'terminal' son botones.


# Cargamos los usuarios conocídos. De no existir creamos una lista vacía.
# KnownUsers es un array de usuarios conocidos

path1 = '/home/ghost/rpibots/BitcoinResearch/Telegram-Bot/'
if(os.path.exists(path1+'knownUsers.npy')):
	aux         = np.load(path1+'knownUsers.npy', allow_pickle='TRUE')
	knownUsers  = aux.tolist()
else:
    knownUsers = []
    np.save(path1+'knownUsers.npy',knownUsers)



#######################################################################
#********************MENU Y RECORRIDO*********************************#
#######################################################################

# El funcionamiento del Bot depende de la ubicacion del usuario dentro de este:
# es como si el bot fuera un lugar (place) con salas que dan acceso a otras salas.

# Por defecto el bot se inicia en el lugar lobby, que espera el comando /start.
# Este comando inicia un registro y saludo al user y lo posiciona en la sala principal.
# es como un  menu = 0 que da acceso a otros dos
# menu = 1 y menu = 2

menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
menu.add('Send IP','Terminal')


#######################################################################
#**********************Funciones***************************************#
#######################################################################



# Función para registrar un log

# La función listener corre cada vez que se invoca al bot
# puede usarse para algún log o para preparar algo previo
def listener(messages):
    pass

#######################################################################
#****************************Inicializamos el bot**********************#
#######################################################################

#creamos el objeto Telegram Bot
bot = telebot.TeleBot(token)
#asignamos nuestra funcion listener al bot
bot.set_update_listener(listener)

#######################################################################
#**********************Estructura de Comandos*************************#
#######################################################################

# START
@bot.message_handler(commands=['start'])
#Cuando se pulse el comando /start
#mira si es un usuario que conoce (en el log) o lo registra si es nuevo
#la variable auxiliar nos ayuda a llevar un orden de menus.
#luego del lobby para usar /start, que seria un valor auxiliar = 0
#viene el menu con dos botones que es como un piso 1, auxiliar = 1
def command_start(m):
    cid = m.chat.id  # ID del usuario
    if cid in knownUsers:    #Con el ID busca si es conocido.
        #Si es conocido, le envia un saludo
        auxiliar = 1
        bot.send_message(cid, "👋Hola,  "+str(m.chat.username)+" que bueno verte nuevamente.",disable_notification= False)
        time.sleep(1)
    else:
        #Si no es conocido, le envia una bienvenida
        bot.send_message(cid, "👋Hola, "+str(m.chat.username)+', ¡Bienvenido!',disable_notification= False)
        time.sleep(1)
        #registra en log
        bot.send_message(cid, "Te voy registrando...",disable_notification= True)
        auxiliar = 1
        np.save(path+'knownUsers.npy', knownUsers)


    bot.send_message(cid, "Iniciando el bot...",disable_notification= True)
    time.sleep(1)
    # Te envia al Menú principal por defecto menu con los botones
    bot.send_message(cid, "🤖Listo ✅...\nPor favor usa los botones.",reply_markup=menu,disable_notification= False)


#Ahora se configuran los botones del menu
# solo tiene 'Send IP' y  'Terminal'

@bot.message_handler(auxiliar = 1)
def menu_menu(m):
    cid = m.chat.id
    text = m.text
    #Una vez en la menu = 0 se delararon 2 opciones:
    if text == 'Send IP':
        bot.send_chat_action(cid, 'upload_document')
        mess = '''Se envia en txt la salida del comando ifconfig'''
        bot.send_message(cid,mess)
        os.popen('ifconfig > ip.txt')
        time.sleep(2)
        with open('ip.txt','rb') as ips:
            bot.send_document(master,ips,reply_markup=menu)
        #se envia el mensaje y se lo deriva al menu (en el mismo lugar)
    elif text == 'Terminal':
        markup = types.ForceReply(selective=False)
        mess = '''Se ejecuta en terminal el comando enviado en respuesta al mensaje'''
        target_n =  bot.send_message(cid,mess,reply_markup=markup);
        bot.register_next_step_handler(target_n,teminal)

def terminal(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    exec_ = os.popen(m.text)
    result = exec_.read()
    bot.send_message(cid, "Resultado: " + result,reply_markup=menu)



def menu_loop():
    print('Run code Run ...')
    bot.polling(True)


if __name__ == '__menu__':
    #para hacer el bot un poco más robusto
    #usamos un bucle while y manejo de excepciones
    while(1):
        try: #ejecuta la función que corre el bot
            menu_loop()
            #solo con una interrupcion que corta
            #proceso, manda un mensaje. En otros casos
            #y errores vuelve a ejecutarse.
        except KeyboardInterrupt:
            print('\nExiting by user request.\n')
        #lo ideal seria implementar un sistema de logs
        # para otros errores

