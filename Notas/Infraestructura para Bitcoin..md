---
Título: 	==Infraestructura para Bitcoin.==
Fecha de creación: 10-25-2022 (mm/dd/aa)
Hora de creación: 17h22/utc-04
tags: ['#bitcoin','#linux','#raspberry']
aliases: [hardware para bitcoin , nodo en bitcoin]
---

Last Update: <%+ tp.file.last_modified_date("dddd D MMMM YYYY HH:mm:ss") %>

---

# Infraestructura para Bitcoin.


Una forma de ver #Bitcoin es como una red descentralizada de ordenadores.

https://bitnodes.io/
![[Pasted image 20221025175745.png]]

Cualquier persona puede integrarse a la Red, como puede salirse en cualquier momento. Para lo cual debe considerar dos cosas principalmente:

- Ordenador, computadora, laptop, etc. que pueda correr el cliente Bitcoin-core.
- Almacenamiento en Disco Duro. Bitcoin tiene una base de datos que va creciendo con el tiempo. A Noviembre de 2022, son aproximadamente 500 Gb que debe validarse. 

[Originalmente el cliente Bitcoin-Core fue escrito en C++ para correr bajo Windows](https://en.bitcoin.it/wiki/Original_Bitcoin_client). Hoy existen distintos clientes en distintos lenguajes para cualquier OS: windows, linux, macos. También para distintas arquitecturas, de 32 o 64 bits, de ARM o x86. 

Participar con un nodo en la Red Bitcoin dependerá del tipo de necesidad que se deba cubrir. 

En este proyecto proponemos una infraestructura mínima y completamente funcional de bajo costo.


## Requerimientos.

Se busca implementar los siguientes servicios:

- [ ] Participar en la Red Bitcoin y tener el Blockchain actualizado.
      Existen clientes que facilitan este punto como: Umbrel, Raspibolt, myNode, etc. Aunque la experiencia es muy buena para un user aficionado, limita mucho el desarrollo de herramientas sobre este. En algunos casos son características de pago para que usuarios avanzados 

- [ ] Obtener datos del Blockchain para realizar distintos análisis. 

- [ ] Automatizar análisis sobre los datos obtenidos.

- [ ] Bots que comuniquen e interactúen con la información elaborada. 




