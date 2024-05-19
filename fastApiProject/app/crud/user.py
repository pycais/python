"""
@author: cs
@version: 1.0.0
@file: user.py
@time: 2024/5/19 5:21
@description: 用户相关的CRUD操作
"""
# app/crud/user.py
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from . import get_db

db = get_db()


def get_user_by_username(username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
