# 快速开始

本指南将帮助您快速安装、配置和使用 CodeViewX 生成项目文档。

## 系统要求

### 基本要求
- **Python 3.8+**：支持 3.8、3.9、3.10、3.11、3.12
- **pip 包管理器**：用于安装依赖
- **ripgrep (rg)**：高性能代码搜索工具
- **Anthropic API Key**：用于 AI 分析

### 操作系统支持
- **macOS**：通过 Homebrew 安装 ripgrep
- **Linux**：通过包管理器安装 ripgrep
- **Windows**：通过 Chocolatey 或 Scoop 安装 ripgrep

## 安装指南

### 1. 获取项目代码

```bash
# 克隆项目
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
```

### 2. 安装依赖

#### 方法一：开发模式安装（推荐）
```bash
# 安装项目到开发环境
pip install -e .
```

#### 方法二：标准安装
```bash
# 标准安装
pip install .
```

#### 方法三：从 PyPI 安装（未来版本）
```bash
# 直接从 PyPI 安装
pip install codeviewx
```

### 3. 安装 ripgrep

#### macOS
```bash
# 使用 Homebrew 安装
brew install ripgrep

# 验证安装
rg --version
```

#### Ubuntu/Debian
```bash
# 使用 apt 安装
sudo apt update
sudo apt install ripgrep

# 验证安装
rg --version
```

#### Windows
```bash
# 使用 Chocolatey 安装
choco install ripgrep

# 或使用 Scoop 安装
scoop install ripgrep

# 验证安装
rg --version
```

### 4. 配置 API 密钥

#### 获取 Anthropic API Key
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册或登录账户
3. 创建新的 API Key
4. 复制 API Key

#### 设置环境变量

##### 临时设置（当前会话）
```bash
# Linux/macOS
export ANTHROPIC_API_KEY='your-api-key-here'

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY='your-api-key-here'

# Windows (CMD)
set ANTHROPIC_API_KEY=your-api-key-here
```

##### 永久设置
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc (Linux/macOS)
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# 或添加到环境变量文件
echo 'ANTHROPIC_API_KEY=your-api-key-here' >> ~/.environment
```

## 基本使用

### 命令行界面

#### 分析当前目录
```bash
# 分析当前目录并生成文档（默认语言：自动检测）
codeviewx
```

#### 指定项目路径
```bash
# 分析指定项目
codeviewx -w /path/to/your/project

# 或使用 --working-dir
codeviewx --working-dir /path/to/your/project
```

#### 指定输出目录
```bash
# 输出到指定目录
codeviewx -w /path/to/project -o /path/to/output

# 或使用 --output-dir
codeviewx --working-dir /path/to/project --output-dir /path/to/output
```

#### 指定文档语言
```bash
# 生成英文文档
codeviewx -l English

# 生成中文文档
codeviewx -l Chinese

# 支持的语言
# Chinese, English, Japanese, Korean, French, German, Spanish, Russian
```

#### 完整配置示例
```bash
# 完整配置：指定项目、输出目录、语言、详细日志
codeviewx \
  --working-dir /path/to/project \
  --output-dir docs \
  --language Chinese \
  --verbose
```

### Python API

#### 基本用法
```python
from codeviewx import generate_docs

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese"
)
```

#### 高级用法
```python
from codeviewx import generate_docs, start_document_web_server

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English",
    ui_language="en",
    recursion_limit=1000,
    verbose=True
)

# 启动 Web 服务器
start_document_web_server("docs")
```

## 文档浏览

### 启动 Web 服务器
```bash
# 启动文档浏览服务器（默认端口 5000）
codeviewx --serve

# 指定文档目录
codeviewx --serve -o docs

# 指定文档目录和输出目录
codeviewx --serve --output-dir /path/to/docs
```

### 访问文档
1. 启动服务器后，在浏览器中访问：
   - 地址：`http://127.0.0.1:5000`
   - 主页显示文档列表和导航

2. 使用文件树导航：
   - 左侧显示所有生成的文档
   - 点击文件名即可浏览

3. 功能特性：
   - 支持 Markdown 渲染
   - 自动生成目录（TOC）
   - 支持 Mermaid 图表
   - 响应式设计

## 常用命令示例

### 1. 快速开始
```bash
# 最简单的使用方式
codeviewx

# 查看帮助信息
codeviewx --help
```

### 2. 开发环境分析
```bash
# 分析当前 Python 项目
codeviewx -l Chinese -o docs

# 分析 JavaScript 项目
codeviewx -w /path/to/js-project -l English -o api-docs
```

### 3. 文档服务
```bash
# 生成文档并启动服务
codeviewx -w . -o docs
codeviewx --serve -o docs
```

### 4. 调试模式
```bash
# 显示详细日志
codeviewx --verbose

# 限制递归深度（避免无限循环）
codeviewx --recursion-limit 500
```

## 配置选项详解

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 | 示例 |
|------|------|------|--------|------|
| `--working-dir` | `-w` | 项目工作目录 | 当前目录 | `-w /path/to/project` |
| `--output-dir` | `-o` | 文档输出目录 | `docs` | `-o /path/to/output` |
| `--language` | `-l` | 文档语言 | 自动检测 | `-l Chinese` |
| `--ui-lang` | - | 界面语言 | 自动检测 | `--ui-lang zh` |
| `--serve` | - | 启动 Web 服务器 | False | `--serve` |
| `--verbose` | - | 显示详细日志 | False | `--verbose` |
| `--recursion-limit` | - | Agent 递归限制 | 1000 | `--recursion-limit 500` |
| `--version` | `-v` | 显示版本号 | - | `-v` |

### 支持的语言

#### 文档语言 (`--language`)
- `Chinese` - 中文（简体）
- `English` - 英文
- `Japanese` - 日文
- `Korean` - 韩文
- `French` - 法文
- `German` - 德文
- `Spanish` - 西班牙文
- `Russian` - 俄文

#### 界面语言 (`--ui-lang`)
- `en` - 英文界面
- `zh` - 中文界面

## 故障排除

### 常见问题

#### 1. ripgrep 未找到
**错误信息**：`ripgrep (rg) is not installed`

**解决方案**：
```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows
choco install ripgrep
```

#### 2. API Key 未设置
**错误信息**：`ANTHROPIC_API_KEY not found`

**解决方案**：
```bash
# 设置环境变量
export ANTHROPIC_API_KEY='your-api-key-here'

# 验证设置
echo $ANTHROPIC_API_KEY
```

#### 3. Python 版本不兼容
**错误信息**：`Python 3.8+ required`

**解决方案**：
```bash
# 检查 Python 版本
python --version

# 升级 Python（使用 pyenv）
pyenv install 3.9.0
pyenv global 3.9.0
```

#### 4. 权限问题
**错误信息**：`Permission denied`

**解决方案**：
```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

pip install -e .
```

### 调试技巧

#### 1. 使用详细日志
```bash
# 显示详细的执行过程
codeviewx --verbose
```

#### 2. 检查项目结构
```bash
# 预先检查项目目录
ls -la /path/to/project

# 使用 ripgrep 测试搜索
rg "class " /path/to/project --type py
```

#### 3. 验证配置
```bash
# 检查环境变量
env | grep ANTHROPIC

# 检查 ripgrep 安装
rg --version

# 检查 Python 环境
python -c "import codeviewx; print('OK')"
```

## 最佳实践

### 1. 项目准备
- 确保项目有清晰的目录结构
- 添加必要的配置文件（`pyproject.toml`、`requirements.txt` 等）
- 编写基本的 `README.md` 文件

### 2. 文档生成
- 对于大型项目，考虑限制分析范围
- 使用适当的文档语言设置
- 定期重新生成文档以保持同步

### 3. 文档维护
- 将生成的文档纳入版本控制
- 定期更新文档内容
- 根据项目变化调整生成参数

### 4. 团队协作
- 统一文档生成配置
- 建立文档更新流程
- 使用 CI/CD 自动化文档生成

## 下一步

完成快速开始后，您可以：

1. **阅读架构文档**：了解系统设计原理
2. **学习核心机制**：深入理解文档生成流程
3. **查看 API 参考**：掌握编程接口使用
4. **参与开发**：贡献代码和改进功能