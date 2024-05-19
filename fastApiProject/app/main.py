"""
@author: cs
@version: 1.0.0
@file: utils.py
@time: 2024/5/19 5:21
@description: 应用程序的入口点，包含FastAPI实例的创建和路由设置
"""
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.endpoints import auth
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.db.session import Base
from app.db.session import engine
from app.handlers.exception_handlers import (
    user_already_exists_exception_handler,
    invalid_credentials_exception_handler,
    custom_http_exception_handler,
    validation_exception_handler,
)
from app.middleware.logging_middleware import log_requests

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

# 日志中间件
app.middleware("http")(log_requests)

# 自定义异常处理器
app.add_exception_handler(UserAlreadyExistsException, user_already_exists_exception_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
