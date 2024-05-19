"""
@author: cs
@version: 1.0.0
@file: auth.py
@time: 2024/5/19 5:19
@description: 
"""
# app/api/v1/endpoints/auth.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dedps import get_db
from app.core import security
from app.core.config import settings
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.core.security import verify_password, get_password_hash, create_access_token
from app.crud.user import get_user_by_username
from app.db.models.user import User
from app.schemas.response import BaseResponse, SuccessResponse
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.utils.code import Code
from app.core.logging_config import logger

router = APIRouter()


@router.post("/token1", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token2", response_model=SuccessResponse)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        # raise HTTPException(
        #     detail="Incorrect username or password",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
        logger.error(f"login error, user: {form_data.username}, is_exist: {bool(user)}")
        raise InvalidCredentialsException(code=Code.failed, message='login error, username or password error')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    return {'code': Code.success}


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
