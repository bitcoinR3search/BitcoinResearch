from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.post("/notify")
async def notify_block(request: Request):
    block_info = await request.json()
    block_hash = block_info.get("hash")
    if not block_hash:
        raise HTTPException(status_code=400, detail="Block hash not provided")

    print(f"New block received: {block_hash}")
    return {"message": "Notification received"}
