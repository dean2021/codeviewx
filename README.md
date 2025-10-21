# CodeViewX

> AI-Powered Code Documentation Generator

[中文](README.zh.md) | English

[![PyPI version](https://img.shields.io/pypi/v/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![Python Version](https://img.shields.io/pypi/pyversions/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://img.shields.io/pypi/dm/codeviewx.svg)](https://pypi.org/project/codeviewx/)

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
export ANTHROPIC_AUTH_TOKEN='your-api-key-here'

# Optional: Configure custom API base URL (for proxy or custom endpoints)
export ANTHROPIC_BASE_URL='https://your-custom-api.example.com'

# Or use the provided setup script (recommended)
bash scripts/setup_api_key.sh
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

# Use custom API base URL
codeviewx --base-url https://your-custom-api.example.com

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

# Generate documentation with custom API base URL
generate_docs(
    working_directory="/path/to/project",
    base_url="https://your-custom-api.example.com"
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

## Troubleshooting

### API Key Related Errors

**Q: Getting "ANTHROPIC_AUTH_TOKEN environment variable not found" error?**

A: This means you haven't set up your Anthropic API key yet. To fix:

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Set the environment variable:
   ```bash
   export ANTHROPIC_AUTH_TOKEN='your-api-key-here'
   ```
3. Or use the provided setup script:
   ```bash
   bash scripts/setup_api_key.sh
   ```

**Q: What if my API key format is incorrect?**

A: Please ensure you've copied the complete API key without any extra spaces or line breaks. If issues persist, regenerate the key from the Anthropic Console.

### Improved Error Handling

CodeViewX now provides more user-friendly error messages:

- 🔍 **Automatic Detection**: Validates API key presence
- 📝 **Clear Messages**: Specific error causes and solution steps
- 🔗 **Direct Links**: Provides direct links to get API keys
- 🌐 **Bilingual Support**: Error messages in English and Chinese
- ⚙️ **Setup Script**: Automated API key configuration tool

## Contributing

Contributions are welcome! See [Contributing Guide](CONTRIBUTING.md) for details.

## License

GNU General Public License v3.0 - see [LICENSE](LICENSE) file.

## Acknowledgments

Built with [Anthropic Claude](https://www.anthropic.com/), [DeepAgents](https://github.com/langchain-ai/deepagents), [LangChain](https://www.langchain.com/), and [ripgrep](https://github.com/BurntSushi/ripgrep).

---

⭐ Star this project if you find it helpful!
