"""
@author: cs
@version: 1.0.0
@file: logging_config.py
@time: 2024/5/20 2:13
@description: 日志配置
"""
# 日志格式
import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 日志文件处理器 (带有日志轮转)
file_handler = RotatingFileHandler(
    'logs/app.log', maxBytes=10485760, backupCount=3
)
file_handler.setFormatter(formatter)

# 获取日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)