"""幼儿管理路由"""
from flask import Blueprint, request, jsonify
from app.extensions import db, csrf
from app.models.child import Child
from app.models.anecdote import Anecdote
from app.models.anecdote_child import AnecdoteChild
from app.utils.response import success, error

children_bp = Blueprint('children', __name__)


@children_bp.route('/children', methods=['GET'])
@csrf.exempt
def get_children():
    """获取幼儿列表"""
    class_id = request.args.get('class_id', type=int)

    query = Child.query
    if class_id:
        query = query.filter_by(class_id=class_id)

    children = query.order_by(Child.created_at.desc()).all()
    data = [c.to_dict() for c in children]
    return jsonify(success(data=data, message='获取幼儿列表成功'))


@children_bp.route('/children', methods=['POST'])
@csrf.exempt
def create_child():
    """添加幼儿"""
    data = request.get_json()
    if not data:
        return jsonify(error('请求数据为空')), 400

    name = data.get('name', '').strip()
    if not name:
        return jsonify(error('幼儿姓名不能为空')), 400

    class_id = data.get('class_id')
    if not class_id:
        return jsonify(error('请指定班级')), 400

    child = Child(
        name=name,
        gender=data.get('gender'),
        birth_date=data.get('birth_date'),
        class_id=class_id,
        notes=data.get('notes'),
    )
    db.session.add(child)
    db.session.commit()

    return jsonify(success(data=child.to_dict(include_class=True), message='添加幼儿成功')), 201


@children_bp.route('/children/<int:child_id>', methods=['GET'])
@csrf.exempt
def get_child(child_id):
    """获取幼儿详情"""
    child = Child.query.get(child_id)
    if not child:
        return jsonify(error('幼儿不存在')), 404

    data = child.to_dict(include_class=True)
    # 附加轶事数量
    data['anecdotes_count'] = child.anecdotes.count()
    return jsonify(success(data=data))


@children_bp.route('/children/<int:child_id>', methods=['PUT'])
@csrf.exempt
def update_child(child_id):
    """更新幼儿信息"""
    child = Child.query.get(child_id)
    if not child:
        return jsonify(error('幼儿不存在')), 404

    data = request.get_json()
    if not data:
        return jsonify(error('请求数据为空')), 400

    if 'name' in data:
        name = data['name'].strip()
        if name:
            child.name = name

    if 'gender' in data:
        child.gender = data['gender']

    if 'birth_date' in data:
        child.birth_date = data['birth_date']

    if 'class_id' in data:
        child.class_id = data['class_id']

    if 'notes' in data:
        child.notes = data['notes']

    db.session.commit()
    return jsonify(success(data=child.to_dict(include_class=True), message='更新幼儿信息成功'))


@children_bp.route('/children/<int:child_id>', methods=['DELETE'])
@csrf.exempt
def delete_child(child_id):
    """删除幼儿"""
    child = Child.query.get(child_id)
    if not child:
        return jsonify(error('幼儿不存在')), 404

    # 删除关联的anecdote_children记录
    AnecdoteChild.query.filter_by(child_id=child_id).delete()

    db.session.delete(child)
    db.session.commit()
    return jsonify(success(message='删除幼儿成功'))


@children_bp.route('/children/<int:child_id>/timeline', methods=['GET'])
@csrf.exempt
def get_child_timeline(child_id):
    """获取幼儿轶事时间线"""
    child = Child.query.get(child_id)
    if not child:
        return jsonify(error('幼儿不存在')), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # 查询与该幼儿关联的轶事记录
    anecdotes = (
        Anecdote.query
        .join(AnecdoteChild, AnecdoteChild.anecdote_id == Anecdote.id)
        .filter(AnecdoteChild.child_id == child_id)
        .order_by(Anecdote.observed_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    data = {
        'child': child.to_dict(include_class=True),
        'timeline': [a.to_dict(include_children=True) for a in anecdotes.items],
        'pagination': {
            'page': anecdotes.page,
            'per_page': anecdotes.per_page,
            'total': anecdotes.total,
            'pages': anecdotes.pages,
        },
    }

    return jsonify(success(data=data))
