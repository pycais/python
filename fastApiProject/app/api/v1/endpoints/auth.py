"""
@author: cs
@version: 1.0.0
@file: auth.py
@time: 2024/5/19 5:19
@description: 
"""
# app/api/v1/endpoints/auth.py
import time
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBasicCredentials, HTTPBasic
from jose import JWTError
from sqlalchemy.orm import Session

from app.api.dedps import get_db
from app.core.config import settings
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException, InvalidTokenException
from app.core.security import verify_password, get_password_hash, create_access_token, refresh_token
from app.crud.user import get_user_by_username
from app.db.models.user import User
from app.schemas.base_response import BaseResponse, SuccessResponse
from app.schemas.token import Token, RefreshTokenValue
from app.schemas.user import UserCreate, UserLogin
from app.utils.code import Code
from app.core.logging_config import logger

router = APIRouter()
security2 = HTTPBasic()


@router.post('/demo', response_model=Token)
def demo(json_ii: UserLogin):
    print(json_ii.model_dump(), '------')
    return {"accessToken": 'access_token', "token_type": "bearer"}


@router.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security2)]):
    print('-------')
    return {"username": credentials.username, "password": credentials.password}


# @router.post("/login", response_model=Token)
# def login_for_access_token(json_data: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == json_data.username).first()
#     if not user or not security.verify_password(json_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = security.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     logger.info(f"User logged in: {user.username}")
#     return {"accessToken": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_for_access_token(json_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == json_data.username).first()
    if not user or not verify_password(json_data.password, user.hashed_password):
        logger.error(f"login error, user: {json_data.username}, is_exist: {bool(user)}")
        raise InvalidCredentialsException(code=Code.failed, message='login error, username or password error')
    access_token_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"User logged in: {user.username}")
    return {"accessToken": access_token, "token_type": "bearer"}


@router.post("/refresh-token", response_model=Token)
def refresh_access_token(token: RefreshTokenValue):
    try:
        print('toekn: ', token.refreshToken)
        payload = refresh_token(token.refreshToken)
        username = payload.get("sub")
        if username is None:
            # raise HTTPException(status_code=401, detail="Invalid token")
            raise InvalidTokenException(code=Code.failed, message='Invalid token')
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        # raise InvalidTokenException(code=Code.failed, message='Invalid token')

    new_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_token = create_access_token(data={"sub": username}, expires_delta=new_token_expires)
    return {"accessToken": new_token, "token_type": "bearer",
            'expires': int(time.time()) + timedelta(minutes=15).seconds}


@router.post("/register", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        # raise HTTPException(status_code=400, detail="user already registered")
        raise UserAlreadyExistsException(user.username)
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}
