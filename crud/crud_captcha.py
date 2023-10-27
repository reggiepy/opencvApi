from crud.base import CRUDBase
from models.captcha import BlockPuzzleCaptcha
from schemas.captcha import BlockPuzzleCaptchaCreate, BlockPuzzleCaptchaUpdate


class CRUDBlockPuzzleCaptcha(CRUDBase[BlockPuzzleCaptcha, BlockPuzzleCaptchaCreate, BlockPuzzleCaptchaUpdate]):
    ...


captcha = CRUDBlockPuzzleCaptcha(BlockPuzzleCaptcha)
