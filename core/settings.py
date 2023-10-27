# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/6/26 11:42
import platform
import sys
from configparser import ConfigParser
from pathlib import Path

from py3utils.pyinstaller_utils import PyinstallerUtils

BASE_DIR = Path(__file__).parent.parent.absolute()
# 元数据目录
BASE_DATA_DIR = Path("/data")
BASE_DATA_DIR.mkdir(parents=True, exist_ok=True)
# 用户项目元数据目录
BASE_PERSON_DIR = BASE_DATA_DIR.joinpath("yongfeng_backend")
BASE_PERSON_DIR.mkdir(parents=True, exist_ok=True)

Config = ConfigParser()
DATA_DIR = BASE_DIR.joinpath("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
# 项目配置目录
CONFIG_DIR = DATA_DIR.joinpath("config")
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
# 默认项目配置文件
DEFAULT_CONFIG_PATH = CONFIG_DIR.joinpath("default_config.ini")

# 用户配置目录
PERSON_CONFIG_DIR = BASE_PERSON_DIR.joinpath("config")
PERSON_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
# 用户配置文件
PERSON_CONFIG_PATH = PERSON_CONFIG_DIR.joinpath("config.ini")
if not PERSON_CONFIG_PATH.exists():
    # PERSON_CONFIG_PATH.write_text(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    PERSON_CONFIG_PATH.write_text("")

Config.read([DEFAULT_CONFIG_PATH, PERSON_CONFIG_PATH])

# 调试模式
DEBUG = False

# api config
HOST = '0.0.0.0'
PORT = 3450
# 指定api启动线程数量
WORKERS = Config.getint("base", "workers", fallback=1)
STATIC_DIR = Path(BASE_DIR).joinpath("static")

DATABASE = BASE_DIR.joinpath("database_current.db")
if PyinstallerUtils.is_build():
    EMPTY_DATABASE = BASE_DIR.joinpath("database_empty.db")
# Database
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE.as_posix()}"
SQLALCHEMY_ASYNC_DATABASE_URI = f"sqlite+aiosqlite:///{DATABASE.as_posix()}"

LOG_PATH = BASE_DIR.joinpath("logs")
LOG_PATH.mkdir(exist_ok=True, parents=True)
LOG_CONFIG = LOGGING_CFG = {
    "version": 1,
    "disable_existing_loggers": "False",
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "formatters": {
        "standard": {
            "format": "%(asctime)s -- %(levelname)s -- %(message)s"
        },
        "short": {
            "format": "%(levelname)s -- %(message)s"
        },
        "long": {
            "format": "%(asctime)s -- %(levelname)s -- %(message)s (%(funcName)s in %(filename)s):%(lineno)d]"
        },
        "free": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "root_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 100000,
            "backupCount": 5,
            "formatter": "long",
            "filename": LOG_PATH.joinpath("root.log"),
            "encoding": "utf-8"
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "long"
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOG_PATH).joinpath("fastapi_access.log"),
            "maxBytes": 100000,
            "backupCount": 5,
            "formatter": "long",
            "encoding": "utf-8"
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOG_PATH).joinpath("fastapi_error.log"),
            "maxBytes": 100000,
            "backupCount": 5,
            "formatter": "long",
            "encoding": "utf-8"
        },
        "yongfeng_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOG_PATH).joinpath("yongfeng.log"),
            "maxBytes": 100000,
            "backupCount": 5,
            "formatter": "long",
            "encoding": "utf-8"
        },
        "db_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOG_PATH).joinpath("db.log"),
            "maxBytes": 100000,
            "backupCount": 5,
            "formatter": "long",
            "encoding": "utf-8"
        },
    },
    "loggers": {
        "yongfeng": {
            "handlers": ["console", "yongfeng_file"],
            "level": "DEBUG" if DEBUG else "INFO",
            'propagate': False,
        },
        "uvicorn.access": {
            "level": "DEBUG" if DEBUG else "INFO",
            "handlers": ["access_file"],
            "propagate": False
        },
        "uvicorn.error": {
            "level": "DEBUG" if DEBUG else "INFO",
            "handlers": ["error_file"],
            "propagate": True
        },
        "sqlalchemy.engine": {
            "level": "DEBUG" if DEBUG else "INFO",
            "handlers": ["db_file"],
            "propagate": True
        },
    }
}

DINGDING_ACCESS_TOKEN = Config.get(
    "notify", "dingding_access_token",
    fallback="a965644755ae0d6b951702b29ce3d75c6d007de06416e99198b38034a2c59ee0"
)
DINGDING_SECRET = Config.get(
    "notify", "dingding_secret",
    fallback="SEC4d69d2b02070f1289d916a204736d477889613a22d118fe9d911bf4f3adf57cd"
)
# 激活码服务地址
LICENSE_CHECK_NEED = Config.getboolean(
    "base", "license_check_need",
    fallback=True
)
LICENSE_SERVER = Config.get(
    "base", "license_server",
    fallback="http://101.42.33.76:6306"
)
LICENSE_USER = Config.get(
    "base", "license_user",
    fallback="root"
)
LICENSE_PASSWORD = Config.get(
    "base", "license_password",
    fallback="user@dev"
)

LICENSE_SECRET = f"{LICENSE_USER}:{LICENSE_PASSWORD}"