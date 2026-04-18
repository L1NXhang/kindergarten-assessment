"""AI报告生成服务

使用DeepSeek API生成幼儿发展评估报告。
"""
import json
import os
from pathlib import Path
from openai import OpenAI
from flask import current_app


class AIReportService:
    """AI报告生成服务"""

    def __init__(self):
        self.prompts_dir = Path(__file__).resolve().parent.parent.parent.parent / 'prompts'

    def _get_client(self):
        """创建OpenAI客户端（连接DeepSeek API）"""
        api_key = current_app.config.get('DEEPSEEK_API_KEY', '')
        base_url = current_app.config.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
        return OpenAI(api_key=api_key, base_url=base_url)

    def _load_prompt_template(self, template_name):
        """加载prompt模板文件"""
        template_path = self.prompts_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f'Prompt模板文件不存在: {template_path}')
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _format_anecdotes(self, anecdotes):
        """格式化轶事记录为文本"""
        if not anecdotes:
            return '暂无轶事记录。'
        texts = []
        for i, a in enumerate(anecdotes, 1):
            date_str = a.observed_at.strftime('%Y-%m-%d') if a.observed_at else '未知日期'
            children_names = ', '.join([c.name for c in a.children]) if a.children else '未指定'
            text = (
                f'【记录{i}】日期：{date_str}\n'
                f'幼儿：{children_names}\n'
                f'地点：{a.location or "未记录"}\n'
                f'活动：{a.activity_type or "未记录"}\n'
                f'内容：{a.content}'
            )
            texts.append(text)
        return '\n\n'.join(texts)

    def generate_individual_report(self, child, anecdotes, period):
        """
        生成幼儿个人发展报告。

        参数:
            child: Child对象
            anecdotes: Anecdote对象列表
            period: {'start': str, 'end': str}

        返回:
            {'content': str, 'domain_scores': dict}
        """
        template = self._load_prompt_template('individual_report.txt')
        anecdotes_text = self._format_anecdotes(anecdotes)

        prompt = template.format(
            child_name=child.name,
            gender=child.gender or '未知',
            age_group=child.class_group.age_group if child.class_group else '未知',
            class_name=child.class_group.name if child.class_group else '未知',
            period_start=period.get('start', ''),
            period_end=period.get('end', ''),
            anecdotes_text=anecdotes_text,
        )

        content = self._generate(prompt, '你是一位经验丰富的幼儿园教育评估专家。')
        domain_scores = self._extract_domain_scores(content)

        return {
            'content': content,
            'domain_scores': domain_scores,
        }

    def generate_class_summary(self, class_group, children_summaries, period):
        """
        生成班级汇总报告。

        参数:
            class_group: ClassGroup对象
            children_summaries: [{'name': str, 'report': str}] 列表
            period: {'start': str, 'end': str}

        返回:
            {'content': str}
        """
        template = self._load_prompt_template('class_summary.txt')

        summaries_text = '\n\n'.join(
            f'【{s["name"]}】\n{s["report"]}'
            for s in children_summaries
        )

        prompt = template.format(
            class_name=class_group.name,
            age_group=class_group.age_group,
            period_start=period.get('start', ''),
            period_end=period.get('end', ''),
            children_summaries=summaries_text,
        )

        content = self._generate(prompt, '你是一位经验丰富的幼儿园教育评估专家。')
        return {'content': content}

    def generate_reflection(self, class_group, assessment_data):
        """
        生成教育反思报告。

        参数:
            class_group: ClassGroup对象
            assessment_data: dict 包含评估相关信息

        返回:
            {'content': str}
        """
        template = self._load_prompt_template('reflection_strategy.txt')

        prompt = template.format(
            class_name=class_group.name,
            age_group=class_group.age_group,
            period_start=assessment_data.get('period_start', ''),
            period_end=assessment_data.get('period_end', ''),
            class_summary=assessment_data.get('class_summary', ''),
        )

        content = self._generate(prompt, '你是一位经验丰富的幼儿园教育评估专家。')
        return {'content': content}

    def generate_stream(self, prompt, system_role='你是一位经验丰富的幼儿园教育评估专家。'):
        """
        流式生成报告内容。

        参数:
            prompt: 用户提示
            system_role: 系统角色设定

        返回:
            生成器，每次产生一段文本
        """
        client = self._get_client()

        stream = client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {'role': 'system', 'content': system_role},
                {'role': 'user', 'content': prompt},
            ],
            temperature=0.3,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def _generate(self, prompt, system_role='你是一位经验丰富的幼儿园教育评估专家。'):
        """非流式生成"""
        client = self._get_client()

        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {'role': 'system', 'content': system_role},
                {'role': 'user', 'content': prompt},
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    def _extract_domain_scores(self, content):
        """
        从报告内容中提取五大领域评分。
        如果AI报告中包含评分信息，则提取并返回。

        返回:
            dict: 五大领域评分
        """
        default_scores = {
            '健康': None,
            '语言': None,
            '社会': None,
            '科学': None,
            '艺术': None,
        }

        try:
            # 尝试从报告中提取JSON格式的评分
            import re
            score_pattern = re.compile(r'领域评分[：:]\s*\n?```json\s*\n?([\s\S]*?)\n?```')
            match = score_pattern.search(content)
            if match:
                scores = json.loads(match.group(1))
                # 合并默认值
                for key in default_scores:
                    if key in scores:
                        default_scores[key] = scores[key]
        except (json.JSONDecodeError, Exception):
            pass

        return default_scores
