# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/2/17 14:57
from fastapi import Depends
from fastapi.routing import APIRouter

from api.api_v1.endpoints import websocket, ping

api_router = APIRouter(prefix="/v1")
api_router.include_router(ping.api, prefix="/ping", tags=["ping"])
api_router.include_router(websocket.api, prefix="/ws")
