# Análisis Onchain


<img alt="jpg" src="./images/onchain.png" width="400" height="200" style="vertical-align:middle;margin:10px
100px 25px">

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/drkostas/Youtube-FirstCommentBot/master/LICENSE)

---
## Tabla de Contenido

+ [Introducción](#intro)
+ [Instalando](#instalando)
    + [Prerequisitos](#req)
+ [Test Funcionamiento](#tests)
+ [Transacciones en Bitcoin](#tx)
+ [Scripts en python](#.py)
  + [hello world](#helloworld)

---
## Introducción  <a name = "intro"></a>

Con un nodo completo de Bitcoin que tenga completada la sinctronización se tiene una copia completa (y auto verificada) del blockchain, desde el primer bloque hasta el último nuevo que se genere. 

Este se configuró (ver [Bitcoin.conf](https://github.com/CobraPython/BitcoinResearch/blob/main/Apuntes/Manuales/Bitcoin.conf.pdf)) de tal forma que admite solicitudes RPC-Json desde otros ordenadores de la red interna para luego procesar data.

## Instalando  <a name = "instalando"></a>

Ya corriendo el nodo, se debe tener en cuenta las credenciales de acceso que se configuraron en el `bitcoin.conf`. Se deben disponer de `user y password` para acceder al RPC de Bitcoin Core. Este se deja 
### Pre requisitos  <a name = "req"></a>

Se crea un entorno de trabajo para Python.

``` sh
git clone
cd BitcoinResearch/Python-Scripts
pip install -r req.txt
```

