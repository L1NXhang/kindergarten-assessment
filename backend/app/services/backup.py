"""数据库备份与恢复服务"""
import os
import shutil
from datetime import datetime
from pathlib import Path
from flask import current_app


def create_backup():
    """
    创建数据库备份。

    将SQLite数据库文件复制到backups/目录，文件名带时间戳。

    返回:
        {'success': bool, 'filename': str, 'message': str}
    """
    try:
        db_path = current_app.config['SQLALCHEMY_DATABASE_URI']
        # 从URI中提取文件路径
        if db_path.startswith('sqlite:///'):
            db_file = db_path[len('sqlite:///'):]
        elif db_path.startswith('sqlite://'):
            db_file = db_path[len('sqlite://'):]
        else:
            return {
                'success': False,
                'filename': None,
                'message': '不支持的数据库类型',
            }

        if not os.path.exists(db_file):
            return {
                'success': False,
                'filename': None,
                'message': '数据库文件不存在',
            }

        # 创建备份目录
        backup_dir = Path(__file__).resolve().parent.parent.parent / 'backups'
        backup_dir.mkdir(parents=True, exist_ok=True)

        # 生成备份文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'assessment_backup_{timestamp}.db'
        backup_path = backup_dir / backup_filename

        # 复制文件
        shutil.copy2(db_file, str(backup_path))

        return {
            'success': True,
            'filename': backup_filename,
            'message': f'备份成功: {backup_filename}',
        }

    except Exception as e:
        return {
            'success': False,
            'filename': None,
            'message': f'备份失败: {str(e)}',
        }


def restore_backup(file):
    """
    从上传的备份文件恢复数据库。

    参数:
        file: 上传的备份文件对象

    返回:
        {'success': bool, 'message': str}
    """
    try:
        db_path = current_app.config['SQLALCHEMY_DATABASE_URI']
        if db_path.startswith('sqlite:///'):
            db_file = db_path[len('sqlite:///'):]
        elif db_path.startswith('sqlite://'):
            db_file = db_path[len('sqlite://'):]
        else:
            return {
                'success': False,
                'message': '不支持的数据库类型',
            }

        # 先创建当前数据库的备份（恢复前的安全备份）
        pre_backup = create_backup()

        # 保存上传文件到临时位置
        temp_dir = Path(__file__).resolve().parent.parent.parent / 'uploads'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir / 'temp_restore.db'

        file.save(str(temp_path))

        # 验证文件是否为有效的SQLite数据库
        with open(str(temp_path), 'rb') as f:
            header = f.read(16)
            if not header.startswith(b'SQLite format 3'):
                temp_path.unlink(missing_ok=True)
                return {
                    'success': False,
                    'message': '不是有效的SQLite数据库文件',
                }

        # 替换数据库文件
        shutil.copy2(str(temp_path), db_file)
        temp_path.unlink(missing_ok=True)

        message = '数据库恢复成功'
        if pre_backup.get('success'):
            message += f'（恢复前备份: {pre_backup["filename"]}）'

        return {
            'success': True,
            'message': message,
        }

    except Exception as e:
        return {
            'success': False,
            'message': f'恢复失败: {str(e)}',
        }
