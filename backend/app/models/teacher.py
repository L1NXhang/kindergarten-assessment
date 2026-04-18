from datetime import datetime
from app.extensions import db


class Teacher(db.Model):
    """教师模型"""
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, comment='教师姓名')
    first_seen_at = db.Column(db.DateTime, comment='首次出现时间（从轶事记录中提取）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    anecdotes = db.relationship('Anecdote', backref='teacher', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'first_seen_at': self.first_seen_at.isoformat() if self.first_seen_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
