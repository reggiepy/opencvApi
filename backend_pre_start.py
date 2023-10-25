# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/10/17 11:06
import logging

from core.db.session import session
from py3utils.wrapper_utils import try_catch_factory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@try_catch_factory(
    times=2,
)
def init() -> None:
    try:
        db = session()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
