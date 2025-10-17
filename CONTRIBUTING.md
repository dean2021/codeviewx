# Contributing to CodeViewX

[中文](CONTRIBUTING.zh.md) | English

First off, thank you for considering contributing to CodeViewX! It's people like you that make CodeViewX such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to dean@csoio.com.

### Our Pledge

We pledge to make participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

**Use the Bug Report Template:**

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Run command '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots/Logs**
If applicable, add screenshots or error logs.

**Environment:**
- OS: [e.g., macOS 13.0, Ubuntu 22.04]
- Python Version: [e.g., 3.9.7]
- CodeViewX Version: [e.g., 0.2.0]
- Installation Method: [pip, source]

**Additional Context**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

**Use the Feature Request Template:**

```markdown
**Is your feature request related to a problem?**
A clear description of the problem. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional Context**
Any other context, mockups, or examples.
```

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `documentation` - Documentation improvements

#### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/codeviewx.git
   cd codeviewx
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install ripgrep**
   ```bash
   # macOS
   brew install ripgrep
   
   # Ubuntu/Debian
   sudo apt install ripgrep
   
   # Windows
   choco install ripgrep
   ```

5. **Configure Environment**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

6. **Verify Setup**
   ```bash
   codeviewx --version
   pytest
   ```

### Pull Requests

#### Before Submitting

1. **Check existing PRs** to avoid duplicates
2. **Follow the coding standards** (see below)
3. **Write tests** for new features
4. **Update documentation** as needed
5. **Run all tests** and ensure they pass

#### PR Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Follow the style guide
   - Add tests

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

4. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a Pull Request**
   - Fill in the PR template
   - Link related issues
   - Request review

#### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran and how to reproduce them.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Related Issues
Closes #(issue number)
```

## Development Setup

### Required Tools

- Python 3.8+
- Git
- ripgrep (rg)
- Code editor (VS Code, PyCharm recommended)

### Recommended VS Code Extensions

- Python
- Pylance
- Black Formatter
- autoDocstring

### Development Dependencies

All development dependencies are installed via:
```bash
pip install -e ".[dev]"
```

This includes:
- pytest (testing)
- pytest-cov (coverage)
- black (formatting)
- flake8 (linting)
- mypy (type checking)
- isort (import sorting)

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications enforced by Black.

#### Code Formatting

**Use Black for formatting:**
```bash
black codeviewx/
```

**Configuration (pyproject.toml):**
```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
```

#### Linting

**Run flake8:**
```bash
flake8 codeviewx/
```

#### Type Hints

Use type hints for all public functions:
```python
def generate_docs(
    working_directory: str,
    output_directory: str = "docs",
    doc_language: str = "English"
) -> None:
    """Generate documentation for a project."""
    pass
```

#### Docstrings

Use Google-style docstrings:
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param1 is empty
    
    Examples:
        >>> function_name("test", 42)
        True
    """
    pass
```

#### Import Organization

Use isort for import sorting:
```bash
isort codeviewx/
```

Import order:
1. Standard library imports
2. Third-party imports
3. Local application imports

Example:
```python
import os
import sys
from typing import Dict, List

from langchain import LLMChain
from langchain_anthropic import ChatAnthropic

from codeviewx.core import generate_docs
from codeviewx.i18n import t
```

### File Organization

- One class per file (unless closely related)
- Group related functions
- Keep files under 500 lines when possible
- Use descriptive file names

### Naming Conventions

- **Modules**: `lowercase_with_underscores.py`
- **Classes**: `CapitalizedWords`
- **Functions**: `lowercase_with_underscores()`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore`

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

### Examples

```bash
# Feature
git commit -m "feat(generator): add support for TypeScript projects"

# Bug fix
git commit -m "fix(cli): correct output directory path handling"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Breaking change
git commit -m "feat(api)!: change generate_docs return type

BREAKING CHANGE: generate_docs now returns a dict instead of None"
```

### Commit Best Practices

1. **Use present tense**: "add feature" not "added feature"
2. **Be concise**: Keep subject under 72 characters
3. **Be descriptive**: Explain what and why, not how
4. **Reference issues**: Use "Closes #123" or "Fixes #456"
5. **One logical change per commit**

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=codeviewx --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::test_generate_docs

# Run with verbose output
pytest -v
```

### Writing Tests

#### Test Structure

```python
import pytest
from codeviewx.core import generate_docs

class TestGenerateDocs:
    """Tests for generate_docs function."""
    
    def test_basic_generation(self, tmp_path):
        """Test basic documentation generation."""
        # Arrange
        working_dir = tmp_path / "project"
        working_dir.mkdir()
        output_dir = tmp_path / "docs"
        
        # Act
        generate_docs(str(working_dir), str(output_dir))
        
        # Assert
        assert output_dir.exists()
        assert (output_dir / "README.md").exists()
    
    def test_invalid_directory(self):
        """Test with non-existent directory."""
        with pytest.raises(ValueError):
            generate_docs("/non/existent/path")
```

#### Test Guidelines

1. **Use descriptive names**: `test_should_raise_error_when_directory_not_found`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **One assertion per test** (when possible)
4. **Use fixtures** for common setup
5. **Mock external dependencies** (API calls, file system when appropriate)

#### Test Coverage Goals

- **Minimum**: 70% overall coverage
- **Target**: 80%+ coverage
- **Critical paths**: 100% coverage

### Test Fixtures

```python
import pytest

@pytest.fixture
def sample_project(tmp_path):
    """Create a sample project structure."""
    project_dir = tmp_path / "sample"
    project_dir.mkdir()
    
    # Create sample files
    (project_dir / "main.py").write_text("print('hello')")
    (project_dir / "README.md").write_text("# Sample")
    
    return project_dir
```

## Documentation

### Code Documentation

- All public APIs must have docstrings
- Use Google-style docstrings
- Include examples when helpful
- Document exceptions that can be raised

### User Documentation

When adding features, update:
- `README.md` - User-facing features
- `docs/` - Detailed documentation
- API reference - If applicable
- Examples - Add to `examples/` directory

### Documentation Build

```bash
# Generate API documentation (if using Sphinx)
cd docs
make html

# Serve documentation locally
python -m http.server --directory docs/_build/html
```

## Community

### Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bugs and feature requests
- **Email**: dean@csoio.com for private matters

### Communication Guidelines

- Be respectful and constructive
- Stay on topic
- Search before posting
- Provide context and details
- Follow up on your issues/PRs

### Recognition

Contributors are recognized in:
- GitHub Contributors page
- Release notes (for significant contributions)
- Project documentation

## License

By contributing to CodeViewX, you agree that your contributions will be licensed under the GNU General Public License v3.0.

---

## Quick Links

- [Issue Tracker](https://github.com/dean2021/codeviewx/issues)
- [Pull Requests](https://github.com/dean2021/codeviewx/pulls)
- [Discussions](https://github.com/dean2021/codeviewx/discussions)
- [Documentation](https://github.com/dean2021/codeviewx/tree/main/docs)

---

Thank you for contributing to CodeViewX! 🎉

