# Este bot es un servidor API - REST que escucha la llegada
# de nuevos bloques desde el nodo. Procesa los datos para
# encontrar ATH en: 
# 1 Hashrate promedio movil de 1 semana
# 2 block time total 
# 3 block time halv
# 4 dificultad

#############################################################
# Librerias

import uvicorn
from app.bot import actualizar, data_metrics, analisis
from fastapi import FastAPI, HTTPException, Request


app = FastAPI()


# Esta sección escucha la llegada de nuevos bloques
# cuando llegan analiza si hay nuevos ATH.
@app.post("/notify")
async def notify_block(request: Request):
    if request.client.host != "127.0.0.1":
        return {"error": "Forbidden"}, 403

    block_info = await request.json()
    block_hash = block_info.get("hash")
    if not block_hash:
        raise HTTPException(status_code=400, detail="Block hash not provided")

    print(f"Nuevo bloque recibido: {block_hash}")
    analisis(hash=block_hash)
    return {"message": "Notification received"}




if __name__ == '__main__':
    # lo primero que hace es sincronizar la base de datos 
    # con el ultimo bloque de la red
    actualizar()
    # luego se realiza el calculo de ATH de la red con los
    # datos actualizados
    data_metrics()
    # una vez que los datos estan procesados se lanza el
    # servidor en localhost y puerto 8000
    uvicorn.run(app, host='127.0.0.1', port=8000)

