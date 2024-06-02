# 表迁移
```angular2html
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 目录结构详细说明

#### `app/`

主应用程序目录，包含所有的应用代码。

#### `app/main.py`

应用程序的入口点，包含FastAPI实例的创建和路由设置。

#### `app/core/`

核心配置和安全相关的代码：

- `config.py`：应用的配置文件。
- `security.py`：包含安全相关的逻辑，如密码哈希和验证。

#### `app/api/`

包含所有API路由和依赖：

- `deps.py`：路由依赖。

- ```
  v1/
  ```

  ：版本化的API，方便将来进行API版本管理。

  - ```
    endpoints/
    ```

    ：具体的API端点。

    - `auth.py`：认证相关的端点。
    - `users.py`：用户相关的端点。

#### `app/db/`

数据库相关的代码：

- `base.py`：包含SQLAlchemy的基础类。

- ```
  models/
  ```

  ：数据库模型。

  - `user.py`：用户模型。

- `session.py`：数据库会话的管理。

#### `app/schemas/`

Pydantic模式定义，用于请求和响应的数据验证：

- `token.py`：Token相关的模式。
- `user.py`：用户相关的模式。

#### `app/crud/`

封装的数据库操作：

- `user.py`：用户相关的CRUD操作。

#### `app/tests/`

测试代码：

- `test_user.py`：用户相关的测试。

#### `app/utils/`

实用工具函数：

- `utils.py`：常用工具函数。

#### `alembic/`

数据库迁移工具Alembic相关文件：

- `env.py`：Alembic环境配置。
- `versions/`：保存数据库迁移版本。

#### `.env`

环境变量配置文件。

#### `alembic.ini`

Alembic配置文件。

#### `requirements.txt`

项目的依赖项列表。

#### `README.md`

项目的说明文档。

#### `run.py`

运行应用的脚本。