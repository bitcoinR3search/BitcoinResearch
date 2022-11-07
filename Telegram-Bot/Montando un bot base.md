# Bot Telegram Base


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




