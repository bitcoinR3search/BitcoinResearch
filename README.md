# Bitcoin Research

![](/images/baner.png)

## ¡BIENVENIDO!

Este proyecto (bajo licencia MIT) brinda una plataforma completa para aprender y aplicar el manejo autogestionado y soberano de Bitcoin. Se muestra a detalle, paso a paso como se monta una infraestructura completa que aproveche el Blockchain de Bitcoin directamente, para no depender de ningun servicio/servidor externo o exchange.

Se cuenta con las siguientes caracteristicas:

- Servidor Electrum.
- Explorador de Bloques.
- Explorador de Mempool.
- Accesibles mediante TOR.
- Nodo completo en Mainnet.
- Nodo completo en Testnet.

## Contenido

El proyecto tiene la siguiente estructura.

---

:open_file_folder: Análisis Onchain/- Al disponer de un nodo sincronizado y actualizado en cada bloque se proponen realizar análisis de datos y obtener métricas. Para obtener la data habilitamos un API en el nodo accesible mediante comandos RPC (Remote Procedure Call) para bitcoin-cli y usando Python realizar análisis de cadena como: 
  - Análisis de transacciones: estudio de las transacciones realizadas en la red Bitcoin, como el volumen de transacciones, el valor transferido, los principales participantes, etc.
  - Análisis de minería: estudio de la actividad minera en la red Bitcoin, como la distribución de potencia de hash, la competencia entre mineros, etc.
  - Análisis de direcciones: estudio de las direcciones Bitcoin, como el número de direcciones activas, el saldo total, el número de transacciones, etc.
  - Análisis de patrones de uso: estudio de la utilización de Bitcoin, como el tipo de transacciones que se realizan, el uso de las direcciones, etc.

:open_file_folder: Apuntes/ - En esta carpeta esta el contenido para aprender sobre Bitcoin.

------> :open_file_folder: Blockchain Py/ - Es un ejercicio en Python para montar una propia red Bitcoin que tiene: Envío de transacciones, Minería y la prueba de trabajo POW, sincronización y validación de la cadena más larga (compentencia de varios nodos y mineros). 

------> :open_file_folder: Manuales/ - Material probado y testeado en el proyecto para montar la Infraestructura de Bitcoin y entender algunas tecnologías útiles como:
   - Nodo Competo en Mainnet con servidor Electrum, explorador de bloques, explorador de mempool.
   - Nodo en testnet, para probar desarrollos de Software para Bitcoin (Apps, scripts, wallets, etc). 
   - Firmas PGP.
   - Timestamps.
   - Opentimestamp.
   - Como configurar un super shell (portada). 

------> :open_file_folder: Posts/ - Distintas entradas (no son documentos técnicos) con temas variados relacionados con Bitcoin: Energía, Económia, Ciencias Computacionales, etc.

:open_file_folder: Bibliografía/ - Libros y papers que usamos como bibliografía para profundizar conceptos. 

:open_file_folder: Bots/ - Se desarrollan una serie de bots para que el nodo pueda desplegar información e interactuar con el mundo externo.

------> :open_file_folder: Twitter-Bot/ - La cuenta oficial del proyecto es [@nodobtcbot](https://twitter.com/nodobtcbot) 𓅪. Este bot esta hecho en Python y tiene las siguientes capacidades:
   - Auto generador de Banner con los últimos seguidores.
   - Despliega información si es invocado con algunos comandos (fee, hashrate, emisión, blockclock).
   - Tuitea estadísticas diariamente.

------> :open_file_folder: Twitter-Bot/ - El nodo tiene una cuenta Bot 🤖 de Telegram: [@onepi_bot](https://t.me/onepi_bot) desarrollado en Python tiene las siguientes capacidades:
   - Facilita la gestión del operador del nodo.
   - Herramienta para verificar archivos `.ots`
   - Herramienta para solicitar información de algun bloque o transacción para verificar las confirmaciones sin dar datos personales.

      ⚠️ Telegram no almacena el IP y con la configuración de privacidad adecuada no deja rastros de otros datos como nombres. El proyecto no almacena ni recopila datos (más que estadisticas de uso).

---



