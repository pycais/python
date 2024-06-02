"""
@author: cs
@version: 1.0.0
@file: logging_config.py
@time: 2024/5/20 2:13
@description: 日志配置
"""
# 日志格式
# import logging
# from logging.handlers import RotatingFileHandler
#
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - [%(filename)s-line:%(lineno)d] %(levelname)s - %(message)s'
# )
#
# # 控制台处理器
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
#
# # 日志文件处理器 (带有日志轮转)
# file_handler = RotatingFileHandler(
#     'logs/app.log', maxBytes=10485760, backupCount=3
# )
# file_handler.setFormatter(formatter)
#
# # 获取日志记录器
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)

import logging
import sys
from logging.config import dictConfig

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            # "format": "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            # "format": "%(asctime)s - %(name)s - [%(filename)s-line:%(lineno)d] %(levelname)s - %(message)s'",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/app.log",
            "formatter": "detailed",
            "level": "INFO",
            "encoding": "utf-8",  # Ensuring UTF-8 encoding
            "when": "midnight",  # Rotate at midnight
            "interval": 1,  # every day
            "backupCount": 30,  # Keep last 30 days' logs
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "sqlalchemy.engine": {
            "handlers": ["console", "file"],
            # "level": "INFO",
            "level": "WARN",
            "propagate": False,
        },
        "alembic": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    },
}

dictConfig(logging_config)

logger = logging.getLogger("app")
