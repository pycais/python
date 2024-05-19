"""
@author: cs
@version: 1.0.0
@file: logging_middleware.py
@time: 2024/5/20 2:25
@description: 
"""
from fastapi import Request
from app.core.logging_config import logger


async def log_requests(request: Request, call_next):
    logger.info(f"New request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Completed request: {request.method} {request.url} with status {response.status_code}")
    return response


# # 日志中间件
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger.info(f"New request: {request.method} {request.url}")
#     response = await call_next(request)
#     logger.info(f"Completed request: {request.method} {request.url} with status {response.status_code}")
#     return response
#
# # 自定义异常处理器：处理用户已存在异常
# @app.exception_handler(UserAlreadyExistsException)
# async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsException):
#     logger.error(f"UserAlreadyExistsException: {exc.user} - {request.method} {request.url}")
#     return JSONResponse(
#         status_code=400,
#         content={"detail": f"User with email {exc.user} already exists."},
#     )
#
#
# # 自定义异常处理器：处理无效凭据异常
# @app.exception_handler(InvalidCredentialsException)
# async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
#     logger.error(f"InvalidCredentialsException: {request.method} {request.url}")
#     return JSONResponse(
#         status_code=401,
#         content={"detail": "Invalid username or password."},
#     )
#
#
# # 全局处理 HTTP 异常
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
#     logger.error(f"HTTPException: {exc.detail} - {request.method} {request.url}")
#     return await http_exception_handler(request, exc)
#
#
# # 全局处理请求验证错误
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     logger.error(f"RequestValidationError: {exc.errors()} - {request.method} {request.url}")
#     return JSONResponse(
#         status_code=422,
#         content={"detail": exc.errors(), "body": exc.body},
#     )
