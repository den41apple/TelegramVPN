"""
Модели БД
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

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
    fz_generated_password = Column(String(100))  # Первоначально сгенерированный пароль при регистрации
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now(), nullable=False)

    def __str__(self):
        return (
            f"User(id={self.id}, chat_id={self.chat_id}, first_name={self.first_name!r}, "
            f"last_name={self.last_name!r}, username={self.username!r}, "
            f"fz_user_id={self.fz_user_id!r}, fz_is_admin={self.fz_is_admin}, "
            f"fz_email={self.fz_email!r}, fz_generated_password={self.fz_generated_password!r})"
        )

    def __repr__(self):
        return str(self)


class DeeplinkAction(Base):
    __tablename__ = "deeplink_actions"
    id = Column(Integer, primary_key=True)
    deeplink_value = Column(String(100), unique=True, nullable=False, default="EMPTY")
    to_link = Column(Boolean, default=False)  # Привязка пользователя
    fz_user_id = Column(String(100), unique=True)
    to_create = Column(Boolean, default=False)  # Создание пользователя
