"""
@author: cs
@version: 1.0.0
@file: response.py
@time: 2024/5/19 8:08
@description: 
"""
from pydantic import BaseModel
from typing import Any, Optional, List


class BaseResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = []


class SuccessResponse(BaseResponse):
    code: int = 0
    message: str = 'success'
    data: List[None] = []


class ErrorResponse(BaseResponse):
    data: Optional[Any] = None


if __name__ == '__main__':
    pass
