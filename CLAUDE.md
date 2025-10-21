# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CodeViewX is an AI-powered code documentation generator that uses Anthropic Claude, DeepAgents, and LangChain to automatically analyze codebases and generate comprehensive technical documentation. The tool supports multiple languages and includes a built-in web server for browsing generated documentation.

## Architecture

### Core Components

- **Core Module** (`codeviewx/core.py`): Public API entry point that exports main functions
- **Generator** (`codeviewx/generator.py`): Main document generation logic using DeepAgents
- **CLI Interface** (`codeviewx/cli.py`): Command-line interface with argument parsing and internationalization
- **Web Server** (`codeviewx/server.py`): Flask-based documentation browser
- **Tools** (`codeviewx/tools/`): File system, search, and command execution tools for AI agents
- **Prompts** (`codeviewx/prompts/`): AI prompt templates for documentation generation
- **i18n** (`codeviewx/i18n.py`): Internationalization support for UI and documentation

### AI Agent Integration

The project uses DeepAgents with LangChain to create AI agents that have access to specialized tools:
- `ripgrep_search`: Fast code search using ripgrep
- `execute_command`: Command execution for project analysis
- `read_real_file`/`write_real_file`: File operations
- `list_real_directory`: Directory traversal

## Development Commands

### Setup and Installation

```bash
# Install from source (development)
pip install -e ".[dev]"

# Install ripgrep (required dependency)
brew install ripgrep          # macOS
sudo apt install ripgrep      # Ubuntu/Debian
choco install ripgrep         # Windows

# Set up API key
export ANTHROPIC_AUTH_TOKEN='your-api-key-here'
```

### Code Quality and Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=codeviewx --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Code formatting
black codeviewx/

# Import sorting
isort codeviewx/

# Linting
flake8 codeviewx/

# Type checking
mypy codeviewx/
```

### Build and Distribution

```bash
# Build package
python -m build

# Install locally in development mode
pip install -e .
```

## Key Development Patterns

### Error Handling

The codebase uses a consistent pattern for error handling in the CLI:
- Catch `KeyboardInterrupt` for graceful shutdown (exit code 130)
- Catch general `Exception` and display user-friendly error messages
- Use verbose mode to show full tracebacks when `--verbose` flag is set

### Internationalization

All user-facing strings should go through the i18n system:
```python
from codeviewx.i18n import t

# Use translation keys
print(t('cli_description'))
print(t('error_message', param=value))
```

### Prompt Template System

Prompts are loaded from markdown files with variable substitution:
```python
from codeviewx.prompt import load_prompt

prompt = load_prompt(
    "document_engineer",
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English"
)
```

### Tool Development

When adding new tools for the AI agent:
1. Implement the tool in `codeviewx/tools/`
2. Add proper type hints and docstrings
3. Include the tool in the tools list in `generator.py`
4. Follow the existing tool naming convention (`*_real_file`, `*_directory`, etc.)

## Testing Strategy

- Unit tests are located in `tests/` directory
- Tests follow pytest conventions with descriptive test names
- Use fixtures for common setup (e.g., `tmp_path` for temporary directories)
- Mock external dependencies (API calls, file system operations when appropriate)
- Test both success and error paths

## Configuration

### pyproject.toml Configuration

- **Black**: Line length 100, Python 3.8+ targets
- **isort**: Black profile compatibility
- **pytest**: Verbose output by default
- **mypy**: Non-strict type checking (allow untyped defs)

### Package Structure

- Main package: `codeviewx/`
- Static files: Templates (`tpl/`), prompts (`prompts/`), static assets (`static/`)
- Documentation: Generated in `docs/` directory with language subdirectories
- Examples: Sample projects in `examples/` directory

## Common Workflows

### Adding New Documentation Languages

1. Update language detection in `codeviewx/language.py`
2. Add translation keys to i18n system
3. Update CLI argument choices
4. Test prompt generation with new language

### Modifying AI Agent Behavior

1. Update prompt templates in `codeviewx/prompts/`
2. Modify tools in `codeviewx/tools/` if needed
3. Adjust agent configuration in `generator.py`
4. Test with various project types

### Extending Web Server

1. Modify Flask app in `codeviewx/server.py`
2. Update HTML templates in `codeviewx/tpl/`
3. Add static assets to `codeviewx/static/`
4. Test with generated documentation

## Dependencies

### Core Dependencies
- **langchain**: AI/LLM integration framework
- **langchain-anthropic**: Anthropic Claude integration
- **deepagents**: AI agent framework
- **ripgrepy**: Python bindings for ripgrep
- **flask**: Web server for documentation browser
- **markdown**: Markdown processing with extensions

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **isort**: Import sorting

## Environment Variables

- `ANTHROPIC_AUTH_TOKEN`: Required for Claude API access
- No other environment variables required for basic operation