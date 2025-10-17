# Quick Start Guide

## System Requirements

Before installing CodeViewX, ensure your system meets the following requirements:

### Core Requirements
- **Python**: 3.8 or higher
- **pip**: Python package manager (included with Python)
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

### External Dependencies
- **ripgrep (rg)**: High-performance code search tool
- **Anthropic API Key**: Required for AI-powered analysis

### Recommended System Resources
- **RAM**: 4GB minimum, 8GB recommended for large projects
- **Storage**: 1GB free space for installation and documentation output
- **Network**: Internet connection for AI API calls

## Installation

### Step 1: Clone the Repository

```bash
# Clone the CodeViewX repository
git clone https://github.com/dean2021/codeviewx.git

# Navigate to the project directory
cd codeviewx
```

### Step 2: Install ripgrep

**macOS (using Homebrew)**:
```bash
brew install ripgrep
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install ripgrep
```

**Windows (using Chocolatey)**:
```bash
choco install ripgrep
```

**Other Systems**: Download from [ripgrep releases](https://github.com/BurntSushi/ripgrep/releases)

### Step 3: Install Python Dependencies

**Development Mode (Recommended)**:
```bash
pip install -e .
```

**Standard Installation**:
```bash
pip install .
```

**With Development Dependencies**:
```bash
pip install -e ".[dev]"
```

### Step 4: Configure Anthropic API Key

**Set Environment Variable (Linux/macOS)**:
```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY='your-api-key-here'

# Apply changes immediately
source ~/.bashrc  # or ~/.zshrc
```

**Set Environment Variable (Windows)**:
```powershell
# Command Prompt
set ANTHROPIC_API_KEY="your-api-key-here"

# PowerShell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

**Get Your API Key**: Visit [Anthropic Console](https://console.anthropic.com/) to create an account and obtain your API key.

## Basic Usage

### Command Line Interface

#### Generate Documentation for Current Directory
```bash
codeviewx
```

#### Specify Project and Output Directories
```bash
codeviewx -w /path/to/your/project -o /path/to/output/docs
```

#### Generate Documentation in Specific Language
```bash
# Generate English documentation
codeviewx -l English

# Generate Chinese documentation  
codeviewx -l Chinese
```

#### Advanced Options
```bash
# Verbose output for debugging
codeviewx --verbose

# Custom recursion limit for complex projects
codeviewx --recursion-limit 2000

# Specify UI language
codeviewx --ui-lang en
```

### Python API Usage

#### Basic Documentation Generation
```python
from codeviewx import generate_docs

# Generate documentation with default settings
generate_docs()

# Generate with custom settings
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English",
    verbose=True
)
```

#### Start Documentation Web Server
```python
from codeviewx import start_document_web_server

# Start server for generated documentation
start_document_web_server("docs")
```

#### Complete Example
```python
from codeviewx import generate_docs, start_document_web_server

# Generate documentation
generate_docs(
    working_directory="./my_project",
    output_directory="./documentation",
    doc_language="English",
    verbose=True
)

# Start web server to view documentation
start_document_web_server("./documentation")
```

## Documentation Web Server

### Start the Server
```bash
# Generate and serve documentation
codeviewx --serve -o docs
```

### Access Documentation
Open your web browser and navigate to:
```
http://localhost:5000
```

### Server Features
- **Interactive Navigation**: Browse documentation with a clean, modern interface
- **Search Functionality**: Quick search across all documentation
- **Code Highlighting**: Syntax-highlighted code examples
- **Mermaid Diagrams**: Interactive architecture and flow diagrams
- **Responsive Design**: Works on desktop and mobile devices

### Stop the Server
Press `Ctrl+C` in the terminal to stop the web server.

## Command Line Options Reference

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--working-dir` | `-w` | Project directory to analyze | `-w /path/to/project` |
| `--output-dir` | `-o` | Documentation output directory | `-o docs` |
| `--language` | `-l` | Documentation language | `-l English` |
| `--ui-lang` | | UI language (en/zh) | `--ui-lang en` |
| `--serve` | | Start web server | `--serve` |
| `--verbose` | `-v` | Show detailed logs | `--verbose` |
| `--recursion-limit` | | Agent recursion limit | `--recursion-limit 1500` |
| `--version` | `-V` | Show version information | `--version` |

## Supported Documentation Languages

CodeViewX supports generating documentation in 8 languages:

- **Chinese** (中文)
- **English** 
- **Japanese** (日本語)
- **Korean** (한국어)
- **French** (Français)
- **German** (Deutsch)
- **Spanish** (Español)
- **Russian** (Русский)

Example usage:
```bash
codeviewx -l French
codeviewx -l Japanese
codeviewx -l German
```

## Example Projects

### Analyze a Python Web Application
```bash
# Analyze a Flask/Django project
codeviewx -w ./my_web_app -o ./web_app_docs -l English
```

### Document a CLI Tool
```bash
# Analyze a command-line tool
codeviewx -w ./my_cli_tool -o ./cli_docs --verbose
```

### Multi-Language Project
```bash
# Analyze a project with multiple programming languages
codeviewx -w ./multi_lang_project -o ./docs --recursion-limit 2000
```

### Generate Documentation in Multiple Languages
```bash
# English documentation
codeviewx -w ./project -o ./docs/en -l English

# Chinese documentation  
codeviewx -w ./project -o ./docs/zh -l Chinese

# Japanese documentation
codeviewx -w ./project -o ./docs/ja -l Japanese
```

## Troubleshooting Common Issues

### Installation Issues

**Problem**: `pip install` fails with permission errors
```bash
# Solution: Use user installation
pip install --user -e .
```

**Problem**: Python version too old
```bash
# Check Python version
python --version

# Update Python (example for Ubuntu)
sudo apt update
sudo apt install python3.9
```

### API Key Issues

**Problem**: Invalid Anthropic API key
```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Test API key (using curl)
curl -X POST https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -d '{"model": "claude-3-haiku-20240307", "max_tokens": 10, "messages": [{"role": "user", "content": "Hi"}]}'
```

### ripgrep Issues

**Problem**: `rg` command not found
```bash
# Check if ripgrep is installed
rg --version

# Install ripgrep if missing
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep
```

### Performance Issues

**Problem**: Analysis takes too long for large projects
```bash
# Increase recursion limit
codeviewx --recursion-limit 3000

# Use verbose mode to monitor progress
codeviewx --verbose
```

### Documentation Issues

**Problem**: Generated documentation is incomplete
```bash
# Use verbose mode to see detailed analysis
codeviewx --verbose

# Check for specific errors in the output
codeviewx --verbose 2>&1 | tee analysis.log
```

## Next Steps

After successfully generating your first documentation:

1. **Review Generated Documentation**: Check the quality and completeness of generated docs
2. **Customize Prompts**: Modify prompt templates for project-specific needs
3. **Integrate with CI/CD**: Add documentation generation to your build pipeline
4. **Explore Advanced Features**: Learn about custom tools and extensions
5. **Contribute**: Consider contributing to the CodeViewX project

For more advanced usage, see the [Development Guide](./07-development-guide.md) and [API Reference](./06-api-reference.md).