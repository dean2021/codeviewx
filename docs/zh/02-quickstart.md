# 快速开始指南

## 概述

本指南将帮助您快速上手 CodeViewX，从安装到生成第一个项目文档。CodeViewX 提供了多种使用方式，包括命令行工具、Python API 和 Web 服务器模式。

## 安装指南

### 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows, macOS, Linux
- **外部工具**: ripgrep (用于代码搜索)

### 步骤 1: 安装 ripgrep

CodeViewX 依赖 ripgrep 进行高性能代码搜索：

#### macOS
```bash
brew install ripgrep
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ripgrep
```

#### Windows
```bash
# 使用 Chocolatey
choco install ripgrep

# 或使用 Scoop
scoop install ripgrep
```

#### 验证安装
```bash
rg --version
```

### 步骤 2: 安装 CodeViewX

#### 从源码安装（推荐）
```bash
# 克隆项目
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# 安装包（开发模式）
pip install -e .

# 或者安装包含开发依赖的完整版本
pip install -e ".[dev]"
```

#### 从 PyPI 安装（未来版本）
```bash
pip install codeviewx
```

### 步骤 3: 配置 API 密钥

CodeViewX 支持多种 AI 模型，需要配置相应的 API 密钥：

#### Anthropic Claude（推荐）
```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

#### OpenAI GPT
```bash
export OPENAI_API_KEY='your-openai-api-key'
```

#### Windows 环境变量设置
```cmd
set ANTHROPIC_API_KEY=your-anthropic-api-key
```

## 快速开始

### 方式 1: 命令行工具

#### 基本使用
```bash
# 分析当前目录，生成文档
codeviewx

# 分析指定项目
codeviewx -w /path/to/your/project

# 自定义输出目录
codeviewx -o documentation

# 完整配置示例
codeviewx -w /path/to/project -o docs --verbose
```

#### 常用参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `-w, --working-dir` | 指定项目目录 | `-w ./my-project` |
| `-o, --output-dir` | 指定输出目录 | `-o docs` |
| `-l, --language` | 指定文档语言 | `-l Chinese` |
| `--verbose` | 显示详细日志 | `--verbose` |
| `--serve` | 启动 Web 服务器 | `--serve` |

#### 实际示例
```bash
# 分析 Python 项目并生成中文文档
codeviewx -w ./my-python-app -l Chinese -o docs --verbose

# 生成文档后立即启动服务器查看
codeviewx -w ./my-project && codeviewx --serve -o docs
```

### 方式 2: Python API

#### 基础使用
```python
from codeviewx import generate_docs

# 分析当前目录
generate_docs()

# 分析指定项目
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese",
    verbose=True
)
```

#### 高级使用
```python
from codeviewx import load_prompt, generate_docs

# 自定义提示词参数
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English"
)

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="documentation",
    doc_language="Chinese",
    recursion_limit=1000,
    verbose=True
)
```

### 方式 3: Web 服务器模式

#### 启动服务器
```bash
# 使用默认设置启动服务器
codeviewx --serve

# 指定文档目录启动
codeviewx --serve -o docs

# 分析完成后自动启动服务器
codeviewx -w ./project && codeviewx --serve -o docs
```

#### 访问文档
- 打开浏览器访问: `http://127.0.0.1:5000`
- 享受美观的 Markdown 渲染和文件树导航
- 按 `Ctrl+C` 停止服务器

## 使用场景示例

### 场景 1: 分析现有项目

假设您有一个 Python Web 项目：

```bash
# 项目结构
my-project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── views.py
├── tests/
├── requirements.txt
└── README.md

# 生成文档
codeviewx -w ./my-project -o tech-docs -l Chinese --verbose

# 查看结果
codeviewx --serve -o tech-docs
```

**生成的文档结构**：
```
tech-docs/
├── README.md           # 文档总览
├── 01-overview.md      # 项目概览
├── 02-quickstart.md    # 快速开始
├── 03-architecture.md  # 架构设计
├── 04-core-mechanisms.md  # 核心机制
└── ...
```

### 场景 2: 集成到 CI/CD

在 GitHub Actions 中自动生成文档：

```yaml
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
        python-version: '3.9'
    
    - name: Install ripgrep
      run: sudo apt install ripgrep
    
    - name: Install CodeViewX
      run: |
        git clone https://github.com/dean2021/codeviewx.git
        cd codeviewx
        pip install -e .
    
    - name: Generate docs
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        codeviewx -w . -o docs --verbose
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
```

### 场景 3: 批量处理多个项目

```python
import os
from codeviewx import generate_docs

def batch_analyze_projects(projects_dir, output_base_dir):
    """批量分析多个项目"""
    for project_name in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project_name)
        
        if os.path.isdir(project_path):
            output_dir = os.path.join(output_base_dir, f"{project_name}-docs")
            
            print(f"正在分析项目: {project_name}")
            generate_docs(
                working_directory=project_path,
                output_directory=output_dir,
                doc_language="Chinese",
                verbose=False
            )
            print(f"✓ 完成: {project_name} -> {output_dir}")

# 使用示例
batch_analyze_projects("./projects", "./generated-docs")
```

## 配置选项详解

### 语言支持

CodeViewX 支持多种文档语言：

| 语言 | 代码 | 自动检测 |
|------|------|----------|
| 中文 | Chinese | zh-* |
| 英文 | English | en-* |
| 日文 | Japanese | ja-* |
| 韩文 | Korean | ko-* |
| 法文 | French | fr-* |
| 德文 | German | de-* |
| 西班牙文 | Spanish | es-* |
| 俄文 | Russian | ru-* |

### 高级配置

#### 递归限制
```bash
# 控制 Agent 递归深度（默认 1000）
codeviewx --recursion-limit 500
```

#### 日志级别
```bash
# 显示详细日志（开发调试用）
codeviewx --verbose

# 静默模式（默认）
codeviewx
```

## 常见问题

### Q: ripgrep 安装失败怎么办？

**A**: 根据不同系统选择安装方式：

```bash
# macOS 使用 Homebrew
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# CentOS/RHEL
sudo yum install ripgrep

# Windows 下载二进制文件
# https://github.com/BurntSushi/ripgrep/releases
```

### Q: API 密钥如何配置？

**A**: 支持多种配置方式：

```bash
# 环境变量（推荐）
export ANTHROPIC_API_KEY="your-key"

# 临时设置
ANTHROPIC_API_KEY="your-key" codeviewx

# Windows
set ANTHROPIC_API_KEY=your-key
```

### Q: 生成速度太慢怎么办？

**A**: 优化建议：

1. **使用精简提示词**：CodeViewX 已优化提示词大小
2. **限制递归深度**：`--recursion-limit 500`
3. **关闭详细日志**：不使用 `--verbose`
4. **分析小项目**：先在小项目上测试

### Q: 如何处理大型项目？

**A**: 大型项目处理策略：

```bash
# 分析特定目录
codeviewx -w ./src -o src-docs

# 分模块分析
codeviewx -w ./modules/core -o core-docs
codeviewx -w ./modules/api -o api-docs

# 使用文件类型过滤
#（需要修改提示词模板）
```

### Q: 生成的文档不准确怎么办？

**A**: 提高文档质量的方法：

1. **使用详细日志**：`--verbose` 查看分析过程
2. **检查代码质量**：确保代码结构清晰
3. **提供 README**：项目根目录的 README.md 会提供上下文
4. **手动调整**：生成后可以手动编辑文档

## 性能优化

### 提高分析速度

1. **使用 SSD**：文件读取更快
2. **增加内存**：AI 处理需要内存
3. **网络优化**：稳定的网络连接到 API 服务
4. **缓存机制**：重复分析相同项目时会更快

### 减少 API 调用

1. **精简提示词**：CodeViewX 已使用 10KB 精简版本
2. **批量处理**：一次分析整个项目而非逐个文件
3. **合理限制**：设置适当的递归限制

## 下一步

- 阅读 [03-architecture.md](03-architecture.md) 了解系统架构
- 查看 [04-core-mechanisms.md](04-core-mechanisms.md) 深入理解核心机制
- 参考 [07-development-guide.md](07-development-guide.md) 参与项目开发

## 获取帮助

- **GitHub Issues**: [项目问题反馈](https://github.com/dean2021/codeviewx/issues)
- **文档**: [完整技术文档](README.md)
- **示例**: [examples/](../examples/) 目录包含更多使用示例

---

**提示**: 如果您遇到任何问题，请先检查是否按照上述步骤正确安装了所有依赖，特别是 ripgrep 工具和 API 密钥配置。