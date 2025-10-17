# Project Overview

## Introduction

CodeViewX is an intelligent code documentation generator that utilizes AI technology to automatically analyze codebases and generate comprehensive technical documentation. The project combines modern AI frameworks with robust code analysis tools to provide developers with accurate, well-structured documentation for their projects.

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Primary programming language |
| **DeepAgents** | 0.0.5 | AI Agent framework for intelligent analysis |
| **LangChain** | 0.3.27 | AI application development framework |
| **LangGraph** | 0.6.10 | Graph-based AI workflow orchestration |
| **Flask** | 3.0.0 | Web server for documentation browsing |
| **ripgrep** | 2.0.0 | High-performance code search |
| **Markdown** | 3.5.1 | Document parsing and rendering |

### Development Dependencies

| Tool | Version | Purpose |
|------|---------|---------|
| **pytest** | 7.0+ | Testing framework |
| **black** | 23.0+ | Code formatting |
| **flake8** | 6.0+ | Linting |
| **mypy** | 1.0+ | Static type checking |
| **isort** | 5.0+ | Import sorting |

### AI Model Support

- **Anthropic Claude** (recommended)
- **OpenAI GPT** models
- Configurable via environment variables

## Project Structure

The CodeViewX project follows a clean, modular architecture with clear separation of concerns:

```
codeviewx/
├── codeviewx/                 # Main package directory
│   ├── __init__.py           # Package initialization and API exports
│   ├── __version__.py        # Version information
│   ├── cli.py                # Command-line interface implementation
│   ├── core.py               # Core functionality and web server
│   ├── tools/                # AI Agent tools package
│   │   ├── __init__.py       # Tool exports
│   │   ├── command.py        # Command execution tool
│   │   ├── filesystem.py     # File system operations
│   │   └── search.py         # Code search functionality
│   ├── prompts/              # AI prompt templates
│   │   ├── DocumentEngineer.md          # Main prompt template
│   │   ├── DocumentEngineer_compact.md  # Optimized compact version
│   │   └── DocumentEngineer_original.md # Original full version
│   ├── tpl/                  # Web templates
│   │   └── doc_detail.html   # Document detail page template
│   └── static/               # Static web assets
│       ├── css/              # Stylesheets
│       └── README.md         # Static files documentation
├── tests/                    # Test suite
│   ├── __init__.py           # Test package initialization
│   ├── test_core.py          # Core functionality tests
│   ├── test_language.py      # Language detection tests
│   ├── test_progress.py      # Progress tracking tests
│   └── test_tools.py         # Tool module tests
├── examples/                 # Usage examples
│   ├── basic_usage.py        # Basic usage demonstration
│   ├── language_demo.py      # Multi-language examples
│   └── progress_demo.py      # Progress display examples
├── docs/                     # Generated documentation
│   ├── en/                   # English documentation
│   └── zh/                   # Chinese documentation
├── pyproject.toml           # PEP 621 package configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── CHANGELOG.md            # Version history
├── LICENSE                  # GPL-3.0 license
└── README.md               # Project documentation
```

## Key Components

### 1. Core Package (`codeviewx/`)

The main package contains all the essential functionality:

- **`cli.py`**: Command-line interface using argparse, providing comprehensive options for document generation and web server
- **`core.py`**: Core functionality including AI agent orchestration, web server, and progress tracking
- **`tools/`**: Specialized tools for AI agents to interact with the file system and search code

### 2. AI Agent Tools

The tools package provides three main categories of functionality:

#### File System Tools (`tools/filesystem.py`)
- `write_real_file()`: Write files with automatic directory creation
- `read_real_file()`: Read files with size and line count information
- `list_real_directory()`: Directory listing with categorized output

#### Search Tools (`tools/search.py`)
- `ripgrep_search()`: High-performance pattern matching using ripgrep
- Support for regular expressions, file type filtering, and case-insensitive search

#### Command Tools (`tools/command.py`)
- `execute_command()`: System command execution with output capture

### 3. Web Interface

The built-in web server provides:

- **Document Browser**: Beautiful Markdown rendering with syntax highlighting
- **File Tree Navigation**: Intuitive file exploration
- **Table of Contents**: Automatic TOC generation
- **Mermaid Support**: Diagram rendering for architecture visualizations

### 4. AI Prompt System

Three prompt template variants:

- **Original**: Full-featured prompt for comprehensive analysis
- **Compact**: Optimized version (70% smaller) for faster processing
- **Custom**: Flexible system for custom documentation requirements

## Entry Points

### Command Line Interface

The primary entry point is through the CLI:

```bash
# File: codeviewx/cli.py | Line: 15 | Description: Main CLI entry point
def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        prog="codeviewx",
        description="CodeViewX - AI 驱动的代码文档生成器",
        # ... argument setup
    )
```

### Python API

Programmatic access through the core module:

```python
# File: codeviewx/__init__.py | Line: 7-8 | Description: API exports
from .core import load_prompt, generate_docs, detect_system_language
```

### Web Server Routes

Flask-based web server with two main routes:

```python
# File: codeviewx/core.py | Line: 33-37 | Description: Web server routes
@app.route("/")
def home():
    return index("README.md")

@app.route("/<path:filename>")
def index(filename):
    # Document rendering logic
```

## Configuration

### Package Configuration (`pyproject.toml`)

The project uses modern Python packaging with PEP 621:

- **Build System**: setuptools with wheel support
- **Dependencies**: Clearly defined with version constraints
- **Scripts**: CLI entry point configuration
- **Development Tools**: Black, isort, mypy configuration
- **Testing**: pytest configuration and coverage settings

### Environment Variables

- `ANTHROPIC_API_KEY`: API key for Claude models
- `OPENAI_API_KEY`: API key for OpenAI models
- Python locale settings for automatic language detection

## Supported Languages

CodeViewX supports documentation generation in 8 languages:

- **Chinese** (中文) - Default, auto-detected
- **English** - Full support
- **Japanese** (日本語) - Full support
- **Korean** (한국어) - Full support
- **French** (Français) - Full support
- **German** (Deutsch) - Full support
- **Spanish** (Español) - Full support
- **Russian** (Русский) - Full support

## Key Features Summary

### 🤖 AI-Powered Analysis
- DeepAgents framework for intelligent code analysis
- LangChain integration for sophisticated prompt handling
- Configurable recursion limits and verbose output

### 🌐 Web Documentation
- Flask-based documentation server
- Beautiful Markdown rendering with Prism.js syntax highlighting
- Responsive design for desktop and mobile
- Mermaid diagram support

### 🔧 Developer Tools
- Comprehensive CLI with multiple options
- Python API for programmatic usage
- Fast code search with ripgrep integration
- Multi-language output support

### 📊 Progress Tracking
- Real-time progress indication
- Task management with TODO tracking
- Detailed logging options
- Performance metrics

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 2GB RAM minimum (4GB recommended)
- 500MB disk space for dependencies
- Internet connection for AI API access

### Optional Requirements
- ripgrep system binary for code search
- Modern web browser for documentation viewing
- Git for version control integration

## Performance Characteristics

- **Document Generation**: Typically 2-5 minutes for medium-sized projects
- **Memory Usage**: 200-500MB during analysis
- **Network**: Moderate API usage for AI processing
- **Storage**: Generated documents typically 1-10MB

---

*This overview provides a comprehensive introduction to the CodeViewX project structure, technology stack, and key features. For detailed implementation information, see the [Core Mechanisms](04-core-mechanisms.md) documentation.*