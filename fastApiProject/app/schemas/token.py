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


class TokenData(BaseModel):
    username: str
    refreshToken: str
    expires: int
    accessToken: str
    token_type: str


class ResponseToken(BaseModel):
    code: Optional[int] = 0
    message: str = 'success'
    data: TokenData


class RefreshToken(BaseModel):
    accessToken: str
    refreshToken: str
    expires: int


class RefreshTokenValue(BaseModel):
    code: Optional[int] = 0
    message: str = 'success'
    data: RefreshToken
