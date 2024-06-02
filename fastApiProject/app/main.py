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

from app.api.v1.endpoints import auth, poster
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.core.logging_config import logger
from app.db.session import Base
from app.db.session import engine
from app.handlers.exception_handlers import (
    user_already_exists_exception_handler,
    invalid_credentials_exception_handler,
    custom_http_exception_handler,
    validation_exception_handler,
)
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.logging_middleware import log_requests

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(poster.router, prefix="/api/v1", tags=["poster"])

# 日志中间件
app.middleware("http")(log_requests)

# 验证token中间件
app.add_middleware(AuthMiddleware)

# 自定义异常处理器
app.add_exception_handler(UserAlreadyExistsException, user_already_exists_exception_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
