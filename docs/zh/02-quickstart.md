# 快速开始指南

## 概述

本指南将帮助您快速安装、配置和使用 CodeViewX 生成项目文档。CodeViewX 是一个基于 AI 的代码文档生成工具，支持多种编程语言和项目类型。

## 系统要求

### 基本要求

- **Python 版本**: 3.8 或更高版本
- **操作系统**: Windows, macOS, Linux
- **内存**: 至少 4GB RAM
- **网络**: 需要访问 Anthropic API

### 外部依赖

- **ripgrep**: 高性能代码搜索工具（必需）

## 安装步骤

### 1. 安装 Python

确保您的系统已安装 Python 3.8+：

```bash
# 检查 Python 版本
python --version
# 或
python3 --version
```

如果未安装，请访问 [Python 官网](https://www.python.org/downloads/) 下载安装。

### 2. 安装 ripgrep

ripgrep 是一个高性能的代码搜索工具，CodeViewX 依赖它进行代码分析：

#### macOS
```bash
brew install ripgrep
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ripgrep
```

#### Windows
```powershell
# 使用 Scoop
scoop install ripgrep

# 或使用 Chocolatey
choco install ripgrep

# 或手动下载
# 访问 https://github.com/BurntSushi/ripgrep/releases
```

#### 验证安装
```bash
rg --version
```

### 3. 安装 CodeViewX

使用 pip 安装 CodeViewX：

```bash
pip install codeviewx
```

或从源码安装最新版本：

```bash
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
pip install -e .
```

### 4. 验证安装

```bash
codeviewx --version
```

## 配置设置

### 1. 获取 Anthropic API 密钥

CodeViewX 使用 Anthropic Claude 模型生成文档：

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册/登录账户
3. 创建新的 API 密钥
4. 复制生成的密钥

### 2. 配置环境变量

设置 API 密钥和基础 URL：

```bash
# 设置 API 密钥
export ANTHROPIC_AUTH_TOKEN='your-api-key-here'

# 设置 API 基础 URL（可选，默认为官方地址）
export ANTHROPIC_BASE_URL='https://api.anthropic.com/v1'
```

#### 持久化配置

**Linux/macOS** (添加到 `~/.bashrc` 或 `~/.zshrc`):
```bash
echo 'export ANTHROPIC_AUTH_TOKEN="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows** (PowerShell):
```powershell
# 临时设置
$env:ANTHROPIC_AUTH_TOKEN="your-api-key-here"

# 永久设置
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "your-api-key-here", "User")
```

### 3. 可选配置

```bash
# 自定义 API 端点（如使用代理）
export ANTHROPIC_BASE_URL='https://your-proxy.com/v1'

# 设置默认文档语言
export CODEVIEWX_LANGUAGE='Chinese'
```

## 基本使用

### 1. 为当前项目生成文档

```bash
# 在项目根目录执行
codeviewx
```

这将：
- 分析当前目录的代码
- 自动检测项目语言
- 生成文档到 `docs/` 目录
- 使用默认语言（中文）

### 2. 指定项目和输出目录

```bash
# 分析指定项目
codeviewx -w /path/to/your/project

# 指定输出目录
codeviewx -w /path/to/project -o /path/to/output

# 完整示例
codeviewx -w ./my-project -o ./docs -l English
```

### 3. 选择文档语言

支持的语言：`Chinese`, `English`, `Japanese`, `Korean`, `French`, `German`, `Spanish`, `Russian`

```bash
# 生成中文文档
codeviewx -l Chinese

# 生成英文文档
codeviewx -l English

# 生成日文文档
codeviewx -l Japanese
```

### 4. 启动文档服务器

生成文档后，启动 Web 服务器浏览文档：

```bash
# 启动服务器（默认 docs 目录）
codeviewx --serve

# 指定文档目录
codeviewx --serve -o /path/to/docs
```

服务器将在 `http://127.0.0.1:5000` 启动。

## 命令行参数详解

### 完整参数列表

```bash
codeviewx [选项]

选项:
  -v, --version              显示版本信息
  -w, --working-dir DIR      项目工作目录 (默认: 当前目录)
  -o, --output-dir DIR       文档输出目录 (默认: docs)
  -l, --language LANG        文档语言 (支持: Chinese, English, Japanese, etc.)
  --ui-lang LANG             界面语言 (en/zh)
  --recursion-limit NUM      Agent 递归限制 (默认: 1000)
  --verbose                  显示详细日志
  --base-url URL             自定义 API 基础 URL
  --serve                    启动文档 Web 服务器
  -h, --help                 显示帮助信息
```

### 常用使用场景

#### 场景1: 分析现有项目
```bash
# 分析 Python 项目，生成英文文档
codeviewx -w ./python-project -l English -o ./docs

# 详细模式，显示所有执行步骤
codeviewx -w ./project --verbose
```

#### 场景2: 开发和调试
```bash
# 使用中文界面，英文文档，详细日志
codeviewx --ui-lang zh -l English --verbose

# 设置递归限制（适用于大型项目）
codeviewx --recursion-limit 2000
```

#### 场景3: 自定义 API 配置
```bash
# 使用自定义 API 端点
codeviewx --base-url https://your-proxy.com/v1

# 结合所有选项
codeviewx -w ./project -o ./output -l Chinese --base-url https://api.example.com --verbose
```

## Python API 使用

除了命令行工具，CodeViewX 也提供 Python API：

### 基本用法

```python
from codeviewx import generate_docs, start_document_web_server

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese",
    verbose=True
)

# 启动 Web 服务器
start_document_web_server("docs")
```

### 高级配置

```python
from codeviewx import generate_docs
import os

# 设置环境变量
os.environ['ANTHROPIC_AUTH_TOKEN'] = 'your-api-key'
os.environ['ANTHROPIC_BASE_URL'] = 'https://api.anthropic.com/v1'

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English",
    ui_language="en",
    recursion_limit=1500,
    verbose=True,
    base_url="https://custom-api.example.com"
)
```

## 常见问题解决

### 1. API 密钥问题

**错误信息**: `ANTHROPIC_AUTH_TOKEN environment variable not found`

**解决方案**:
```bash
# 检查环境变量
echo $ANTHROPIC_AUTH_TOKEN

# 重新设置
export ANTHROPIC_AUTH_TOKEN='your-api-key-here'

# 验证设置
codeviewx --version
```

### 2. ripgrep 未找到

**错误信息**: `rg: command not found`

**解决方案**:
```bash
# 检查 ripgrep 是否安装
which rg

# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt-get install ripgrep

# 验证安装
rg --version
```

### 3. Python 版本不兼容

**错误信息**: `Python 3.8+ is required`

**解决方案**:
```bash
# 检查 Python 版本
python --version

# 使用 pyenv 管理 Python 版本
pyenv install 3.9.16
pyenv global 3.9.16

# 或使用 conda
conda create -n codeviewx python=3.9
conda activate codeviewx
```

### 4. 网络连接问题

**错误信息**: `Connection timeout` 或 `SSL error`

**解决方案**:
```bash
# 设置代理
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 使用自定义 API 端点
codeviewx --base-url https://your-proxy.com/v1

# 增加超时时间
codeviewx --verbose  # 查看详细错误信息
```

### 5. 权限问题

**错误信息**: `Permission denied`

**解决方案**:
```bash
# 检查目录权限
ls -la /path/to/project

# 修改权限
chmod 755 /path/to/project

# 使用用户目录
codeviewx -w ~/my-project -o ~/docs
```

## 最佳实践

### 1. 项目准备

在生成文档前，确保项目结构清晰：

```
project/
├── README.md           # 项目说明
├── requirements.txt    # Python 依赖
├── setup.py/pyproject.toml  # 项目配置
├── src/               # 源代码
├── tests/             # 测试文件
├── docs/              # 现有文档（可选）
└── examples/          # 示例代码
```

### 2. 文档优化

- **添加 README.md**: 提供项目概述和背景
- **完善配置文件**: 确保依赖信息完整
- **代码注释**: 添加关键函数和类的注释
- **类型提示**: 使用 Python 类型提示提高可读性

### 3. 性能优化

对于大型项目：

```bash
# 增加递归限制
codeviewx --recursion-limit 2000

# 分模块分析
codeviewx -w ./src/core -o ./docs/core
codeviewx -w ./src/utils -o ./docs/utils

# 使用详细模式监控进度
codeviewx --verbose
```

### 4. 文档维护

- **定期更新**: 代码变更后重新生成文档
- **版本控制**: 将生成的文档纳入 Git 管理
- **自定义模板**: 根据需求修改提示词模板

## 下一步

安装配置完成后，您可以：

1. [了解系统架构](03-architecture.md) - 深入理解 CodeViewX 的工作原理
2. [查看核心机制](04-core-mechanisms.md) - 了解文档生成的详细流程
3. [阅读开发指南](07-development-guide.md) - 学习如何贡献代码

---

💡 **提示**: 遇到问题时，使用 `--verbose` 参数查看详细的执行日志，有助于定位问题原因。