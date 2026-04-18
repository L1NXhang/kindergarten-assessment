from datetime import datetime
from app.extensions import db


class Child(db.Model):
    """幼儿模型"""
    __tablename__ = 'children'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, comment='幼儿姓名')
    gender = db.Column(
        db.String(2),
        db.CheckConstraint("gender IN ('男', '女')"),
        comment='性别：男/女'
    )
    birth_date = db.Column(db.Date, comment='出生日期')
    class_id = db.Column(db.Integer, db.ForeignKey('class_groups.id'), nullable=False)
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：多对多通过anecdote_children表
    anecdotes = db.relationship(
        'Anecdote',
        secondary='anecdote_children',
        back_populates='children',
        lazy='dynamic'
    )

    def to_dict(self, include_class=False):
        data = {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'class_id': self.class_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_class and self.class_group:
            data['class_group'] = self.class_group.to_dict()
        return data
