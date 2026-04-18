import os
from pathlib import Path
from flask import Flask, send_from_directory
from dotenv import load_dotenv
from flask_talisman import Talisman

from app.config import Config
from app.extensions import db, csrf


def create_app(config_class=Config):
    """Flask应用工厂函数"""

    # 加载.env文件
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder=str(Path(__file__).resolve().parent.parent / 'static'),
    )
    app.config.from_object(config_class)

    # 确保instance目录存在
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(str(app.config['UPLOAD_FOLDER']), exist_ok=True)
    os.makedirs(str(Path(__file__).resolve().parent.parent / 'backups'), exist_ok=True)

    # 初始化扩展
    db.init_app(app)
    csrf.init_app(app)

    # 配置Flask-Talisman安全头
    csp = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: blob:",
        'font-src': "'self' data:",
        'connect-src': "'self'",
    }
    Talisman(
        app,
        force_https=False,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'],
    )

    # 导入模型（确保所有模型在create_tables之前注册）
    from app.models import (  # noqa: F401
        ClassGroup, Child, Teacher,
        Anecdote, AnecdoteChild,
        Assessment, AssessmentReport,
    )

    # 创建数据库表
    with app.app_context():
        db.create_all()

    # 注册蓝图
    from app.routes import register_blueprints
    register_blueprints(app)

    # catch-all路由：服务前端静态文件（SPA）
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        static_folder = app.static_folder
        if static_folder and os.path.exists(static_folder):
            if path and os.path.exists(os.path.join(static_folder, path)):
                return send_from_directory(static_folder, path)
            # SPA fallback: 返回index.html
            index_path = os.path.join(static_folder, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder, 'index.html')
        return {'code': 200, 'message': '幼儿园评估系统API服务运行中', 'data': None}, 200

    return app
