"""
@author: cs
@version: 1.0.0
@file: exception_handlers.py
@time: 2024/5/20 2:19
@description: 
"""
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.core.logging_config import logger
from app.schemas.base_response import ErrorResponse
from app.utils.code import Code


async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsException):
    logger.error(f"UserAlreadyExistsException: {exc.user} - {request.method} {request.url}")
    return JSONResponse(
        status_code=400,
        content={"detail": f"User with user {exc.user} already exists."},
    )


# 自定义异常处理器：处理无效凭据异常
async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    logger.error(f"InvalidCredentialsException: {request.method} {request.url}")
    return JSONResponse(
        status_code=401,
        content=ErrorResponse(code=exc.code, message=exc.message).model_dump(),
    )


# 全局处理 HTTP 异常
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTPException: {exc.detail} - {request.method} {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(code=Code.failed, message=exc.detail).model_dump(),
    )


# 全局处理请求验证错误
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(request.body())
    logger.error(f"RequestValidationError: {request.url} {request.method} - {exc.errors()} - {exc.body}")
    messages = []
    for err in exc.errors():
        params = err.get('loc')[1] if len(err.get('loc')) == 2 else err.get('loc')
        err_type = err.get('type')
        msg = err.get('msg')
        _input = err.get('input')
        messages.append(f'request params: {params} {msg}, but {err_type}, input: {_input}')
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(code=Code.failed, message='; '.join(messages)).model_dump(),
    )
