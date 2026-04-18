"""轶事记录管理路由"""
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db, csrf
from app.models.anecdote import Anecdote
from app.models.anecdote_child import AnecdoteChild
from app.models.child import Child
from app.models.class_group import ClassGroup
from app.utils.response import success, error
from app.services.name_recognition import NameRecognizer

anecdotes_bp = Blueprint('anecdotes', __name__)


@anecdotes_bp.route('/anecdotes', methods=['GET'])
@csrf.exempt
def get_anecdotes():
    """获取轶事记录列表（分页）"""
    class_id = request.args.get('class_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    child_id = request.args.get('child_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Anecdote.query

    if class_id:
        query = query.filter_by(class_id=class_id)

    if date_from:
        try:
            dt_from = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Anecdote.observed_at >= dt_from)
        except ValueError:
            pass

    if date_to:
        try:
            dt_to = datetime.strptime(date_to, '%Y-%m-%d')
            # 包含当天结束
            dt_to = dt_to.replace(hour=23, minute=59, second=59)
            query = query.filter(Anecdote.observed_at <= dt_to)
        except ValueError:
            pass

    if child_id:
        query = (
            query
            .join(AnecdoteChild, AnecdoteChild.anecdote_id == Anecdote.id)
            .filter(AnecdoteChild.child_id == child_id)
        )

    query = query.order_by(Anecdote.observed_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    data = {
        'items': [a.to_dict(include_children=True) for a in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
        },
    }

    return jsonify(success(data=data, message='获取轶事记录列表成功'))


@anecdotes_bp.route('/anecdotes', methods=['POST'])
@csrf.exempt
def create_anecdote():
    """创建轶事记录（自动识别姓名）"""
    data = request.get_json()
    if not data:
        return jsonify(error('请求数据为空')), 400

    content = data.get('content', '').strip()
    if not content:
        return jsonify(error('观察内容不能为空')), 400

    class_id = data.get('class_id')
    if not class_id:
        return jsonify(error('请指定班级')), 400

    # 验证班级存在
    class_group = ClassGroup.query.get(class_id)
    if not class_group:
        return jsonify(error('班级不存在')), 404

    # 解析观察时间
    observed_at = data.get('observed_at')
    if observed_at:
        try:
            observed_at = datetime.fromisoformat(observed_at)
        except (ValueError, TypeError):
            observed_at = datetime.utcnow()
    else:
        observed_at = datetime.utcnow()

    # 创建轶事记录
    anecdote = Anecdote(
        class_id=class_id,
        teacher_id=data.get('teacher_id'),
        location=data.get('location'),
        activity_type=data.get('activity_type'),
        observed_at=observed_at,
        content=content,
        status=data.get('status', 'draft'),
    )
    db.session.add(anecdote)
    db.session.flush()  # 获取anecdote.id

    # 自动识别姓名
    recognizer = NameRecognizer()
    recognition = recognizer.recognize(content, class_id)

    # 关联识别到的幼儿
    for child_info in recognition.get('children', []):
        ac = AnecdoteChild(
            anecdote_id=anecdote.id,
            child_id=child_info['id'],
            confidence=child_info.get('confidence', 1.0),
        )
        db.session.add(ac)

    # 关联教师
    teacher_info = recognition.get('teacher')
    if teacher_info:
        anecdote.teacher_id = teacher_info['id']

    # 缓存识别结果
    anecdote.recognized_names = json.dumps(recognition, ensure_ascii=False)

    db.session.commit()

    return jsonify(success(data=anecdote.to_dict(include_children=True), message='创建轶事记录成功')), 201


@anecdotes_bp.route('/anecdotes/<int:anecdote_id>', methods=['GET'])
@csrf.exempt
def get_anecdote(anecdote_id):
    """获取轶事记录详情"""
    anecdote = Anecdote.query.get(anecdote_id)
    if not anecdote:
        return jsonify(error('轶事记录不存在')), 404

    return jsonify(success(data=anecdote.to_dict(include_children=True)))


@anecdotes_bp.route('/anecdotes/<int:anecdote_id>', methods=['PUT'])
@csrf.exempt
def update_anecdote(anecdote_id):
    """更新轶事记录"""
    anecdote = Anecdote.query.get(anecdote_id)
    if not anecdote:
        return jsonify(error('轶事记录不存在')), 404

    data = request.get_json()
    if not data:
        return jsonify(error('请求数据为空')), 400

    if 'content' in data:
        content = data['content'].strip()
        if content:
            anecdote.content = content

    if 'class_id' in data:
        anecdote.class_id = data['class_id']

    if 'teacher_id' in data:
        anecdote.teacher_id = data['teacher_id']

    if 'location' in data:
        anecdote.location = data['location']

    if 'activity_type' in data:
        anecdote.activity_type = data['activity_type']

    if 'observed_at' in data:
        try:
            anecdote.observed_at = datetime.fromisoformat(data['observed_at'])
        except (ValueError, TypeError):
            pass

    if 'status' in data:
        anecdote.status = data['status']

    # 更新关联的幼儿
    if 'child_ids' in data:
        child_ids = data['child_ids']
        # 删除旧关联
        AnecdoteChild.query.filter_by(anecdote_id=anecdote_id).delete()
        # 添加新关联
        for cid in child_ids:
            ac = AnecdoteChild(
                anecdote_id=anecdote_id,
                child_id=cid,
                confidence=1.0,
            )
            db.session.add(ac)

    db.session.commit()
    return jsonify(success(data=anecdote.to_dict(include_children=True), message='更新轶事记录成功'))


@anecdotes_bp.route('/anecdotes/<int:anecdote_id>', methods=['DELETE'])
@csrf.exempt
def delete_anecdote(anecdote_id):
    """删除轶事记录"""
    anecdote = Anecdote.query.get(anecdote_id)
    if not anecdote:
        return jsonify(error('轶事记录不存在')), 404

    # 删除关联
    AnecdoteChild.query.filter_by(anecdote_id=anecdote_id).delete()

    db.session.delete(anecdote)
    db.session.commit()
    return jsonify(success(message='删除轶事记录成功'))


@anecdotes_bp.route('/anecdotes/recognize-names', methods=['POST'])
@csrf.exempt
def recognize_names():
    """预览姓名识别（不保存）"""
    data = request.get_json()
    if not data:
        return jsonify(error('请求数据为空')), 400

    content = data.get('content', '').strip()
    class_id = data.get('class_id')

    if not content:
        return jsonify(error('内容不能为空')), 400

    if not class_id:
        return jsonify(error('请指定班级')), 400

    class_group = ClassGroup.query.get(class_id)
    if not class_group:
        return jsonify(error('班级不存在')), 404

    recognizer = NameRecognizer()
    result = recognizer.recognize(content, class_id)

    return jsonify(success(data=result, message='姓名识别完成'))
