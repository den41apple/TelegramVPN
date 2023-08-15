"""
Инициализация объектов базы данных
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
import config


engine = create_engine(url=config.TG_DB_URL, echo=config.TG_DB_ECHO)

metadata = MetaData()
Base = declarative_base(bind=engine, metadata=metadata)


