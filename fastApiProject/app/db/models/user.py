"""
@author: cs
@version: 1.0.0
@file: user.py
@time: 2024/5/19 5:20
@description: 用户模型
"""
# app/db/models/user.py
from sqlalchemy import Column, Integer, String
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(64))
