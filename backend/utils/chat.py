from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List

# WebSocket 관리 클래스
class ChatRoom:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)

    def add_connection(self, websocket: WebSocket):
        self.connections.append(websocket)

    def remove_connection(self, websocket: WebSocket):
        self.connections.remove(websocket)

class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[int, ChatRoom] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom()
        await websocket.accept()
        self.rooms[room_id].add_connection(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.rooms:
            self.rooms[room_id].remove_connection(websocket)
            if not self.rooms[room_id].connections:
                del self.rooms[room_id]

    async def send_message(self, room_id: int, message: str):
        if room_id in self.rooms:
            await self.rooms[room_id].broadcast(message)

manager = ConnectionManager()