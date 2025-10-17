"""
CodeViewX core module - Public API entry point
"""

from .language import detect_system_language
from .prompt import load_prompt
from .server import start_document_web_server
from .generator import generate_docs


__all__ = [
    'detect_system_language',
    'load_prompt',
    'start_document_web_server',
    'generate_docs',
]


if __name__ == "__main__":
    generate_docs(verbose=True)
