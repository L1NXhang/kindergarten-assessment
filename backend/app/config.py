import os
from pathlib import Path


class Config:
    """应用配置"""

    # 安全密钥
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 数据库 - 使用instance目录下的SQLite文件
    BASE_DIR = Path(__file__).resolve().parent.parent
    INSTANCE_DIR = BASE_DIR / 'instance'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'sqlite:///' + str(INSTANCE_DIR / 'assessment.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DeepSeek API 配置
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
    DEEPSEEK_BASE_URL = 'https://api.deepseek.com'

    # 文件上传配置
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    UPLOAD_EXTENSIONS = ['.xlsx', '.xls']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Session Cookie 配置（局域网HTTP环境）
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # 分页默认值
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
