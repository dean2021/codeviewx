"""
语言检测模块
"""

import locale


def detect_system_language() -> str:
    """
    检测系统语言
    
    Returns:
        语言代码字符串，如 'Chinese', 'English', 'Japanese' 等
    
    Examples:
        >>> detect_system_language()
        'Chinese'  # 在中文系统上
    """
    try:
        # 尝试获取系统语言设置
        lang, encoding = locale.getdefaultlocale()
        
        if lang:
            # 规范化语言代码
            if lang.startswith('zh'):
                return 'Chinese'  # 中文
            elif lang.startswith('ja'):
                return 'Japanese'  # 日语
            elif lang.startswith('ko'):
                return 'Korean'  # 韩语
            elif lang.startswith('fr'):
                return 'French'  # 法语
            elif lang.startswith('de'):
                return 'German'  # 德语
            elif lang.startswith('es'):
                return 'Spanish'  # 西班牙语
            elif lang.startswith('ru'):
                return 'Russian'  # 俄语
            else:
                return 'English'  # 默认英文
        
        # 如果无法检测，返回英文
        return 'English'
        
    except Exception:
        # 发生异常时默认返回英文
        return 'English'

