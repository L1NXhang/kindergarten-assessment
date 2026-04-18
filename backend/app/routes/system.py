"""系统管理路由"""
from flask import Blueprint, request, jsonify
from app.extensions import db, csrf
from app.models.class_group import ClassGroup
from app.models.child import Child
from app.models.anecdote import Anecdote
from app.models.teacher import Teacher
from app.models.assessment import Assessment
from app.utils.response import success, error
from app.utils.validators import validate_upload_file
from app.services.backup import create_backup, restore_backup

system_bp = Blueprint('system', __name__)


@system_bp.route('/system/dashboard', methods=['GET'])
@csrf.exempt
def get_dashboard():
    """获取仪表盘统计数据"""
    # 基本统计
    total_classes = ClassGroup.query.count()
    total_children = Child.query.count()
    total_anecdotes = Anecdote.query.count()
    total_teachers = Teacher.query.count()
    total_assessments = Assessment.query.count()

    # 近期轶事（最近7天）
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_anecdotes = Anecdote.query.filter(Anecdote.observed_at >= week_ago).count()

    # 各年龄段统计
    age_groups = db.session.query(
        ClassGroup.age_group,
        db.func.count(Child.id).label('children_count'),
    ).outerjoin(Child, ClassGroup.id == Child.class_id).group_by(ClassGroup.age_group).all()

    age_group_stats = [
        {'age_group': ag, 'children_count': count}
        for ag, count in age_groups
    ]

    # 最近评估
    recent_assessments = Assessment.query.order_by(Assessment.created_at.desc()).limit(5).all()

    data = {
        'overview': {
            'total_classes': total_classes,
            'total_children': total_children,
            'total_anecdotes': total_anecdotes,
            'total_teachers': total_teachers,
            'total_assessments': total_assessments,
            'recent_anecdotes': recent_anecdotes,
        },
        'age_groups': age_group_stats,
        'recent_assessments': [a.to_dict() for a in recent_assessments],
    }

    return jsonify(success(data=data, message='获取仪表盘数据成功'))


@system_bp.route('/system/backup', methods=['POST'])
@csrf.exempt
def backup():
    """创建数据库备份"""
    result = create_backup()

    if result['success']:
        return jsonify(success(data=result, message=result['message']))
    else:
        return jsonify(error(result['message'])), 500


@system_bp.route('/system/restore', methods=['POST'])
@csrf.exempt
def restore():
    """从备份文件恢复数据库"""
    if 'file' not in request.files:
        return jsonify(error('请上传备份文件')), 400

    file = request.files['file']
    if not file.filename:
        return jsonify(error('请上传备份文件')), 400

    result = restore_backup(file)

    if result['success']:
        return jsonify(success(data=result, message=result['message']))
    else:
        return jsonify(error(result['message'])), 500


@system_bp.route('/system/teachers', methods=['GET'])
@csrf.exempt
def get_teachers():
    """获取教师列表"""
    teachers = Teacher.query.order_by(Teacher.created_at.desc()).all()
    data = [t.to_dict() for t in teachers]
    return jsonify(success(data=data, message='获取教师列表成功'))
