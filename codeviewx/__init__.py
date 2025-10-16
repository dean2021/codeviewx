"""
CodeViewX - AI 驱动的代码文档生成器

基于 DeepAgents 和 LangChain 的智能文档生成工具。
"""

from .__version__ import __version__, __author__, __description__
from .core import load_prompt, generate_docs, detect_system_language

__all__ = [
    "__version__",
    "__author__",
    "__description__",
    "load_prompt",
    "generate_docs",
    "detect_system_language",
]

