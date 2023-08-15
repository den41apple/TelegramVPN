"""
Модели БД
"""
from sqlalchemy import Column, Integer, String, Boolean

from .db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50))
    fz_user_id = Column(String(100), unique=True)
    fz_is_admin = Column(Boolean, default=False)
    fz_email = Column(String(100))
    # fz_generated_password = Column(String(100))  # Первоначально сгенерированный пароль при регистрации
