"""
@author: cs
@version: 1.0.0
@file: base.py
@time: 2024/5/19 5:19
@description: 包含SQLAlchemy的基础类
"""
# app/db/base.py
from app.db.session import Base
from app.db.models.user import User

# 导入你所有的模型到这里，使得Alembic能找到它们
