"""
@author: cs
@version: 1.0.0
@file: exceptions.py
@time: 2024/5/20 1:22
@description: 异常处理
"""


class UserAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.user = username


class InvalidCredentialsException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
