# API Reference

This document provides comprehensive API documentation for CodeViewX, covering all public functions, classes, and interfaces available for integration and extension.

## Core API

### `generate_docs()`

The primary function for generating documentation from code analysis.

```python
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    ui_language: Optional[str] = None,
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None
```

**Purpose**: Main entry point for programmatic documentation generation

**Parameters**:
- `working_directory` (Optional[str]): Path to the project directory to analyze. Defaults to current directory.
- `output_directory` (str): Directory where generated documentation will be saved. Defaults to "docs".
- `doc_language` (Optional[str]): Language for generated documentation. Supports: 'Chinese', 'English', 'Japanese', 'Korean', 'French', 'German', 'Spanish', 'Russian'. Auto-detected if not specified.
- `ui_language` (Optional[str]): Interface language for progress messages. Options: 'en', 'zh'. Auto-detected if not specified.
- `recursion_limit` (int): Maximum recursion depth for AI agent. Default: 1000.
- `verbose` (bool): Enable detailed logging output. Default: False.

**Returns**: None

**Raises**: 
- `FileNotFoundError`: If working directory doesn't exist
- `ValueError`: If invalid language specified
- `Exception`: For API or system errors

**Examples**:
```python
# Basic usage with defaults
from codeviewx import generate_docs
generate_docs()

# Custom configuration
generate_docs(
    working_directory="/path/to/my/project",
    output_directory="technical_docs",
    doc_language="English",
    verbose=True
)

# Generate documentation in Chinese
generate_docs(doc_language="Chinese", ui_language="zh")
```

**Implementation Details**:
- Initializes logging system based on verbose flag
- Detects and configures language settings
- Loads appropriate prompt templates
- Creates AI agent with tool access
- Executes analysis workflow with progress tracking

Reference: [generator.py](../codeviewx/generator.py#L25)

### `start_document_web_server()`

Starts a Flask-based web server for browsing generated documentation.

```python
def start_document_web_server(output_directory: str) -> None
```

**Purpose**: Launch web server for interactive documentation viewing

**Parameters**:
- `output_directory` (str): Path to directory containing generated documentation

**Returns**: None

**Raises**:
- `FileNotFoundError`: If output directory doesn't exist
- `Exception`: For server startup errors

**Examples**:
```python
from codeviewx import start_document_web_server

# Start server for default docs directory
start_document_web_server("docs")

# Start server for custom documentation directory
start_document_web_server("/path/to/generated/docs")
```

**Features**:
- Serves documentation at http://localhost:5000
- Renders Markdown with syntax highlighting
- Supports Mermaid diagram rendering
- Provides file tree navigation
- Auto-generates table of contents

Reference: [server.py](../codeviewx/server.py#L140)

### `load_prompt()`

Loads and formats AI prompt templates for documentation generation.

```python
def load_prompt(name: str, **kwargs) -> str
```

**Purpose**: Load prompt templates with dynamic variable substitution

**Parameters**:
- `name` (str): Prompt template name (without .md extension)
- `**kwargs`: Template variables for substitution

**Returns**: 
- `str`: Formatted prompt text

**Raises**:
- `FileNotFoundError`: If prompt template doesn't exist
- `ValueError`: If required template variables not provided

**Examples**:
```python
from codeviewx import load_prompt

# Load basic prompt
prompt = load_prompt("document_engineer")

# Load with custom variables
prompt = load_prompt(
    "document_engineer",
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English"
)
```

**Template Variables**:
- `working_directory`: Project path being analyzed
- `output_directory`: Documentation output path
- `doc_language`: Target documentation language

Reference: [prompt.py](../codeviewx/prompt.py#L15)

## Language and Localization API

### `detect_system_language()`

Automatically detects the system's preferred language for documentation.

```python
def detect_system_language() -> str
```

**Purpose**: Auto-detect system language for documentation generation

**Returns**: 
- `str`: Detected language code. Supported: 'Chinese', 'English', 'Japanese', 'Korean', 'French', 'German', 'Spanish', 'Russian'

**Examples**:
```python
from codeviewx.language import detect_system_language

language = detect_system_language()
print(f"Detected language: {language}")
```

**Detection Strategy**:
1. Check system locale settings
2. Analyze environment variables
3. Fall back to English if detection fails

### `detect_ui_language()`

Detects the appropriate UI language for progress messages.

```python
def detect_ui_language() -> str
```

**Purpose**: Auto-detect UI language for interface messages

**Returns**: 
- `str`: UI language code ('en' or 'zh')

**Examples**:
```python
from codeviewx.i18n import detect_ui_language

ui_lang = detect_ui_language()
print(f"UI Language: {ui_lang}")
```

### `get_i18n()`

Returns the global internationalization manager instance.

```python
def get_i18n() -> I18n
```

**Purpose**: Access the i18n system for localization

**Returns**: 
- `I18n`: Internationalization manager instance

**Examples**:
```python
from codeviewx.i18n import get_i18n

i18n = get_i18n()
message = i18n.t('starting')
print(message)
```

### `t()`

Translation function for localized messages.

```python
def t(key: str, **kwargs) -> str
```

**Purpose**: Translate message keys to localized text

**Parameters**:
- `key` (str): Message key to translate
- `**kwargs`: Format variables for message templates

**Returns**: 
- `str`: Translated and formatted message

**Examples**:
```python
from codeviewx.i18n import t

# Simple translation
message = t('starting')

# With variables
message = t('generated_files', count=5)
print(message)  # "✓ Generated 5 document files"
```

### `set_locale()`

Sets the current locale for the i18n system.

```python
def set_locale(locale: str) -> None
```

**Purpose**: Change the active locale for translations

**Parameters**:
- `locale` (str): Locale code ('en' or 'zh')

**Examples**:
```python
from codeviewx.i18n import set_locale, t

# Set to Chinese
set_locale('zh')
message = t('starting')  # "🚀 启动 CodeViewX 文档生成器"

# Set to English
set_locale('en')
message = t('starting')  # "🚀 Starting CodeViewX Documentation Generator"
```

## Tool API

### File System Tools

#### `write_real_file()`

Writes content to the file system with automatic directory creation.

```python
def write_real_file(file_path: str, content: str) -> str
```

**Purpose**: Write files with directory structure creation

**Parameters**:
- `file_path` (str): Target file path (relative or absolute)
- `content` (str): Content to write to file

**Returns**: 
- `str`: Success/error message with file size information

**Examples**:
```python
from codeviewx.tools import write_real_file

# Write documentation file
result = write_real_file("docs/README.md", "# Project Documentation")
print(result)  # "✅ Successfully wrote file: docs/README.md (0.25 KB)"
```

**Features**:
- Automatically creates parent directories
- Returns file size information
- UTF-8 encoding by default
- Comprehensive error handling

Reference: [filesystem.py](../codeviewx/tools/filesystem.py#L12)

#### `read_real_file()`

Reads file contents with metadata and error handling.

```python
def read_real_file(file_path: str) -> str
```

**Purpose**: Read file contents with formatted output

**Parameters**:
- `file_path` (str): Path to file to read

**Returns**: 
- `str`: File content with metadata header or error message

**Examples**:
```python
from codeviewx.tools import read_real_file

content = read_real_file("src/main.py")
print(content)
# Output:
# File: src/main.py (2.45 KB, 85 lines)
# ============================================================
# def main():
#     # Main function implementation
#     pass
```

**Features**:
- Includes file metadata (size, line count)
- UTF-8 encoding with error handling
- Descriptive error messages for common issues

Reference: [filesystem.py](../codeviewx/tools/filesystem.py#L50)

#### `list_real_directory()`

Lists directory contents with classification and statistics.

```python
def list_real_directory(directory: str = ".") -> str
```

**Purpose**: List directory contents with formatting

**Parameters**:
- `directory` (str): Directory path to list (default: current directory)

**Returns**: 
- `str`: Formatted directory listing or error message

**Examples**:
```python
from codeviewx.tools import list_real_directory

listing = list_real_directory("/path/to/project")
print(listing)
# Output:
# Directory: /path/to/project
# Total 5 directories, 12 files
#
# Directories:
# 📁 src/
# 📁 tests/
# 📁 docs/
#
# Files:
# 📄 README.md
# 📄 requirements.txt
# 📄 main.py
```

**Features**:
- Classifies directories and files separately
- Provides statistics
- Uses emojis for visual distinction
- Sorted output for consistency

Reference: [filesystem.py](../codeviewx/tools/filesystem.py#L78)

### Code Search Tools

#### `ripgrep_search()`

High-performance code search using ripgrep engine.

```python
def ripgrep_search(
    pattern: str,
    path: str = ".",
    file_type: Optional[str] = None,
    ignore_case: bool = False,
    max_count: int = 100
) -> str
```

**Purpose**: Fast pattern searching in code files

**Parameters**:
- `pattern` (str): Regular expression pattern to search for
- `path` (str): Search path (default: current directory)
- `file_type` (Optional[str]): File type filter (e.g., 'py', 'js', 'md')
- `ignore_case` (bool): Case-insensitive search (default: False)
- `max_count` (int): Maximum results to return (default: 100)

**Returns**: 
- `str`: Search results with file paths and line numbers

**Examples**:
```python
from codeviewx.tools import ripgrep_search

# Search for function definitions in Python files
results = ripgrep_search("def main", ".", "py")

# Case-insensitive search for TODO comments
results = ripgrep_search("TODO", ".", ignore_case=True)

# Search for import statements
results = ripgrep_search("import.*requests", ".", "py")
```

**Features**:
- Automatically ignores common non-source directories
- Supports regular expressions
- Shows line numbers and file paths
- Much faster than traditional grep

Reference: [search.py](../codeviewx/tools/search.py#L15)

### Command Execution Tools

#### `execute_command()`

Executes system commands with output capture and error handling.

```python
def execute_command(command: str, working_dir: Optional[str] = None) -> str
```

**Purpose**: Safe system command execution

**Parameters**:
- `command` (str): Command to execute
- `working_dir` (Optional[str]): Working directory for command execution

**Returns**: 
- `str`: Command output or error message

**Examples**:
```python
from codeviewx.tools import execute_command

# List files in directory
output = execute_command("ls -la")

# Run tests
output = execute_command("pytest tests/", "/path/to/project")

# Get Git status
output = execute_command("git status")
```

**Features**:
- Captures stdout and stderr
- Supports custom working directory
- Comprehensive error handling
- Returns formatted output

## CLI API

### `main()`

Command-line interface entry point.

```python
def main() -> None
```

**Purpose**: CLI entry point for command-line usage

**Returns**: None

**Command-line Options**:
```bash
codeviewx [OPTIONS]

Options:
  -v, --version              Show version and exit
  -w, --working-dir PATH     Project working directory
  -o, --output-dir PATH      Documentation output directory
  -l, --language LANGUAGE    Documentation language
  --ui-lang LANGUAGE         UI language (en/zh)
  --recursion-limit INTEGER  Agent recursion limit
  --verbose                  Show detailed logs
  --serve                    Start web server
  --help                     Show help message
```

**Examples**:
```bash
# Basic usage
codeviewx

# Custom configuration
codeviewx -w /path/to/project -o docs -l English --verbose

# Start web server
codeviewx --serve -o docs

# Generate Chinese documentation
codeviewx -l Chinese --ui-lang zh
```

Reference: [cli.py](../codeviewx/cli.py#L16)

## Configuration API

### Version Information

```python
from codeviewx import __version__, __author__, __description__

print(__version__)      # "0.2.0"
print(__author__)        # "CodeViewX Team"
print(__description__)   # "AI-Driven Code Documentation Generator"
```

### Environment Variables

CodeViewX responds to several environment variables:

- `ANTHROPIC_AUTH_TOKEN`: Anthropic API key for Claude access
- `PYTHONPATH`: Python path for module resolution
- `LANG`: System locale for language detection

**Example Setup**:
```bash
export ANTHROPIC_AUTH_TOKEN="your-api-key-here"
export LANG="en_US.UTF-8"
```

## Error Handling

### Common Exceptions

| Exception Type | Cause | Resolution |
|---------------|-------|------------|
| `FileNotFoundError` | Working directory doesn't exist | Verify directory path |
| `ValueError` | Invalid language specified | Use supported language codes |
| `PermissionError` | Insufficient file permissions | Check directory permissions |
| `ConnectionError` | API connectivity issues | Verify network and API key |

### Error Response Format

Tool functions return descriptive error messages:

```python
result = read_real_file("nonexistent.txt")
print(result)  # "❌ Error: File 'nonexistent.txt' does not exist"

result = ripgrep_search("pattern", "/invalid/path")
print(result)  # "❌ Error: Directory '/invalid/path' does not exist"
```

## Integration Examples

### Basic Python Integration

```python
from codeviewx import generate_docs, start_document_web_server

# Generate documentation
generate_docs(
    working_directory="./my_project",
    output_directory="./docs",
    doc_language="English",
    verbose=True
)

# Start web server
start_document_web_server("./docs")
```

### Custom Tool Integration

```python
from codeviewx.tools import ripgrep_search, read_real_file
from codeviewx.prompt import load_prompt

# Custom analysis workflow
def analyze_project(project_path):
    # Find entry points
    entry_points = ripgrep_search("def main|if __name__", project_path, "py")
    
    # Read configuration
    config_content = read_real_file(f"{project_path}/pyproject.toml")
    
    # Load custom prompt
    prompt = load_prompt("custom_analysis", project_data=entry_points)
    
    return {
        "entry_points": entry_points,
        "config": config_content,
        "prompt": prompt
    }
```

### Batch Processing

```python
from codeviewx import generate_docs
import os

def process_multiple_projects(projects):
    for project in projects:
        output_dir = f"docs_{os.path.basename(project)}"
        
        try:
            generate_docs(
                working_directory=project,
                output_directory=output_dir,
                doc_language="English",
                verbose=False
            )
            print(f"✅ Generated docs for {project}")
        except Exception as e:
            print(f"❌ Failed to process {project}: {e}")

# Usage
projects = ["/path/to/project1", "/path/to/project2", "/path/to/project3"]
process_multiple_projects(projects)
```

### CI/CD Integration

```python
#!/usr/bin/env python3
"""
CI/CD script for automated documentation generation
"""

import os
import sys
from codeviewx import generate_docs

def main():
    project_dir = os.getenv("PROJECT_DIR", ".")
    output_dir = os.getenv("OUTPUT_DIR", "docs")
    language = os.getenv("DOC_LANGUAGE", "English")
    
    try:
        generate_docs(
            working_directory=project_dir,
            output_directory=output_dir,
            doc_language=language,
            verbose=True
        )
        
        print(f"✅ Documentation generated successfully in {output_dir}")
        return 0
        
    except Exception as e:
        print(f"❌ Documentation generation failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

This API reference provides comprehensive documentation for all public interfaces in CodeViewX, enabling developers to integrate the system into their workflows and extend its functionality as needed.