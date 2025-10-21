# CodeViewX

> AI-Powered Code Documentation Generator

[中文](README.zh.md) | English

[![PyPI version](https://img.shields.io/pypi/v/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![Python Version](https://img.shields.io/pypi/pyversions/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://img.shields.io/pypi/dm/codeviewx.svg)](https://pypi.org/project/codeviewx/)

CodeViewX automatically analyzes your codebase and generates professional technical documentation using AI (Anthropic Claude + DeepAgents + LangChain).

## ✨ Key Features

- 🤖 **AI-Powered Analysis**: Automatically understands code structure and business logic
- 📝 **Complete Documentation**: Generates 8 standard chapters (overview, quick start, architecture, core mechanisms, data models, API reference, development guide, testing)
- 🌐 **Multi-Language**: Supports Chinese, English, Japanese, Korean, French, German, Spanish, Russian
- 🖥️ **Documentation Browser**: Built-in web server for elegant documentation display
- ⚡ **Fast Search**: Integrated ripgrep for high-speed code search

## 📦 Quick Start

### Installation

```bash
# Install CodeViewX
pip install codeviewx

# Install ripgrep (code search tool)
brew install ripgrep  # macOS
# sudo apt install ripgrep  # Ubuntu/Debian

# Configure API Key
export ANTHROPIC_AUTH_TOKEN='your-api-key-here'
```

Get your API key at [Anthropic Console](https://console.anthropic.com/)

### Basic Usage

```bash
# Generate documentation for current directory
codeviewx

# Specify project path and language
codeviewx -w /path/to/project -l English -o docs

# Start documentation browser
codeviewx --serve -o docs
```

### Python API

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

## 📚 Documentation

For complete documentation, visit the [docs/en](docs/en/) directory:

- [📖 Overview](docs/en/01-overview.md) - Tech stack and project structure
- [🚀 Quick Start](docs/en/02-quickstart.md) - Detailed installation and configuration
- [🏗️ Architecture](docs/en/03-architecture.md) - Architecture design and components
- [⚙️ Core Mechanisms](docs/en/04-core-mechanisms.md) - Deep dive into how it works
- [🔌 API Reference](docs/en/06-api-reference.md) - Complete API documentation
- [👨‍💻 Development Guide](docs/en/07-development-guide.md) - Development and contribution guide
- [🧪 Testing](docs/en/08-testing.md) - Testing strategies and examples
- [🔒 Security](docs/en/09-security.md) - Security best practices
- [⚡ Performance](docs/en/10-performance.md) - Performance optimization
- [🚀 Deployment](docs/en/11-deployment.md) - Deployment guide
- [🔧 Troubleshooting](docs/en/12-troubleshooting.md) - Common issues and solutions

## 🔧 Troubleshooting

Having issues? Check the [detailed documentation](docs/en/12-troubleshooting.md) for help.

**Quick Tips:**
- API key error? Ensure `ANTHROPIC_AUTH_TOKEN` environment variable is set correctly
- Search not working? Check if `ripgrep` is installed
- More questions? See [docs/en](docs/en/) for complete documentation

## 🤝 Contributing

Contributions are welcome! See [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

GNU General Public License v3.0 - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

Built with [Anthropic Claude](https://www.anthropic.com/), [DeepAgents](https://github.com/langchain-ai/deepagents), [LangChain](https://www.langchain.com/), and [ripgrep](https://github.com/BurntSushi/ripgrep).

---

⭐ Star this project if you find it helpful!
