"""
@author: cs
@version: 1.0.0
@file: test_user.py
@time: 2024/5/19 5:21
@description: 用户相关的测试
"""
import requests

# 设置 API 的基本 URL
base_url = "http://127.0.0.1:8000"

# 测试用户注册功能
def test_register_user():
    # 构造用户注册的数据
    data = {
        "email": "test@example.com",
        "password": "password"
    }
    # 发送 POST 请求进行用户注册
    response = requests.post(f"{base_url}/register", json=data)
    # 断言状态码为 200，表示注册成功
    assert response.status_code == 200
    # 打印响应内容
    print("User registered successfully")

# 测试用户登录和获取令牌功能
def test_login_and_get_token():
    # 构造用户登录的数据
    data = {
        "username": "test@example.com",
        "password": "password"
    }
    # 发送 POST 请求进行用户登录
    response = requests.post(f"{base_url}/token", data=data)
    # 断言状态码为 200，表示登录成功
    assert response.status_code == 200
    # 解析响应内容，获取访问令牌
    access_token = response.json()["access_token"]
    # 打印访问令牌
    print("Access Token:", access_token)

if __name__ == "__main__":
    # 运行测试函数
    test_register_user()
    test_login_and_get_token()