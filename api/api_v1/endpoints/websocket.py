# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/2/17 14:10
from typing import Dict, Any

from fastapi import WebSocket, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field
from starlette.websockets import WebSocketDisconnect

from core.common import logger

api = APIRouter(tags=["websocket"])

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <label>User ID: <input type="text" id="userId" autocomplete="off" value="wtt"/></label>
        <button onclick="connect(event)">Connect</button>
        <button id="clear" onclick="clearMessages()">Clear Message</button>
        <br>
        <form action="" onsubmit="sendMessage(event)">
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <hr>
        <ul id='messages'>
        </ul>
        <script>
            var ws = null;
            function connect(event) {
                var itemId = document.getElementById("userId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://127.0.0.1:3323/v1/ws/client?user_id=" 
                + itemId.value + "&test_flag=true");
                ws.onmessage = function(event) {
                    console.log(event.data)
                    if ( event.data === "pong" ){
                        return
                    }
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                ws.onclose = function(event) {
                    console.log(event.type)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
            function clearMessages() {
                document.getElementById('messages').innerHTML = "";
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[Any, WebSocket] = {}

    async def connect(self, websocket: WebSocket, ident: Any):
        if ident in self.active_connections:
            self.disconnect(ident)
        await websocket.accept()
        self.active_connections[ident] = websocket

    def disconnect(self, ident: Any):
        if ident in self.active_connections:
            del self.active_connections[ident]
            try:
                self.active_connections[ident].close()
            except Exception:
                pass

    async def send_personal_message(self, message: str, ident: Any):
        if ident in self.active_connections:
            websocket = self.active_connections[ident]
            try:
                await websocket.send_text(message)
            except Exception:
                self.disconnect(ident)
            return True, "sent message successfully"
        return False, "连接不存在"

    async def broadcast(self, message: str):
        for ident in list(self.active_connections.keys()):
            await self.send_personal_message(message, ident)


manager = ConnectionManager()


@api.get(
    "/",
    name="test websocket connection",
    description="test websocket connection",
)
async def websocket_index():
    return HTMLResponse(html)


@api.websocket("/client")
async def websocket_endpoint(
        websocket: WebSocket,
        user_id: str = Query(..., description="user id"),
        platform: str = Query("", description="平台"),
        version: str = Query("", description="版本"),
        test_flag: bool = Query(False, description="test flag"),
):
    ident = gen_ident(user_id=user_id)
    await manager.connect(websocket, ident)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
            else:
                await manager.send_personal_message(f"You wrote: {data}", ident)
                if test_flag:
                    await manager.broadcast(f"Client #{ident} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(ident)
        if test_flag:
            await manager.broadcast(f"Client #{ident} left the chat")
    except Exception as e:
        logger.error(f"Client #{ident} error: {e}")


class MessageRequest(BaseModel):
    message: str = Field(..., description="message")


class MessageResponse(BaseModel):
    code: int = Field(..., description="code")
    message: str = Field(..., description="message")
    result: Any = Field(..., description="result")


class Code:
    CODE_MESSAGE_MAP = {}
    SUCCESS = 200
    CODE_MESSAGE_MAP[SUCCESS] = "Success"
    FAILED = 500
    CODE_MESSAGE_MAP[FAILED] = "Failed"

    @classmethod
    def gen_result(cls, code, result, message=None):
        if message is None:
            if code in cls.CODE_MESSAGE_MAP:
                message = cls.CODE_MESSAGE_MAP[code]
            else:
                raise ValueError(f"message must not be None")
        return MessageResponse(code=code, message=message, result=result)


def gen_ident(user_id):
    return f"{user_id}"


@api.post(
    "/send",
    name="Send a message to websocket",
    description="Send a message to websocket",
)
async def websocket_send(
        request: Request,
        data: MessageRequest,
        user_id: str = Query(..., description="user id"),
        platform: str = Query("", description="平台"),
        version: str = Query("", description="版本"),
):
    result = {}
    ident = gen_ident(user_id=user_id)
    try:
        status, msg = await manager.send_personal_message(message=data.message, ident=ident)
    except WebSocketDisconnect:
        manager.disconnect(ident)
    except Exception as e:
        return Code.gen_result(Code.FAILED, result, message=str(e))
    else:
        if not status:
            return Code.gen_result(Code.FAILED, result, message=msg)
    return Code.gen_result(Code.SUCCESS, result)
