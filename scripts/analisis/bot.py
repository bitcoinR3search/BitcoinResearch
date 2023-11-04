# este es el script 












import socket
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

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

@app.post("/notify")
async def notify_block(request: Request):
    block_info = await request.json()
    block_hash = block_info.get("hash")
    if not block_hash:
        raise HTTPException(status_code=400, detail="Block hash not provided")

    print(f"New block received: {block_hash}")
    return {"message": "Notification received"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
