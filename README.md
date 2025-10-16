# CodeViewX

> AI 驱动的代码文档生成器，基于 DeepAgents 和 LangChain

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

CodeViewX 是一个智能的代码文档生成工具，它使用 AI 技术深入分析您的代码库，自动生成全面、专业的技术文档。

## ✨ 特性

- 🤖 **AI 驱动** - 基于 DeepAgents 和 LangChain 的智能分析
- 📝 **完整文档** - 生成项目概览、架构图、核心机制等多维度文档
- 🔧 **命令行工具** - 简单易用的 CLI 接口
- 🐍 **Python API** - 可作为库集成到您的项目中
- 🚀 **快速搜索** - 集成 ripgrep 实现超快代码搜索
- 📦 **标准包** - 符合 PyPI 规范，可通过 pip 安装

## 📦 安装

### 从源码安装（开发模式）

```bash
# 克隆项目
git clone https://github.com/yourusername/codeviewx.git
cd codeviewx

# 安装包（可编辑模式）
pip install -e .

# 或安装开发依赖
pip install -e ".[dev]"
```

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
# 分析当前目录，输出到 .wiki/
codeviewx

# 分析指定项目
codeviewx -w /path/to/project

# 自定义输出目录
codeviewx -o docs

# 显示详细日志
codeviewx --verbose

# 完整配置
codeviewx -w /path/to/project -o docs --verbose
```

查看帮助信息：

```bash
codeviewx --help
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
    output_directory=".wiki"
)
```

## 📖 文档结构

生成的文档包含以下文件：

```
.wiki/                          # 默认输出目录
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

### 设置开发环境

```bash
# 克隆项目
git clone https://github.com/yourusername/codeviewx.git
cd codeviewx

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"

# 安装 pre-commit hooks（可选）
pre-commit install
```

### 代码格式化

```bash
# 使用 black 格式化代码
black codeviewx/ tests/

# 使用 isort 排序导入
isort codeviewx/ tests/

# 运行 flake8 检查
flake8 codeviewx/ tests/
```

### 构建包

```bash
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 检查包
twine check dist/*
```

## 📚 更多文档

- [使用示例](docs/usage-examples.md) - 详细的使用示例
- [PromptTemplate 指南](docs/prompt-template-guide.md) - 提示词模板使用
- [重构方案](docs/refactoring-plan.md) - 项目重构文档

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)（待添加）了解详情。

### 贡献流程

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [DeepAgents](https://github.com/deepagents/deepagents) - 强大的 AI Agent 框架
- [LangChain](https://github.com/langchain-ai/langchain) - AI 应用开发框架
- [ripgrep](https://github.com/BurntSushi/ripgrep) - 超快的代码搜索工具
- [Anthropic Claude](https://www.anthropic.com) - 优秀的 AI 模型

## 📮 联系方式

- GitHub Issues: [https://github.com/yourusername/codeviewx/issues](https://github.com/yourusername/codeviewx/issues)
- Email: your.email@example.com

## 🗺️ 路线图

- [ ] 支持更多 AI 模型（OpenAI GPT-4, Google Gemini 等）
- [ ] 添加配置文件支持（`.codeviewx.yaml`）
- [ ] 支持增量更新文档
- [ ] 添加文档模板系统
- [ ] 支持多语言文档生成
- [ ] 集成 GitHub Actions
- [ ] Web 界面
- [ ] 文档版本管理

## 📊 项目状态

- **版本**: 0.1.0
- **状态**: Alpha（活跃开发中）
- **Python**: 3.8+
- **许可证**: MIT

---

⭐ 如果这个项目对您有帮助，请给个星标！
