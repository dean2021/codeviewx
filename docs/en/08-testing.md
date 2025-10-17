# Testing Strategy

## Overview

This document outlines the comprehensive testing strategy for CodeViewX, including unit tests, integration tests, performance tests, and quality assurance processes.

## Testing Philosophy

### Testing Principles

1. **Test-Driven Development (TDD)**: Write tests before implementation
2. **Comprehensive Coverage**: Aim for high code coverage across all modules
3. **Automated Testing**: All tests should be automated and runnable in CI/CD
4. **Fast Feedback**: Tests should execute quickly to provide rapid feedback
5. **Maintainable Tests**: Tests should be clear, concise, and easy to maintain

### Testing Pyramid

```
    E2E Tests (5%)
   ─────────────────
  Integration Tests (15%)
 ─────────────────────────
Unit Tests (80%)
```

- **Unit Tests**: Fast, isolated tests of individual functions and classes
- **Integration Tests**: Tests of component interactions and workflows
- **End-to-End Tests**: Tests of complete user scenarios

## Test Structure

### Directory Organization

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and fixtures
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_core.py           # Core functionality tests
│   ├── test_cli.py            # CLI interface tests
│   ├── test_tools.py          # Tool module tests
│   ├── test_language.py       # Language detection tests
│   └── test_progress.py       # Progress tracking tests
├── integration/                # Integration tests
│   ├── __init__.py
│   ├── test_workflows.py      # Workflow integration tests
│   ├── test_web_server.py     # Web server integration tests
│   └── test_ai_integration.py # AI model integration tests
├── e2e/                        # End-to-end tests
│   ├── __init__.py
│   ├── test_full_generation.py # Complete documentation generation
│   └── test_user_scenarios.py  # Real-world usage scenarios
├── performance/                # Performance tests
│   ├── __init__.py
│   ├── test_memory_usage.py   # Memory usage tests
│   ├── test_execution_time.py # Execution time tests
│   └── test_api_usage.py      # API usage optimization tests
├── fixtures/                   # Test data and fixtures
│   ├── sample_projects/       # Sample code projects
│   ├── mock_responses/        # Mock API responses
│   └── test_configs/          # Test configuration files
└── utils/                      # Test utilities and helpers
    ├── __init__.py
    ├── helpers.py             # Common test utilities
    ├── mocks.py               # Mock objects and functions
    └── assertions.py          # Custom assertion helpers
```

## Unit Testing

### Core Functionality Tests

```python
# tests/unit/test_core.py
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from codeviewx.core import (
    detect_system_language,
    load_prompt,
    get_markdown_title,
    generate_file_tree
)

class TestLanguageDetection:
    """Test system language detection functionality"""
    
    def test_detect_system_language_english(self):
        """Test English language detection"""
        with patch('locale.getdefaultlocale', return_value=('en_US', 'UTF-8')):
            language = detect_system_language()
            assert language == 'English'
    
    def test_detect_system_language_chinese(self):
        """Test Chinese language detection"""
        with patch('locale.getdefaultlocale', return_value=('zh_CN', 'UTF-8')):
            language = detect_system_language()
            assert language == 'Chinese'
    
    def test_detect_system_language_fallback(self):
        """Test fallback to English on error"""
        with patch('locale.getdefaultlocale', side_effect=Exception()):
            language = detect_system_language()
            assert language == 'English'
    
    @pytest.mark.parametrize("locale,expected", [
        ('ja_JP', 'Japanese'),
        ('ko_KR', 'Korean'),
        ('fr_FR', 'French'),
        ('de_DE', 'German'),
        ('es_ES', 'Spanish'),
        ('ru_RU', 'Russian'),
        ('unknown', 'English'),
        (None, 'English')
    ])
    def test_detect_system_language_variants(self, locale, expected):
        """Test various locale variants"""
        with patch('locale.getdefaultlocale', return_value=(locale, 'UTF-8')):
            language = detect_system_language()
            assert language == expected

class TestPromptLoading:
    """Test prompt template loading functionality"""
    
    def test_load_prompt_basic(self):
        """Test basic prompt loading"""
        prompt = load_prompt("DocumentEngineer_compact")
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "工作目录" in prompt or "working directory" in prompt.lower()
    
    def test_load_prompt_with_variables(self):
        """Test prompt loading with variable substitution"""
        prompt = load_prompt(
            "DocumentEngineer_compact",
            working_directory="/test/project",
            output_directory="docs",
            doc_language="English"
        )
        assert "/test/project" in prompt
        assert "docs" in prompt
        assert "English" in prompt
    
    def test_load_prompt_nonexistent(self):
        """Test loading nonexistent prompt"""
        with pytest.raises(FileNotFoundError):
            load_prompt("NonexistentPrompt")
    
    def test_load_prompt_missing_variables(self):
        """Test prompt loading with missing variables"""
        with pytest.raises(ValueError):
            load_prompt("DocumentEngineer_compact", nonexistent_var="value")

class TestMarkdownProcessing:
    """Test Markdown processing utilities"""
    
    def test_get_markdown_title_with_title(self):
        """Test extracting title from markdown with title"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Document\n\nThis is a test.")
            f.flush()
            
            title = get_markdown_title(f.name)
            assert title == "Test Document"
            
            os.unlink(f.name)
    
    def test_get_markdown_title_without_title(self):
        """Test extracting title from markdown without title"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("This is a document without a title.")
            f.flush()
            
            title = get_markdown_title(f.name)
            assert title is None
            
            os.unlink(f.name)
    
    def test_get_markdown_title_nonexistent_file(self):
        """Test extracting title from nonexistent file"""
        title = get_markdown_title("nonexistent.md")
        assert title is None

class TestFileTreeGeneration:
    """Test file tree generation functionality"""
    
    def test_generate_file_tree_empty_directory(self, tmp_path):
        """Test file tree generation with empty directory"""
        file_tree = generate_file_tree(str(tmp_path))
        assert file_tree == []
    
    def test_generate_file_tree_with_markdown_files(self, tmp_path):
        """Test file tree generation with markdown files"""
        # Create test files
        (tmp_path / "README.md").write_text("# Test README")
        (tmp_path / "guide.md").write_text("# Guide\n\nContent")
        (tmp_path / "config.txt").write_text("config data")
        
        file_tree = generate_file_tree(str(tmp_path))
        
        # Check structure
        assert len(file_tree) == 3
        
        # Find README.md (should have display_name 'README')
        readme = next(item for item in file_tree if item['name'] == 'README.md')
        assert readme['display_name'] == 'README'
        assert readme['type'] == 'markdown'
        
        # Find guide.md (should extract title)
        guide = next(item for item in file_tree if item['name'] == 'guide.md')
        assert guide['display_name'] == 'Guide'
        assert guide['type'] == 'markdown'
        
        # Find config.txt
        config = next(item for item in file_tree if item['name'] == 'config.txt')
        assert config['display_name'] == 'config.txt'
        assert config['type'] == 'file'
    
    def test_generate_file_tree_with_current_file(self, tmp_path):
        """Test file tree generation with current file highlighting"""
        (tmp_path / "README.md").write_text("# README")
        (tmp_path / "guide.md").write_text("# Guide")
        
        file_tree = generate_file_tree(str(tmp_path), "guide.md")
        
        guide = next(item for item in file_tree if item['name'] == 'guide.md')
        assert guide['active'] is True
        
        readme = next(item for item in file_tree if item['name'] == 'README.md')
        assert readme['active'] is False
```

### Tool Testing

```python
# tests/unit/test_tools.py
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock

from codeviewx.tools import (
    write_real_file,
    read_real_file,
    list_real_directory,
    ripgrep_search
)

class TestFileSystemTools:
    """Test file system tool functionality"""
    
    def test_write_real_file_new_file(self, tmp_path):
        """Test writing a new file"""
        file_path = tmp_path / "test.md"
        content = "# Test Document\n\nThis is test content."
        
        result = write_real_file(str(file_path), content)
        
        assert "✅" in result
        assert "test.md" in result
        assert file_path.exists()
        assert file_path.read_text() == content
    
    def test_write_real_file_with_directory_creation(self, tmp_path):
        """Test writing file with automatic directory creation"""
        file_path = tmp_path / "subdir" / "test.md"
        content = "Test content"
        
        result = write_real_file(str(file_path), content)
        
        assert "✅" in result
        assert file_path.exists()
        assert file_path.parent.exists()
    
    def test_read_real_file_existing_file(self, tmp_path):
        """Test reading an existing file"""
        file_path = tmp_path / "test.txt"
        content = "Test file content"
        file_path.write_text(content)
        
        result = read_real_file(str(file_path))
        
        assert "test.txt" in result
        assert content in result
        assert "1 行" in result or "1 line" in result.lower()
    
    def test_read_real_file_nonexistent_file(self):
        """Test reading a nonexistent file"""
        result = read_real_file("nonexistent.txt")
        assert "❌" in result
        assert "不存在" in result or "not found" in result.lower()
    
    def test_list_real_directory_with_files(self, tmp_path):
        """Test listing directory with files"""
        # Create test structure
        (tmp_path / "subdir").mkdir()
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.md").write_text("# Title")
        
        result = list_real_directory(str(tmp_path))
        
        assert "subdir/" in result
        assert "file1.txt" in result
        assert "file2.md" in result
        assert "2 个文件" in result or "2 files" in result.lower()
    
    def test_list_real_directory_nonexistent(self):
        """Test listing nonexistent directory"""
        result = list_real_directory("nonexistent_dir")
        assert "❌" in result
        assert "不存在" in result or "not found" in result.lower()

class TestSearchTools:
    """Test search tool functionality"""
    
    @patch('codeviewx.tools.search.Ripgrepy')
    def test_ripgrep_search_success(self, mock_ripgrepy):
        """Test successful ripgrep search"""
        # Mock ripgrep behavior
        mock_rg = MagicMock()
        mock_rg.line_number.return_value = mock_rg
        mock_rg.with_filename.return_value = mock_rg
        mock_rg.max_count.return_value = mock_rg
        mock_rg.ignore_case.return_value = mock_rg
        mock_rg.type_add.return_value = mock_rg
        mock_rg.glob.return_value = mock_rg
        mock_rg.run.return_value.as_string = "file.py:10:pattern found"
        mock_ripgrepy.return_value = mock_rg
        
        result = ripgrep_search("pattern", "/path/to/search")
        
        assert "pattern found" in result
        assert "file.py" in result
        assert "10" in result
    
    @patch('codeviewx.tools.search.Ripgrepy')
    def test_ripgrep_search_no_results(self, mock_ripgrepy):
        """Test ripgrep search with no results"""
        mock_rg = MagicMock()
        mock_rg.line_number.return_value = mock_rg
        mock_rg.with_filename.return_value = mock_rg
        mock_rg.max_count.return_value = mock_rg
        mock_rg.type_add.return_value = mock_rg
        mock_rg.glob.return_value = mock_rg
        mock_rg.run.return_value.as_string = ""
        mock_ripgrepy.return_value = mock_rg
        
        result = ripgrep_search("nonexistent", "/path/to/search")
        
        assert "未找到匹配" in result or "no matches" in result.lower()
    
    def test_ripgrep_search_not_installed(self):
        """Test ripgrep search when ripgrep is not installed"""
        with patch('codeviewx.tools.search.Ripgrepy', side_effect=Exception("rg: not found")):
            result = ripgrep_search("pattern", "/path/to/search")
            assert "rg 未安装" in result or "rg not installed" in result.lower()
```

### CLI Testing

```python
# tests/unit/test_cli.py
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from codeviewx.cli import main

class TestCLI:
    """Test command-line interface functionality"""
    
    def test_cli_version(self):
        """Test CLI version command"""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert "CodeViewX" in result.output
    
    def test_cli_help(self):
        """Test CLI help command"""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert "CodeViewX" in result.output
        assert "--working-dir" in result.output
        assert "--output-dir" in result.output
        assert "--language" in result.output
    
    @patch('codeviewx.cli.generate_docs')
    def test_cli_basic_generation(self, mock_generate):
        """Test basic documentation generation"""
        mock_generate.return_value = None
        runner = CliRunner()
        result = runner.invoke(main, [])
        
        assert result.exit_code == 0
        mock_generate.assert_called_once()
    
    @patch('codeviewx.cli.generate_docs')
    def test_cli_with_options(self, mock_generate):
        """Test CLI with all options"""
        mock_generate.return_value = None
        runner = CliRunner()
        result = runner.invoke(main, [
            '--working-dir', '/test/project',
            '--output-dir', 'test-docs',
            '--language', 'English',
            '--recursion-limit', '500',
            '--verbose'
        ])
        
        assert result.exit_code == 0
        mock_generate.assert_called_once_with(
            working_directory='/test/project',
            output_directory='test-docs',
            doc_language='English',
            recursion_limit=500,
            verbose=True
        )
    
    @patch('codeviewx.cli.start_document_web_server')
    def test_cli_serve_mode(self, mock_serve):
        """Test CLI serve mode"""
        mock_serve.return_value = None
        runner = CliRunner()
        result = runner.invoke(main, ['--serve'])
        
        assert result.exit_code == 0
        mock_serve.assert_called_once_with('docs')
    
    @patch('codeviewx.cli.start_document_web_server')
    def test_cli_serve_with_custom_output(self, mock_serve):
        """Test CLI serve mode with custom output directory"""
        mock_serve.return_value = None
        runner = CliRunner()
        result = runner.invoke(main, ['--serve', '--output-dir', 'custom-docs'])
        
        assert result.exit_code == 0
        mock_serve.assert_called_once_with('custom-docs')
    
    @patch('codeviewx.cli.generate_docs')
    def test_cli_generation_error(self, mock_generate):
        """Test CLI error handling during generation"""
        mock_generate.side_effect = Exception("Test error")
        runner = CliRunner()
        result = runner.invoke(main, [])
        
        assert result.exit_code == 1
        assert "Error: Test error" in result.output
```

## Integration Testing

### Workflow Integration Tests

```python
# tests/integration/test_workflows.py
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from codeviewx.core import generate_docs

class TestDocumentationGenerationWorkflow:
    """Test complete documentation generation workflow"""
    
    @pytest.fixture
    def sample_project(self, tmp_path):
        """Create a sample project for testing"""
        project_dir = tmp_path / "sample_project"
        project_dir.mkdir()
        
        # Create project structure
        (project_dir / "README.md").write_text("# Sample Project\n\nA test project.")
        (project_dir / "src").mkdir()
        (project_dir / "src" / "main.py").write_text("""
def main():
    \"\"\"Main function\"\"\"
    print("Hello, World!")

if __name__ == "__main__":
    main()
""")
        (project_dir / "pyproject.toml").write_text("""
[project]
name = "sample-project"
version = "0.1.0"
description = "A sample project"
""")
        
        return project_dir
    
    @patch('codeviewx.core.create_deep_agent')
    def test_complete_documentation_generation(self, mock_agent, sample_project):
        """Test complete documentation generation workflow"""
        # Mock AI agent
        mock_agent_instance = MagicMock()
        mock_agent_instance.stream.return_value = [
            {"messages": [MagicMock(tool_calls=[], content="Starting analysis...")]},
            {"messages": [MagicMock(tool_calls=[{
                'name': 'list_real_directory',
                'args': {'directory': str(sample_project)}
            }])]},
            {"messages": [MagicMock(tool_calls=[{
                'name': 'write_real_file',
                'args': {'file_path': 'docs/README.md', 'content': '# Generated Docs'}
            }])]}
        ]
        mock_agent.return_value = mock_agent_instance
        
        # Generate documentation
        output_dir = sample_project / "docs"
        generate_docs(
            working_directory=str(sample_project),
            output_directory=str(output_dir),
            doc_language="English",
            verbose=False
        )
        
        # Verify agent was created and called
        mock_agent.assert_called_once()
        mock_agent_instance.stream.assert_called_once()
        
        # Verify output directory was created
        assert output_dir.exists()
    
    @patch('codeviewx.core.create_deep_agent')
    def test_language_specific_generation(self, mock_agent, sample_project):
        """Test documentation generation in different languages"""
        mock_agent_instance = MagicMock()
        mock_agent_instance.stream.return_value = []
        mock_agent.return_value = mock_agent_instance
        
        # Test Chinese documentation generation
        generate_docs(
            working_directory=str(sample_project),
            output_directory=str(sample_project / "docs_zh"),
            doc_language="Chinese"
        )
        
        # Verify agent was called with Chinese prompt
        call_args = mock_agent.call_args
        prompt = call_args[0][1]  # Second argument is the prompt
        assert "Chinese" in prompt or "中文" in prompt
    
    def test_error_handling_invalid_directory(self):
        """Test error handling with invalid directory"""
        with pytest.raises(Exception):
            generate_docs(
                working_directory="/nonexistent/directory",
                output_directory="docs"
            )
```

### Web Server Integration Tests

```python
# tests/integration/test_web_server.py
import pytest
import tempfile
from unittest.mock import patch

from codeviewx.core import start_document_web_server, generate_file_tree

class TestWebServerIntegration:
    """Test web server integration functionality"""
    
    @pytest.fixture
    def documentation_dir(self, tmp_path):
        """Create a documentation directory for testing"""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        # Create sample documentation files
        (docs_dir / "README.md").write_text("# Documentation\n\nWelcome to the docs.")
        (docs_dir / "guide.md").write_text("# Guide\n\nThis is a guide.")
        (docs_dir / "api.md").write_text("# API Reference\n\nAPI documentation.")
        
        return docs_dir
    
    def test_file_tree_generation_for_web(self, documentation_dir):
        """Test file tree generation for web server"""
        file_tree = generate_file_tree(str(documentation_dir))
        
        assert len(file_tree) == 3
        
        # Check structure
        files = {item['name']: item for item in file_tree}
        assert 'README.md' in files
        assert 'guide.md' in files
        assert 'api.md' in files
        
        # Check display names
        assert files['README.md']['display_name'] == 'README'
        assert files['guide.md']['display_name'] == 'Guide'
        assert files['api.md']['display_name'] == 'API Reference'
    
    @patch('codeviewx.core.app.run')
    def test_web_server_startup(self, mock_run, documentation_dir):
        """Test web server startup"""
        # This test would normally start a server, but we mock it
        with pytest.raises(SystemExit):
            # Start server in a separate thread for testing
            import threading
            import time
            
            def run_server():
                start_document_web_server(str(documentation_dir))
            
            server_thread = threading.Thread(target=run_server)
            server_thread.daemon = True
            server_thread.start()
            
            # Give server time to start
            time.sleep(0.1)
            
            # In a real test, we would make HTTP requests here
            # For now, just verify the server starts without errors
```

## Performance Testing

### Memory Usage Tests

```python
# tests/performance/test_memory_usage.py
import pytest
import psutil
import os
from memory_profiler import profile

from codeviewx.core import generate_docs

class TestMemoryUsage:
    """Test memory usage and optimization"""
    
    def test_memory_usage_large_project(self, large_project_dir):
        """Test memory usage with large projects"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Generate documentation for large project
        generate_docs(
            working_directory=str(large_project_dir),
            output_directory=str(large_project_dir / "docs"),
            recursion_limit=100  # Limit to avoid excessive memory usage
        )
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 500MB)
        assert memory_increase < 500 * 1024 * 1024, f"Memory increase: {memory_increase / 1024 / 1024:.2f} MB"
    
    @profile
    def test_memory_profiling_sample_function(self):
        """Profile memory usage of sample function"""
        # This would be run with: python -m memory_profiler tests/performance/test_memory_usage.py
        from codeviewx.tools import list_real_directory
        
        result = list_real_directory(".")
        assert result is not None
```

### Execution Time Tests

```python
# tests/performance/test_execution_time.py
import pytest
import time
from unittest.mock import patch

from codeviewx.core import generate_docs

class TestExecutionTime:
    """Test execution time performance"""
    
    @pytest.mark.slow
    def test_execution_time_small_project(self, small_project_dir):
        """Test execution time with small projects"""
        start_time = time.time()
        
        generate_docs(
            working_directory=str(small_project_dir),
            output_directory=str(small_project_dir / "docs"),
            verbose=False
        )
        
        execution_time = time.time() - start_time
        
        # Small project should complete within 5 minutes
        assert execution_time < 300, f"Execution time: {execution_time:.2f} seconds"
    
    def test_tool_execution_performance(self):
        """Test individual tool execution performance"""
        from codeviewx.tools import ripgrep_search
        
        start_time = time.time()
        result = ripgrep_search("def", ".", "py", max_count=50)
        execution_time = time.time() - start_time
        
        # Search should complete within 10 seconds
        assert execution_time < 10, f"Search time: {execution_time:.2f} seconds"
        assert result is not None
```

## Test Configuration

### Pytest Configuration

```python
# conftest.py
import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def small_project_dir(temp_dir):
    """Create a small sample project"""
    project_dir = temp_dir / "small_project"
    project_dir.mkdir()
    
    # Create basic project structure
    (project_dir / "README.md").write_text("# Small Project")
    (project_dir / "main.py").write_text("print('Hello, World!')")
    (project_dir / "requirements.txt").write_text("flask>=2.0")
    
    return project_dir

@pytest.fixture
def large_project_dir(temp_dir):
    """Create a large sample project for performance testing"""
    project_dir = temp_dir / "large_project"
    project_dir.mkdir()
    
    # Create many files
    for i in range(100):
        (project_dir / f"module_{i}.py").write_text(f"""
def function_{i}():
    \"\"\"Function {i}\"\"\"
    return {i}

class Class{i}:
    \"\"\"Class {i}\"\"\"
    pass
""")
    
    # Create subdirectories
    for subdir in ['src', 'tests', 'docs', 'config']:
        (project_dir / subdir).mkdir()
        for i in range(10):
            (project_dir / subdir / f"file_{i}.py").write_text(f"# {subdir} file {i}")
    
    return project_dir

@pytest.fixture(autouse=True)
def mock_api_keys(monkeypatch):
    """Mock API keys for testing"""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-api-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

@pytest.fixture
def mock_ai_agent():
    """Mock AI agent for testing"""
    from unittest.mock import MagicMock
    
    mock_agent = MagicMock()
    mock_agent.stream.return_value = []
    return mock_agent
```

### Test Configuration File

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: Marks tests as slow (deselect with '-m "not slow"')
    integration: Marks tests as integration tests
    unit: Marks tests as unit tests
    e2e: Marks tests as end-to-end tests
```

## Continuous Integration

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
        sudo apt-get install ripgrep
    
    - name: Lint with flake8
      run: |
        flake8 codeviewx tests --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 codeviewx tests --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics
    
    - name: Type check with mypy
      run: mypy codeviewx
    
    - name: Run unit tests
      run: |
        pytest tests/unit -v --cov=codeviewx --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration -v
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

### Test Coverage

#### Coverage Configuration

```ini
# .coveragerc
[run]
source = codeviewx
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

#### Coverage Goals

- **Unit Tests**: > 90% line coverage
- **Integration Tests**: > 80% feature coverage
- **Overall**: > 85% combined coverage

## Test Data Management

### Fixtures and Mock Data

```python
# tests/fixtures/mock_responses.py
"""Mock API responses for testing"""

MOCK_ANALYSIS_RESPONSE = {
    "messages": [
        {
            "role": "assistant",
            "content": "I'll analyze your project structure and generate comprehensive documentation."
        }
    ]
}

SAMPLE_PROJECT_STRUCTURE = {
    "README.md": "# Sample Project\n\nThis is a sample project.",
    "src/main.py": """
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""",
    "requirements.txt": "flask>=2.0.0\nrequests>=2.25.0",
    "pyproject.toml": """
[project]
name = "sample-project"
version = "0.1.0"
description = "A sample project"
"""
}
```

### Test Utilities

```python
# tests/utils/helpers.py
"""Test utilities and helper functions"""

import tempfile
import shutil
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def temporary_directory():
    """Create a temporary directory context manager"""
    temp_dir = tempfile.mkdtemp()
    try:
        yield Path(temp_dir)
    finally:
        shutil.rmtree(temp_dir)

def create_sample_project(base_dir, structure):
    """Create a sample project from structure dictionary"""
    base_path = Path(base_dir)
    
    for file_path, content in structure.items():
        full_path = base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
    
    return base_path

def assert_documentation_generated(output_dir):
    """Assert that documentation was generated correctly"""
    output_path = Path(output_dir)
    
    # Check that output directory exists
    assert output_path.exists(), "Output directory was not created"
    
    # Check for essential files
    essential_files = ["README.md", "01-overview.md", "02-quickstart.md"]
    for file_name in essential_files:
        file_path = output_path / file_name
        assert file_path.exists(), f"Essential file {file_name} was not generated"
        assert file_path.stat().st_size > 0, f"File {file_name} is empty"
```

## Debugging Tests

### Test Debugging Techniques

1. **Verbose Output**: Run tests with `-v` flag for detailed output
2. **Print Debugging**: Add print statements for quick debugging
3. **Debugger Integration**: Use IDE debugger with test breakpoints
4. **Logging**: Enable debug logging during tests

### Common Test Issues

#### 1. Mock Configuration

```python
# Incorrect mock configuration
@patch('codeviewx.core.create_deep_agent')
def test_incorrect_mock(mock_agent):
    mock_agent.return_value.stream.return_value = []  # Too specific

# Correct mock configuration
@patch('codeviewx.core.create_deep_agent')
def test_correct_mock(mock_agent):
    mock_instance = MagicMock()
    mock_instance.stream.return_value = []
    mock_agent.return_value = mock_instance
```

#### 2. Temporary File Handling

```python
# Incorrect: files not cleaned up
def test_file_operations():
    f = open("test.txt", "w")
    f.write("test")
    # File not closed or cleaned up

# Correct: using context managers
def test_file_operations():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test")
        temp_path = f.name
    
    try:
        # Test with temporary file
        result = process_file(temp_path)
        assert result is not None
    finally:
        os.unlink(temp_path)
```

#### 3. Async/Await Testing

```python
# For async functions, use pytest-asyncio
import pytest
from codeviewx.core import async_function

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

---

*This testing strategy provides comprehensive guidelines for ensuring CodeViewX quality and reliability. For implementation details, see the [Development Guide](07-development-guide.md).*