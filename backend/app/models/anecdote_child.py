from app.extensions import db


class AnecdoteChild(db.Model):
    """轶事-幼儿关联模型（多对多中间表）"""
    __tablename__ = 'anecdote_children'

    id = db.Column(db.Integer, primary_key=True)
    anecdote_id = db.Column(
        db.Integer,
        db.ForeignKey('anecdotes.id'),
        nullable=False
    )
    child_id = db.Column(
        db.Integer,
        db.ForeignKey('children.id'),
        nullable=False
    )
    confidence = db.Column(db.Float, default=1.0, comment='识别置信度')

    # 联合唯一约束
    __table_args__ = (
        db.UniqueConstraint('anecdote_id', 'child_id', name='uq_anecdote_child'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'anecdote_id': self.anecdote_id,
            'child_id': self.child_id,
            'confidence': self.confidence,
        }
