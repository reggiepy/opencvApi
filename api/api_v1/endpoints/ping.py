# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/2/28 10:08

from fastapi import Request, Response
from fastapi.routing import APIRouter

api = APIRouter()


@api.get("/")
async def ping(request: Request, response: Response):
    return "pong"


@api.post("/")
async def ping(request: Request, response: Response):
    print(await request.body())
    return {"status": "200"}
