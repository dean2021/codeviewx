# Testing Documentation

This document provides comprehensive information about the testing strategy, test framework, and testing best practices used in CodeViewX.

## Testing Strategy Overview

CodeViewX employs a multi-layered testing approach to ensure reliability, correctness, and maintainability of the codebase. The testing strategy covers unit tests, integration tests, and end-to-end tests across all major components.

### Testing Goals

1. **Functionality Verification**: Ensure all features work as specified
2. **Regression Prevention**: Catch breaking changes before they reach users
3. **API Contract Testing**: Verify public APIs maintain backward compatibility
4. **Error Handling Validation**: Ensure robust error handling across all components
5. **Performance Validation**: Monitor performance characteristics and prevent degradation

### Test Coverage Targets

- **Unit Test Coverage**: Minimum 85% line coverage
- **Integration Test Coverage**: Critical workflows covered
- **API Test Coverage**: All public APIs tested
- **Error Path Coverage**: All error scenarios tested

## Test Framework Architecture

### Primary Testing Framework: pytest

CodeViewX uses pytest as the primary testing framework due to its powerful fixtures, parameterized testing, and plugin ecosystem.

#### pytest Configuration

```ini
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "api: marks tests that require API access"
]
```

Reference: [pyproject.toml](../pyproject.toml#L95-L104)

### Test Dependencies

Testing dependencies are defined in `requirements-dev.txt`:

```txt
pytest>=7.0.0              # Core testing framework
pytest-cov>=4.0.0          # Coverage reporting
pytest-mock>=3.10.0        # Mocking capabilities
pytest-asyncio>=0.21.0     # Async testing support
```

## Test Suite Structure

### Test Organization

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and configuration
├── test_core.py             # Core functionality tests
├── test_language.py         # Language detection tests
├── test_tools.py            # Tool module tests
├── test_progress.py         # Progress tracking tests
├── test_generator.py        # Documentation generator tests
├── test_server.py           # Web server tests
├── test_cli.py              # CLI interface tests
├── integration/             # Integration tests
│   ├── test_full_workflow.py
│   └── test_api_integration.py
└── fixtures/                # Test data and fixtures
    ├── sample_projects/
    └── mock_responses/
```

### Test Categories

#### Unit Tests
- **Purpose**: Test individual functions and methods in isolation
- **Scope**: Single function or class
- **Dependencies**: Mocked external dependencies
- **Execution Speed**: Fast (milliseconds)

#### Integration Tests
- **Purpose**: Test interaction between components
- **Scope**: Multiple components working together
- **Dependencies**: Real dependencies where appropriate
- **Execution Speed**: Medium (seconds)

#### End-to-End Tests
- **Purpose**: Test complete workflows from user perspective
- **Scope**: Full application workflows
- **Dependencies**: Real external services (when feasible)
- **Execution Speed**: Slow (minutes)

## Core Testing Components

### Test Fixtures

Shared fixtures defined in `conftest.py`:

```python
# tests/conftest.py
import pytest
import tempfile
import os
from unittest.mock import MagicMock
from codeviewx.i18n import I18n

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create standard project structure
        src_dir = os.path.join(temp_dir, "src")
        os.makedirs(src_dir)
        
        # Create sample files
        with open(os.path.join(src_dir, "main.py"), "w") as f:
            f.write("def main():\n    print('Hello World')\n")
        
        with open(os.path.join(temp_dir, "requirements.txt"), "w") as f:
            f.write("flask>=2.0.0\n")
        
        yield temp_dir

@pytest.fixture
def mock_ai_agent():
    """Create a mock AI agent for testing"""
    agent = MagicMock()
    agent.stream.return_value = [
        {"messages": [MagicMock(content="Analysis complete")]}
    ]
    return agent

@pytest.fixture
def test_i18n():
    """Create test i18n instance"""
    return I18n('en')
```

### Tool Testing

#### File System Tools

```python
# tests/test_tools.py
import pytest
import tempfile
import os
from codeviewx.tools import write_real_file, read_real_file, list_real_directory

class TestFileSystemTools:
    def test_write_real_file_success(self, temp_project_dir):
        """Test successful file writing"""
        test_file = os.path.join(temp_project_dir, "test.txt")
        content = "Test content"
        
        result = write_real_file(test_file, content)
        
        assert "✅ Successfully wrote file" in result
        assert os.path.exists(test_file)
        
        # Verify content
        with open(test_file, 'r') as f:
            assert f.read() == content
    
    def test_write_real_file_creates_directories(self, temp_project_dir):
        """Test that write_real_file creates parent directories"""
        deep_path = os.path.join(temp_project_dir, "deep", "nested", "file.txt")
        content = "Deep content"
        
        result = write_real_file(deep_path, content)
        
        assert "✅ Successfully wrote file" in result
        assert os.path.exists(deep_path)
    
    def test_read_real_file_success(self, temp_project_dir):
        """Test successful file reading"""
        test_file = os.path.join(temp_project_dir, "test.txt")
        content = "Line 1\nLine 2\nLine 3"
        
        with open(test_file, 'w') as f:
            f.write(content)
        
        result = read_real_file(test_file)
        
        assert "File:" in result
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result
    
    def test_read_real_file_not_found(self):
        """Test reading non-existent file"""
        result = read_real_file("nonexistent.txt")
        
        assert "❌ Error: File 'nonexistent.txt' does not exist" in result
    
    def test_list_real_directory_success(self, temp_project_dir):
        """Test successful directory listing"""
        # Create test structure
        os.makedirs(os.path.join(temp_project_dir, "subdir"))
        with open(os.path.join(temp_project_dir, "file1.txt"), 'w') as f:
            f.write("content")
        
        result = list_real_directory(temp_project_dir)
        
        assert "Total 1 directories, 1 files" in result
        assert "📁 subdir/" in result
        assert "📄 file1.txt" in result
```

#### Search Tools

```python
class TestSearchTools:
    def test_ripgrep_search_success(self, temp_project_dir):
        """Test successful pattern search"""
        # Create test Python file
        test_file = os.path.join(temp_project_dir, "test.py")
        with open(test_file, 'w') as f:
            f.write("def main():\n    pass\n\ndef helper():\n    pass\n")
        
        result = ripgrep_search("def main", temp_project_dir, "py")
        
        assert "def main" in result
        assert "test.py" in result
    
    def test_ripgrep_search_no_matches(self, temp_project_dir):
        """Test search with no matches"""
        test_file = os.path.join(temp_project_dir, "test.py")
        with open(test_file, 'w') as f:
            f.write("def main():\n    pass\n")
        
        result = ripgrep_search("def nonexistent", temp_project_dir, "py")
        
        assert "No matches found" in result
    
    def test_ripgrep_search_ignore_patterns(self, temp_project_dir):
        """Test that ignore patterns work correctly"""
        # Create files in ignored directories
        os.makedirs(os.path.join(temp_project_dir, ".git"))
        with open(os.path.join(temp_project_dir, ".git", "config"), 'w') as f:
            f.write("git config content")
        
        # Create normal file
        with open(os.path.join(temp_project_dir, "normal.txt"), 'w') as f:
            f.write("normal content")
        
        result = ripgrep_search("content", temp_project_dir)
        
        assert "normal.txt" in result
        assert ".git" not in result  # Should be ignored
```

### Core Functionality Testing

```python
# tests/test_core.py
import pytest
from unittest.mock import patch, MagicMock
from codeviewx.core import generate_docs, load_prompt
from codeviewx.language import detect_system_language
from codeviewx.i18n import get_i18n, t

class TestCoreFunctionality:
    def test_load_prompt_success(self):
        """Test successful prompt loading"""
        prompt = load_prompt("document_engineer")
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "You are a senior technical documentation engineer" in prompt
    
    def test_load_prompt_with_variables(self):
        """Test prompt loading with variable substitution"""
        prompt = load_prompt(
            "document_engineer",
            working_directory="/test/project",
            output_directory="/test/docs",
            doc_language="English"
        )
        
        assert "/test/project" in prompt
        assert "/test/docs" in prompt
        assert "English" in prompt
    
    def test_load_prompt_not_found(self):
        """Test loading non-existent prompt"""
        with pytest.raises(FileNotFoundError):
            load_prompt("nonexistent_prompt")
    
    @patch('codeviewx.generator.create_deep_agent')
    def test_generate_docs_basic(self, mock_create_agent, temp_project_dir):
        """Test basic documentation generation"""
        # Mock AI agent
        mock_agent = MagicMock()
        mock_agent.stream.return_value = [
            {"messages": [MagicMock(content="Analysis complete")]}
        ]
        mock_create_agent.return_value = mock_agent
        
        # Run generation
        generate_docs(
            working_directory=temp_project_dir,
            output_directory="test_docs"
        )
        
        # Verify agent was created and used
        mock_create_agent.assert_called_once()
        mock_agent.stream.assert_called_once()
    
    def test_detect_system_language(self):
        """Test language detection"""
        language = detect_system_language()
        assert language in ['Chinese', 'English', 'Japanese', 'Korean', 
                          'French', 'German', 'Spanish', 'Russian']
    
    def test_i18n_translation(self):
        """Test internationalization functionality"""
        i18n = get_i18n()
        
        # Test English translation
        i18n.set_locale('en')
        message = t('starting')
        assert "Starting" in message
        
        # Test Chinese translation
        i18n.set_locale('zh')
        message = t('starting')
        assert "启动" in message
```

### CLI Testing

```python
# tests/test_cli.py
import pytest
from unittest.mock import patch
from click.testing import CliRunner
from codeviewx.cli import main

class TestCLI:
    def test_cli_version(self):
        """Test version command"""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        
        assert result.exit_code == 0
        assert "CodeViewX" in result.output
    
    def test_cli_help(self):
        """Test help command"""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "CodeViewX" in result.output
        assert "--working-dir" in result.output
    
    @patch('codeviewx.generator.generate_docs')
    def test_cli_basic_generation(self, mock_generate):
        """Test basic CLI generation"""
        mock_generate.return_value = None
        
        runner = CliRunner()
        result = runner.invoke(main, [
            '--working-dir', '/test/project',
            '--output-dir', 'test_docs',
            '--language', 'English'
        ])
        
        assert result.exit_code == 0
        mock_generate.assert_called_once_with(
            working_directory='/test/project',
            output_directory='test_docs',
            doc_language='English',
            ui_language=None,
            recursion_limit=1000,
            verbose=False
        )
    
    @patch('codeviewx.server.start_document_web_server')
    def test_cli_serve_mode(self, mock_server):
        """Test CLI serve mode"""
        runner = CliRunner()
        
        # Should fail without docs directory
        result = runner.invoke(main, ['--serve', '--output-dir', 'nonexistent'])
        assert result.exit_code == 1
        assert "does not exist" in result.output
        
        # Should start server with docs directory
        with patch('os.path.exists', return_value=True):
            result = runner.invoke(main, ['--serve', '--output-dir', 'docs'])
            mock_server.assert_called_once_with('docs')
```

## Integration Testing

### Full Workflow Testing

```python
# tests/integration/test_full_workflow.py
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock

class TestFullWorkflow:
    @pytest.mark.integration
    @patch('codeviewx.generator.create_deep_agent')
    def test_complete_documentation_generation(self, mock_create_agent):
        """Test complete documentation generation workflow"""
        # Create mock agent that simulates real workflow
        mock_agent = MagicMock()
        
        # Simulate agent responses for different phases
        responses = [
            {"messages": [MagicMock(tool_calls=[
                MagicMock(name='write_todos', args={'todos': [
                    {'content': 'Analyze project', 'status': 'pending'},
                    {'content': 'Generate overview', 'status': 'pending'}
                ]})
            ])]},
            {"messages": [MagicMock(tool_calls=[
                MagicMock(name='list_real_directory', args={'directory': '/test'})
            ])]},
            {"messages": [MagicMock(tool_calls=[
                MagicMock(name='ripgrep_search', args={'pattern': 'def main'})
            ])]},
            {"messages": [MagicMock(tool_calls=[
                MagicMock(name='write_real_file', args={
                    'file_path': 'test_docs/01-overview.md',
                    'content': '# Project Overview'
                })
            ])]},
            {"messages": [MagicMock(tool_calls=[
                MagicMock(name='write_real_file', args={
                    'file_path': 'test_docs/02-quickstart.md',
                    'content': '# Quick Start'
                })
            ])]},
        ]
        
        mock_agent.stream.return_value = responses
        mock_create_agent.return_value = mock_agent
        
        # Create temporary project
        with tempfile.TemporaryDirectory() as temp_dir:
            os.makedirs(os.path.join(temp_dir, "src"))
            with open(os.path.join(temp_dir, "src", "main.py"), 'w') as f:
                f.write("def main(): pass")
            
            # Run full workflow
            from codeviewx.generator import generate_docs
            
            generate_docs(
                working_directory=temp_dir,
                output_directory="test_docs",
                doc_language="English"
            )
            
            # Verify all expected tool calls were made
            tool_names = [call['name'] for call in mock_agent.method_calls]
            assert 'write_todos' in tool_names
            assert 'list_real_directory' in tool_names
            assert 'ripgrep_search' in tool_names
            assert 'write_real_file' in tool_names
```

### API Integration Testing

```python
# tests/integration/test_api_integration.py
import pytest
from unittest.mock import patch

class TestAPIIntegration:
    @pytest.mark.api
    @pytest.mark.slow
    def test_real_api_integration(self):
        """Test integration with real Anthropic API (requires API key)"""
        import os
        
        # Skip if no API key
        if not os.getenv('ANTHROPIC_API_KEY'):
            pytest.skip("No ANTHROPIC_API_KEY available")
        
        # Create simple test project
        with tempfile.TemporaryDirectory() as temp_dir:
            os.makedirs(os.path.join(temp_dir, "src"))
            with open(os.path.join(temp_dir, "src", "main.py"), 'w') as f:
                f.write("""
def main():
    '''Main function for the application'''
    print("Hello World")
    
if __name__ == "__main__":
    main()
""")
            
            # Test real API call
            try:
                from codeviewx.generator import generate_docs
                
                generate_docs(
                    working_directory=temp_dir,
                    output_directory="test_docs",
                    doc_language="English",
                    recursion_limit=100  # Lower limit for faster testing
                )
                
                # Verify documentation was generated
                assert os.path.exists("test_docs/01-overview.md")
                assert os.path.exists("test_docs/02-quickstart.md")
                
            except Exception as e:
                pytest.fail(f"API integration test failed: {e}")
```

## Performance Testing

### Benchmark Testing

```python
# tests/test_performance.py
import pytest
import time
import tempfile
import os

class TestPerformance:
    @pytest.mark.slow
    def test_large_project_analysis_performance(self):
        """Test performance with large projects"""
        # Create large test project
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create many Python files
            for i in range(100):
                file_path = os.path.join(temp_dir, f"module_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(f"""
def function_{i}():
    '''Function {i} documentation'''
    return {i}

class Class{i}:
    '''Class {i} documentation'''
    
    def method_{i}(self):
        return self.function_{i}()
""")
            
            # Measure analysis time
            start_time = time.time()
            
            from codeviewx.tools import list_real_directory, ripgrep_search
            
            # Test directory listing performance
            result = list_real_directory(temp_dir)
            list_time = time.time() - start_time
            
            # Test search performance
            search_start = time.time()
            result = ripgrep_search("def function", temp_dir, "py")
            search_time = time.time() - search_start
            
            # Performance assertions (adjust based on expectations)
            assert list_time < 1.0, f"Directory listing too slow: {list_time}s"
            assert search_time < 2.0, f"Search too slow: {search_time}s"
    
    def test_memory_usage(self):
        """Test memory usage during operations"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Perform memory-intensive operations
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create many files
            for i in range(1000):
                file_path = os.path.join(temp_dir, f"file_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(f"def function_{i}(): pass\n")
            
            # Analyze all files
            from codeviewx.tools import ripgrep_search
            result = ripgrep_search("def function", temp_dir, "py")
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Memory usage should be reasonable
            assert memory_increase < 100, f"Memory usage too high: {memory_increase} MB increase"
```

## Test Data Management

### Test Fixtures and Data

```python
# tests/fixtures/sample_projects.py
import tempfile
import os

def create_sample_web_project(temp_dir):
    """Create a sample web project for testing"""
    # Project structure
    dirs = ['src', 'tests', 'docs', 'static']
    for dir_name in dirs:
        os.makedirs(os.path.join(temp_dir, dir_name))
    
    # Configuration files
    with open(os.path.join(temp_dir, 'requirements.txt'), 'w') as f:
        f.write("flask>=2.0.0\npytest>=7.0.0\n")
    
    # Main application
    with open(os.path.join(temp_dir, 'src', 'app.py'), 'w') as f:
        f.write("""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return {'message': 'Hello World'}

if __name__ == '__main__':
    app.run(debug=True)
""")
    
    # Test files
    with open(os.path.join(temp_dir, 'tests', 'test_app.py'), 'w') as f:
        f.write("""
import pytest
from src.app import app

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_api_data():
    with app.test_client() as client:
        response = client.get('/api/data')
        assert response.status_code == 200
        assert 'message' in response.json
""")

def create_sample_cli_project(temp_dir):
    """Create a sample CLI project for testing"""
    # Project structure
    dirs = ['src', 'tests']
    for dir_name in dirs:
        os.makedirs(os.path.join(temp_dir, dir_name))
    
    # Main CLI module
    with open(os.path.join(temp_dir, 'src', 'cli.py'), 'w') as f:
        f.write("""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Sample CLI tool')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('input_file', help='Input file to process')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Processing {args.input_file}")
    
    # Process file
    try:
        with open(args.input_file, 'r') as f:
            content = f.read()
            print(f"File has {len(content.split())} words")
    except FileNotFoundError:
        print(f"Error: File {args.input_file} not found")
        sys.exit(1)

if __name__ == '__main__':
    main()
""")
```

## Continuous Integration Testing

### GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Install ripgrep
      run: |
        sudo apt-get update
        sudo apt-get install -y ripgrep
    
    - name: Run unit tests
      run: |
        pytest tests/ -m "not integration and not api" --cov=codeviewx --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/ -m "integration" --cov=codeviewx --cov-report=xml --cov-append
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

### Quality Gates

```yaml
# .github/workflows/quality.yml
name: Quality Checks

on:
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Check code formatting
      run: |
        black --check codeviewx/
    
    - name: Check import sorting
      run: |
        isort --check-only codeviewx/
    
    - name: Run linting
      run: |
        flake8 codeviewx/
    
    - name: Run type checking
      run: |
        mypy codeviewx/
    
    - name: Run security checks
      run: |
        bandit -r codeviewx/
```

## Running Tests

### Local Development

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=codeviewx --cov-report=html

# Run specific test categories
pytest -m unit                    # Unit tests only
pytest -m integration             # Integration tests only
pytest -m "not slow"              # Exclude slow tests

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_tools.py

# Run specific test function
pytest tests/test_tools.py::TestFileSystemTools::test_write_real_file_success

# Run with debugging
pytest --pdb -x  # Stop on first failure and open debugger
```

### CI/CD Integration

```bash
# In CI environment
pytest --junitxml=test-results.xml --cov=codeviewx --cov-report=xml

# Generate coverage badge
coverage-badge
```

## Test Best Practices

### Writing Good Tests

1. **Descriptive Test Names**: Use clear, descriptive test names that explain what is being tested
2. **Arrange-Act-Assert Pattern**: Structure tests with clear setup, execution, and assertion phases
3. **Test Independence**: Ensure tests don't depend on each other
4. **Mock External Dependencies**: Mock external services and APIs
5. **Test Edge Cases**: Test both happy paths and error conditions
6. **Use Fixtures**: Reuse test setup code through fixtures

### Example of Well-Structured Test

```python
def test_write_real_file_creates_nested_directories_and_writes_content():
    """
    Test that write_real_file creates parent directories when they don't exist
    and successfully writes content to the target file.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        deep_path = os.path.join(temp_dir, "level1", "level2", "test.txt")
        content = "Test content for nested file"
        
        # Act
        result = write_real_file(deep_path, content)
        
        # Assert
        assert "✅ Successfully wrote file" in result
        assert os.path.exists(deep_path)
        
        with open(deep_path, 'r') as f:
            assert f.read() == content
```

This comprehensive testing documentation ensures CodeViewX maintains high quality standards and provides reliable functionality to users.