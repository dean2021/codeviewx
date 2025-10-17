# Quick Start Guide

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **pip**: Package manager
- **ripgrep (rg)**: High-performance code search tool
- **API Key**: Anthropic API key for AI analysis

### Installing ripgrep

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows (with Chocolatey)
choco install ripgrep

# Windows (with Scoop)
scoop install ripgrep

# Manual installation
# Download from: https://github.com/BurntSushi/ripgrep/releases
```

### Getting API Key

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key for configuration

## Installation

### Option 1: Development Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# Install in development mode
pip install -e .
```

### Option 2: Standard Installation

```bash
# Clone the repository
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# Install normally
pip install .
```

### Option 3: Install from PyPI (when available)

```bash
pip install codeviewx
```

## Configuration

### Setting API Key

```bash
# Method 1: Environment variable (recommended)
export ANTHROPIC_API_KEY="your-api-key-here"

# Method 2: Add to shell profile
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
# or for zsh
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc

# Reload shell configuration
source ~/.bashrc  # or source ~/.zshrc
```

### Verification

```bash
# Verify installation
codeviewx --version

# Verify ripgrep
rg --version

# Verify API key (optional)
echo $ANTHROPIC_API_KEY
```

## Basic Usage

### Command Line Interface

#### 1. Analyze Current Directory

```bash
# Basic usage - analyze current directory
codeviewx

# Output will be in docs/ directory by default
```

#### 2. Specify Project Directory

```bash
# Analyze specific project
codeviewx -w /path/to/your/project

# Example
codeviewx -w ~/my-project
```

#### 3. Specify Output Directory

```bash
# Custom output directory
codeviewx -o my-docs

# Combine with project directory
codeviewx -w /path/to/project -o documentation
```

#### 4. Language Selection

```bash
# Generate English documentation
codeviewx -l English

# Generate Chinese documentation
codeviewx -l Chinese

# Available languages:
# Chinese, English, Japanese, Korean, French, German, Spanish, Russian
```

#### 5. Verbose Mode

```bash
# Show detailed logs
codeviewx --verbose

# Useful for debugging and understanding the process
```

#### 6. Complete Example

```bash
# Full configuration example
codeviewx -w ~/my-project -o docs -l English --verbose
```

### Python API

#### Basic Usage

```python
from codeviewx import generate_docs

# Generate documentation
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English"
)
```

#### Advanced Usage

```python
from codeviewx import generate_docs

# With all parameters
generate_docs(
    working_directory="/path/to/project",
    output_directory="technical-docs",
    doc_language="Chinese",
    ui_language="en",
    recursion_limit=1500,
    verbose=True
)
```

### Web Server

#### Start Documentation Server

```bash
# Start server (requires docs to exist)
codeviewx --serve

# Start with custom directory
codeviewx --serve -o docs

# Server will be available at: http://127.0.0.1:5000
```

#### Python API for Server

```python
from codeviewx import start_document_web_server

# Start web server
start_document_web_server("docs")
```

## Generated Documentation Structure

After running CodeViewX, you'll get a complete documentation set:

```
docs/
├── README.md              # Overview and navigation
├── 01-overview.md         # Project overview and tech stack
├── 02-quickstart.md       # Quick start guide (like this file)
├── 03-architecture.md     # System architecture
├── 04-core-mechanisms.md  # Core working mechanisms
├── 05-data-models.md      # Data models (if applicable)
├── 06-api-reference.md    # API documentation (if applicable)
├── 07-development-guide.md # Development guide
└── 08-testing.md          # Testing documentation (if applicable)
```

## Common Use Cases

### 1. Document Your Own Project

```bash
# Navigate to your project
cd my-project

# Generate documentation
codeviewx -l English

# Start web server to view
codeviewx --serve
```

### 2. Analyze Open Source Projects

```bash
# Clone a project
git clone https://github.com/user/repo.git
cd repo

# Generate documentation
codeviewx -w . -o repo-docs -l English

# View documentation
codeviewx --serve -o repo-docs
```

### 3. Multi-Language Documentation

```bash
# Generate English docs
codeviewx -l English -o docs-en

# Generate Chinese docs
codeviewx -l Chinese -o docs-zh

# Generate Japanese docs
codeviewx -l Japanese -o docs-ja
```

## Troubleshooting

### Common Issues

#### 1. API Key Not Found
```
Error: ANTHROPIC_API_KEY not found
```
**Solution**: Set the environment variable properly
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

#### 2. ripgrep Not Found
```
Error: rg command not found
```
**Solution**: Install ripgrep following the installation instructions

#### 3. Permission Denied
```
Error: Permission denied when writing to output directory
```
**Solution**: Check directory permissions or use a different output directory
```bash
codeviewx -o /tmp/docs
```

#### 4. Python Version Incompatible
```
Error: Python 3.8+ required
```
**Solution**: Upgrade Python or use virtual environment

### Debug Mode

For detailed troubleshooting, use verbose mode:

```bash
codeviewx --verbose
```

This will show:
- Detailed AI agent steps
- Tool calls and results
- File processing details
- Error stack traces

## Tips and Best Practices

### 1. Project Preparation
- Ensure your project has clear structure
- Remove sensitive files (`.env`, `.secrets`)
- Include meaningful file names and comments

### 2. Optimize Performance
- Use `.gitignore` to exclude unnecessary files
- Large projects may require higher recursion limits
- Use specific project directories instead of entire repositories

### 3. Documentation Quality
- Review generated documentation for accuracy
- Add project-specific customizations
- Consider multiple language outputs for international projects

### 4. Workflow Integration
- Integrate into CI/CD pipelines
- Generate docs automatically on release
- Use web server for team collaboration

## Next Steps

- [Project Overview](01-overview.md) - Understand the project structure
- [Architecture](03-architecture.md) - Learn about system design
- [Core Mechanisms](04-core-mechanisms.md) - Deep dive into implementation

---

*Need help? Check the [Development Guide](07-development-guide.md) or open an issue on GitHub.*