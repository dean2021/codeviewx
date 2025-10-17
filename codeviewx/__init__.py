"""
CodeViewX - AI-Driven Code Documentation Generator

Intelligent documentation generation tool based on DeepAgents and LangChain.
"""

from .__version__ import __version__, __author__, __description__
from .core import load_prompt, generate_docs, detect_system_language
from .i18n import get_i18n, t, set_locale, detect_ui_language

__all__ = [
    "__version__",
    "__author__",
    "__description__",
    "load_prompt",
    "generate_docs",
    "detect_system_language",
    "get_i18n",
    "t",
    "set_locale",
    "detect_ui_language",
]

