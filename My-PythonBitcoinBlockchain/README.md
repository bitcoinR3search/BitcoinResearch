
# Blockchain.py


En este estudio vamos a revisar como funciona la tecnología detrás del #blockchain de #Bitcoin aplicando #Python. Se mostrará como se podría implementar conceptualmente. 

![My Image](./adjuntos/Pasted%20image%2020220311123607.png)

---

## Introducción

<font color="green"> Bitcoin </font> se presenta al mundo por primera vez en un paper en el año 2008. En ese documento técnico se propone una forma de realizar <font color="green">transferencias P2P de dinero electrónico</font>.  Tienen entre sus referencias a ocho fuentes sobre distintas tecnologías que se aplican en la propuesta. Estas tecnologías fueron ampliamente estudiadas con anterioridad a bitcoin, por ejemplo, la criptografía asimétrica (también llamada de llave pública) que basa su fundamento teórico en distintas técnicas matemáticas (para el cifrado de llave pública bitcoin utiliza el cifrado por curva elíptica ECC).

En el año 2009 se pone por primera vez el core de Bitcoin en funcionamiento, desplegando la solución planteada en el white paper meses antes. Se liberó el código para que cualquier persona en el mundo pueda ser parte del proyecto al ejecutarlo en su propio ordenador. Este "core bitcoin" es un programa de código abierto desarrollado, mantenido y mejorado constantemente por distintos developers que periodicamente proponen distintas mejoras que van desde el rendimiento hasta la seguridad. 

Este código libre se puede encontrar en Internet, el repositorio en Github que guarda una copia: https://github.com/bitcoin/bitcoin tiene el código original posteado por Satoshi escrito completamente en c++. Siendo Bitcoin Core un software tipo cliente usado para acceder a la red Bitcoin existen múltiples implementaciones que interactúan igualmente con esta red de Bitcoin. Hoy se pueden encontrar proyectos de Bitcoin Core escritos en Python por ejemplo.
En el estudio no se busca implementar un core completo en Bitcoin, sino explicar como funciona ilustrando conceptos involucrados.

---

## Entorno de trabajo

Para desarrollar el proyecto se ha optado usar Python por sus caracteristicas multiplaforma y multiparadigma. De manera que se pueda montar la aplicación Blockchain en cualquier sistema operativo y cualquier arquitectura (se ha probado en Mac, Windows, Debian y en RaspberryPi) aprovechando que Python permite la programación orientada a objetos. 

Para empezar se crea un nuevo entorno de trabajo que facilite la gestión de paquetes. 
``` sh
~ python -m venv blockchain
~ cd blockchain
~ source bin/activate
(blockchain)~ 
```

Se implementará un servicio API REST para que la red pueda interactuar mediante el protocolo HTTP. Existen distintos frameworks como Django o Flask que facilitan el trabajo en Python. En este caso se escogió usar FASTAPI por su velocidad de respuesta y rápida puesta en marcha. 

Para facilitar la instalación de todos los paquetes se puede descargar el repositorio de GitHub del proyecto e instalar la lista de requerimientos:

``` sh
(blockchain)~ git clone https://github.com/jpcrespo/bitcoin
(blockchain)~ pip install -r req.txt
```


### Scripts

Para poder facilitar la legibilidad del código se dividió el proyecto en dos scripts:

   - core.py
   Script que contiene las clases y métodos usados.
   
   - blockchain.py
   Script que conforma el comportamiento del API REST.

---


## Block of Blockchain

El principal componente base de un blockchain (cadena de bloques, en español) es el bloque. Este, es simplemente un conjunto de información en texto plano que contiene las siguientes categorías:
	
	indice - Muestra la posición del bloque en el orden que se añade al blockchain.
	
	Hash_anterior - El hash256 se puede entender como una compresión de la información del bloque anterior que se añade al nuevo bloque como una especie de firma. 
	
	transacciones - Es la parte del bloque que contiene las transacciones o movimientos de bitcoin que se desean realizar. 
	
	tiempo - Este es un sello de tiempo que marca el momento que el bloque es añadido al blockchain. Es una prueba de que la información que contiene el bloque existía en el momento en que se invoca la marca temporal. 
	
	nonce - Es un valor que se agrega al bloque para que el hash del mismo coincida con un criterio de dificultad. En el caso de bitcoin la dificultad se relaciona con la cantidad de ceros con la que inicia el hash del bloque. 

Cuando la cantidad de bloques es muy grande hacer la verificación hash a hash es muy costoso computacionalmente como también su requerimiento en memoria (hardware) va creciendo a medida que la cadena va creciendo. Para resolver este problema Bitcoin hace uso de los árboles de Merkle. 

![My Image](./adjuntos/Pasted%20image%2020220311125053.png)


El árbol de Merkle es una forma de estructurar datos. Al usar la verificación por hashes configura una capa de seguridad para evitar el problema de doble gasto o cambios en las transacciones. Permite verificar conjuntos de transacciones rápida y eficientemente con solo el hash padre, permitiendo verificar de manera 'ligera' toda la cadena de bloques sin la necesidad de descargar todo el blockchain. 

Por simplicidad para este proyecto no abordamos como se representan las transacciones usando el árbol de Merkle, sino simplemente como un texto plano. 

---

## core.py


Vamos a explicar cada sección de código.


### Librerias

Se usan las siguientes librerías:

	sys - acceder a las variables del interprete
	json - manejo de datos en formato JSON
	request - manejo de solicitudes http
	time - obtiene la hora del ordenador
	hashlib sha256 - módulo para aplicar hash
	urlparse - manejo de url 

![My Image](./adjuntos/Pasted%20image%2020220311125438.png)


### Función Hash

Un método que facilita obtener el hash de un bloque.

![My Image](./adjuntos/Pasted%20image%2020220311125711.png)

### Clase Bloque

Se define el constructor de un bloque, con la información que debe contener.

![My Image](./adjuntos/Pasted%20image%2020220311125610.png)

### Clase Blockchain

Se define el constructor blockchain inicializando varibles que serán comunes a lo largo del funcionamiento:

	dificultad = '0000' La dificultad en este estudio se debe específicar explícitamente siendo más costoso mientras más ceros contenga. 

	El valor de la dificultad en Bitcoin depende del poder computacional conjunto de la red de mineros. Este se actualiza en función del tiempo promedio en el que se obtienen los nuevos bloques, buscando que este tiempo aproximadamente sea de 10 min por bloque. De manera que la dificultad depende del poder computacional de la red Bitcoin. Mientras mayor sea este la dificultad ira aumentando.

	nodes = Un set con los nodos que conforman la red. (El set es una estructura en python que no asegura la unicidad de sus datos, es decir, no acepta duplicidad de ID)

	chain = Una lista que contiene la información de todos los bloques.

	transacciones_pendientes = Una lista donde se almacenan las transacciones solicitadas para ser verificadas en un nuevo bloque.

Los bloques contienen un campo de información del "Hash Anterior". Esto concatena un bloque con el anterior, sin embargo, el bloque 0 no tiene un bloque anterior. Para salvar esta dificultad se usa el hash de un texto que cumple la función de hash anterior. 
Con todos los campos de información (indice, hash anterior, transacciones (null), tiempo) se procesa un Proof of Work para obtener un nonce.

![My Image](./adjuntos/Pasted%20image%2020220311125903.png)

Todo este proceso se realiza al crear un objeto Blockchain a partir de su constructor. 
Si buscamos en un explorador del blockchain de bitcoin:

 https://explorer.bit2me.com/btc/block/00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048 

podemos encontrar el primer bloque de Bitcoin que fue verificado el 8 de enero del 2009. El bloque génesis conocido como Bloque \#0 fue minado unos días antes, el 3 de enero de 2009. 

![My Image](./adjuntos/Pasted%20image%2020220311130801.png)

El bloque génesis contenia el siguiente texto como prueba de la fecha de su creación:

>_“The Times 03 / Ene / 2009 Canciller al borde del segundo rescate para los bancos”_.

Este fue el titular del periódico The Times de esa fecha.

![My Image](./adjuntos/Pasted%20image%2020220311130939.png)
![My Image](./adjuntos/Pasted%20image%2020220311131007.png)

### Proof of Work

La prueba de trabajo (PoW por sus siglas en inglés) es un protocolo de consenso que consiste en que las partes de una red pueda llevar a cabo un trabajo computacionalmente costoso para que pueda ejecutar recursos del sistema. Esto se implementa con el objetivo de eliminar clientes maliciosos que desean modificar transacciones.

Este problema computacional no guarda complejidad ni utilidad práctica. Usa la fuerza bruta de prueba y error para resolverse y consiste en asignar un valor extra al bloque (llamado nonce), de manera que al evaluar su HASH256 el resultado empiece con una cantidad de ceros que coincida con la dificultad de la red. 

Obtener el hash256 del bloque es un proceso matemático computacionalmente fácil de realizar, la dificultad consiste en ir probando distintos nonces hasta obtener un hash válido. No existe otra forma de encontrar el nonce, convirtiendose en una suerte de lotería encontrar un hash válido ya que depende del número de hashes por segundo que se puedan obtener. 

Por esta razón mientras más aumenta el hash-rate global de la red bitcoin, más aumenta la dificultad.

![My Image](./adjuntos/Pasted%20image%2020220311131410.png)

La función empieza con un nonce, crea el bloque y verifica si es válido. Si no es válido aumenta el valor del nonce y vuelve a calcular el hash.

La válidación consiste en verificar que el hash del bloque empieza con la misma cantidad de ceros de la dificultad.

![My Image](./adjuntos/Pasted%20image%2020220311131452.png)

### Añadiendo bloques

Cuando se cumple el criterio de dificultad y la prueba de trabajo encuentra el nonce para el hash válido del bloque, se lo añade a la cadena. Cada vez que un bloque nuevo es minado y añadido contiene todas transacciones pendientes anterior a ese bloque.

En el ejemplo no existe un límite pero en la implementación del core de Bitcoin, un bloque tiene un tamaño máximo de 1 MB. Almacenando en cada bloque una cantidad limitada de transacciones. Aproximadamente se realizan 7 transacciones/segundo (en promedio).

![My Image](./adjuntos/Pasted%20image%2020220311131516.png)

También se facilita con una función el obtener el último bloque válido de la cadena de manera más directa.
   
![My Image](./adjuntos/Pasted%20image%2020220311131540.png)

### Añadir transacciones

Esta función añade transacciones para ser procesadas. Para lo cual se debe entregar cierta información:

	envia - Envía una cantidad de dinero
	recibe - Recibe la cantidad de dinero
	monto - La cantidad de dinero 

![My Image](./adjuntos/Pasted%20image%2020220311131621.png)

### Métodos de Sincronización

Cuando la aplicación final corre en un nodo, este debe formar una red con otros nodos que tienen su propio blockchain verificado y se encuentran en competencia para minar nuevos bloques. La sincronización asegura que se tenga por válida la cadena más larga y que esta copia sea común entre todos los nodos. 

El proceso pasa por verificar cada cadena que se propaga en la red en cada nodo. Por lo cual se debe registrar todos los nodos que conforman la red. 

![My Image](./adjuntos/Pasted%20image%2020220311131702.png)

### Validación en la sincronización

Esta función tiene como parámetro la cadena de bloques y verifica en dos tiempo la validez:

1. Comprueba que el hash_anterior que almacena un bloque n+1, sea igual al hash calculado del bloque n. De esta forma se verifica la integridad de la cadena.
2. Comprueba que el hash del bloque n+1 cumpla con el criterio de dificultad. De esta forma se verifica que el bloque es totalmente válido.

![My Image](./adjuntos/Pasted%20image%2020220311131804.png)

###  Update en la sincronización

Este método busca actualizar el blockchain a la copia válida más larga que se propague en la red.
Para cada nodo se verifica la integridad de TODA la cadena. Copiando como suya la cadena válida mas larga. 

![My Image](./adjuntos/Pasted%20image%2020220311131822.png)

---

## blockchain.py

Este segundo script se encarga del enrutamiento de las solicitudes HTTP de la aplicación API REST

### Librerias y setup

Se aplican las siguientes librerías

	uuid4 - módulo para crear identificadores id para los nodos.
	btc - módulo con las clases y métodos de btc.py
	Fastapi - Framework para manejo http
	pydantic - Estructura de datos para las solicitudes

![My Image](./adjuntos/Pasted%20image%2020220311131851.png)

En los métodos POST, que se usan para añadir transacciones y nodos, se declaran estructuras de datos esperados. Luego se genera un UUID cuando se ejecuta el script e inicia un objeto Blockchain (Cuyo constructor se detallo en btc.py). 

![My Image](./adjuntos/Pasted%20image%2020220311131920.png)

### Métodos de enrutamiento

En esta sección se especifican las rutas y el comportamiento que tendra la aplicación.

El nodo al ejecutar el script habilita la dirección IP para empezar a recibir solicitudes. Para consultar sus resultados se puede acceder por un navegador web mediante el puerto que se le indica. En el ejemplo el IP y puerto asignado al ordenador es:

http://192.168.1.3:5000

![My Image](./adjuntos/Pasted%20image%2020220311132018.png)

### Obtener la cadena de bloques

Cuando se accede al url: 
http://192.168.1.3:5000/chain

se obtiene una respuesta en JSON que contiene un diccionario con dos claves: 
La cadena "chain" y su largo "lenght".

![My Image](./adjuntos/Pasted%20image%2020220311132117.png)

### Minar un nuevo bloque

En este método se añade una transacción que se llama 'premio btc!' que representa la recompensa por añadir un nuevo bloque válido. Inicialmente este valor era de 50 BTC y esta diseñado para rebajar a la mitad este valor cada cierto periodo de tiempo (4 años), a este proceso de reducción de recompensa se le llama Halving. 

Como vimos bitcoin empezó a minarse en 2009, por lo cual hoy en día (2022) el premio de minado es 6.25 BTC y se estima que el año 2140 sea minado el último bitcoin para completar los 21 millones de bitcoins propuestos desde un inicio.

![My Image](./adjuntos/Pasted%20image%2020220311132145.png)

No existe otra forma de crear bitcoins, y este proceso guarda un registro de todas las formas en que se gastan desde que fueron minados. Esta transacción de recompensa es la que pone en movimiento todo bitcoin transferiendo a otros usuarios que no tienen un nodo que mine nuevos bloques. 

A esta transacción especial tipo incentivo se la denomina coinbase.

### Añadir nuevas transacciones/nodos

Mediante estas direcciones se pueden añadir información al blockchain:

1. Las transacciones que se van a emitir en cada bloque.
 
![My Image](./adjuntos/Pasted%20image%2020220311132201.png)

Para añadir una transacción basta con usar el comando \$ curl 
de la siguiente forma:
``` sh
curl -X 'POST'   'http://192.168.1.3:5000/transaciones/new' -H 'Content-Type: application/json' -d '{"envia": "ramona","recibe": "juanchex","monto": 666}'
```

Teniendo que editar la dirección de cada nodo al cual se solicita que procese una transacción.

2. Los nodos que conforman la red.

![My Image](./adjuntos/Pasted%20image%2020220311132514.png)

Se debe poner en conocimiento los nodos que conforman la red. Se puede realizar de la siguiente forma para cada nodo, suponiendo:

	ordenador 1   -  http://192.168.1.1:5000/
	ordenador 2  -  http://192.168.1.2:5000/

``` sh
curl -X POST 'http://192.168.1.1:5000/addnode'  -H 'Content-Type: application/json' -d '{"nodes" :"http://192.168.1.2:5000"}'

curl -X POST 'http://192.168.1.2:5000/addnode'  -H 'Content-Type: application/json' -d '{"nodes" :"http://192.168.1.1:5000"}'
```


### Sincronización de nodos

Mediante estas dirección se solicita al nodo que verifique las cadenas de la red y tome la copia de la cadena valida más larga. 

![My Image](./adjuntos/Pasted%20image%2020220311132905.png)

---

## Funcionamiento y Resultados. 

Mostramos algunos resultados y comparaciones:

Equipos usados:

1. Ordenador 1 - Intel i7 Windows10
	IP y puerto: 192.168.1.3:5000

	![My Image](./adjuntos/Pasted%20image%2020220311162045.png)
2. Ordenador 2 - Armv7 RaspberryPi3
	IP y puerto: 192.168.1.9:5000

	![My Image](./adjuntos/Pasted%20image%2020220311162005.png)
	

Corremos la aplicación en cada ordenador y usaremos el navegador Firefox para interactuar con cada uno.

### Obteniendo el Blockchain

Usando la dirección:

1. http://192.168.1.3:5000/chain

Obtenemos la siguiente respuesta.

![My Image](./adjuntos/Pasted%20image%2020220311164834.png)

2. http://192.168.1.9:5000/chain

Obtenemos la siguiente respuesta.

![My Image](./adjuntos/Pasted%20image%2020220311164859.png)


En ambos casos el bloque génesis parte del mismo texto base.  Es idéntico para ambos y se puede comprobar que tienen el mismo hash.
Sin embargo el primer bloque es distinto para ambas cadenas pues el sello de tiempo (timestamp) usado es distinto en ambos, y por lo tanto el nonce también. El primer bloque es completamente distinto.

### Añadiendo transacciones

Para mostrar como se van minando y añadiendo bloques, primero agregamos unas transacciones como ejemplo.
Para lo cual se mandan los siguientes comandos:

Para el 1er Ordenador:
``` sh
curl -X 'POST' 'http://192.168.1.3:5000/transaciones/new' -H 'Content-Type: application/json' -d '{"envia": "Ramona","recibe": "Juan","monto": 1.25}'
```

![My Image](./adjuntos/Pasted%20image%2020220311163509.png)

Para el 2do Ordenador:
``` sh
curl -X 'POST' 'http://192.168.1.9:5000/transaciones/new' -H 'Content-Type: application/json' -d '{"envia": "Eduardo","recibe": "Jose","monto": 0.0025}'
```

![My Image](./adjuntos/Pasted%20image%2020220311163530.png)

### Minando y agregando nuevos bloques

Una vez añadidas las transacciones, estas se guardar como una solicitud hasta que se mina un bloque nuevo. El tiempo que demora en minar un nuevo bloque depende del poder de computo donde se corre el nodo y de la dificultad que se fijó. 

1. Para el ordenador 1.
   
![My Image](./adjuntos/Pasted%20image%2020220311164939.png)

2. Para el ordenador 2

![My Image](./adjuntos/Pasted%20image%2020220311165015.png)

De esta forma, si volvermos a obtener el blockchain de por ejemplo, el ordenador 1 tenemos el siguiente cambio:

![My Image](./adjuntos/Pasted%20image%2020220311165137.png)

Aquí vale la pena hacer una pausa para comentar estos resultados:

1. El tiempo de minado de un bloque en un mismo ordenador no es constante entre bloques. Esto se debe porque el nonce buscado es aleatorio, en algún caso se obtiene muy pronto y en otros demora un poco más. Es por esta razón que se toma un promedio de este tiempo. <font color="green"> En Bitcoin la dificultad varía deacuerdo con este tiempo promedio, que debe ser aproximado a los ~10 min. por bloque </font>. Si en promedio el bloque demora menos de 10 min. la dificultad sube, y si demora más la dificultad baja. 
2. Cada cadena en los ejemplos es válida, pero la diferencia del tiempo en obtenerlas hace que una pueda creecer mas rápido que la otra. Esto se debe a que el poder de computo de un Intel i7 es muy superior a un Armv7. 

En este caso ejemplo, para mostrar la sincronización minamos en el ordenador 2 (Raspberry pi) diez bloques para mostrar la ventaja:

1. Ordenador 1 (intel)

![My Image](./adjuntos/Pasted%20image%2020220311170023.png)
2. Ordenador 2 (Rpi)
   
![My Image](./adjuntos/Pasted%20image%2020220311170142.png)

### Agregando Nodos

Hasta este momento ambas cadenas son válidas pero distintas entre ambas. Se busca tener  <font color="green"> una sola cadena </font> para lo cual ambos nodos deben saber de la existencia del otro.

Para lo cual añadimos la dirección:

Para el Ordenador 1.
``` sh
curl -X POST 'http://192.168.1.3:5000/addnode'  -H 'Content-Type: application/json' -d '{"nodes" :"http://192.168.1.9:5000"}'
```

![My Image](./adjuntos/Pasted%20image%2020220311170822.png)

Para el Ordenador 2.
``` sh
curl -X POST 'http://192.168.1.9:5000/addnode'  -H 'Content-Type: application/json' -d '{"nodes" :"http://192.168.1.3:5000"}'
```

![My Image](./adjuntos/Pasted%20image%2020220311170834.png)

De esta forma, ahora ambos sistemas saben de la existencia del otro. Cada uno ahora debe validar la cadena del otro y comparar si es más larga que la propia, tomando como cadena válida para toda la red la más larga.

### Sincronizando Nodos

Para que ambos nodos sincronicen su cadena de bloques accedemos para cada nodo a la dirección '...\/nodo\/sync'

Para este caso iniciamos con el Ordenador 2 que tiene la cadena válida más larga.
En la solicitud a http://192.168.1.9:5000/nodo/sync tenemos la siguiente respuesta:

![My Image](./adjuntos/Pasted%20image%2020220311171452.png)

Para el ordenador 1.

Con la solicitud  http://192.168.1.3:5000/nodo/sync tenemos la siguiente respuesta:

![My Image](./adjuntos/Pasted%20image%2020220311171610.png)

Ahora toda la red comparte la misma cadena de bloques.

1. Para el ordenador 1

![My Image](./adjuntos/Pasted%20image%2020220311171926.png)

 2. Para el ordenador 2
 
![My Image](./adjuntos/Pasted%20image%2020220311171805.png)

Ahora ambos nodos entregan la misma copia al solicitar la cadena de bloques.


