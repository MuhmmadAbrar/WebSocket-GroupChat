from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from models import Message

app = FastAPI()

active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    client_name = f"Client-{websocket.client.host}:{websocket.client.port}"
    
    active_connections.append((websocket, client_name))
    
    try:
        while True:
            message = await websocket.receive_text()
            
            for connection, name in active_connections:
                if connection != websocket:
                    await connection.send_text(f"{message} from {name}")
                    
    except WebSocketDisconnect:
        active_connections[:] = [conn for conn in active_connections if conn[0] != websocket]

@app.get("/status")
async def get_status():
    return {"status": "Server is running"}

@app.get("/active_clients")
def get_active_clients():
    res = []
    for key, name in active_connections:
        res.append(name)
    return {"active_clients: ": res}

@app.post("/send_message")
async def send_message(msg: Message):
    if not active_connections:
        raise HTTPException(status_code=400, detail = "No active websocket clients.")
    disconnected_clients = []
    for connection, name in active_connections:
        try:
            await connection.send_text(f"Server Broadcast: {msg.message}")
        
        except:
            disconnected_clients.append((connection,name))
    
    for conn in disconnected_clients:
        active_connections.remove(conn)
    
    return {"detail": f"Messsage broadcasted to {len(active_connections)} clients."}
