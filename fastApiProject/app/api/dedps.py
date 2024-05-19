"""
@author: cs
@version: 1.0.0
@file: config.py
@time: 2024/5/19 5:16
@description: 路由依赖
"""
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
