# 文化遗产档案系统

## 项目简介

文化遗产档案系统是一个基于 Python Flask 框架开发的 Web 应用，用于管理和展示中国文化遗产档案信息。系统支持档案的录入、分类浏览、全文搜索、图片展示、报告导出以及用户管理等功能。

## 适用场景

- 博物馆、文化馆等机构的文物档案数字化管理
- 文化遗产保护项目的资料整理与归档
- 学术研究中的文物信息检索与整理
- 文化教育展示平台

## 核心功能

1. **档案管理**：支持文化遗产档案的创建、编辑、删除和查看，包含标题、描述、年代、地点、图片等字段
2. **分类浏览**：支持按书法、绘画、陶瓷、青铜器、织绣、建筑等分类浏览档案，支持树形分类结构
3. **全文搜索**：支持按标题、描述、年代、地点进行关键词搜索，支持分类和状态筛选
4. **图片展示**：支持上传和展示档案相关图片
5. **报告导出**：支持将档案数据导出为 CSV 格式，支持导出统计摘要文本
6. **用户管理**：支持用户注册、登录、登出，区分管理员、编辑员、浏览者三种角色
7. **合集管理**：支持创建合集并将多个档案归入同一合集进行分组管理

## 技术栈

- **后端**：Python 3.11 + Flask 3.0
- **数据库**：SQLite（通过 Flask-SQLAlchemy ORM）
- **认证**：Flask-Login
- **模板引擎**：Jinja2
- **前端**：原生 HTML/CSS/JavaScript
- **部署**：Docker

## 目录结构

```
repo/
├── app.py                  # 应用入口
├── config.py               # 配置文件
├── seed.py                 # 种子数据脚本
├── requirements.txt        # Python 依赖
├── instance/               # SQLite 数据库目录
├── app/
│   ├── __init__.py         # Flask 应用工厂
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py         # 用户模型
│   │   ├── archive.py      # 档案模型
│   │   ├── category.py     # 分类模型
│   │   └── collection.py   # 合集模型
│   ├── services/
│   │   ├── __init__.py
│   │   ├── archive_service.py   # 档案服务
│   │   ├── category_service.py  # 分类服务
│   │   ├── collection_service.py # 合集服务
│   │   └── report_service.py    # 报告服务
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py         # 首页路由
│   │   ├── auth.py         # 认证路由
│   │   ├── archives.py     # 档案路由
│   │   ├── categories.py   # 分类路由
│   │   ├── collections.py  # 合集路由
│   │   ├── reports.py      # 报告路由
│   │   └── api.py          # API 路由
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── archives/
│   │   ├── categories/
│   │   ├── collections/
│   │   ├── reports/
│   │   ├── auth/
│   │   └── partials/
│   └── static/
│       ├── css/style.css
│       ├── js/main.js
│       └── images/
```

## Docker 启动方式

```bash
# 构建镜像
docker build -t culture-archive .

# 运行容器
docker run -d -p 5000:5000 -p 2222:22 culture-archive

# 访问应用
# 浏览器打开 http://localhost:5000
```

## 本地启动方式

```bash
# 进入项目目录
cd repo

# 安装依赖
pip install -r requirements.txt

# 初始化数据库并启动
python app.py

# 访问应用
# 浏览器打开 http://localhost:5000
```

## 默认账号

| 用户名    | 密码       | 角色   |
|-----------|------------|--------|
| admin     | admin123   | 管理员 |
| editor    | editor123  | 编辑员 |
| viewer    | viewer123  | 浏览者 |

## 可扩展方向

- 增加档案审核工作流，支持多级审批
- 集成 OCR 识别，自动提取文物铭文信息
- 增加地图可视化，按地理位置展示文化遗产分布
- 支持多语言国际化
- 增加 RESTful API 文档（Swagger/OpenAPI）
- 集成全文搜索引擎（如 Elasticsearch）提升搜索性能
- 增加数据备份与恢复功能
- 支持批量导入导出档案数据
- 增加用户操作日志审计
- 支持 IIIF 协议的高清图片展示
