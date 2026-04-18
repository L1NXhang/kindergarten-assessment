"""姓名识别服务

从轶事记录内容中自动识别幼儿姓名和教师姓名。
"""
import re
import json
from app.extensions import db
from app.models.child import Child
from app.models.teacher import Teacher


class NameRecognizer:
    """姓名识别器"""

    def __init__(self):
        # 教师"XX老师"模式
        self.teacher_pattern = re.compile(r'([\u4e00-\u9fa5]{1,4})老师')

    def recognize(self, content, class_id):
        """
        识别内容中的幼儿姓名和教师姓名。

        参数:
            content: 轶事记录文本内容
            class_id: 班级ID，用于限定幼儿搜索范围

        返回:
            {
                'children': [{'id': int, 'name': str, 'confidence': float, 'positions': [int]}],
                'teacher': {'id': int, 'name': str} or None
            }
        """
        if not content or not class_id:
            return {'children': [], 'teacher': None}

        # 获取班级内所有幼儿
        children = Child.query.filter_by(class_id=class_id).all()
        if not children:
            return {'children': [], 'teacher': None}

        # 识别幼儿姓名
        recognized_children = self._recognize_children(content, children)

        # 识别教师姓名
        teacher = self._recognize_teacher(content)

        return {
            'children': recognized_children,
            'teacher': teacher,
        }

    def _recognize_children(self, content, children):
        """识别幼儿姓名，使用精确匹配和模糊容错"""
        results = []
        matched_positions = set()

        for child in children:
            name = child.name
            if not name:
                continue

            # 精确匹配
            positions = []
            for match in re.finditer(re.escape(name), content):
                positions.append(match.start())

            # 模糊容错1: 去掉"小"前缀
            if not positions and name.startswith('小') and len(name) > 1:
                short_name = name[1:]
                for match in re.finditer(re.escape(short_name), content):
                    positions.append(match.start())

            # 模糊容错2: 姓和名之间有空格
            if not positions and ' ' in name:
                compact_name = name.replace(' ', '')
                for match in re.finditer(re.escape(compact_name), content):
                    positions.append(match.start())

            # 模糊容错3: 带"小"前缀匹配
            if not positions and not name.startswith('小'):
                xiao_name = '小' + name
                for match in re.finditer(re.escape(xiao_name), content):
                    positions.append(match.start())

            if positions:
                # 过滤掉已被其他更长姓名匹配的位置
                unique_positions = [p for p in positions if p not in matched_positions]
                if unique_positions:
                    confidence = 1.0 if len(name) >= 2 else 0.8
                    results.append({
                        'id': child.id,
                        'name': child.name,
                        'confidence': confidence,
                        'positions': unique_positions,
                    })
                    matched_positions.update(unique_positions)

        # 按位置排序
        results.sort(key=lambda x: x['positions'][0])
        return results

    def _recognize_teacher(self, content):
        """识别教师姓名"""
        matches = self.teacher_pattern.findall(content)
        if not matches:
            return None

        # 取第一个匹配的教师名
        teacher_name = matches[0]

        # 查找或创建教师记录
        teacher = Teacher.query.filter_by(name=teacher_name).first()
        if not teacher:
            teacher = Teacher(name=teacher_name)
            db.session.add(teacher)
            db.session.commit()

        return {
            'id': teacher.id,
            'name': teacher.name,
        }
