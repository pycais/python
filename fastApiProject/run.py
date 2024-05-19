"""
@author: cs
@version: 1.0.0
@file: run.py
@time: 2024/5/19 5:26
@description: 运行应用的脚本
"""
from app.main import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True)
