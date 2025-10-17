"""
CodeViewX 核心功能模块 - 公共API入口
"""

# 从各个模块导入主要功能
from .language import detect_system_language
from .prompt import load_prompt
from .server import start_document_web_server
from .generator import generate_docs


# 导出所有公共API
__all__ = [
    'detect_system_language',
    'load_prompt',
    'start_document_web_server',
    'generate_docs',
]


# 向后兼容：保持原有的脚本执行方式
if __name__ == "__main__":
    generate_docs(verbose=True)
