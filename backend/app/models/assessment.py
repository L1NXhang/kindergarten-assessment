from datetime import datetime, date
from app.extensions import db


class Assessment(db.Model):
    """评估任务模型"""
    __tablename__ = 'assessments'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_groups.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False, comment='评估标题')
    period_start = db.Column(db.Date, nullable=False, comment='评估周期开始日期')
    period_end = db.Column(db.Date, nullable=False, comment='评估周期结束日期')
    status = db.Column(
        db.String(20),
        default='pending',
        comment='状态：pending/generating/completed/failed'
    )
    created_by = db.Column(db.String(100), comment='创建者')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, comment='完成时间')

    # 关系
    reports = db.relationship('AssessmentReport', backref='assessment', lazy='dynamic',
                              cascade='all, delete-orphan')

    def to_dict(self, include_reports=False):
        data = {
            'id': self.id,
            'class_id': self.class_id,
            'title': self.title,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
        if include_reports:
            data['reports'] = [r.to_dict() for r in self.reports.all()]
        return data


class AssessmentReport(db.Model):
    """评估报告模型"""
    __tablename__ = 'assessment_reports'

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey('assessments.id'),
        nullable=False
    )
    report_type = db.Column(
        db.String(30),
        nullable=False,
        comment='报告类型：individual/class_summary/reflection'
    )
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=True)
    content = db.Column(db.Text, nullable=False, comment='报告内容')
    domain_scores = db.Column(db.Text, comment='五大领域评分（JSON）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    child = db.relationship('Child', backref='assessment_reports')

    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'report_type': self.report_type,
            'child_id': self.child_id,
            'child_name': self.child.name if self.child else None,
            'content': self.content,
            'domain_scores': self.domain_scores,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
