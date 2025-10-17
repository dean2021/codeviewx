# Development Guide

## Overview

This guide provides comprehensive information for developers who want to contribute to CodeViewX, extend its functionality, or understand the internal development processes.

## Development Environment Setup

### Prerequisites

- **Python**: 3.8 or higher
- **Git**: Version control system
- **ripgrep**: Fast code search tool
- **Code Editor**: VS Code, PyCharm, or similar
- **API Keys**: Anthropic Claude or OpenAI API key

### Initial Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

#### 3. Install Development Dependencies

```bash
# Install in development mode with all dependencies
pip install -e ".[dev]"

# Verify installation
pip list | grep codeviewx
```

#### 4. Install ripgrep

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows
choco install ripgrep
# or using scoop
scoop install ripgrep
```

#### 5. Configure API Keys

```bash
# Set environment variables
export ANTHROPIC_API_KEY='your-api-key-here'
# or
export OPENAI_API_KEY='your-api-key-here'

# Add to shell profile for persistence
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
```

### Development Tools Configuration

#### VS Code Setup

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug CodeViewX",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/codeviewx/cli.py",
            "args": ["--verbose", "-w", "${workspaceFolder}/examples"],
            "console": "integratedTerminal",
            "env": {
                "ANTHROPIC_API_KEY": "${env:ANTHROPIC_API_KEY}"
            }
        }
    ]
}
```

#### Pre-commit Hooks

Install pre-commit hooks for code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3
        args: [--line-length=100]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## Project Structure

### Directory Organization

```
codeviewx/
├── codeviewx/                 # Main package
│   ├── __init__.py           # Package exports
│   ├── __version__.py        # Version information
│   ├── cli.py                # Command-line interface
│   ├── core.py               # Core functionality
│   ├── tools/                # AI agent tools
│   │   ├── __init__.py       # Tool exports
│   │   ├── command.py        # Command execution
│   │   ├── filesystem.py     # File operations
│   │   └── search.py         # Code search
│   ├── prompts/              # AI prompt templates
│   │   ├── DocumentEngineer.md
│   │   ├── DocumentEngineer_compact.md
│   │   └── DocumentEngineer_original.md
│   ├── tpl/                  # Web templates
│   │   └── doc_detail.html   # Documentation page
│   └── static/               # Static assets
│       ├── css/              # Stylesheets
│       └── README.md
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_language.py
│   ├── test_progress.py
│   └── test_tools.py
├── examples/                 # Usage examples
│   ├── basic_usage.py
│   ├── language_demo.py
│   └── progress_demo.py
├── docs/                     # Generated documentation
├── pyproject.toml           # Package configuration
├── requirements.txt         # Dependencies
├── requirements-dev.txt     # Development dependencies
└── README.md               # Project documentation
```

### Code Organization Principles

1. **Single Responsibility**: Each module has a clear, focused purpose
2. **Dependency Injection**: Dependencies are injected rather than hard-coded
3. **Interface Segregation**: Public APIs are minimal and well-defined
4. **Configuration Driven**: Behavior is controlled through configuration
5. **Error Handling**: Comprehensive error handling with user-friendly messages

## Development Workflow

### 1. Feature Development

#### Create Feature Branch

```bash
# Create feature branch
git checkout -b feature/new-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

#### Development Steps

1. **Write Tests First** (TDD approach)
2. **Implement Feature**
3. **Run Tests**: `pytest tests/`
4. **Code Quality Checks**: `pre-commit run --all-files`
5. **Manual Testing**: Test CLI and API functionality

#### Example: Adding a New Tool

```python
# 1. Create tool in codeviewx/tools/new_tool.py
def new_analysis_tool(file_path: str, pattern: str) -> str:
    """
    New analysis tool for specialized file processing
    
    Args:
        file_path: Path to file to analyze
        pattern: Pattern to search for
        
    Returns:
        Analysis results
    """
    try:
        # Implementation here
        results = perform_analysis(file_path, pattern)
        return f"✅ Analysis complete: {results}"
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}"

# 2. Export in codeviewx/tools/__init__.py
from .new_tool import new_analysis_tool

__all__ = [
    # Existing tools...
    'new_analysis_tool',
]

# 3. Write tests in tests/test_new_tool.py
import pytest
from codeviewx.tools import new_analysis_tool

def test_new_analysis_tool():
    result = new_analysis_tool("test.txt", "pattern")
    assert "✅" in result

# 4. Register tool in core.py
tools = [
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
    new_analysis_tool,  # Add new tool
]
```

### 2. Testing

#### Test Structure

```python
# tests/test_example.py
import pytest
from codeviewx import generate_docs, detect_system_language

class TestCodeViewXCore:
    """Test core functionality"""
    
    def test_detect_system_language(self):
        """Test language detection"""
        language = detect_system_language()
        assert language in ['Chinese', 'English', 'Japanese', 'Korean', 
                          'French', 'German', 'Spanish', 'Russian']
    
    def test_generate_docs_basic(self, tmp_path):
        """Test basic documentation generation"""
        output_dir = tmp_path / "docs"
        generate_docs(
            working_directory="examples",
            output_directory=str(output_dir),
            doc_language="English",
            verbose=False
        )
        assert output_dir.exists()
        assert (output_dir / "README.md").exists()
```

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=codeviewx --cov-report=html

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_core.py::TestCodeViewXCore::test_detect_system_language
```

#### Test Categories

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Test performance characteristics

### 3. Code Quality

#### Code Formatting

```bash
# Format code with Black
black codeviewx/ tests/

# Sort imports with isort
isort codeviewx/ tests/

# Lint with flake8
flake8 codeviewx/ tests/

# Type check with mypy
mypy codeviewx/
```

#### Code Standards

1. **PEP 8 Compliance**: Follow Python style guidelines
2. **Type Hints**: Use type annotations for all public functions
3. **Docstrings**: Comprehensive docstrings for all modules and functions
4. **Error Handling**: Proper exception handling with informative messages

#### Documentation Standards

```python
def example_function(
    param1: str,
    param2: int = 10,
    param3: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Example function with comprehensive documentation
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter with default value
        param3: Optional parameter description
        
    Returns:
        Dictionary containing:
            - 'status': Operation status
            - 'data': Processed data
            - 'metadata': Additional information
            
    Raises:
        ValueError: When param1 is invalid
        FileNotFoundError: When required file is not found
        
    Examples:
        >>> result = example_function("test", 20, True)
        >>> print(result['status'])
        'success'
        
    Note:
        This function requires external dependencies that must be installed
        separately. See the requirements.txt file for details.
    """
```

### 4. Debugging

#### Debug Configuration

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use verbose mode
generate_docs(verbose=True)
```

#### Common Debugging Techniques

1. **Logging**: Add detailed logging for troubleshooting
2. **Assertion Checks**: Use assertions for debugging
3. **Print Statements**: Temporary print statements for quick debugging
4. **IDE Debugger**: Use IDE debugger for step-through debugging

#### Debugging Example

```python
def debug_generate_docs():
    """Debug version of generate_docs with detailed logging"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add debug prints
    print(f"Working directory: {working_directory}")
    print(f"Output directory: {output_directory}")
    
    # Use debugger breakpoints
    import pdb; pdb.set_trace()
    
    # Continue with generation
    generate_docs()
```

## Architecture Guidelines

### 1. Tool Development

#### Tool Interface Pattern

```python
def tool_function(param1: type1, param2: type2 = default) -> str:
    """
    Standard tool function pattern
    
    Returns:
        Formatted result string with success/error indicators
        - Success: "✅ Success message"
        - Error: "❌ Error message"
    """
    try:
        # Validate inputs
        if not param1:
            return "❌ Error: param1 is required"
        
        # Perform operation
        result = perform_operation(param1, param2)
        
        # Format success response
        return f"✅ Operation successful: {result}"
        
    except Exception as e:
        # Format error response
        return f"❌ Error: {str(e)}"
```

#### Tool Registration

```python
# In tools/__init__.py
__all__ = [
    'existing_tool1',
    'existing_tool2',
    'new_tool',  # Add new tool to exports
]

# In core.py
tools = [
    existing_tool1,
    existing_tool2,
    new_tool,  # Register new tool with agent
]
```

### 2. Error Handling

#### Exception Hierarchy

```python
class CodeViewXError(Exception):
    """Base exception for CodeViewX"""
    pass

class ConfigurationError(CodeViewXError):
    """Configuration-related errors"""
    pass

class ToolExecutionError(CodeViewXError):
    """Tool execution errors"""
    pass

class FileSystemError(CodeViewXError):
    """File system operation errors"""
    pass
```

#### Error Handling Pattern

```python
def safe_operation():
    """Example of comprehensive error handling"""
    try:
        # Validate preconditions
        if not validate_conditions():
            raise ConfigurationError("Invalid configuration")
        
        # Perform operation
        result = perform_operation()
        
        # Validate result
        if not result:
            raise ToolExecutionError("Operation returned invalid result")
        
        return result
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return "❌ Configuration error"
    except ToolExecutionError as e:
        logger.error(f"Tool execution error: {e}")
        return "❌ Tool execution failed"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "❌ Unexpected error occurred"
```

### 3. Configuration Management

#### Configuration Pattern

```python
# Configuration class
class CodeViewXConfig:
    """Centralized configuration management"""
    
    def __init__(self):
        self.working_directory = os.getcwd()
        self.output_directory = "docs"
        self.doc_language = None
        self.recursion_limit = 1000
        self.verbose = False
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
    
    def validate(self):
        """Validate configuration"""
        if not self.api_key:
            raise ConfigurationError("API key is required")
        
        if not os.path.exists(self.working_directory):
            raise ConfigurationError("Working directory does not exist")
    
    def from_args(self, args):
        """Load configuration from CLI arguments"""
        self.working_directory = args.working_directory or self.working_directory
        self.output_directory = args.output_directory or self.output_directory
        # ... other attributes
```

## Performance Optimization

### 1. Memory Management

#### Efficient File Processing

```python
def process_large_file(file_path: str) -> str:
    """Process large files efficiently"""
    try:
        # Process in chunks for large files
        chunk_size = 8192
        results = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Process chunk
                chunk_result = process_chunk(chunk)
                results.append(chunk_result)
        
        return combine_results(results)
        
    except MemoryError:
        return "❌ Error: File too large to process"
```

#### Caching Strategy

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def cached_analysis(file_path: str, file_hash: str) -> str:
    """Cached analysis with file hash for invalidation"""
    # Expensive analysis operation
    return perform_analysis(file_path)

def analyze_with_cache(file_path: str) -> str:
    """Analyze file with caching"""
    try:
        # Calculate file hash for cache key
        file_hash = calculate_file_hash(file_path)
        
        # Use cached result if available
        return cached_analysis(file_path, file_hash)
        
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}"
```

### 2. API Optimization

#### Prompt Optimization

```python
def create_compact_prompt(working_dir: str, output_dir: str, language: str) -> str:
    """Create optimized prompt for reduced token usage"""
    # Use compact template
    template = load_compact_template()
    
    # Minimize variable content
    context = {
        'wd': working_dir,  # Short variable names
        'od': output_dir,
        'lang': language[:3],  # Shorten language codes
    }
    
    return template.format(**context)
```

#### Batch Processing

```python
def batch_process_files(file_paths: List[str]) -> Dict[str, str]:
    """Process multiple files efficiently"""
    results = {}
    
    # Batch process files
    for file_path in file_paths:
        try:
            result = process_file(file_path)
            results[file_path] = result
        except Exception as e:
            results[file_path] = f"❌ Error: {str(e)}"
    
    return results
```

## Release Process

### 1. Version Management

#### Semantic Versioning

- **Major**: Breaking changes (2.0.0)
- **Minor**: New features (1.1.0)
- **Patch**: Bug fixes (1.0.1)

#### Version Update Process

```bash
# 1. Update version in __version__.py
echo '__version__ = "1.1.0"' > codeviewx/__version__.py

# 2. Update pyproject.toml
# Edit version field in pyproject.toml

# 3. Update CHANGELOG.md
# Add new version entry with changes

# 4. Commit changes
git add .
git commit -m "Release v1.1.0"

# 5. Create tag
git tag v1.1.0

# 6. Push to repository
git push origin main --tags
```

### 2. Testing Before Release

#### Pre-release Checklist

```bash
# 1. Run full test suite
pytest --cov=codeviewx

# 2. Run code quality checks
pre-commit run --all-files

# 3. Test installation
pip install -e .
codeviewx --help

# 4. Test documentation generation
codeviewx -w examples -o test-docs

# 5. Test web server
codeviewx --serve -o test-docs

# 6. Clean up test artifacts
rm -rf test-docs
```

### 3. Distribution

#### Build Package

```bash
# Install build dependencies
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*
```

#### Test Installation

```bash
# Test installation from wheel
pip install dist/codeviewx-1.1.0-py3-none-any.whl

# Test installation from source
pip install dist/codeviewx-1.1.0.tar.gz

# Verify installation
python -c "import codeviewx; print(codeviewx.__version__)"
```

## Contributing Guidelines

### 1. Pull Request Process

#### Before Submitting PR

1. **Create Feature Branch**: `git checkout -b feature/your-feature`
2. **Write Tests**: Comprehensive test coverage
3. **Update Documentation**: Include new features in docs
4. **Run Quality Checks**: `pre-commit run --all-files`
5. **Test Manual**: Verify functionality works end-to-end

#### Pull Request Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
```

### 2. Code Review Guidelines

#### Review Checklist

- **Functionality**: Does the code work as intended?
- **Testing**: Are tests comprehensive and appropriate?
- **Documentation**: Is the code well-documented?
- **Style**: Does the code follow project standards?
- **Performance**: Are there any performance concerns?
- **Security**: Are there any security implications?

#### Review Process

1. **Automated Checks**: CI/CD pipeline validation
2. **Peer Review**: Code review by at least one maintainer
3. **Testing**: Manual testing of new functionality
4. **Integration**: Verify no regressions in existing functionality

### 3. Community Guidelines

#### Code of Conduct

1. **Respect**: Treat all contributors with respect
2. **Inclusivity**: Welcome contributors from all backgrounds
3. **Constructive**: Provide constructive feedback
4. **Collaboration**: Work together to improve the project

#### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions and reviews

---

*This development guide provides comprehensive information for contributing to CodeViewX. For implementation details, see the [Core Mechanisms](04-core-mechanisms.md) documentation.*