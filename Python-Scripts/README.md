# Python y Bitcoin-cli


<img alt="jpg" src="./images/rpi.jpg" width="400" height="200" style="vertical-align:middle;margin:10px
100px 25px">

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/drkostas/Youtube-FirstCommentBot/master/LICENSE)


## Tabla de Contenido

+ [Introducción](#intro)
+ [Instalando](#instalando)
    + [Prerequisitos](#req)




# Introducción  <a name = "intro"></a>
Después de seguir la nota :pencil: [Nodo Bitcoin](https://github.com/CobraPython/BitcoinResearch/blob/main/Apuntes/Nodo%20Bitcoin.pdf) se tiene un Bitcoin-Core configurado y sincronizando el Blockchain.

Se puede ver el estado del core de Bitcoin de varias formas:

Consultando el estatus del demon:

``` sh
sudo systemctl status bitcoind.service
``` 

Nos da una salida por el estilo.

![](/Python-Scripts/images/bitcoind.png)


Usando comandos del Bitcoin-Cli:

``` sh
bitcoin-cli getblockchaininfo
```

Nos devuelve un json

![](/Python-Scripts/images/bitcoincli.png)


Utilizando los comandos bitcoin-cli se puede extraer directamente la información del Blockchain como transacciones, bloques, hash, montos, fees, wallets, movimientos, etc. 

## Instalando  <a name = "instalando"></a>
Es de interes en el proyecto BitcoinResearch el usar scripts de python para realizar consultas a bitcoin-cli en el nodo. Pero como se detalló en la nota :pencil: [Infraestructura para Bitcoin](https://github.com/CobraPython/BitcoinResearch/blob/main/Apuntes/Infraestructura%20para%20Bitcoin..pdf) se quiere tener otro Rpi desde otros punto que este dedicado para realizar análisis de datos y exclusivamente el Rpi del nodo para extraerlos.

Para lograrlo explicamos un poco el procedimiento que seguimos:

1. Bitcoin-Core tiene un gestionador para solicitar y entregar información, el RPC (remote procedure call) 


### Pre requisitos  <a name = "req"></a>

``` sh
git clone
cd BitcoinResearch/Python-Scripts
pip install -r req.txt
```

