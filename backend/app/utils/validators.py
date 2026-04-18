"""验证工具模块"""

from flask import current_app


# Excel文件的Magic Number（文件头签名）
EXCEL_MAGIC_NUMBERS = {
    b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': 'xls',      # OLE2 (old .xls)
    b'\x50\x4b\x03\x04': 'xlsx',                       # ZIP (new .xlsx)
    b'\x50\x4b\x05\x06': 'xlsx',                       # ZIP (empty)
    b'\x50\x4b\x07\x08': 'xlsx',                       # ZIP spanned
}


def validate_upload_file(file):
    """
    验证上传文件：
    1. 检查扩展名白名单
    2. 检查Magic Number（文件头签名）

    返回: (is_valid, error_message)
    """
    if not file or not file.filename:
        return False, '未选择文件'

    # 检查文件扩展名
    filename = file.filename.lower()
    allowed_extensions = current_app.config.get('UPLOAD_EXTENSIONS', ['.xlsx', '.xls'])
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        return False, f'不支持的文件格式，仅允许: {", ".join(allowed_extensions)}'

    # 检查Magic Number
    try:
        file.seek(0)
        header = file.read(8)
        file.seek(0)

        is_valid_magic = False
        for magic, fmt in EXCEL_MAGIC_NUMBERS.items():
            if header.startswith(magic):
                is_valid_magic = True
                break

        if not is_valid_magic:
            return False, '文件内容与扩展名不匹配，可能不是有效的Excel文件'
    except Exception:
        return False, '文件读取失败，请重试'

    return True, None
