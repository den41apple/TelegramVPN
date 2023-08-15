"""
Инициализация объектов базы данных
"""
from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy.orm import declarative_base
import config


engine = create_engine(url=config.TG_DB_URL, echo=config.TG_DB_ECHO)

metadata = MetaData()
Base = declarative_base(bind=engine, metadata=metadata)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50))
    fz_user_id = Column(String(100), unique=True)
