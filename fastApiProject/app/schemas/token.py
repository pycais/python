"""
@author: cs
@version: 1.0.0
@file: token.py
@time: 2024/5/19 5:20
@description: Token相关的模式
"""
# app/schemas/token.py
import time

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    accessToken: str
    token_type: str
    code: Optional[int] = 1
    expires: int = int(time.time())
    refreshToken: str = ''
    username: str = 'qq'


class RefreshTokenValue(BaseModel):
    refreshToken: str
