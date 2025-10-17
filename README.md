# CodeViewX

> AI-Powered Code Documentation Generator

[中文](README.zh.md) | English

[![PyPI version](https://badge.fury.io/py/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Downloads](https://pepy.tech/badge/codeviewx)](https://pepy.tech/project/codeviewx)

CodeViewX automatically analyzes your codebase and generates professional technical documentation using AI (Anthropic Claude + DeepAgents + LangChain).

## Features

- 🤖 AI-powered code analysis and documentation generation
- 📝 Generates comprehensive documentation (8 chapters: overview, quick start, architecture, core mechanisms, data models, API reference, development guide, testing)
- 🌐 Multi-language support (Chinese, English, Japanese, Korean, French, German, Spanish, Russian)
- 🖥️ Built-in web server for browsing documentation
- ⚡ Fast code search with ripgrep integration

## Installation

**From PyPI (Recommended):**
```bash
# Install CodeViewX
pip install codeviewx

# Install ripgrep
brew install ripgrep  # macOS
# sudo apt install ripgrep  # Ubuntu/Debian

# Configure API Key
export ANTHROPIC_API_KEY='your-api-key-here'
```

**From Source (Development):**
```bash
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
pip install -e .
```

Get your API key at [Anthropic Console](https://console.anthropic.com/)

## Usage

**Command Line:**
```bash
# Generate documentation for current directory
codeviewx

# Specify project and language
codeviewx -w /path/to/project -l English -o docs

# Browse documentation
codeviewx --serve -o docs
```

**Python API:**
```python
from codeviewx import generate_docs, start_document_web_server

# Generate documentation
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English"
)

# Start web server
start_document_web_server("docs")
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code quality
black codeviewx/
flake8 codeviewx/
```

## Contributing

Contributions are welcome! See [Contributing Guide](CONTRIBUTING.md) for details.

## License

GNU General Public License v3.0 - see [LICENSE](LICENSE) file.

## Acknowledgments

Built with [Anthropic Claude](https://www.anthropic.com/), [DeepAgents](https://github.com/langchain-ai/deepagents), [LangChain](https://www.langchain.com/), and [ripgrep](https://github.com/BurntSushi/ripgrep).

---

⭐ Star this project if you find it helpful!
