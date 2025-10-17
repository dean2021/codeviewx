# Quick Start Guide

## Overview

This guide will help you get CodeViewX up and running quickly. CodeViewX is an AI-powered code documentation generator that can analyze your codebase and create comprehensive technical documentation in minutes.

## Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 2GB RAM minimum (4GB recommended)
- **Disk Space**: 500MB for installation
- **Internet**: Required for AI API access

### Required Dependencies

1. **ripgrep** - Fast code search tool (system dependency)
2. **AI API Key** - Anthropic Claude or OpenAI

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
```

### Step 2: Install ripgrep

**macOS (using Homebrew):**
```bash
brew install ripgrep
```

**Ubuntu/Debian:**
```bash
sudo apt install ripgrep
```

**Windows (using Chocolatey):**
```bash
choco install ripgrep
```

**Windows (using Scoop):**
```bash
scoop install ripgrep
```

### Step 3: Install Python Package

```bash
# Install in development mode (recommended)
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Step 4: Configure API Key

**For Anthropic Claude (recommended):**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**For OpenAI:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY='your-api-key-here'
```

## Basic Usage

### Command Line Interface

#### Generate Documentation

```bash
# Analyze current directory (auto-detect language)
codeviewx

# Analyze specific project
codeviewx -w /path/to/your/project

# Specify output directory
codeviewx -o documentation

# Specify language
codeviewx -l English
```

#### Start Web Server

```bash
# Start server (default docs directory)
codeviewx --serve

# Start server with custom directory
codeviewx --serve -o documentation
```

Then visit `http://127.0.0.1:5000` in your browser.

### Python API

```python
from codeviewx import generate_docs

# Basic usage
generate_docs()

# Custom configuration
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English",
    verbose=True
)
```

## Complete Examples

### Example 1: Analyze a Python Project

```bash
# Step 1: Generate documentation
codeviewx -w /path/to/python-project -o docs -l English

# Step 2: View in browser
codeviewx --serve -o docs
```

Expected output:
```
CodeViewX v0.1.0

================================================================================
🚀 启动 CodeViewX 文档生成器 - 2025-06-17 14:30:00
================================================================================
📂 工作目录: /path/to/python-project
📝 输出目录: docs
🌍 文档语言: English (用户指定)
✓ 已加载系统提示词（已注入工作目录、输出目录和文档语言）
✓ 已创建 AI Agent
✓ 已注册 5 个自定义工具: execute_command, ripgrep_search, write_real_file, read_real_file, list_real_directory
================================================================================

📝 开始分析项目并生成文档...

🔍 分析项目结构...
📄 正在生成文档 (1): README.md
📄 正在生成文档 (2): 01-overview.md
...

================================================================================
✅ 文档生成完成!
================================================================================

📊 总结:
   ✓ 共生成 8 个文档文件
   ✓ 文档位置: docs/
   ✓ 执行步骤: 45 步
```

### Example 2: Multi-Language Documentation

```bash
# Generate English documentation
codeviewx -l English -o docs/en

# Generate Chinese documentation
codeviewx -l Chinese -o docs/zh

# Generate Japanese documentation
codeviewx -l Japanese -o docs/ja
```

### Example 3: Python Integration

```python
#!/usr/bin/env python3
from codeviewx import generate_docs, detect_system_language

# Detect system language
language = detect_system_language()
print(f"Detected language: {language}")

# Generate documentation
generate_docs(
    working_directory=".",
    output_directory="documentation",
    doc_language=language,
    verbose=True
)

print("Documentation generation completed!")
```

### Example 4: CI/CD Integration

```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        sudo apt install ripgrep
        pip install -e .
    
    - name: Generate documentation
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        codeviewx -l English -o docs
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
```

## Common Use Cases

### 1. Documenting an Existing Project

```bash
# Quick analysis of current project
codeviewx --verbose

# Then view results
codeviewx --serve
```

### 2. Creating Developer Onboarding Docs

```bash
# Generate comprehensive documentation
codeviewx -l English -o developer-docs

# Start web server for team access
codeviewx --serve -o developer-docs
```

### 3. API Documentation Generation

```bash
# Focus on API-related files
codeviewx -w /path/to/api-project -o api-docs -l English
```

### 4. Multi-Language Projects

```bash
# Generate docs in different languages
for lang in English Chinese Japanese; do
    codeviewx -l $lang -o docs/$lang
done
```

## Command Line Options Reference

### Basic Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--working-dir` | `-w` | Project directory to analyze | Current directory |
| `--output-dir` | `-o` | Documentation output directory | `docs` |
| `--language` | `-l` | Documentation language | Auto-detect |
| `--verbose` | | Show detailed logs | False |
| `--serve` | | Start web server | False |

### Language Options

- `Chinese` (中文)
- `English`
- `Japanese` (日本語)
- `Korean` (한국어)
- `French` (Français)
- `German` (Deutsch)
- `Spanish` (Español)
- `Russian` (Русский)

### Advanced Options

| Option | Description | Default |
|--------|-------------|---------|
| `--recursion-limit` | Agent recursion limit | 1000 |
| `--version` | Show version information | |
| `--help` | Show help message | |

## Troubleshooting

### Common Issues

#### 1. ripgrep not found

**Error**: `ripgrep (rg) 未安装`

**Solution**:
```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Verify installation
rg --version
```

#### 2. API Key Issues

**Error**: `Authentication failed`

**Solution**:
```bash
# Check if API key is set
echo $ANTHROPIC_API_KEY

# Set API key correctly
export ANTHROPIC_API_KEY='your-actual-api-key'
```

#### 3. Permission Errors

**Error**: `Permission denied`

**Solution**:
```bash
# Check directory permissions
ls -la /path/to/project

# Use appropriate permissions
codeviewx -w /path/to/accessible/project
```

#### 4. Memory Issues

**Error**: `Memory allocation failed`

**Solution**:
```bash
# Reduce recursion limit
codeviewx --recursion-limit 500

# Or use smaller project for testing
codeviewx -w /small/project
```

### Debug Mode

For troubleshooting, use verbose mode:

```bash
codeviewx --verbose
```

This will show:
- Detailed AI agent reasoning
- Complete tool execution logs
- Error stack traces
- Performance metrics

### Log Files

Check the following for debugging information:

```bash
# View recent logs
tail -f ~/.codeviewx/logs/codeviewx.log

# Check error logs
grep ERROR ~/.codeviewx/logs/codeviewx.log
```

## Performance Tips

### 1. Optimize Analysis Scope

```bash
# Exclude unnecessary directories
codeviewx -w /project --exclude node_modules --exclude .git
```

### 2. Use Compact Prompts

The system automatically uses optimized prompts for better performance.

### 3. Limit Recursion

For large projects, consider reducing recursion limit:

```bash
codeviewx --recursion-limit 500
```

### 4. Parallel Processing

CodeViewX automatically processes multiple files in parallel when possible.

## Next Steps

After successfully generating documentation:

1. **Review Generated Docs**: Check the quality and completeness
2. **Customize Prompts**: Modify prompt templates if needed
3. **Integrate with CI/CD**: Set up automatic documentation generation
4. **Contribute**: Report issues or contribute improvements

## Getting Help

- **Documentation**: [Project Overview](01-overview.md)
- **Architecture**: [System Architecture](03-architecture.md)
- **Advanced Usage**: [Core Mechanisms](04-core-mechanisms.md)
- **API Reference**: [API Documentation](06-api-reference.md)

---

*This quick start guide covers the essential steps to get CodeViewX running. For more detailed information, please refer to the other documentation sections.*