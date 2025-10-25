from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from typing import Dict



class SocketConnectionManager:
    def __init__(self):
        self.socket_connections: Dict[int, Dict[int, WebSocket]] = {}
        #{room_id: {user_id: WebSocket}}

    async def connect(self, websocket: WebSocket, user_id: int, room_id: int):

        await websocket.accept()
        if room_id not in self.socket_connections:
            self.socket_connections[room_id] = {}
        self.socket_connections[room_id][user_id] = websocket


    async def disconnect(self, room_id: int, user_id: int):
        if room_id in self.socket_connections and user_id in self.socket_connections[room_id]:
            del self.socket_connections[room_id][user_id]


    async def broadcast(self, message: str, sender_id: int, room_id: int, websocket: WebSocket):
        if room_id in self.socket_connections:
            for user_id, connection in self.socket_connections[room_id].items():
                message = {
                    "sender_id": sender_id,
                    "text": message
                }

                await connection.send_text(message)



manager = SocketConnectionManager()
socket_router = APIRouter(prefix='/ws/chat')


@socket_router.websocket("/{room_id}/{user_id}")
async def websocket_connection(websocket: WebSocket, room_id: int, user_id: int):
    try:
        await manager.connect(websocket, user_id, room_id)
        while True:
            data = await websocket.receive_text()
            message = f"{user_id} has send  a message:{data}"
            await manager.broadcast(message, user_id, room_id, websocket)
    except WebSocketDisconnect:
        await manager.disconnect(room_id, user_id)
