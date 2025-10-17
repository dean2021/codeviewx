# CodeViewX

> AI 驱动的智能代码文档生成器

中文 | [English](README.md)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/dean2021/codeviewx)

CodeViewX 是一个智能代码文档生成工具，基于 Anthropic Claude 和 DeepAgents 框架，自动分析代码库并生成专业的技术文档。

## 核心特性

- 🤖 **AI 智能分析**：基于 Anthropic Claude、DeepAgents 和 LangChain 框架
- 📝 **完整文档体系**：自动生成 8 个核心章节的技术文档
- 🌐 **多语言支持**：支持 8 种语言（中文、英文、日文、韩文、法文、德文、西班牙文、俄文）
- 🖥️ **内置 Web 服务器**：美观的文档浏览界面，支持 Mermaid 图表
- ⚡ **高性能搜索**：集成 ripgrep 实现快速代码搜索

## 系统要求

- Python 3.8+
- pip 包管理器
- ripgrep (rg) 代码搜索工具
- Anthropic API Key

## 安装

### 1. 克隆项目
```bash
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
```

### 2. 安装依赖
```bash
# 开发模式安装（推荐）
pip install -e .

# 或标准安装
pip install .
```

### 3. 安装 ripgrep
```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows
choco install ripgrep
```

### 4. 配置 API 密钥
```bash
# 设置环境变量
export ANTHROPIC_API_KEY='your-api-key-here'

# 或添加到 ~/.bashrc 或 ~/.zshrc
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

获取 API Key：访问 [Anthropic Console](https://console.anthropic.com/)

## 快速开始

### 命令行使用

```bash
# 分析当前目录并生成文档
codeviewx

# 指定项目路径和输出目录
codeviewx -w /path/to/project -o docs

# 生成英文文档
codeviewx -w /path/to/project -l English

# 启动文档浏览服务器
codeviewx --serve -o docs
```

### Python API

```python
from codeviewx import generate_docs

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese"
)

# 启动 Web 服务器
from codeviewx import start_document_web_server
start_document_web_server("docs")
```

## 生成的文档结构

```
docs/
├── 01-项目概览.md
├── 02-快速开始.md
├── 03-系统架构.md
├── 04-核心机制.md
├── 05-数据模型.md
├── 06-API参考.md
├── 07-开发指南.md
├── 08-测试文档.md
└── README.md
```

## 开发

### 安装开发依赖
```bash
pip install -e ".[dev]"
```

### 运行测试
```bash
pytest
pytest --cov=codeviewx --cov-report=html
```

### 代码质量
```bash
black codeviewx/    # 格式化
flake8 codeviewx/   # 代码检查
mypy codeviewx/     # 类型检查
```

## 贡献

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.zh.md)了解以下详情：

- 如何提交问题和功能请求
- 开发环境设置和工作流程
- 编码标准和最佳实践
- 测试指南
- Pull Request 流程

英文版本请参阅 [Contributing Guide](CONTRIBUTING.md)。

## 项目结构

```
codeviewx/
├── codeviewx/              # 主包
│   ├── cli.py             # 命令行接口
│   ├── core.py            # 核心 API
│   ├── generator.py       # 文档生成器
│   ├── server.py          # Web 服务器
│   ├── prompt.py          # 提示词管理
│   ├── i18n.py            # 国际化
│   ├── language.py        # 语言检测
│   ├── prompts/           # 提示词模板
│   ├── tools/             # 工具模块
│   ├── tpl/               # HTML模板
│   └── static/            # 静态资源
├── tests/                 # 测试文件
├── examples/              # 示例代码
└── pyproject.toml         # 项目配置
```

## 许可证

本项目采用 GNU General Public License v3.0 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

- 📧 Email: dean@csoio.com
- 🐙 GitHub: [@dean2021](https://github.com/dean2021)
- 🔗 项目主页: [CodeViewX](https://github.com/dean2021/codeviewx)

## 致谢

感谢以下优秀的开源项目：

- [Anthropic Claude](https://www.anthropic.com/) - AI 模型
- [DeepAgents](https://github.com/langchain-ai/deepagents) - AI Agent 框架
- [LangChain](https://www.langchain.com/) - LLM 应用框架
- [LangGraph](https://langchain-ai.github.io/langgraph/) - 工作流编排
- [ripgrep](https://github.com/BurntSushi/ripgrep) - 代码搜索

---

⭐ 如果这个项目对您有帮助，请给个星标！

