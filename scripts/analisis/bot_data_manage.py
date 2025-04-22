from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.post("/notify")
async def notify_block(request: Request):
    if request.client.host != "127.0.0.1":
        return {"error": "Forbidden"}, 403

    # Obtener los datos del cuerpo de la solicitud
    body = await request.json()
    n = body.get("tipo")
    data = body.get("data")

    # Imprimir los valores recibidos
    print(n, data)
    
    return {"message": "Notification received"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
