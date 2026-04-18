"""路由蓝图注册"""
from flask import Blueprint
from app.routes.classes import classes_bp
from app.routes.children import children_bp
from app.routes.anecdotes import anecdotes_bp
from app.routes.assessments import assessments_bp
from app.routes.reports import reports_bp
from app.routes.system import system_bp


def register_blueprints(app):
    """注册所有蓝图"""
    url_prefix = '/api/v1'

    app.register_blueprint(classes_bp, url_prefix=url_prefix)
    app.register_blueprint(children_bp, url_prefix=url_prefix)
    app.register_blueprint(anecdotes_bp, url_prefix=url_prefix)
    app.register_blueprint(assessments_bp, url_prefix=url_prefix)
    app.register_blueprint(reports_bp, url_prefix=url_prefix)
    app.register_blueprint(system_bp, url_prefix=url_prefix)
