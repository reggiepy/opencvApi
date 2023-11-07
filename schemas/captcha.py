from typing import Optional

from pydantic import BaseModel, Field


# Shared properties
class BlockPuzzleCaptchaBase(BaseModel):
    img_bg: Optional[str] = Field(None, description="背景图片")
    img_tp: Optional[str] = Field(None, description="标记图片")


class BlockPuzzleCaptchaRequest(BlockPuzzleCaptchaBase):
    img_bg: Optional[str] = Field(..., description="背景图片")
    img_tp: Optional[str] = Field(..., description="标记图片")


class BlockPuzzleCaptchaResponse(BaseModel):
    move_px: int = 0
    fix_move_px: int = 0
    fix_px: int = 0
    match_image_base64: str = ""


# Properties to receive on item creation
class BlockPuzzleCaptchaCreate(BlockPuzzleCaptchaBase):
    img_bg: str
    img_tp: str


# Properties to receive on item update
class BlockPuzzleCaptchaUpdate(BlockPuzzleCaptchaBase):
    pass


# Properties shared by models stored in DB
class BlockPuzzleCaptchaInDBBase(BlockPuzzleCaptchaBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class BlockPuzzleCaptcha(BlockPuzzleCaptchaInDBBase):
    pass


# Properties properties stored in DB
class BlockPuzzleCaptchaInDB(BlockPuzzleCaptchaInDBBase):
    pass
