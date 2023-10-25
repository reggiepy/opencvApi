# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/10/17 10:57
import logging

from core.db.init_db import init_db
from core.db.session import session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = session()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()