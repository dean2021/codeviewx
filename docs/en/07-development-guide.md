# Development Guide

This guide provides comprehensive information for developers who want to contribute to CodeViewX, extend its functionality, or understand its internal architecture.

## Development Environment Setup

### Prerequisites

Before setting up the development environment, ensure you have:

- **Python 3.8+** with pip
- **ripgrep (rg)** installed on your system
- **Git** for version control
- **Anthropic API key** for AI functionality

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Development Dependencies

The development setup includes additional tools for code quality and testing:

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **isort**: Import sorting

### Verify Installation

```bash
# Test the CLI installation
codeviewx --version

# Run basic functionality test
codeviewx --help

# Test AI functionality (requires API key)
export ANTHROPIC_API_KEY="your-api-key"
codeviewx --working-dir . --output-dir test_docs --verbose
```

## Project Structure Deep Dive

### Core Package Organization

```
codeviewx/
├── codeviewx/                    # Main package
│   ├── __init__.py              # Public API exports
│   ├── __version__.py           # Version information
│   ├── cli.py                   # Command-line interface
│   ├── core.py                  # Core API functions
│   ├── generator.py             # Main documentation generator
│   ├── server.py                # Web documentation server
│   ├── prompt.py                # Prompt template management
│   ├── i18n.py                  # Internationalization system
│   ├── language.py              # Language detection
│   ├── tools/                   # Tool modules
│   │   ├── __init__.py          # Tool exports
│   │   ├── filesystem.py        # File system operations
│   │   ├── search.py            # Code search functionality
│   │   └── command.py           # System command execution
│   ├── prompts/                 # AI prompt templates
│   │   ├── document_engineer.md     # English prompts
│   │   └── document_engineer_zh.md  # Chinese prompts
│   ├── tpl/                     # Web interface templates
│   │   └── doc_detail.html      # Documentation viewer template
│   └── static/                  # Static assets
│       ├── css/                 # Stylesheets
│       ├── js/                  # JavaScript files
│       └── images/              # Images and icons
├── tests/                       # Test suite
├── examples/                    # Usage examples
└── docs/                        # Generated documentation
```

### Module Responsibilities

#### `cli.py` - Command-Line Interface
- **Purpose**: Handle user input, argument parsing, and command coordination
- **Key Functions**:
  - `main()`: Primary CLI entry point
  - Argument parsing and validation
  - Progress reporting and error handling
- **Design Pattern**: Command Pattern with argparse

Reference: [cli.py](../codeviewx/cli.py#L16)

#### `core.py` - Public API
- **Purpose**: Provide clean, programmatic access to CodeViewX functionality
- **Key Functions**: Exports main functions from other modules
- **Design Pattern**: Facade Pattern - simplifies complex subsystem access

Reference: [core.py](../codeviewx/core.py#L12)

#### `generator.py` - Documentation Generator
- **Purpose**: Orchestrate the entire documentation generation process
- **Key Functions**:
  - `generate_docs()`: Main generation workflow
  - Progress tracking and user feedback
  - AI agent coordination
- **Design Pattern**: Orchestrator Pattern

Reference: [generator.py](../codeviewx/generator.py#L25)

#### `server.py` - Web Server
- **Purpose**: Provide interactive documentation browsing
- **Key Functions**:
  - `start_document_web_server()`: Flask server startup
  - `generate_file_tree()`: File tree generation
  - Markdown rendering with extensions
- **Design Pattern**: MVC Pattern with Flask

Reference: [server.py](../codeviewx/server.py#L140)

## Development Workflow

### Code Style and Quality

CodeViewX follows strict code quality standards:

#### Code Formatting with Black
```bash
# Format all Python files
black codeviewx/

# Check formatting without making changes
black --check codeviewx/

# Format specific file
black codeviewx/generator.py
```

#### Import Sorting with isort
```bash
# Sort imports in all files
isort codeviewx/

# Check without making changes
isort --check-only codeviewx/
```

#### Linting with flake8
```bash
# Run linting
flake8 codeviewx/

# Check specific file
flake8 codeviewx/cli.py
```

#### Type Checking with mypy
```bash
# Run type checking
mypy codeviewx/

# Check specific module
mypy codeviewx/generator.py
```

### Pre-commit Hooks

Set up pre-commit hooks to automatically enforce code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

Example `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### Testing

#### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=codeviewx --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run with verbose output
pytest -v

# Run specific test function
pytest tests/test_generator.py::test_generate_docs_basic
```

#### Writing Tests

Test files follow the pattern `test_*.py` in the `tests/` directory:

```python
# tests/test_generator.py
import pytest
from unittest.mock import patch, MagicMock
from codeviewx.generator import generate_docs

class TestGenerateDocs:
    def test_generate_docs_basic(self):
        """Test basic documentation generation"""
        with patch('codeviewx.generator.create_deep_agent') as mock_agent:
            mock_agent.return_value.stream.return_value = []
            
            generate_docs(
                working_directory="test_project",
                output_directory="test_docs",
                doc_language="English"
            )
            
            mock_agent.assert_called_once()
    
    def test_generate_docs_with_verbose(self):
        """Test documentation generation with verbose output"""
        with patch('codeviewx.generator.create_deep_agent') as mock_agent:
            mock_agent.return_value.stream.return_value = []
            
            generate_docs(verbose=True)
            
            # Verify logging level was set to DEBUG
            import logging
            assert logging.getLogger().level == logging.DEBUG
```

#### Test Structure

```python
# tests/conftest.py - Shared test fixtures
import pytest
import tempfile
import os

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample project structure
        os.makedirs(os.path.join(temp_dir, "src"))
        
        # Create sample files
        with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
            f.write("def main():\n    pass\n")
        
        yield temp_dir

@pytest.fixture
def mock_api_key():
    """Provide mock API key for testing"""
    return "test-api-key-12345"
```

### Debugging

#### Verbose Mode
Use verbose mode to see detailed execution information:

```bash
codeviewx --verbose --working-dir /path/to/project
```

#### Logging Configuration
For development, you can enable detailed logging:

```python
import logging

# Enable debug logging for all modules
logging.basicConfig(level=logging.DEBUG)

# Enable specific module logging
logging.getLogger('codeviewx.generator').setLevel(logging.DEBUG)
```

#### Common Debugging Scenarios

**AI Agent Issues**:
```python
# Add debugging to generator.py
import logging
logger = logging.getLogger(__name__)

# In generate_docs function:
logger.debug(f"Agent configuration: {agent_config}")
logger.debug(f"Tools registered: {[t.__name__ for t in tools]}")
```

**Tool Execution Issues**:
```python
# In tools/filesystem.py
import logging
logger = logging.getLogger(__name__)

def write_real_file(file_path: str, content: str) -> str:
    logger.debug(f"Writing to file: {file_path}")
    # ... implementation
    logger.debug(f"Successfully wrote {file_size} bytes")
```

## Adding New Features

### Adding a New Tool

To add a new analysis tool:

1. **Create Tool Function**:
```python
# codeviewx/tools/new_tool.py
def custom_analysis(file_path: str, pattern: str) -> str:
    """
    Custom analysis tool for specific patterns
    
    Args:
        file_path: Path to file to analyze
        pattern: Pattern to search for
    
    Returns:
        Analysis results as formatted string
    """
    try:
        # Implementation here
        return f"Analysis complete for {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"
```

2. **Export from Tools Package**:
```python
# codeviewx/tools/__init__.py
from .new_tool import custom_analysis

__all__ = [
    'execute_command',
    'ripgrep_search', 
    'write_real_file',
    'read_real_file',
    'list_real_directory',
    'custom_analysis',  # Add new tool
]
```

3. **Register Tool in Generator**:
```python
# codeviewx/generator.py
from .tools import (
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
    custom_analysis,  # Import new tool
)

# In generate_docs function:
tools = [
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
    custom_analysis,  # Add to tools list
]
```

4. **Add Tests**:
```python
# tests/test_new_tool.py
import pytest
from codeviewx.tools import custom_analysis

def test_custom_analysis_success():
    """Test successful custom analysis"""
    result = custom_analysis("test_file.py", "pattern")
    assert "Analysis complete" in result

def test_custom_analysis_error():
    """Test error handling"""
    result = custom_analysis("nonexistent.txt", "pattern")
    assert "Error:" in result
```

### Adding New Documentation Language

1. **Add Language Support to i18n.py**:
```python
# codeviewx/i18n.py
MESSAGES: Dict[str, Dict[str, str]] = {
    'en': { /* existing */ },
    'zh': { /* existing */ },
    'fr': {  # Add French
        'starting': '🚀 Démarrage du générateur de documentation CodeViewX',
        'working_dir': '📂 Répertoire de travail',
        # ... add all required translations
    }
}
```

2. **Update Language Detection**:
```python
# codeviewx/language.py
def detect_system_language() -> str:
    # Add French detection logic
    try:
        lang, _ = locale.getdefaultlocale()
        if lang:
            if lang.startswith('fr'):
                return 'French'
            # ... existing logic
    except Exception:
        pass
    return 'English'
```

3. **Create Language-Specific Prompt**:
```markdown
# codeviewx/prompts/document_engineer_fr.md
# Add French version of the prompt template
```

4. **Update CLI Options**:
```python
# codeviewx/cli.py
parser.add_argument(
    "-l", "--language",
    dest="doc_language",
    choices=['Chinese', 'English', 'French', 'Japanese', 'Korean', 'German', 'Spanish', 'Russian'],
    help="Documentation language"
)
```

### Adding New Output Format

To support a new documentation format (e.g., HTML, PDF):

1. **Create Output Formatter**:
```python
# codeviewx/formatters/html_formatter.py
def format_to_html(markdown_content: str) -> str:
    """Convert markdown to HTML"""
    import markdown
    html = markdown.markdown(
        markdown_content,
        extensions=['tables', 'fenced_code', 'toc']
    )
    return wrap_in_html_template(html)

def wrap_in_html_template(content: str) -> str:
    """Wrap content in HTML template"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Documentation</title></head>
    <body>{content}</body>
    </html>
    """
```

2. **Integrate with Generator**:
```python
# codeviewx/generator.py
def generate_docs(output_format="markdown", **kwargs):
    """Generate docs in specified format"""
    if output_format == "html":
        # Use HTML formatter
        from .formatters.html_formatter import format_to_html
        # Apply formatting to generated content
```

## Performance Optimization

### Profiling

Use Python's built-in profiling tools:

```bash
# Profile the generator
python -m cProfile -o profile.stats codeviewx --working-dir /path/to/project

# Analyze profile results
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(20)
"
```

### Memory Usage Monitoring

```python
# Add memory monitoring to generator.py
import psutil
import os

def log_memory_usage():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")

# Call this at key points in generate_docs()
```

### Optimization Strategies

1. **Caching**: Cache results of expensive operations
2. **Lazy Loading**: Load modules and resources only when needed
3. **Parallel Processing**: Use concurrent operations where possible
4. **Efficient Search**: Optimize ripgrep patterns and filters

## Architecture Decisions

### Why DeepAgents Framework?

The choice of DeepAgents provides several advantages:
- **Sophisticated Reasoning**: Multi-step AI reasoning capabilities
- **Tool Integration**: Natural tool usage and coordination
- **Error Recovery**: Built-in error handling and alternative strategies

### Why LangChain/LangGraph?

- **Workflow Management**: Structured AI workflow execution
- **State Management**: Maintains context across analysis steps
- **Ecosystem Integration**: Broad tool and model support

### Why ripgrep for Search?

- **Performance**: 10-100x faster than traditional grep
- **Feature Rich**: Regular expressions, file type filtering, ignore patterns
- **Cross-Platform**: Consistent behavior across operating systems

## Common Development Patterns

### Error Handling Pattern

```python
def robust_function(param1: str, param2: Optional[str] = None) -> str:
    """
    Standard error handling pattern for CodeViewX functions
    """
    try:
        # Validate inputs
        if not param1:
            return "❌ Error: Parameter 1 is required"
        
        # Core logic
        result = perform_operation(param1, param2)
        
        # Return success message
        return f"✅ Success: {result}"
        
    except FileNotFoundError as e:
        return f"❌ Error: File not found - {str(e)}"
    except PermissionError as e:
        return f"❌ Error: Permission denied - {str(e)}"
    except Exception as e:
        return f"❌ Error: Unexpected error - {str(e)}"
```

### Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

def logged_function():
    """Standard logging pattern"""
    logger.debug("Starting function execution")
    
    try:
        result = perform_operation()
        logger.info(f"Operation completed successfully: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise
```

### Tool Interface Pattern

```python
def standardized_tool(param1: str, param2: Optional[str] = None) -> str:
    """
    Standardized tool interface for AI agent integration
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (optional)
    
    Returns:
        Formatted string result or error message
    
    Examples:
        >>> standardized_tool("input")
        '✅ Success: Operation completed'
    """
    # Implementation
```

## Contributing Guidelines

### Code Review Process

1. **Create Feature Branch**:
```bash
git checkout -b feature/new-feature
```

2. **Make Changes**:
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation

3. **Run Quality Checks**:
```bash
black codeviewx/
isort codeviewx/
flake8 codeviewx/
mypy codeviewx/
pytest --cov=codeviewx
```

4. **Submit Pull Request**:
   - Clear description of changes
   - Reference related issues
   - Include testing instructions

### Commit Message Format

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(generator): add support for custom output formats

Adds HTML and PDF output generation capabilities through
new formatter modules. Includes comprehensive tests and
documentation updates.

Closes #123
```

```
fix(tools): handle empty directories in list_real_directory

Prevents crashes when scanning empty directories and
provides appropriate user feedback.

Fixes #456
```

### Issue Reporting

When reporting bugs or requesting features:

1. **Search existing issues** first
2. **Use appropriate templates**
3. **Provide complete information**:
   - Python version
   - Operating system
   - CodeViewX version
   - Steps to reproduce
   - Expected vs actual behavior

## Release Process

### Version Management

CodeViewX follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update version** in `codeviewx/__version__.py`
2. **Update changelog** in `CHANGELOG.md`
3. **Run full test suite** with coverage
4. **Update documentation**
5. **Tag release**:
```bash
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```
6. **Build and publish**:
```bash
python -m build
twine upload dist/*
```

This development guide provides comprehensive information for contributing to CodeViewX, from basic setup to advanced feature development. Following these guidelines ensures consistent, high-quality contributions to the project.