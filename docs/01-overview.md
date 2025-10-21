# Project Overview

## Technology Stack

### Core Technologies

#### Python Framework
- **Python**: 3.8+ (primary development language)
- **Package Management**: setuptools with pyproject.toml
- **Code Quality**: Black (formatting), flake8 (linting), mypy (type checking)

#### AI and Machine Learning
- **LangChain**: 0.3.27 - AI/LLM integration framework
- **LangChain Anthropic**: 0.3.22 - Anthropic Claude integration
- **LangChain Core**: 0.3.79 - Core LangChain components
- **LangGraph**: 0.6.10 - Graph-based AI agent framework
- **DeepAgents**: 0.0.5 - AI agent framework for code analysis
- **LangSmith**: 0.4.34 - AI application monitoring and debugging

#### Web Framework and Content Processing
- **Flask**: 3.0.0 - Web server for documentation browser
- **Markdown**: 3.5.1 - Markdown processing with extensions
- **pymdown-extensions**: 10.5 - Enhanced Markdown extensions

#### Search and Utilities
- **ripgrepy**: 2.0.0 - Python bindings for ripgrep (fast code search)

### Development Tools
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting (line length: 100)
- **flake8**: Linting
- **mypy**: Type checking (non-strict mode)
- **isort**: Import sorting

## Project Structure

```
codeviewx/
├── codeviewx/                    # Main package directory
│   ├── __init__.py              # Package initialization and public API
│   ├── __version__.py           # Version information
│   ├── cli.py                   # Command-line interface (entry point)
│   ├── core.py                  # Core API functions
│   ├── generator.py             # Document generation logic
│   ├── server.py                # Flask web server
│   ├── i18n.py                  # Internationalization support
│   ├── language.py              # Language detection utilities
│   ├── prompt.py                # Prompt template system
│   ├── tools/                   # AI agent tools
│   │   ├── __init__.py          # Tools package initialization
│   │   ├── command.py           # Command execution tool
│   │   ├── filesystem.py        # File system operations
│   │   └── search.py            # Code search with ripgrep
│   ├── prompts/                 # AI prompt templates
│   │   ├── document_engineer.md # Main documentation generation prompt
│   │   └── document_engineer_zh.md # Chinese version
│   ├── static/                  # Static web assets
│   │   └── css/                 # CSS stylesheets
│   └── tpl/                     # HTML templates for web server
│       └── doc_detail.html      # Documentation page template
├── examples/                    # Usage examples
│   ├── basic_usage.py           # Basic API usage
│   ├── i18n_demo.py             # Internationalization demo
│   ├── language_demo.py         # Language detection demo
│   └── progress_demo.py         # Progress tracking demo
├── tests/                       # Test suite
│   ├── test_core.py             # Core functionality tests
│   ├── test_language.py         # Language detection tests
│   ├── test_progress.py         # Progress tracking tests
│   └── test_tools.py            # Tool functionality tests
├── docs/                        # Generated documentation (output)
├── dist/                        # Build artifacts
├── .git/                        # Git repository
├── pyproject.toml               # Project configuration and dependencies
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Development dependencies
├── README.md                    # Project README
├── CLAUDE.md                    # Claude Code development guide
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # GPL-3.0 license
└── MANIFEST.in                  # Package manifest
```

## Key Components

### 1. CLI Interface (`cli.py`)
- **Entry Point**: `main()` function - command-line argument parsing and execution
- **Features**: Multi-language support, verbose logging, web server mode
- **Configuration**: Working directory, output directory, language settings

### 2. Core API (`core.py`)
- **Public Functions**: `generate_docs()`, `start_document_web_server()`, `load_prompt()`
- **Abstraction Layer**: Clean interface between CLI and internal modules

### 3. Document Generator (`generator.py`)
- **AI Integration**: DeepAgents framework with LangChain
- **Agent Tools**: File system, search, command execution
- **Progress Tracking**: Real-time progress reporting with task planning
- **Output Management**: Structured documentation generation

### 4. Web Server (`server.py`)
- **Flask Application**: Documentation browsing interface
- **Markdown Processing**: Real-time markdown to HTML conversion
- **File Tree Navigation**: Dynamic documentation structure
- **Internationalization**: Multi-language UI support

### 5. Tools System (`tools/`)
- **File Operations**: Read, write, list directory contents
- **Search Integration**: ripgrep-based code searching
- **Command Execution**: System command running for project analysis
- **AI Agent Integration**: LangChain tool interface

### 6. Internationalization (`i18n.py`)
- **Multi-language Support**: English and Chinese UI
- **Dynamic Language Detection**: System locale-based detection
- **Message Formatting**: Parameterized message templates
- **Documentation Languages**: 8 supported languages for generated content

## Configuration and Dependencies

### Runtime Dependencies
```toml
dependencies = [
    "langchain>=0.3.27",
    "langchain-anthropic>=0.3.22", 
    "langchain-core>=0.3.79",
    "langchain-text-splitters>=0.3.11",
    "langgraph>=0.6.10",
    "langgraph-checkpoint>=2.1.2",
    "langgraph-prebuilt>=0.6.4",
    "langgraph-sdk>=0.2.9",
    "langsmith>=0.4.34",
    "deepagents>=0.0.5",
    "ripgrepy>=2.0.0",
    "flask>=2.0.0",
    "markdown>=3.4.0",
]
```

### Development Dependencies
```toml
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "flake8>=6.0",
    "mypy>=1.0",
    "isort>=5.0",
]
```

### Code Quality Configuration
- **Black**: Line length 100, Python 3.8+ targets
- **isort**: Black profile compatibility
- **pytest**: Verbose output by default
- **mypy**: Non-strict type checking (allow untyped defs)

## Entry Points and Execution Flow

### CLI Entry Point
```python
# File: codeviewx/cli.py | Lines: 16 | Description: Main CLI entry point
def main():
    """Command line entry point"""
    # Argument parsing, configuration, and execution
```

### Package Entry Point
```python
# File: pyproject.toml | Lines: 85 | Description: Package script entry point
[project.scripts]
codeviewx = "codeviewx.cli:main"
```

### Core API Entry Point
```python
# File: codeviewx/core.py | Lines: 19 | Description: Direct execution entry point  
if __name__ == "__main__":
    generate_docs(verbose=True)
```

## Supported Languages

### Documentation Generation
- Chinese (中文)
- English
- Japanese (日本語)
- Korean (한국어)
- French (Français)
- German (Deutsch)
- Spanish (Español)
- Russian (Русский)

### User Interface
- English (en)
- Chinese (zh)

## External Dependencies

### System Requirements
- **Python**: 3.8 or higher
- **ripgrep**: Fast text search utility (install via package manager)
  - macOS: `brew install ripgrep`
  - Ubuntu/Debian: `sudo apt install ripgrep`
  - Windows: `choco install ripgrep`

### API Keys
- **ANTHROPIC_API_KEY**: Required for Claude AI integration
- Optional: OpenAI API key for alternative models

## Project Type Classification

CodeViewX is classified as a **CLI Tool/Library SDK** hybrid:
- Primary usage: Command-line tool for documentation generation
- Secondary usage: Python library for integration into other projects
- Architecture: Event-driven AI agent system with web interface
- Domain: Developer tools and documentation automation