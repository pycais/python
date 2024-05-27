"""
@author: cs
@version: 1.0.0
@file: config.py
@time: 2024/5/19 5:16
@description: 应用的配置文件
"""
# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "My FastAPI Project"
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    ALGORITHM = "HS256"


settings = Settings()
