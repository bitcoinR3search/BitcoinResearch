# Bot Telegram Node


El bot de telegram base consiste en configurar en un Raspberry pi4 un script de Python que este online 24/7. Se lo ejecuta de tal forma que tenga robustes ante cuelgues, re inicios inesperados y cierre de procesos forzado. 

## Requisitos

Primero es aconsejable crear un entorno de trabajo exclusivo.

``` sh
$ python -m venv rpibots
$ cd rpibots
$ source bin/activate
(rpibots)$ git clone git@github.com:CobraPython/BitcoinResearch.git
```

Descargamos e instalamos los requerimientos.

``` sh
(rpibots)$ cd BitcoinResearch/Telegram-Bot
(rpibots)$ pip install -r req.txt
```

### Token Telegram

Telegram tiene un bot 'Padre' que se encarga de configurar las credenciales de acceso de los todos los bots en la plataforma. 

![](/Telegram-Bot/images/fatherbot.png)

A través de este bot se puede configurar uno propio y solicitar tokens de acceso.

Estos tokens serán las credenciales de autentificación que usara el bot.
![](/Telegram-Bot/images/token.png)

> OJO nunca se debe compartir el Token

## Instalando el Bot

Como una buena práctica el token no se muestra directamente en el código ni en ningún script pre compilado. Es  enmascarado como variables de entorno en un archivo `.env`.

Si corremos el script `bot_telegram.py` en el entorno creado, el bot empieza a funcionar y se encuentra esperando a nuevos usuarios en bucle.

``` sh
(rpibots)$ python bot_telegram.py
>Run Bot Run
```
### Automatizando

El objetivo es hacer que el bot corra automáticamente en el Raspberry Pi4 aún cuando se reinicie, se corte el servicio o se detenga por algún error. Es decir, que el script del bot este siempre ejecutandose. 

Existen muchas formas de lograrlo. Una forma es usar 'supervisor'. 

``` shell
sudo apt install supervisor
```

Se le otorgan permisos de ejecución.

``` sh
 sudo nano /etc/supervisor/supervisord.conf
```
modificando solamente las líneas.
``` txt
chmod=0770
chown=root:admin
```

Finalmente se configura el nuevo servicio, el bot.
```
sudo nano /etc/supervisor/conf.d/my-proccess.conf
```
Con el siguiente esquema.

``` txt
[program:bot_telegram]
command = ~/python bot_telegram.py
directory = ~/BitcoinResearch/Bot-telegram/
autostart = true
autorestart =true
user = admin
logfile = ~/supervisor_tgbot.log
logfile_maxbytes = 50MB
logfile_backups=10
loglevel = info
``` 
Al terminar de guardar esta configuración, al hacer un `reboot` el bot estará funcionando automáticamente. 

Incluso si se busca parar manualmente el proceso `pid` (puedes rastrear el número del proceso del bot con el comando `top` y terminarlo con `kill #`) es automáticamente re ejecutado. 

¡Hasta ahora esta forma de configurar un Bot de Telegram me ha funcionado muy bien!

## Comentarios Finales

El bot es más estable en su funcionamiento si el Raspberry Pi4 esta conectado a Internet mediante cable ethernet. Se ha testeado de esta forma por varias semanas y no se reportó níngun problema.
Se ha testeado también con el Raspberry conectado por Wifi. Dependiendo de la estabilidad de la señal ocacionalmente se desconecta y necesita reiniciarse manualmente el Raspberry. 

Aparte del log que se genera con script python exite un segundo nível de log que genera 'supervisor' para registrar reinicios, errores de memoria, interrupción del sistema, etc. Para tener un seguimiento de posibles problemas. 

