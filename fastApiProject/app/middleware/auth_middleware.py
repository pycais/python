"""
@author: cs
@version: 1.0.0
@file: auth_middleware.py
@time: 2024/5/26 1:15
@description: 用户认证中间件
"""

from fastapi import Request, HTTPException
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.logging_config import logger
from app.core.security import refresh_token
from app.schemas.base_response import ErrorResponse
from app.utils.code import Code

# 无需登录的接口
NO_AUTH_PATHS = ['/docs', '/openapi.json', "/token", "/api/v1/login", "/api/v1/register", "/api/v1/refresh-token"]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 检查路径是否在无需认证的路径列表中
        # print(request.url.path, ' --------------')
        if request.url.path in NO_AUTH_PATHS:
            response = await call_next(request)
            return response

        if "Authorization" not in request.headers:
            logger.error('%s: Authorization header missing', request.url)
            # return JSONResponse(status_code=401, content={"detail": "Authorization header missing"})
            return JSONResponse(
                status_code=401,
                content=ErrorResponse(code=Code.failed, message="Authorization header missing").model_dump()
            )

        # token = request.headers["Authorization"].split(" ")[1]
        token = request.headers["Authorization"]
        try:
            payload = refresh_token(token)
            user = payload.get('sub')
            request.state.user = user
        except JWTError:
            logger.error('%s: Invalid token, signature has expired', request.url)
            return JSONResponse(
                status_code=401,
                content=ErrorResponse(code=Code.failed, message="Invalid token, signature has expired").model_dump()
            )
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=ErrorResponse(code=Code.failed, message=e.detail).model_dump()
            )

        response = await call_next(request)
        return response
