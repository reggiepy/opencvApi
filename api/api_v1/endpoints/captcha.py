# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/10/25 11:17
import base64
import io

from fastapi import File, UploadFile, HTTPException
from fastapi.routing import APIRouter

from common_api.captcha_api import CaptchaApi
from schemas.captcha import BlockPuzzleCaptchaRequest

api = APIRouter()


@api.post("/block_puzzle_captcha/")
async def block_puzzle_captcha(
        bg_img: UploadFile = File(..., description="背景图片"),
        tp_img: UploadFile = File(..., description="缺口图片")
):
    io_bg_img = io.BytesIO()
    io_bg_img.write(await bg_img.read())
    io_bg_img.seek(0)

    io_tp_img = io.BytesIO()
    io_tp_img.write(await tp_img.read())
    io_tp_img.seek(0)
    out, err, rc = CaptchaApi.block_puzzle_captcha(io_bg_img, io_tp_img)
    if rc:
        raise HTTPException(500, err)
    return out


@api.post("/block_puzzle_captcha/base64image/")
def block_puzzle_captcha(req: BlockPuzzleCaptchaRequest):
    io_bg_img = io.BytesIO()
    io_bg_img.write(base64.b64decode(req.img_bg))
    io_bg_img.seek(0)

    io_tp_img = io.BytesIO()
    io_tp_img.write(base64.b64decode(req.img_tp))
    io_tp_img.seek(0)
    out, err, rc = CaptchaApi.block_puzzle_captcha(io_bg_img, io_tp_img)
    if rc:
        raise HTTPException(500, err)
    return out
