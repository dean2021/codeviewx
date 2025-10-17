# Development Guide

## Overview

This guide provides comprehensive information for developers who want to contribute to CodeViewX, including development environment setup, coding standards, testing practices, and contribution guidelines.

## Development Environment Setup

### Prerequisites

- **Python**: 3.8 or higher
- **Git**: For version control
- **ripgrep (rg)**: Code search tool
- **Anthropic API Key**: For AI functionality testing

### Local Development Setup

#### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

#### 2. Configuration

```bash
# Set up environment variables
export ANTHROPIC_API_KEY="your-api-key-here"

# Verify installation
codeviewx --version
```

#### 3. Development Tools Configuration

```bash
# Install pre-commit hooks (if configured)
pre-commit install

# Verify development tools
black --version
flake8 --version
mypy --version
```

## Project Structure for Developers

```
codeviewx/
├── 📁 codeviewx/                 # Main package
│   ├── 📄 __init__.py           # Package exports
│   ├── 📄 __version__.py        # Version information
│   ├── 📄 cli.py                # CLI interface
│   ├── 📄 core.py               # Core API
│   ├── 📄 generator.py          # Main generator
│   ├── 📄 server.py             # Web server
│   ├── 📄 prompt.py             # Prompt management
│   ├── 📄 i18n.py               # Internationalization
│   ├── 📄 language.py           # Language detection
│   ├── 📁 prompts/              # AI prompt templates
│   ├── 📁 tools/                # Custom tools
│   ├── 📁 tpl/                  # HTML templates
│   └── 📁 static/               # Static assets
├── 📁 tests/                    # Test files
├── 📁 examples/                 # Example usage
├── 📄 pyproject.toml            # Project configuration
└── 📄 requirements-dev.txt      # Development dependencies
```

## Code Standards and Guidelines

### 1. Code Style

#### Black Formatting

CodeViewX uses Black for code formatting. Configure your editor to use Black or run it manually:

```bash
# Format all code
black codeviewx/

# Check formatting without changing files
black --check codeviewx/

# Format specific file
black codeviewx/cli.py
```

**Configuration** (from `pyproject.toml`):
```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
```

#### Import Sorting

Use isort for import organization:

```bash
# Sort imports
isort codeviewx/

# Check without changing
isort --check-only codeviewx/
```

**Configuration**:
```toml
[tool.isort]
profile = "black"
line_length = 100
```

### 2. Type Hints

CodeViewX uses mypy for type checking. Add type hints to all functions:

```python
# Good practice
from typing import Optional, List, Dict
from pathlib import Path

def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    verbose: bool = False
) -> None:
    """Generate documentation for a project."""
    pass

# Return type hints
def detect_system_language() -> str:
    """Auto-detect system language."""
    return "English"
```

### 3. Documentation Standards

#### Docstrings

Use Google-style docstrings:

```python
def read_real_file(file_path: str) -> str:
    """Read file content from real filesystem.
    
    Args:
        file_path: File path (relative or absolute)
        
    Returns:
        File content, or error message if failed
        
    Raises:
        FileNotFoundError: When file doesn't exist
        PermissionError: When no read permission
        
    Examples:
        >>> read_real_file("main.py")
        'print("hello world")'
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"❌ Error: File '{file_path}' does not exist"
```

#### Comments

Add meaningful comments for complex logic:

```python
# Check if TOC marker exists, insert if missing for auto-generation
if '[TOC]' not in content:
    lines = content.split('\n')
    insert_index = 0
    # Find first heading to insert TOC before it
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            insert_index = i
            break
```

### 4. Error Handling

Follow consistent error handling patterns:

```python
# Use specific exception types
try:
    result = subprocess.run(command, timeout=30)
except subprocess.TimeoutExpired:
    return "❌ Error: Command execution timeout (30 seconds)"
except FileNotFoundError:
    return f"❌ Error: Command not found: {command}"
except Exception as e:
    return f"❌ Unexpected error: {str(e)}"

# Always provide user-friendly error messages
def validate_file_path(file_path: str) -> bool:
    """Validate file path is safe and accessible."""
    if not file_path:
        raise ValueError("File path cannot be empty")
    
    # Prevent path traversal attacks
    if '..' in file_path or file_path.startswith('/'):
        raise ValueError("Invalid file path: path traversal not allowed")
    
    return True
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=codeviewx --cov-report=html

# Run specific test file
pytest tests/test_generator.py

# Run with verbose output
pytest -v

# Run specific test function
pytest tests/test_cli.py::test_main_help
```

### Test Structure

```
tests/
├── test_cli.py              # CLI interface tests
├── test_generator.py        # Generator tests
├── test_server.py           # Web server tests
├── test_i18n.py             # Internationalization tests
├── test_tools/              # Tool tests
│   ├── test_filesystem.py
│   ├── test_search.py
│   └── test_command.py
└── fixtures/                # Test data and mock files
```

### Writing Tests

#### Unit Tests

```python
# tests/test_i18n.py
import pytest
from codeviewx.i18n import I18n, detect_ui_language

def test_i18n_basic_translation():
    """Test basic message translation."""
    i18n = I18n('en')
    assert i18n.t('starting') == '🚀 Starting CodeViewX Documentation Generator'

def test_i18n_parameter_substitution():
    """Test parameter substitution in translations."""
    i18n = I18n('en')
    result = i18n.t('generated_files', count=5)
    assert '5' in result

def test_detect_ui_language():
    """Test UI language detection."""
    # This test may need mocking for different system locales
    result = detect_ui_language()
    assert result in ['en', 'zh']
```

#### Integration Tests

```python
# tests/test_generator.py
import pytest
import tempfile
import os
from codeviewx.generator import generate_docs

def test_generate_docs_basic():
    """Test basic documentation generation."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a simple test project
        test_project = os.path.join(temp_dir, "test_project")
        os.makedirs(test_project)
        
        # Write test files
        with open(os.path.join(test_project, "main.py"), "w") as f:
            f.write('print("Hello, World!")')
        
        output_dir = os.path.join(temp_dir, "docs")
        
        # Generate documentation (this would need mocking for CI)
        # generate_docs(
        #     working_directory=test_project,
        #     output_directory=output_dir,
        #     doc_language="English"
        # )
        
        # Verify documentation files exist
        # assert os.path.exists(os.path.join(output_dir, "README.md"))
```

#### Mock Tests for AI Components

```python
# tests/test_generator.py
import pytest
from unittest.mock import Mock, patch
from codeviewx.generator import generate_docs

@patch('codeviewx.generator.create_deep_agent')
def test_generate_docs_with_mock_agent(mock_create_agent):
    """Test documentation generation with mocked AI agent."""
    # Mock the AI agent
    mock_agent = Mock()
    mock_agent.stream.return_value = [
        {"messages": [Mock(type="AIMessage", content="Documentation generated")]}
    ]
    mock_create_agent.return_value = mock_agent
    
    with tempfile.TemporaryDirectory() as temp_dir:
        generate_docs(
            working_directory=temp_dir,
            output_directory=os.path.join(temp_dir, "docs"),
            doc_language="English"
        )
        
        # Verify agent was created and called
        mock_create_agent.assert_called_once()
        mock_agent.stream.assert_called_once()
```

### Coverage Requirements

- **Target Coverage**: 80% or higher
- **Critical Paths**: 100% coverage for core functionality
- **Error Handling**: All error paths should be tested

```bash
# Generate coverage report
pytest --cov=codeviewx --cov-report=html --cov-fail-under=80

# View coverage report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-ai-tool

# Make changes
# ... develop feature ...

# Run tests
pytest
black codeviewx/
flake8 codeviewx/
mypy codeviewx/

# Commit changes
git add .
git commit -m "feat: add new AI tool for XYZ analysis"

# Push and create PR
git push origin feature/new-ai-tool
```

### 2. Commit Message Standards

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Maintenance tasks

**Examples**:
```
feat(cli): add verbose mode flag
fix(generator): handle empty directories gracefully
docs(readme): update installation instructions
```

### 3. Code Review Process

#### Before Submitting PR

1. **Code Quality**:
   ```bash
   # Run all quality checks
   black codeviewx/
   isort codeviewx/
   flake8 codeviewx/
   mypy codeviewx/
   pytest
   ```

2. **Functionality Testing**:
   - Test new features manually
   - Test edge cases and error conditions
   - Verify backward compatibility

3. **Documentation**:
   - Update relevant documentation
   - Add examples for new features
   - Update CHANGELOG if applicable

#### Review Guidelines

- **Code Review**: Focus on logic, style, and best practices
- **Test Coverage**: Ensure new code is properly tested
- **Documentation**: Verify documentation is accurate and complete
- **Performance**: Consider performance implications

## Architecture Guidelines

### 1. Module Design

#### Single Responsibility

Each module should have a single, well-defined responsibility:

```python
# Good: Separate concerns
# cli.py - Command line interface only
# generator.py - Documentation generation only
# server.py - Web server only

# Avoid: Mixed responsibilities
# avoid putting CLI logic in generator.py
```

#### Dependency Injection

Use dependency injection for testability:

```python
# Good: Configurable dependencies
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    agent_factory: Callable = create_deep_agent,  # Injectable
    verbose: bool = False
) -> None:
    agent = agent_factory(tools, prompt)
```

### 2. Tool System Design

When creating new tools for AI agents:

```python
# New tool template
def new_tool(
    parameter1: str,
    parameter2: Optional[int] = None,
    **kwargs
) -> str:
    """New tool for AI agents.
    
    Args:
        parameter1: Description of parameter1
        parameter2: Description of parameter2
        
    Returns:
        Tool result description
        
    Examples:
        >>> new_tool("test")
        'Success: operation completed'
    """
    try:
        # Tool implementation
        result = perform_operation(parameter1, parameter2)
        return f"✅ Success: {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

### 3. Internationalization

When adding new user-facing text:

```python
# 1. Add to MESSAGES dictionary in i18n.py
MESSAGES = {
    'en': {
        # ... existing messages
        'new_feature_description': 'New feature description: {detail}',
    },
    'zh': {
        # ... existing messages
        'new_feature_description': '新功能描述：{detail}',
    }
}

# 2. Use translation function
from codeviewx.i18n import t
print(t('new_feature_description', detail="feature details"))
```

## Debugging and Troubleshooting

### 1. Debug Mode

Enable verbose logging for development:

```bash
# Run with debug output
codeviewx --verbose

# Python API with debug
generate_docs(verbose=True)
```

### 2. Common Issues

#### API Key Problems

```python
# Debug API key issues
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"API Key present: {bool(api_key)}")
```

#### Tool Execution Issues

```python
# Debug tool execution
from codeviewx.tools import execute_command

# Test command execution
result = execute_command("echo 'test'", working_dir=".")
print(result)
```

#### Import Issues

```python
# Debug import paths
import sys
print(sys.path)

# Test module imports
try:
    from codeviewx import generate_docs
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
```

### 3. Performance Profiling

```python
# Profile execution time
import time
import cProfile

def profile_generation():
    start_time = time.time()
    generate_docs(...)
    end_time = time.time()
    print(f"Generation took {end_time - start_time:.2f} seconds")

# Detailed profiling
cProfile.run('generate_docs(...)', 'profile_output.prof')
```

## Release Process

### 1. Version Management

Version information is managed in `codeviewx/__version__.py`:

```python
# __version__.py
__version__ = "0.1.0"
__author__ = "CodeViewX Team"
__description__ = "AI-powered code documentation generator"
```

### 2. Release Checklist

#### Before Release

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version number incremented
- [ ] Performance tests run
- [ ] Security review completed

#### Release Process

```bash
# 1. Update version
echo "__version__ = '0.2.0'" > codeviewx/__version__.py

# 2. Update changelog
# Edit CHANGELOG.md

# 3. Run full test suite
pytest --cov=codeviewx

# 4. Build package
python -m build

# 5. Upload to PyPI (if applicable)
python -m twine upload dist/*

# 6. Create Git tag
git tag v0.2.0
git push origin v0.2.0
```

### 3. Testing Releases

```bash
# Test local build
pip install dist/codeviewx-0.2.0-py3-none-any.whl

# Test installation from source
pip install git+https://github.com/dean2021/codeviewx.git@v0.2.0
```

## Contributing Guidelines

### 1. Types of Contributions

- **Bug Reports**: Use GitHub Issues with detailed information
- **Feature Requests**: Describe use case and proposed solution
- **Code Contributions**: Follow development workflow
- **Documentation**: Improve existing documentation
- **Testing**: Add tests for uncovered scenarios

### 2. Issue Reporting

#### Bug Report Template

```markdown
## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Run command `...`
2. With parameters `...`
3. See error `...`

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS 13.0]
- Python: [e.g., 3.9.0]
- CodeViewX: [e.g., 0.1.0]
```

#### Feature Request Template

```markdown
## Feature Description
Clear description of requested feature

## Use Case
Why this feature is needed

## Proposed Solution
How the feature should work

## Alternatives Considered
Other approaches considered
```

### 3. Community Guidelines

- **Be Respectful**: Maintain professional and constructive communication
- **Be Helpful**: Assist others and share knowledge
- **Be Patient**: Allow time for review and discussion
- **Be Thorough**: Provide complete information in issues and PRs

### 4. Getting Help

- **Documentation**: Check existing documentation first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for sensitive issues

## Resources

### Development Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing framework

### Documentation

- **CodeViewX Documentation**: This guide and other docs
- **Anthropic Claude API**: https://docs.anthropic.com/
- **DeepAgents Framework**: https://github.com/whoami1234321/deepagents
- **LangChain Documentation**: https://python.langchain.com/

### Community

- **GitHub Repository**: https://github.com/dean2021/codeviewx
- **Issues**: https://github.com/dean2021/codeviewx/issues
- **Discussions**: https://github.com/dean2021/codeviewx/discussions

---

*Thank you for contributing to CodeViewX! Your contributions help make code documentation more accessible and comprehensive for everyone.*