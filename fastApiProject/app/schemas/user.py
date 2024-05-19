"""
@author: cs
@version: 1.0.0
@file: user.py
@time: 2024/5/19 5:20
@description: 用户相关的模式
"""
# app/schemas/user.py
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
