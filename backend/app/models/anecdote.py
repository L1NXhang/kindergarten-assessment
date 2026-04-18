from datetime import datetime
from app.extensions import db


class Anecdote(db.Model):
    """轶事记录模型"""
    __tablename__ = 'anecdotes'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_groups.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    location = db.Column(db.String(200), comment='观察地点')
    activity_type = db.Column(db.String(100), comment='活动类型')
    observed_at = db.Column(db.DateTime, nullable=False, comment='观察时间')
    content = db.Column(db.Text, nullable=False, comment='观察内容')
    recognized_names = db.Column(db.Text, comment='识别到的姓名（JSON缓存）')
    status = db.Column(db.String(20), default='draft', comment='状态：draft/final')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：多对多通过anecdote_children表
    children = db.relationship(
        'Child',
        secondary='anecdote_children',
        back_populates='anecdotes',
        lazy='joined'
    )

    def to_dict(self, include_children=True):
        data = {
            'id': self.id,
            'class_id': self.class_id,
            'teacher_id': self.teacher_id,
            'location': self.location,
            'activity_type': self.activity_type,
            'observed_at': self.observed_at.isoformat() if self.observed_at else None,
            'content': self.content,
            'recognized_names': self.recognized_names,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_children:
            data['children'] = [c.to_dict() for c in self.children]
        return data
