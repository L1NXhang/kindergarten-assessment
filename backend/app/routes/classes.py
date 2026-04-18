"""班级管理路由"""
from flask import Blueprint, request, jsonify
from app.extensions import db, csrf
from app.models.class_group import ClassGroup
from app.models.child import Child
from app.models.anecdote import Anecdote
from app.utils.response import success, error
from app.utils.validators import validate_upload_file
from app.services.excel_import import ExcelImportService

classes_bp = Blueprint('classes', __name__)


@classes_bp.route('/classes', methods=['GET'])
@csrf.exempt
def get_classes():
    """获取班级列表（含幼儿数统计）"""
    classes = ClassGroup.query.order_by(ClassGroup.created_at.desc()).all()
    data = []
    for c in classes:
        item = c.to_dict(include_children_count=True)
        data.append(item)
    return jsonify(success(data=data, message='获取班级列表成功'))


@classes_bp.route('/classes', methods=['POST'])
@csrf.exempt
def create_class():
    """创建班级"""
    data = request.get_json()
    if not data:
        return jsonify(error('请求数据为空')), 400

    name = data.get('name', '').strip()
    if not name:
        return jsonify(error('班级名称不能为空')), 400

    # 检查名称唯一性
    existing = ClassGroup.query.filter_by(name=name).first()
    if existing:
        return jsonify(error('班级名称已存在')), 400

    class_group = ClassGroup(
        name=name,
        age_group=data.get('age_group', '3-4岁'),
        academic_year=data.get('academic_year'),
    )
    db.session.add(class_group)
    db.session.commit()

    return jsonify(success(data=class_group.to_dict(), message='创建班级成功')), 201


@classes_bp.route('/classes/<int:class_id>', methods=['GET'])
@csrf.exempt
def get_class(class_id):
    """获取班级详情"""
    class_group = ClassGroup.query.get(class_id)
    if not class_group:
        return jsonify(error('班级不存在')), 404

    data = class_group.to_dict(include_children_count=True)
    return jsonify(success(data=data))


@classes_bp.route('/classes/<int:class_id>', methods=['PUT'])
@csrf.exempt
def update_class(class_id):
    """更新班级"""
    class_group = ClassGroup.query.get(class_id)
    if not class_group:
        return jsonify(error('班级不存在')), 404

    data = request.get_json()
    if not data:
        return jsonify(error('请求数据为空')), 400

    name = data.get('name', '').strip()
    if name and name != class_group.name:
        existing = ClassGroup.query.filter_by(name=name).first()
        if existing:
            return jsonify(error('班级名称已存在')), 400
        class_group.name = name

    if 'age_group' in data:
        class_group.age_group = data['age_group']
    if 'academic_year' in data:
        class_group.academic_year = data['academic_year']

    db.session.commit()
    return jsonify(success(data=class_group.to_dict(), message='更新班级成功'))


@classes_bp.route('/classes/<int:class_id>', methods=['DELETE'])
@csrf.exempt
def delete_class(class_id):
    """删除班级"""
    class_group = ClassGroup.query.get(class_id)
    if not class_group:
        return jsonify(error('班级不存在')), 404

    # 检查是否有关联幼儿
    children_count = class_group.children.count()
    if children_count > 0:
        return jsonify(error(f'该班级下还有{children_count}名幼儿，无法删除')), 400

    db.session.delete(class_group)
    db.session.commit()
    return jsonify(success(message='删除班级成功'))


@classes_bp.route('/classes/<int:class_id>/import-children', methods=['POST'])
@csrf.exempt
def import_children(class_id):
    """Excel导入幼儿名单"""
    class_group = ClassGroup.query.get(class_id)
    if not class_group:
        return jsonify(error('班级不存在')), 404

    if 'file' not in request.files:
        return jsonify(error('请上传文件')), 400

    file = request.files['file']
    is_valid, err_msg = validate_upload_file(file)
    if not is_valid:
        return jsonify(error(err_msg)), 400

    service = ExcelImportService()
    result = service.import_children(file, class_id)

    return jsonify(success(data=result, message=f'导入完成：成功{result["success"]}个，跳过{result["skipped"]}个'))


@classes_bp.route('/classes/<int:class_id>/statistics', methods=['GET'])
@csrf.exempt
def get_class_statistics(class_id):
    """获取班级统计数据"""
    class_group = ClassGroup.query.get(class_id)
    if not class_group:
        return jsonify(error('班级不存在')), 404

    # 幼儿统计
    total_children = class_group.children.count()
    boys = class_group.children.filter_by(gender='男').count()
    girls = class_group.children.filter_by(gender='女').count()

    # 轶事记录统计
    total_anecdotes = class_group.anecdotes.count()
    draft_anecdotes = class_group.anecdotes.filter_by(status='draft').count()
    final_anecdotes = class_group.anecdotes.filter_by(status='final').count()

    # 评估统计
    total_assessments = class_group.assessments.count()
    completed_assessments = class_group.assessments.filter_by(status='completed').count()

    data = {
        'class': class_group.to_dict(),
        'children': {
            'total': total_children,
            'boys': boys,
            'girls': girls,
        },
        'anecdotes': {
            'total': total_anecdotes,
            'draft': draft_anecdotes,
            'final': final_anecdotes,
        },
        'assessments': {
            'total': total_assessments,
            'completed': completed_assessments,
        },
    }

    return jsonify(success(data=data))
