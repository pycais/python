"""
@author: cs
@version: 1.0.0
@file: token.py
@time: 2024/5/19 5:20
@description: Token相关的模式
"""
# app/schemas/token.py
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
