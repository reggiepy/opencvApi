# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/10/25 11:17
import io
import random

import numpy as np
from fastapi import Request, Response, File, UploadFile, HTTPException
from fastapi.routing import APIRouter
import cv2

from common_api.captcha_api import CaptchaApi

api = APIRouter()


@api.post("/block_puzzle_captcha/")
async def block_puzzle_captcha(bg_img: UploadFile = File(...), tp_img: UploadFile = File(...)):
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
