"""
@author: cs
@version: 1.0.0
@file: code.py
@time: 2024/5/19 8:32
@description: 
"""


class Code:
    success = 0
    failed = 1


class Co:
    # 成功自定义状态码
    success = 2000  # 通用成功，可选地用于区分HTTP200的成功响应，提供更多业务层面的细节。
    db_create = 2001  # 创建成功，比如新用户注册成功、新订单创建成功等。
    db_update = 2002  # 更新成功，数据更新操作无误。
    db_delete = 2003  # 删除成功，资源删除成功。

    # 客户端错误自定义状态码
    param_error = 1001  # 参数错误，请求参数缺失或格式不正确。
    validation_error = 1002  # 验证失败，如用户名密码错误、验证码错误。
    already_repeat = 1003  # 重复操作，比如尝试重复注册、重复提交表单。
    permission_error = 1004  # 访问受限，用户权限不足访问特定资源。

    # 服务器端错误自定义状态码
    server_error = 2001  # 服务器内部错误，未预期的异常。
    db_operation_failed = 2002  # 数据库操作失败，如查询失败、插入失败。
    resource_not_exist = 2004  # 资源不存在，请求的资源在服务器上未找到。

    # 业务逻辑错误自定义状态码
    token_expired = 3004  # 会话过期，用户的登录状态失效。
