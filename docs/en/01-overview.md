# Project Overview

## Project Introduction

CodeViewX is an intelligent code documentation generator that leverages artificial intelligence to automatically analyze codebases and generate comprehensive technical documentation. The project combines modern AI technologies with traditional software engineering practices to provide developers with high-quality documentation.

## Technology Stack

### Core Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **langchain** | 0.3.27 | LLM application framework |
| **langchain-anthropic** | 0.3.22 | Anthropic Claude integration |
| **langchain-core** | 0.3.79 | LangChain core components |
| **langchain-text-splitters** | 0.3.11 | Text processing utilities |
| **langgraph** | 0.6.10 | Workflow orchestration |
| **langgraph-checkpoint** | 2.1.2 | State management |
| **langgraph-prebuilt** | 0.6.4 | Pre-built components |
| **langgraph-sdk** | 0.2.9 | SDK for LangGraph |
| **langsmith** | 0.4.34 | Monitoring and tracing |
| **deepagents** | 0.0.5 | AI Agent framework |
| **ripgrepy** | 2.0.0 | Python wrapper for ripgrep |
| **flask** | 3.0.0 | Web server for documentation browsing |
| **markdown** | 3.5.1 | Markdown processing |
| **pymdown-extensions** | 10.5 | Markdown extensions |

### Development Dependencies

| Dependency | Purpose |
|------------|---------|
| **pytest** | Testing framework |
| **pytest-cov** | Coverage reporting |
| **black** | Code formatting |
| **flake8** | Linting |
| **mypy** | Type checking |
| **isort** | Import sorting |

## Project Structure

```
codeviewx/
├── 📁 codeviewx/                 # Main package
│   ├── 📄 __init__.py           # Package initialization and exports
│   ├── 📄 __version__.py        # Version information
│   ├── 📄 cli.py                # Command line interface (CLI)
│   ├── 📄 core.py               # Core API entry point
│   ├── 📄 generator.py          # Main documentation generator
│   ├── 📄 server.py             # Web documentation server
│   ├── 📄 prompt.py             # Prompt management system
│   ├── 📄 i18n.py               # Internationalization support
│   ├── 📄 language.py           # Language detection utilities
│   ├── 📁 prompts/              # AI prompt templates
│   │   ├── 📄 document_engineer.md
│   │   └── 📄 document_engineer_zh.md
│   ├── 📁 tools/                # Custom tools for AI agents
│   │   ├── 📄 command.py        # System command execution
│   │   ├── 📄 filesystem.py     # File system operations
│   │   └── 📄 search.py         # Code search utilities
│   ├── 📁 tpl/                  # HTML templates for web server
│   └── 📁 static/               # Static assets (CSS, JS)
├── 📁 tests/                    # Test files
├── 📁 examples/                 # Example usage
├── 📄 pyproject.toml            # Project configuration
├── 📄 requirements.txt          # Runtime dependencies
├── 📄 requirements-dev.txt      # Development dependencies
├── 📄 MANIFEST.in              # Package manifest
├── 📄 LICENSE                  # GPL-3.0 license
└── 📄 README.md                # Project documentation
```

## Core Components

### 1. CLI Module (`cli.py`)
**Entry Point**: `def main()` (Line 16)
- Command line argument parsing
- User interface language detection
- Workflow orchestration

### 2. Generator Module (`generator.py`)
**Core Function**: `def generate_docs()` (Line 24)
- AI agent creation and management
- Documentation generation workflow
- Progress tracking and logging

### 3. Server Module (`server.py`)
**Core Function**: `def start_document_web_server()` (Line 105)
- Flask web server
- Markdown rendering
- File tree generation

### 4. Internationalization (`i18n.py`)
**Core Class**: `class I18n:` (Line 200)
- Multi-language support
- Message translation
- Locale detection

### 5. Tools System
- **Command Tool**: System command execution
- **Filesystem Tool**: File operations
- **Search Tool**: Code searching with ripgrep

## Key Features

### AI-Powered Analysis
- Uses Anthropic Claude for code understanding
- DeepAgents framework for agent orchestration
- LangChain for LLM integration

### Multi-Language Support
- 8 documentation languages supported
- 2 UI languages (English/Chinese)
- Automatic language detection

### Web Interface
- Beautiful documentation browsing
- Mermaid diagram support
- Interactive file tree

### High Performance
- ripgrep for fast code searching
- Efficient file processing
- Progressive generation

## Design Philosophy

1. **Accuracy First**: Only describe verified information from actual code analysis
2. **Depth Priority**: Provide detailed analysis with sequence diagrams and code examples
3. **Structured Output**: Clear hierarchy with Markdown formatting
4. **Practicality**: Explain design decisions and provide actionable guides
5. **Context Association**: Reference specific code locations in documentation

## Configuration

### Entry Points
- **CLI Command**: `codeviewx` (defined in `pyproject.toml`)
- **Python API**: `from codeviewx import generate_docs`

### Environment Variables
- `ANTHROPIC_API_KEY`: Anthropic API key
- `OPENAI_API_KEY`: OpenAI API key (optional)

### Default Settings
- **Output Directory**: `docs/`
- **Language**: Auto-detect system language
- **Recursion Limit**: 1000 steps
- **Server Port**: 5000

---

*Next: [Quick Start Guide](02-quickstart.md)*