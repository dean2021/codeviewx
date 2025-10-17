# Quick Start Guide

This guide will help you get started with CodeViewX quickly, from installation to generating your first set of documentation.

## Installation

### Prerequisites

Before installing CodeViewX, ensure you have the following:

- **Python 3.8+** installed on your system
- **pip** package manager
- **ripgrep** (rg) installed on your system (required for code search functionality)

### Install ripgrep

```bash
# macOS (using Homebrew)
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# CentOS/RHEL/Fedora
sudo dnf install ripgrep

# Windows (using Chocolatey)
choco install ripgrep

# Or download from: https://github.com/BurntSushi/ripgrep
```

### Install CodeViewX

#### Option 1: From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

#### Option 2: From PyPI (Future Release)

```bash
# Note: Not yet published to PyPI
pip install codeviewx
```

### Configure API Keys

CodeViewX requires an API key for AI services. Currently supports Anthropic Claude:

```bash
# Set Anthropic API key
export ANTHROPIC_API_KEY='your-anthropic-api-key-here'

# Or add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
echo 'export ANTHROPIC_API_KEY="your-anthropic-api-key-here"' >> ~/.bashrc
```

### Verify Installation

```bash
# Check if CodeViewX is installed
codeviewx --version

# Expected output: CodeViewX 0.1.0
```

## Basic Usage

### 1. Generate Documentation for Current Directory

The simplest way to use CodeViewX is to run it in your project directory:

```bash
# Navigate to your project
cd /path/to/your/project

# Generate documentation (auto-detects language)
codeviewx

# Documentation will be generated in the 'docs' directory
```

### 2. Specify Project Directory

Generate documentation for a specific project:

```bash
# Analyze a specific project
codeviewx -w /path/to/project

# Or using long form
codeviewx --working-dir /path/to/project
```

### 3. Choose Output Directory

Specify where to save the generated documentation:

```bash
# Output to custom directory
codeviewx -w /path/to/project -o my-docs

# Or using long form
codeviewx --working-dir /path/to/project --output-dir my-docs
```

### 4. Select Documentation Language

Choose from 8 supported languages:

```bash
# Generate English documentation
codeviewx -l English

# Generate Chinese documentation
codeviewx -l Chinese

# Other supported languages:
# codeviewx -l Japanese
# codeviewx -l Korean
# codeviewx -l French
# codeviewx -l German
# codeviewx -l Spanish
# codeviewx -l Russian
```

### 5. Enable Verbose Logging

See detailed progress and debugging information:

```bash
# Enable verbose output
codeviewx --verbose

# Combined with other options
codeviewx -w /path/to/project -l English --verbose
```

## Web Documentation Browser

CodeViewX includes a built-in web server for browsing generated documentation.

### Start Web Server

```bash
# Start server for default docs directory
codeviewx --serve

# Start server for custom documentation directory
codeviewx --serve -o my-docs

# Or using long form
codeviewx --serve --output-dir my-docs
```

### Access Documentation

Once the server is running:

1. Open your web browser
2. Navigate to **http://127.0.0.1:5000**
3. Browse your generated documentation with:
   - Interactive table of contents
   - File tree navigation
   - Syntax-highlighted code
   - Mermaid diagram support

### Stop Web Server

Press **Ctrl+C** in the terminal to stop the web server.

## Python API Usage

You can also use CodeViewX as a Python library in your projects.

### Basic API Usage

```python
from codeviewx import generate_docs

# Generate documentation with default settings
generate_docs()

# Generate documentation with custom settings
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English",
    verbose=True
)
```

### Advanced API Usage

```python
from codeviewx import generate_docs, detect_system_language

# Detect system language
language = detect_system_language()
print(f"Detected language: {language}")

# Generate documentation with detected language
generate_docs(
    working_directory="/path/to/project",
    output_directory="technical-docs",
    doc_language=language,
    recursion_limit=1000,
    verbose=False
)
```

### Language Detection

```python
from codeviewx.language import detect_system_language

# Detect system language
detected_lang = detect_system_language()
print(f"System language: {detected_lang}")

# Expected outputs: 'Chinese', 'English', 'Japanese', 'Korean', 
#                  'French', 'German', 'Spanish', 'Russian'
```

## Command Line Reference

### Complete Command Syntax

```bash
codeviewx [OPTIONS]
```

### Available Options

| Option | Short | Long | Description | Default |
|--------|-------|------|-------------|---------|
| Working Directory | `-w` | `--working-dir` | Project directory to analyze | Current directory |
| Output Directory | `-o` | `--output-dir` | Documentation output directory | `docs` |
| Language | `-l` | `--language` | Documentation language | Auto-detect |
| Recursion Limit | | `--recursion-limit` | Agent recursion limit | `1000` |
| Verbose | | `--verbose` | Show detailed logging | `False` |
| Serve Mode | | `--serve` | Start web server | `False` |
| Version | `-v` | `--version` | Show version information | |
| Help | `-h` | `--help` | Show help message | |

### Supported Languages

| Language | Code | Description |
|----------|------|-------------|
| English | `English` | Default language |
| Chinese | `Chinese` | 中文 |
| Japanese | `Japanese` | 日本語 |
| Korean | `Korean` | 한국어 |
| French | `French` | Français |
| German | `German` | Deutsch |
| Spanish | `Spanish` | Español |
| Russian | `Russian` | Русский |

## Example Workflows

### 1. Quick Documentation for Your Project

```bash
# Navigate to your project
cd my-awesome-project

# Generate documentation
codeviewx

# Start web server to view
codeviewx --serve

# Open http://127.0.0.1:5000 in your browser
```

### 2. Multi-Language Documentation

```bash
# Generate English documentation
codeviewx -l English -o docs-en

# Generate Chinese documentation  
codeviewx -l Chinese -o docs-zh

# Start servers for both (in different terminals)
# Terminal 1:
codeviewx --serve -o docs-en -p 5000

# Terminal 2:
codeviewx --serve -o docs-zh -p 5001
```

### 3. Automated Documentation Generation

```python
# save as generate_docs.py
from codeviewx import generate_docs
import os

# Configuration
projects = [
    {"path": "/path/to/project1", "lang": "English"},
    {"path": "/path/to/project2", "lang": "Chinese"},
    {"path": "/path/to/project3", "lang": "Japanese"}
]

# Generate documentation for all projects
for project in projects:
    print(f"Generating docs for {project['path']} in {project['lang']}...")
    
    # Create output directory name
    output_dir = f"docs-{project['lang'].lower()}-{os.path.basename(project['path'])}"
    
    generate_docs(
        working_directory=project['path'],
        output_directory=output_dir,
        doc_language=project['lang'],
        verbose=True
    )
    
    print(f"✅ Documentation generated: {output_dir}")

print("🎉 All documentation generated successfully!")
```

### 4. CI/CD Integration

```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install ripgrep
      run: sudo apt-get install ripgrep
    
    - name: Install CodeViewX
      run: |
        git clone https://github.com/dean2021/codeviewx.git
        cd codeviewx
        pip install -e .
    
    - name: Generate Documentation
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        codeviewx -w . -o docs -l English --verbose
    
    - name: Upload Documentation
      uses: actions/upload-artifact@v2
      with:
        name: documentation
        path: docs/
```

## Troubleshooting

### Common Issues

#### 1. "ripgrep not found" Error

```bash
# Install ripgrep
brew install ripgrep  # macOS
sudo apt install ripgrep  # Linux

# Verify installation
rg --version
```

#### 2. API Key Issues

```bash
# Check if API key is set
echo $ANTHROPIC_API_KEY

# Set API key temporarily
export ANTHROPIC_API_KEY="your-key-here"

# Add to shell profile permanently
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### 3. Permission Issues

```bash
# Check file permissions
ls -la /path/to/project

# Fix permissions if needed
chmod -R 755 /path/to/project
```

#### 4. Memory Issues with Large Projects

```bash
# Increase recursion limit for large projects
codeviewx --recursion-limit 2000 -w /path/to/large/project

# Or analyze specific subdirectories
codeviewx -w /path/to/project/src
```

### Debug Mode

Enable verbose logging to troubleshoot issues:

```bash
# Enable verbose output
codeviewx --verbose

# This will show:
# - Detailed step-by-step progress
# - AI agent responses
# - Tool execution results
# - Error details
```

### Getting Help

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the generated documentation
- **Examples**: Review the `examples/` directory for usage patterns

## Next Steps

Once you've successfully generated documentation:

1. **Review Generated Docs**: Check the quality and completeness
2. **Customize Prompts**: Modify prompt templates if needed
3. **Integrate with CI/CD**: Set up automated documentation generation
4. **Contribute**: Help improve CodeViewX by reporting issues or submitting PRs

For more advanced usage and configuration options, see the [Development Guide](07-development-guide.md) and [API Reference](06-api-reference.md).