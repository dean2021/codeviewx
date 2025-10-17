# CodeViewX

> AI 驱动的代码文档生成器，基于 DeepAgents 和 LangChain

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

CodeViewX 是一个智能的代码文档生成工具，它使用 AI 技术深入分析您的代码库，自动生成全面、专业的技术文档。

## ✨ 特性

- 🤖 **AI 驱动** - 基于 DeepAgents 和 LangChain 的智能分析
- 📝 **完整文档** - 生成项目概览、架构图、核心机制等多维度文档
- 🌐 **Web 服务器** - 内置文档浏览服务器，美观的 Markdown 渲染
- 🔧 **命令行工具** - 简单易用的 CLI 接口
- 🐍 **Python API** - 可作为库集成到您的项目中
- 🚀 **快速搜索** - 集成 ripgrep 实现超快代码搜索
- 📦 **标准包** - 符合 PyPI 规范，可通过 pip 安装
- ⚡ **优化提示词** - 精简系统提示从 33KB → 10KB，避免 API 限制

## 📦 安装

### 从源码安装（开发模式）

```bash
# 克隆项目
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# 安装包（可编辑模式，包含所有依赖）
pip install -e .

# 或安装开发依赖
pip install -e ".[dev]"
```

**注意**：安装会自动包含所有必需的依赖：
- AI 框架：`deepagents`, `langchain`, `langgraph`
- Web 服务器：`flask`, `markdown`（用于 `--serve` 功能）
- 代码搜索：`ripgrepy`

### 安装依赖工具

CodeViewX 依赖 `ripgrep` 进行快速代码搜索：

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows
choco install ripgrep

# 或使用 Scoop
scoop install ripgrep
```

### 配置 API 密钥

CodeViewX 使用 Anthropic Claude 模型（也支持其他模型）：

```bash
# 设置 Anthropic API 密钥
export ANTHROPIC_API_KEY='your-api-key-here'

# 或者设置 OpenAI API 密钥
export OPENAI_API_KEY='your-api-key-here'
```

## 🚀 快速开始

### 命令行使用

```bash
# 分析当前目录，输出到 docs/（默认显示简洁进度）
codeviewx

# 分析指定项目
codeviewx -w /path/to/project

# 自定义输出目录
codeviewx -o docs

# 显示详细日志（开发调试用）
codeviewx --verbose

# 完整配置
codeviewx -w /path/to/project -o docs --verbose

# 启动 Web 服务器查看已生成的文档（推荐）🌐
codeviewx --serve

# 指定文档目录启动服务器
codeviewx --serve -o docs

# 查看帮助信息
codeviewx --help
```

**说明：**
- 默认使用简洁进度模式，智能跟踪任务执行状态
- 使用 `--verbose` 显示完整的执行日志

### Web 服务器模式 🌐

生成文档后，可以启动内置的 Web 服务器来浏览文档：

```bash
# 启动服务器（默认 docs 目录）
codeviewx --serve

# 指定文档目录
codeviewx --serve -o docs
```

**功能特点**：
- ✅ 美观的 Markdown 渲染（支持代码高亮、表格、图表）
- ✅ 自动生成目录（TOC）
- ✅ 文件树导航
- ✅ 实时预览文档
- ✅ 支持 Mermaid 图表渲染
- 🔗 访问地址：`http://127.0.0.1:5000`
- ⏹️ 停止服务：按 `Ctrl+C`

**使用流程**：
```bash
# 1. 生成文档
codeviewx -w /path/to/project

# 2. 启动服务器查看
codeviewx --serve

# 3. 在浏览器中访问 http://127.0.0.1:5000
```

### Python API 使用

```python
from codeviewx import generate_docs

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    verbose=True
)
```

更多使用示例：

```python
from codeviewx import load_prompt, generate_docs

# 示例 1: 分析当前目录
generate_docs()

# 示例 2: 自定义路径
generate_docs(
    working_directory="/Users/user/myproject",
    output_directory="documentation"
)

# 示例 3: 只加载提示词
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/path/to/project",
    output_directory="docs"
)
```

## 📖 文档结构

生成的文档包含以下文件：

```
docs/                          # 默认输出目录
├── README.md                   # 文档索引和导航
├── 01-overview.md             # 项目概览
├── 02-quickstart.md           # 快速入门
├── 03-architecture.md         # 系统架构
├── 04-core-mechanisms.md      # 核心工作机制
├── 05-data-models.md          # 数据模型（如适用）
├── 06-api-reference.md        # API 文档（如适用）
├── 07-development-guide.md    # 开发指南
├── 08-testing.md              # 测试文档
├── 09-security.md             # 安全性分析
├── 10-performance.md          # 性能与优化
└── 11-deployment.md           # 部署运维
```

## 🏗️ 项目结构

```
codeviewx/
├── codeviewx/                 # 包目录
│   ├── __init__.py           # 包初始化
│   ├── __version__.py        # 版本信息
│   ├── cli.py                # 命令行工具
│   ├── core.py               # 核心功能
│   ├── tools/                # 工具模块
│   │   ├── command.py        # 命令执行
│   │   ├── filesystem.py     # 文件系统操作
│   │   └── search.py         # 代码搜索
│   └── prompts/              # 提示词模板
│       └── DocumentEngineer.md
├── tests/                    # 测试
├── docs/                     # 项目文档
├── examples/                 # 使用示例
├── pyproject.toml           # 包配置
├── LICENSE                  # MIT 许可证
└── README.md               # 本文件
```

## 🧪 测试

运行测试：

```bash
# 安装测试依赖
pip install pytest

# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_core.py -v

# 运行并显示覆盖率
pip install pytest-cov
pytest --cov=codeviewx --cov-report=html
```

## 🔧 开发

```bash
# 克隆项目
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"
```

## 🤝 贡献

欢迎贡献！

### 贡献流程

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 GPL-3.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

### 这意味着：

✅ **你可以：**
- 自由使用、研究、修改和分发
- 用于个人和商业项目
- 提供基于此的服务（SaaS）

⚠️ **但必须：**
- 保持相同的GPL-3.0许可证
- 公开修改后的源代码
- 保留版权和许可声明

❌ **不可以：**
- 将修改后的代码闭源
- 用专有许可证重新发布

## 🙏 致谢

- [DeepAgents](https://github.com/langchain-ai/deepagents) - 强大的 AI Agent 框架
- [LangChain](https://github.com/langchain-ai/langchain) - AI 应用开发框架
- [ripgrep](https://github.com/BurntSushi/ripgrep) - 超快的代码搜索工具
- [Anthropic Claude](https://www.anthropic.com) - 优秀的 AI 模型

## 📮 联系方式

- GitHub Issues: [https://github.com/dean2021/codeviewx/issues](https://github.com/dean2021/codeviewx/issues)
- Email: dean@csoio.com

---

⭐ 如果这个项目对您有帮助，请给个星标！
