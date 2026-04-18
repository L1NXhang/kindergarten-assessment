"""工具模块"""


def success(data=None, message='操作成功'):
    """成功响应"""
    return {
        'code': 200,
        'message': message,
        'data': data,
    }


def error(message='操作失败', code=400, errors=None):
    """错误响应"""
    resp = {
        'code': code,
        'message': message,
    }
    if errors:
        resp['errors'] = errors
    return resp
