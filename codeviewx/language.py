"""
Language detection module
"""

import locale


def detect_system_language() -> str:
    """
    Detect system language
    
    Returns:
        Language code string, e.g. 'Chinese', 'English', 'Japanese', etc.
    
    Examples:
        >>> detect_system_language()
        'Chinese'
    """
    try:
        lang, encoding = locale.getdefaultlocale()
        
        if lang:
            if lang.startswith('zh'):
                return 'Chinese'
            elif lang.startswith('ja'):
                return 'Japanese'
            elif lang.startswith('ko'):
                return 'Korean'
            elif lang.startswith('fr'):
                return 'French'
            elif lang.startswith('de'):
                return 'German'
            elif lang.startswith('es'):
                return 'Spanish'
            elif lang.startswith('ru'):
                return 'Russian'
            else:
                return 'English'
        
        return 'English'
        
    except Exception:
        return 'English'

