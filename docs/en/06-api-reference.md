# API Reference

## Overview

This document provides a comprehensive reference for all public APIs in CodeViewX, including the command-line interface, Python API, and internal function interfaces.

## Command Line Interface (CLI)

### Main Command: `codeviewx`

#### Syntax

```bash
codeviewx [OPTIONS]
```

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--working-dir` | `-w` | `PATH` | Current directory | Project directory to analyze |
| `--output-dir` | `-o` | `PATH` | `docs` | Documentation output directory |
| `--language` | `-l` | `STRING` | Auto-detect | Documentation language |
| `--recursion-limit` | | `INTEGER` | `1000` | Agent recursion limit |
| `--verbose` | | `FLAG` | `False` | Show detailed logs |
| `--serve` | | `FLAG` | `False` | Start web server |
| `--version` | `-v` | `FLAG` | | Show version information |
| `--help` | `-h` | `FLAG` | | Show help message |

#### Language Options

- `Chinese` (中文)
- `English`
- `Japanese` (日本語)
- `Korean` (한국어)
- `French` (Français)
- `German` (Deutsch)
- `Spanish` (Español)
- `Russian` (Русский)

#### Usage Examples

```bash
# Basic usage
codeviewx

# Analyze specific project
codeviewx -w /path/to/project

# Custom output directory and language
codeviewx -o documentation -l English

# Verbose mode with custom recursion limit
codeviewx --verbose --recursion-limit 500

# Start web server
codeviewx --serve

# Complete configuration
codeviewx -w /project -o docs -l English --verbose --recursion-limit 800
```

#### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | Optional (if using Claude) |
| `OPENAI_API_KEY` | OpenAI API key | Optional (if using OpenAI) |
| `PYTHONPATH` | Python path extensions | Optional |
| `LANG` | System language locale | Optional |

#### Exit Codes

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | General error |
| `130` | User interrupt (Ctrl+C) |

---

## Python API

### Core Functions

#### `generate_docs()`

Generate documentation for a project.

```python
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None:
```

**Parameters:**

- `working_directory` (`Optional[str]`): Project directory to analyze. If `None`, uses current directory.
- `output_directory` (`str`): Directory where documentation will be generated. Default: `"docs"`.
- `doc_language` (`Optional[str]`): Language for generated documentation. If `None`, auto-detects system language.
- `recursion_limit` (`int`): Maximum recursion depth for AI agent. Default: `1000`.
- `verbose` (`bool`): Enable detailed logging output. Default: `False`.

**Example:**

```python
from codeviewx import generate_docs

# Basic usage
generate_docs()

# Custom configuration
generate_docs(
    working_directory="/path/to/project",
    output_directory="documentation",
    doc_language="English",
    verbose=True
)
```

#### `start_document_web_server()`

Start the web documentation server.

```python
def start_document_web_server(output_directory: str = "docs") -> None:
```

**Parameters:**

- `output_directory` (`str`): Directory containing generated documentation. Default: `"docs"`.

**Example:**

```python
from codeviewx import start_document_web_server

# Start server with default directory
start_document_web_server()

# Start server with custom directory
start_document_web_server("documentation")
```

#### `detect_system_language()`

Detect the system's default language.

```python
def detect_system_language() -> str:
```

**Returns:**

- `str`: Detected language code (e.g., `"English"`, `"Chinese"`, `"Japanese"`)

**Example:**

```python
from codeviewx import detect_system_language

language = detect_system_language()
print(f"Detected language: {language}")
```

#### `load_prompt()`

Load and format a prompt template.

```python
def load_prompt(name: str, **kwargs) -> str:
```

**Parameters:**

- `name` (`str`): Name of the prompt template (without extension).
- `**kwargs`: Template variables for substitution.

**Returns:**

- `str`: Formatted prompt text.

**Example:**

```python
from codeviewx import load_prompt

# Load basic prompt
prompt = load_prompt("DocumentEngineer")

# Load with variables
prompt = load_prompt(
    "DocumentEngineer_compact",
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English"
)
```

### Utility Functions

#### `get_markdown_title()`

Extract the first title from a markdown file.

```python
def get_markdown_title(file_path: str) -> Optional[str]:
```

**Parameters:**

- `file_path` (`str`): Path to markdown file.

**Returns:**

- `Optional[str]`: First title found, or `None` if no title exists.

**Example:**

```python
from codeviewx import get_markdown_title

title = get_markdown_title("README.md")
if title:
    print(f"Document title: {title}")
```

#### `generate_file_tree()`

Generate a file tree structure for navigation.

```python
def generate_file_tree(directory: str, current_file: Optional[str] = None) -> List[dict]:
```

**Parameters:**

- `directory` (`str`): Directory to scan.
- `current_file` (`Optional[str]`): Currently active file for highlighting.

**Returns:**

- `List[dict]`: List of file tree nodes.

**Example:**

```python
from codeviewx import generate_file_tree

file_tree = generate_file_tree("docs", "README.md")
for node in file_tree:
    print(f"{node['name']}: {node['type']}")
```

---

## Tool APIs

### File System Tools

#### `write_real_file()`

Write content to a file in the real file system.

```python
def write_real_file(file_path: str, content: str) -> str:
```

**Parameters:**

- `file_path` (`str`): Path to the file to write.
- `content` (`str`): Content to write to the file.

**Returns:**

- `str`: Success message with file information.

**Example:**

```python
from codeviewx.tools import write_real_file

result = write_real_file("docs/test.md", "# Test Document\n\nThis is a test.")
print(result)  # Output: ✅ 成功写入文件: docs/test.md (0.05 KB)
```

#### `read_real_file()`

Read content from a file in the real file system.

```python
def read_real_file(file_path: str) -> str:
```

**Parameters:**

- `file_path` (`str`): Path to the file to read.

**Returns:**

- `str`: File content with metadata header.

**Example:**

```python
from codeviewx.tools import read_real_file

content = read_real_file("README.md")
print(content)  # File content with size and line information
```

#### `list_real_directory()`

List contents of a directory in the real file system.

```python
def list_real_directory(directory: str = ".") -> str:
```

**Parameters:**

- `directory` (`str`): Directory path to list. Default: current directory.

**Returns:**

- `str`: Formatted directory listing.

**Example:**

```python
from codeviewx.tools import list_real_directory

listing = list_real_directory(".")
print(listing)  # Directory contents with categorization
```

### Search Tools

#### `ripgrep_search()`

Search for text patterns using ripgrep.

```python
def ripgrep_search(
    pattern: str,
    path: str = ".",
    file_type: Optional[str] = None,
    ignore_case: bool = False,
    max_count: int = 100
) -> str:
```

**Parameters:**

- `pattern` (`str`): Regular expression pattern to search for.
- `path` (`str`): Directory to search in. Default: current directory.
- `file_type` (`Optional[str]`): File type filter (e.g., `"py"`, `"js"`).
- `ignore_case` (`bool`): Perform case-insensitive search. Default: `False`.
- `max_count` (`int`): Maximum number of results to return. Default: `100`.

**Returns:**

- `str`: Search results with file paths and line numbers.

**Example:**

```python
from codeviewx.tools import ripgrep_search

# Search for function definitions
results = ripgrep_search("def main", ".", "py")
print(results)

# Case-insensitive search
results = ripgrep_search("TODO", "/path/to/project", ignore_case=True)
print(results)
```

### Command Tools

#### `execute_command()`

Execute system commands and return output.

```python
def execute_command(command: str) -> str:
```

**Parameters:**

- `command` (`str`): Command to execute.

**Returns:**

- `str`: Command output.

**Example:**

```python
from codeviewx.tools import execute_command

# List directory contents
output = execute_command("ls -la")
print(output)

# Get Git status
output = execute_command("git status")
print(output)
```

---

## Web Server APIs

### Flask Routes

The web server provides the following routes:

#### GET `/`

Serve the default documentation page (README.md).

**Response:** HTML page with rendered documentation.

#### GET `/<path:filename>`

Serve a specific documentation file.

**Parameters:**

- `filename` (`str`): Path to the documentation file relative to output directory.

**Response:** HTML page with rendered documentation.

**Example:**

```
GET /01-overview.md
GET /api-reference.md
GET /static/css/style.css
```

### Template Context

The documentation template receives the following context variables:

```python
{
    'markdown_html_content': str,    # Rendered HTML content
    'file_tree': List[dict],         # Navigation file tree
    'current_file': str,             # Current file path
    'title': str,                    # Document title
    'toc': str                       # Table of contents HTML
}
```

---

## Error Handling

### Exception Types

#### `FileNotFoundError`

Raised when a required file is not found.

```python
try:
    content = read_real_file("nonexistent.md")
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

#### `PermissionError`

Raised when file system permissions are insufficient.

```python
try:
    write_real_file("/protected/file.md", "content")
except PermissionError as e:
    print(f"Permission denied: {e}")
```

#### `ValueError`

Raised when invalid parameters are provided.

```python
try:
    prompt = load_prompt("nonexistent_prompt")
except ValueError as e:
    print(f"Invalid prompt: {e}")
```

### Error Response Format

Tool functions return standardized error messages:

```
❌ Error: [Error description]
```

Example:
```
❌ 错误: 文件 'nonexistent.md' 不存在
❌ 搜索错误: ripgrep (rg) 未安装
❌ 写入文件失败: Permission denied
```

---

## Configuration APIs

### Package Configuration

Access package configuration through `pyproject.toml`:

```python
# Example: Access package metadata
from codeviewx import __version__, __description__

print(f"Version: {__version__}")
print(f"Description: {__description__}")
```

### Environment Configuration

Access environment variables:

```python
import os

# Get API keys
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

# Get system language
import locale
lang, encoding = locale.getdefaultlocale()
```

---

## Integration Examples

### Basic Integration

```python
#!/usr/bin/env python3
"""
Example: Basic CodeViewX integration
"""

from codeviewx import generate_docs, detect_system_language

def main():
    # Detect system language
    language = detect_system_language()
    print(f"Using language: {language}")
    
    # Generate documentation
    generate_docs(
        working_directory=".",
        output_directory="docs",
        doc_language=language,
        verbose=True
    )
    
    print("Documentation generation completed!")

if __name__ == "__main__":
    main()
```

### Advanced Integration

```python
#!/usr/bin/env python3
"""
Example: Advanced CodeViewX integration with error handling
"""

import os
import sys
from pathlib import Path
from codeviewx import generate_docs, start_document_web_server, detect_system_language

def validate_environment():
    """Validate required environment"""
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("Error: No API key found. Please set ANTHROPIC_API_KEY or OPENAI_API_KEY")
        return False
    
    # Check if ripgrep is available
    try:
        import subprocess
        subprocess.run(["rg", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: ripgrep not found. Install with: brew install ripgrep")
    
    return True

def generate_project_docs(project_path: str, output_dir: str = "docs"):
    """Generate documentation for a project"""
    try:
        # Validate project path
        if not Path(project_path).exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")
        
        # Detect language or use English
        language = detect_system_language()
        print(f"Generating documentation in {language}")
        
        # Generate documentation
        generate_docs(
            working_directory=project_path,
            output_directory=output_dir,
            doc_language=language,
            verbose=True
        )
        
        print(f"Documentation generated in: {output_dir}")
        return True
        
    except Exception as e:
        print(f"Error generating documentation: {e}")
        return False

def main():
    """Main integration function"""
    if not validate_environment():
        sys.exit(1)
    
    # Configuration
    project_path = "/path/to/your/project"
    output_dir = "documentation"
    
    # Generate documentation
    if generate_project_docs(project_path, output_dir):
        # Optionally start web server
        print("Starting web server...")
        start_document_web_server(output_dir)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### CI/CD Integration

```python
#!/usr/bin/env python3
"""
Example: CI/CD integration
"""

import os
import sys
from pathlib import Path
from codeviewx import generate_docs

def generate_docs_for_ci():
    """Generate documentation in CI/CD environment"""
    # CI/CD configuration
    project_path = os.getenv("PROJECT_PATH", ".")
    output_dir = os.getenv("OUTPUT_DIR", "docs")
    language = os.getenv("DOC_LANGUAGE", "English")
    
    # Validate inputs
    if not Path(project_path).exists():
        print(f"Error: Project path {project_path} does not exist")
        sys.exit(1)
    
    # Generate documentation
    try:
        generate_docs(
            working_directory=project_path,
            output_directory=output_dir,
            doc_language=language,
            verbose=True
        )
        print(f"✅ Documentation generated successfully in {output_dir}")
        
        # List generated files
        output_path = Path(output_dir)
        if output_path.exists():
            files = list(output_path.glob("**/*.md"))
            print(f"📄 Generated {len(files)} documentation files:")
            for file in sorted(files):
                print(f"   - {file.relative_to(output_dir)}")
        
    except Exception as e:
        print(f"❌ Error generating documentation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_docs_for_ci()
```

---

## Performance Considerations

### Memory Usage

- **Large Projects**: Use `--recursion-limit` to control memory usage
- **File Processing**: Large files are processed in chunks
- **Caching**: Results are cached to avoid repeated operations

### API Usage

- **Rate Limiting**: Built-in rate limiting for AI API calls
- **Token Optimization**: Compact prompts reduce token usage
- **Batch Processing**: Multiple files processed in parallel when possible

### File System

- **Path Validation**: All paths are validated for security
- **Permission Checks**: File permissions are checked before operations
- **Atomic Operations**: File writes use atomic operations when possible

---

## Troubleshooting

### Common Issues

#### 1. ripgrep not found

```bash
# Error: ripgrep (rg) 未安装
# Solution: Install ripgrep
brew install ripgrep  # macOS
sudo apt install ripgrep  # Ubuntu/Debian
```

#### 2. API key issues

```python
# Check API key configuration
import os
if not os.getenv("ANTHROPIC_API_KEY"):
    print("Please set ANTHROPIC_API_KEY environment variable")
```

#### 3. Permission errors

```python
# Check file permissions
import os
if not os.access("/path/to/directory", os.R_OK):
    print("No read permission for directory")
```

### Debug Mode

Enable verbose logging for debugging:

```python
# CLI
codeviewx --verbose

# Python API
generate_docs(verbose=True)
```

### Log Analysis

Check logs for detailed error information:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
generate_docs()
```

---

*This API reference provides comprehensive documentation for all public interfaces in CodeViewX. For implementation details and usage examples, see the [Core Mechanisms](04-core-mechanisms.md) documentation.*