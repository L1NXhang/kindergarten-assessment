# 导入所有模型，确保SQLAlchemy能注册所有表
from app.models.class_group import ClassGroup
from app.models.child import Child
from app.models.teacher import Teacher
from app.models.anecdote import Anecdote
from app.models.anecdote_child import AnecdoteChild
from app.models.assessment import Assessment, AssessmentReport

__all__ = [
    'ClassGroup',
    'Child',
    'Teacher',
    'Anecdote',
    'AnecdoteChild',
    'Assessment',
    'AssessmentReport',
]
