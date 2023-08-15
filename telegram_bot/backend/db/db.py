"""
Инициализация объектов базы данных
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import config



async_engine = create_async_engine(url=config.TG_DB_URL, echo=config.TG_DB_ECHO)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

metadata = MetaData()
Base = declarative_base(bind=async_engine, metadata=metadata)


