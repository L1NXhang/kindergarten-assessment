from datetime import datetime
from app.extensions import db


class ClassGroup(db.Model):
    """班级模型"""
    __tablename__ = 'class_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, comment='班级名称')
    age_group = db.Column(
        db.String(20),
        nullable=False,
        comment='年龄段：3-4岁/4-5岁/5-6岁'
    )
    academic_year = db.Column(db.String(20), comment='学年，如2025-2026')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    children = db.relationship('Child', backref='class_group', lazy='dynamic')
    anecdotes = db.relationship('Anecdote', backref='class_group', lazy='dynamic')
    assessments = db.relationship('Assessment', backref='class_group', lazy='dynamic')

    def to_dict(self, include_children_count=False):
        data = {
            'id': self.id,
            'name': self.name,
            'age_group': self.age_group,
            'academic_year': self.academic_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_children_count:
            data['children_count'] = self.children.count()
        return data
