# Project Overview

## Introduction

CodeViewX is an intelligent code documentation generator that leverages artificial intelligence to analyze source code repositories and automatically generate comprehensive technical documentation. The project combines advanced AI technologies with practical development tools to provide a seamless documentation experience for developers.

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Primary programming language |
| **LangChain** | 0.3.27+ | AI framework for building applications |
| **LangChain Anthropic** | 0.3.22+ | Integration with Anthropic Claude |
| **LangChain Core** | 0.3.79+ | Core LangChain functionality |
| **LangChain Text Splitters** | 0.3.11+ | Text processing utilities |
| **LangGraph** | 0.6.10+ | Graph-based AI workflow orchestration |
| **LangGraph Checkpoint** | 2.1.2+ | State management for workflows |
| **LangGraph Prebuilt** | 0.6.4+ | Pre-built components |
| **LangGraph SDK** | 0.2.9+ | SDK for LangGraph integration |
| **LangSmith** | 0.4.34+ | AI development and monitoring platform |
| **DeepAgents** | 0.0.5+ | AI agent framework |
| **Flask** | 3.0.0+ | Web framework for documentation server |
| **Markdown** | 3.5.1+ | Markdown processing |
| **Ripgrep** | 2.0.0+ (ripgrepy) | High-performance text search |

### Development Dependencies

| Dependency | Purpose |
|------------|---------|
| **pytest** | Testing framework |
| **pytest-cov** | Coverage testing |
| **black** | Code formatting |
| **flake8** | Linting |
| **mypy** | Type checking |
| **isort** | Import sorting |

## Project Structure

```
codeviewx/
├── codeviewx/                    # Main package directory
│   ├── __init__.py              # Package initialization and exports
│   ├── __version__.py           # Version information
│   ├── cli.py                   # Command-line interface
│   ├── core.py                  # Core functionality module
│   ├── generator.py             # Documentation generation engine
│   ├── language.py              # Language detection utilities
│   ├── prompt.py                # Prompt loading and management
│   ├── server.py                # Web documentation server
│   ├── tools/                   # AI agent tools
│   │   ├── __init__.py          # Tools package initialization
│   │   ├── command.py           # System command execution tool
│   │   ├── filesystem.py        # File system operations
│   │   └── search.py            # Code search functionality
│   ├── prompts/                 # AI prompt templates
│   │   ├── DocumentEngineer.md      # Original comprehensive prompt
│   │   └── DocumentEngineer_compact.md  # Optimized compact prompt
│   ├── static/                  # Static web assets
│   │   └── css/                 # Stylesheets
│   │       └── typo.css         # Typography and styling
│   └── tpl/                     # HTML templates
│       └── doc_detail.html      # Documentation page template
├── examples/                    # Usage examples
│   ├── basic_usage.py           # Basic usage example
│   ├── language_demo.py         # Multi-language demo
│   └── progress_demo.py         # Progress tracking demo
├── tests/                       # Test suite
│   ├── __init__.py              # Test package initialization
│   ├── test_core.py             # Core functionality tests
│   ├── test_language.py         # Language detection tests
│   ├── test_progress.py         # Progress tracking tests
│   └── test_tools.py            # Tools functionality tests
├── docs/                        # Generated documentation
│   ├── zh/                      # Chinese documentation
│   └── en/                      # English documentation
├── pyproject.toml               # Project configuration and metadata
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Development dependencies
├── README.md                    # Project README
├── CHANGELOG.md                 # Version history
├── LICENSE                      # GPL-3.0 license
├── MANIFEST.in                  # Package manifest
└── .gitignore                   # Git ignore rules
```

## Core Components

### 1. Main Package (`codeviewx/`)

The main package contains the core functionality organized into focused modules:

- **`__init__.py`**: Package initialization with convenient imports
- **`cli.py`**: Command-line interface using argparse
- **`core.py`**: Public API exports and module coordination
- **`generator.py`**: Main documentation generation engine with AI workflow orchestration
- **`language.py`**: System language detection for multi-language support
- **`prompt.py`**: AI prompt template loading and variable substitution
- **`server.py`**: Flask-based web server for documentation browsing

### 2. Tools (`codeviewx/tools/`)

Specialized tools that provide AI agents with capabilities to interact with the system:

- **`command.py`**: Execute system commands with timeout and error handling
- **`filesystem.py`**: Read, write, and list file/directory operations
- **`search.py`**: High-performance code search using ripgrep

### 3. Templates and Assets

- **`prompts/`**: AI prompt templates for documentation generation
- **`tpl/`**: HTML templates for web documentation interface
- **`static/`**: CSS and other static assets for the web interface

### 4. Examples and Tests

- **`examples/`**: Demonstrative scripts showing various usage patterns
- **`tests/`**: Comprehensive test suite covering all major functionality

## Key Features

### AI-Powered Documentation Generation

The core functionality revolves around using AI to analyze code structure and generate documentation:

1. **Code Analysis**: Intelligent scanning of project structure, dependencies, and code patterns
2. **Content Generation**: AI-driven creation of comprehensive documentation sections
3. **Multi-format Output**: Support for various documentation formats with structured organization

### Multi-Language Support

Supports documentation generation in 8 languages with automatic language detection:

- Chinese, English, Japanese, Korean
- French, German, Spanish, Russian

### Web Documentation Browser

Built-in Flask web server provides an elegant documentation viewing experience:

- Markdown rendering with syntax highlighting
- Interactive table of contents
- File tree navigation
- Mermaid diagram support

### Developer-Friendly CLI

Comprehensive command-line interface with various options:

```bash
# Basic usage
codeviewx

# Advanced usage
codeviewx -w /path/to/project -o docs -l English --verbose

# Web server mode
codeviewx --serve -o docs
```

## Development Workflow

### Installation and Setup

1. **Clone Repository**: Standard git clone workflow
2. **Install Dependencies**: pip with development dependencies
3. **Configure API Keys**: Environment variables for AI services
4. **Install ripgrep**: System dependency for code search

### Development Environment

- **Code Formatting**: Black with 100-character line length
- **Import Sorting**: isort with Black profile
- **Type Checking**: mypy for static analysis
- **Linting**: flake8 for code quality
- **Testing**: pytest with coverage reporting

### Build and Distribution

- **Build System**: setuptools with setuptools_scm
- **Package Configuration**: pyproject.toml for modern Python packaging
- **Distribution**: Supports wheel distribution via PyPI

## Integration Points

### AI Framework Integration

The project integrates deeply with modern AI frameworks:

- **LangChain**: For AI orchestration and prompt management
- **LangGraph**: For complex workflow management
- **DeepAgents**: For agent-based AI interactions
- **Anthropic Claude**: For high-quality text generation

### System Integration

- **File System**: Direct interaction with project files and directories
- **Command Line**: Shell command execution for system operations
- **Web Server**: HTTP server for documentation serving
- **Text Processing**: Markdown parsing and rendering

## Configuration and Customization

### Project Configuration

- **pyproject.toml**: Centralized project configuration
- **requirements.txt**: Runtime dependencies
- **requirements-dev.txt**: Development dependencies

### AI Configuration

- **API Keys**: Configured via environment variables
- **Prompts**: Customizable through prompt templates
- **Model Selection**: Configurable through AI framework settings

### Web Server Configuration

- **Templates**: Customizable HTML templates
- **Static Assets**: Configurable CSS and JavaScript
- **Routing**: Flexible Flask routing configuration

## Quality Assurance

### Testing Strategy

- **Unit Tests**: Comprehensive test coverage for all modules
- **Integration Tests**: End-to-end testing of workflows
- **Example Validation**: Verified example scripts
- **Error Handling**: Robust error handling and validation

### Code Quality

- **Type Hints**: Full type annotation coverage
- **Documentation**: Comprehensive docstrings and comments
- **Code Style**: Consistent formatting and linting
- **Error Messages**: Clear, actionable error reporting

This overview provides a comprehensive understanding of the CodeViewX project structure, technology stack, and core capabilities. The following sections will dive deeper into specific aspects of the system, including usage guides, architecture details, and development workflows.