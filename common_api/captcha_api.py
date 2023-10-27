# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/10/27 14:02
import io
import random

import cv2
import numpy as np


class CaptchaApi:
    @classmethod
    def block_puzzle_captcha(cls, bg_img, tp_img):
        if isinstance(bg_img, str):
            bg_image = cv2.imread(bg_img)
        elif isinstance(bg_img, io.BytesIO):
            file_bytes = np.asarray(bytearray(bg_img.read()), dtype=np.uint8)
            bg_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        else:
            return None, f"Invalid bg_img type: {type(bg_img)}", 1
        if isinstance(tp_img, str):
            tp_image = cv2.imread(tp_img)
        elif isinstance(tp_img, io.BytesIO):
            file_bytes = np.asarray(bytearray(tp_img.read()), dtype=np.uint8)
            tp_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        else:
            return None, f"Invalid tp_img type: {type(bg_img)}", 1
        # cv2.imshow('imshow1', bg_image)
        # cv2.imshow('imshow2', bg_image)

        # 识别图片边缘
        bg_edge = cv2.Canny(bg_image, 100, 200)
        tp_edge = cv2.Canny(tp_image, 100, 200)
        # cv2.imshow('imshow3', bg_edge)
        # cv2.imshow('imshow4', tp_edge)

        # 转换图片格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

        # 缺口匹配
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)

        x, y = np.unravel_index(res.argmax(), res.shape)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

        # 绘制方框
        th, tw = tp_pic.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标

        cv2.rectangle(bg_image, tl, br, (0, 0, 255), 2)  # 绘制矩形
        # cv2.imshow('imshow7', bg_image)
        # cv2.imwrite(dest_img_name, bg_image)  # 保存在本地

        # 背景的高度、宽度
        bh, bw = bg_image.shape[:2]

        fix = f"{random.choice(['-', '+'])}{random.uniform(0, 0.5)}"
        if tl[0] > bw / 2:
            move_px = tl[0]
        else:
            move_px = tl[0] - tw
            move_px = tl[0]
        fix_move_px = eval(f"{move_px}{fix}")
        print(move_px, fix, fix_move_px)
        # print(cls.diffImg(bg_image, bg_image))

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return move_px, "success", 0
