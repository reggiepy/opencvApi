from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

from core import settings

sync_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=True,
    # 解决sqladmin查询数据库异常问题, 或者直接使用下面的 async_engine
    # sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.
    # The object was created in thread id 108204 and this is thread id 107824.
    connect_args={"check_same_thread": False}
)
SyncSession = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
async_engine = create_async_engine(settings.SQLALCHEMY_ASYNC_DATABASE_URI, echo=True, future=True)
AsyncSession = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with AsyncSession() as s:
        yield s


def get_sync_session() -> AsyncSession:
    with SyncSession() as s:
        yield s
