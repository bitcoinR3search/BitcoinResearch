''' 
Este script corre un bot que espera la llegada de nuevos bloques verificados
por el nodo con Bitcoin-Core y procesa los datos de la red para encontrar
nuevos ATH (all time high) y eventos propios de la red.

Para ello se corre un servidor API REST en un Rpi dedicado para procesar
datos. 

El script blocknotify muestra el envió desde el rpi1
al servidor rpi2
'''

import socket
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()



# El scrip se configura de manera que aprovecha el mdns
# donde el ip se enmascara en el mismo dispositivo
# previamente configurados. Solo acepta datos enviados
# desde rpi1 denegando cualquier otro. 

@app.middleware("http")
async def check_ip_middleware(request: Request, call_next):
    client_ip = request.client.host
    try:
        allowed_ip = socket.gethostbyname('nodeone.local')
    except socket.gaierror:
        return JSONResponse(content={"error": "Hostname resolution failed"}, status_code=500)
    
    if client_ip != allowed_ip:
        return JSONResponse(content={"error": "Forbidden"}, status_code=403)
    
    response = await call_next(request)
    return response

# Lo que sucede cuando llega un bloque es que se envia en formato diccionario
# el hash del nuevo bloque. PQ? pq la comunicación esta no esta encryptada, y 
# de tener un ataque, un middleware podría interceptar la comunicación
# unidireccional y reemplazar el dato. 
# Lo que seria evidente por el hash. 


@app.post("/notify")
async def notify_block(request: Request):
    block_info = await request.json()
    block_hash = block_info.get("hash")
    if not block_hash:
        raise HTTPException(status_code=400, detail="Block hash not provided")

    print(f"New block received: {block_hash}")
    return {"message": "Notification received"}
    analysis(block_hash)


if __name__ == '__main__':
    import uvicorn

    # Antes de empezar a lanzar el servidor, actualiza la base de datos

    uvicorn.run(app, host='0.0.0.0', port=8000)
