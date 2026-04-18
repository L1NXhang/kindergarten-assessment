"""评估管理路由"""
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db, csrf
from app.models.assessment import Assessment, AssessmentReport
from app.models.class_group import ClassGroup
from app.models.child import Child
from app.models.anecdote import Anecdote
from app.models.anecdote_child import AnecdoteChild
from app.utils.response import success, error
from app.services.ai_report import AIReportService

assessments_bp = Blueprint('assessments', __name__)

# 存储生成进度（生产环境应使用Redis等）
_generation_progress = {}


@assessments_bp.route('/assessments', methods=['GET'])
@csrf.exempt
def get_assessments():
    """获取评估列表"""
    class_id = request.args.get('class_id', type=int)

    query = Assessment.query
    if class_id:
        query = query.filter_by(class_id=class_id)

    assessments = query.order_by(Assessment.created_at.desc()).all()
    data = [a.to_dict() for a in assessments]
    return jsonify(success(data=data, message='获取评估列表成功'))


@assessments_bp.route('/assessments', methods=['POST'])
@csrf.exempt
def create_assessment():
    """创建评估任务"""
    data = request.get_json()
    if not data:
        return jsonify(error('请求数据为空')), 400

    title = data.get('title', '').strip()
    if not title:
        return jsonify(error('评估标题不能为空')), 400

    class_id = data.get('class_id')
    if not class_id:
        return jsonify(error('请指定班级')), 400

    class_group = ClassGroup.query.get(class_id)
    if not class_group:
        return jsonify(error('班级不存在')), 404

    period_start = data.get('period_start')
    period_end = data.get('period_end')

    if not period_start or not period_end:
        return jsonify(error('请指定评估周期')), 400

    try:
        period_start = datetime.strptime(period_start, '%Y-%m-%d').date()
        period_end = datetime.strptime(period_end, '%Y-%m-%d').date()
    except ValueError:
        return jsonify(error('日期格式错误，请使用YYYY-MM-DD')), 400

    assessment = Assessment(
        class_id=class_id,
        title=title,
        period_start=period_start,
        period_end=period_end,
        status='pending',
        created_by=data.get('created_by'),
    )
    db.session.add(assessment)
    db.session.commit()

    return jsonify(success(data=assessment.to_dict(), message='创建评估任务成功')), 201


@assessments_bp.route('/assessments/<int:assessment_id>', methods=['GET'])
@csrf.exempt
def get_assessment(assessment_id):
    """获取评估详情"""
    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify(error('评估任务不存在')), 404

    return jsonify(success(data=assessment.to_dict(include_reports=True)))


@assessments_bp.route('/assessments/<int:assessment_id>', methods=['DELETE'])
@csrf.exempt
def delete_assessment(assessment_id):
    """删除评估任务"""
    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify(error('评估任务不存在')), 404

    # 删除关联的报告
    AssessmentReport.query.filter_by(assessment_id=assessment_id).delete()

    db.session.delete(assessment)
    db.session.commit()
    return jsonify(success(message='删除评估任务成功'))


@assessments_bp.route('/assessments/<int:assessment_id>/generate', methods=['POST'])
@csrf.exempt
def generate_reports(assessment_id):
    """触发AI生成报告"""
    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify(error('评估任务不存在')), 404

    if assessment.status == 'generating':
        return jsonify(error('报告正在生成中，请勿重复操作')), 400

    # 更新状态为生成中
    assessment.status = 'generating'
    db.session.commit()

    # 初始化进度
    _generation_progress[assessment_id] = {
        'status': 'generating',
        'total': 0,
        'current': 0,
        'message': '正在准备生成...',
    }

    try:
        _do_generate(assessment)
    except Exception as e:
        assessment.status = 'failed'
        _generation_progress[assessment_id] = {
            'status': 'failed',
            'message': f'生成失败: {str(e)}',
        }
        db.session.commit()

    return jsonify(success(data=_generation_progress.get(assessment_id), message='报告生成任务已启动'))


def _do_generate(assessment):
    """执行报告生成（同步执行，生产环境应改为异步任务）"""
    service = AIReportService()
    class_group = assessment.class_group

    # 获取周期内的轶事记录
    anecdotes = (
        Anecdote.query
        .filter_by(class_id=assessment.class_id)
        .filter(
            Anecdote.observed_at >= datetime.combine(assessment.period_start, datetime.min.time()),
            Anecdote.observed_at <= datetime.combine(assessment.period_end, datetime.max.time()),
        )
        .all()
    )

    # 获取班级所有幼儿
    children = Child.query.filter_by(class_id=assessment.class_id).all()
    total = len(children) + 2  # 每个幼儿 + 班级汇总 + 教育反思
    _generation_progress[assessment.id]['total'] = total

    period = {
        'start': assessment.period_start.isoformat(),
        'end': assessment.period_end.isoformat(),
    }

    children_summaries = []

    # 1. 为每个幼儿生成个人报告
    for i, child in enumerate(children):
        _generation_progress[assessment.id]['current'] = i + 1
        _generation_progress[assessment.id]['message'] = f'正在生成 {child.name} 的个人报告...'

        # 获取该幼儿的轶事
        child_anecdotes = [
            a for a in anecdotes
            if any(ac.child_id == child.id for ac in a.anecdote_children)
        ]

        try:
            result = service.generate_individual_report(child, child_anecdotes, period)

            report = AssessmentReport(
                assessment_id=assessment.id,
                report_type='individual',
                child_id=child.id,
                content=result['content'],
                domain_scores=json.dumps(result.get('domain_scores', {}), ensure_ascii=False),
            )
            db.session.add(report)

            children_summaries.append({
                'name': child.name,
                'report': result['content'][:500],  # 摘要
            })
        except Exception as e:
            _generation_progress[assessment.id]['message'] = f'{child.name} 报告生成失败: {str(e)}'

    # 2. 生成班级汇总报告
    _generation_progress[assessment.id]['current'] = len(children) + 1
    _generation_progress[assessment.id]['message'] = '正在生成班级汇总报告...'

    try:
        summary_result = service.generate_class_summary(class_group, children_summaries, period)
        summary_report = AssessmentReport(
            assessment_id=assessment.id,
            report_type='class_summary',
            content=summary_result['content'],
        )
        db.session.add(summary_report)
    except Exception as e:
        _generation_progress[assessment.id]['message'] = f'班级汇总报告生成失败: {str(e)}'

    # 3. 生成教育反思报告
    _generation_progress[assessment.id]['current'] = len(children) + 2
    _generation_progress[assessment.id]['message'] = '正在生成教育反思报告...'

    try:
        assessment_data = {
            'period_start': period['start'],
            'period_end': period['end'],
            'class_summary': summary_result.get('content', '')[:500] if 'summary_result' in dir() else '',
        }
        reflection_result = service.generate_reflection(class_group, assessment_data)
        reflection_report = AssessmentReport(
            assessment_id=assessment.id,
            report_type='reflection',
            content=reflection_result['content'],
        )
        db.session.add(reflection_report)
    except Exception as e:
        _generation_progress[assessment.id]['message'] = f'教育反思报告生成失败: {str(e)}'

    # 更新评估状态
    assessment.status = 'completed'
    assessment.completed_at = datetime.utcnow()
    db.session.commit()

    _generation_progress[assessment.id] = {
        'status': 'completed',
        'total': total,
        'current': total,
        'message': '报告生成完成',
    }


@assessments_bp.route('/assessments/<int:assessment_id>/status', methods=['GET'])
@csrf.exempt
def get_generation_status(assessment_id):
    """获取报告生成进度"""
    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify(error('评估任务不存在')), 404

    progress = _generation_progress.get(assessment_id, {
        'status': assessment.status,
        'message': '未知状态',
    })

    return jsonify(success(data=progress))


@assessments_bp.route('/assessments/<int:assessment_id>/reports', methods=['GET'])
@csrf.exempt
def get_reports(assessment_id):
    """获取评估报告列表"""
    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify(error('评估任务不存在')), 404

    reports = AssessmentReport.query.filter_by(assessment_id=assessment_id).all()
    data = [r.to_dict() for r in reports]
    return jsonify(success(data=data, message='获取报告列表成功'))


@assessments_bp.route('/assessments/<int:assessment_id>/reports/<int:report_id>', methods=['GET'])
@csrf.exempt
def get_report(assessment_id, report_id):
    """获取单个报告详情"""
    report = AssessmentReport.query.filter_by(
        id=report_id,
        assessment_id=assessment_id,
    ).first()

    if not report:
        return jsonify(error('报告不存在')), 404

    return jsonify(success(data=report.to_dict()))
