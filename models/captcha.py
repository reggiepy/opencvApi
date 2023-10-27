from typing import Optional

from sqlmodel import Field

from models.base import BaseDateTime


class BlockPuzzleCaptcha(BaseDateTime):
    id: Optional[int] = Field(default=None, primary_key=True)
    img_bg: Optional[str] = Field(None, description="背景图片")
    img_tp: Optional[str] = Field(None, description="标记图片")
