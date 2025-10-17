# CodeViewX

> AI-Powered Intelligent Code Documentation Generator

[中文](README.zh.md) | English

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/dean2021/codeviewx)

CodeViewX is an intelligent code documentation generator based on Anthropic Claude and DeepAgents framework that automatically analyzes codebases and generates professional technical documentation.

## Key Features

- 🤖 **AI-Powered Analysis**: Built on Anthropic Claude, DeepAgents, and LangChain frameworks
- 📝 **Complete Documentation**: Automatically generates 8 core technical documentation chapters
- 🌐 **Multi-language Support**: Supports 8 languages (Chinese, English, Japanese, Korean, French, German, Spanish, Russian)
- 🖥️ **Built-in Web Server**: Beautiful documentation browsing interface with Mermaid diagram support
- ⚡ **High-Performance Search**: Integrated ripgrep for fast code searching

## System Requirements

- Python 3.8+
- pip package manager
- ripgrep (rg) code search tool
- Anthropic API Key

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
```

### 2. Install Dependencies
```bash
# Development mode installation (recommended)
pip install -e .

# Or standard installation
pip install .
```

### 3. Install ripgrep
```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows
choco install ripgrep
```

### 4. Configure API Key
```bash
# Set environment variable
export ANTHROPIC_API_KEY='your-api-key-here'

# Or add to ~/.bashrc or ~/.zshrc
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

Get your API Key at: [Anthropic Console](https://console.anthropic.com/)

## Quick Start

### Command Line Usage

```bash
# Analyze current directory and generate documentation
codeviewx

# Specify project path and output directory
codeviewx -w /path/to/project -o docs

# Generate English documentation
codeviewx -w /path/to/project -l English

# Start documentation web server
codeviewx --serve -o docs
```

### Python API

```python
from codeviewx import generate_docs

# Generate documentation
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English"
)

# Start web server
from codeviewx import start_document_web_server
start_document_web_server("docs")
```

## Generated Documentation Structure

```
docs/
├── 01-project-overview.md
├── 02-quick-start.md
├── 03-system-architecture.md
├── 04-core-mechanisms.md
├── 05-data-models.md
├── 06-api-reference.md
├── 07-development-guide.md
├── 08-testing-documentation.md
└── README.md
```

## Development

### Install Development Dependencies
```bash
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
pytest --cov=codeviewx --cov-report=html
```

### Code Quality
```bash
black codeviewx/    # Format code
flake8 codeviewx/   # Lint code
mypy codeviewx/     # Type checking
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- How to submit issues and feature requests
- Development setup and workflow
- Coding standards and best practices
- Testing guidelines
- Pull request process

For the Chinese version, see [贡献指南](CONTRIBUTING.zh.md).

## Project Structure

```
codeviewx/
├── codeviewx/              # Main package
│   ├── cli.py             # Command-line interface
│   ├── core.py            # Core API
│   ├── generator.py       # Documentation generator
│   ├── server.py          # Web server
│   ├── prompt.py          # Prompt management
│   ├── i18n.py            # Internationalization
│   ├── language.py        # Language detection
│   ├── prompts/           # Prompt templates
│   ├── tools/             # Tool modules
│   ├── tpl/               # HTML templates
│   └── static/            # Static resources
├── tests/                 # Test files
├── examples/              # Example code
└── pyproject.toml         # Project configuration
```

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) file for details.

## Contact

- 📧 Email: dean@csoio.com
- 🐙 GitHub: [@dean2021](https://github.com/dean2021)
- 🔗 Homepage: [CodeViewX](https://github.com/dean2021/codeviewx)

## Acknowledgments

Thanks to these excellent open-source projects:

- [Anthropic Claude](https://www.anthropic.com/) - AI Model
- [DeepAgents](https://github.com/langchain-ai/deepagents) - AI Agent Framework
- [LangChain](https://www.langchain.com/) - LLM Application Framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Workflow Orchestration
- [ripgrep](https://github.com/BurntSushi/ripgrep) - Code Search

---

⭐ If this project helps you, please give it a star!
