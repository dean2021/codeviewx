# CodeViewX

> AI 驱动的代码文档生成器

中文 | [English](README.md)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/dean2021/codeviewx)

CodeViewX 使用 AI（Anthropic Claude + DeepAgents + LangChain）自动分析您的代码库并生成专业的技术文档。

## 功能特性

- 🤖 AI 智能代码分析与文档生成
- 📝 生成完整文档体系（8个章节：项目概览、快速开始、系统架构、核心机制、数据模型、API参考、开发指南、测试文档）
- 🌐 多语言支持（中文、英文、日文、韩文、法文、德文、西班牙文、俄文）
- 🖥️ 内置 Web 服务器用于浏览文档
- ⚡ 集成 ripgrep 实现快速代码搜索

## 安装

```bash
# 安装 CodeViewX
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
pip install -e .

# 安装 ripgrep
brew install ripgrep  # macOS
# sudo apt install ripgrep  # Ubuntu/Debian

# 配置 API 密钥
export ANTHROPIC_API_KEY='your-api-key-here'
```

获取 API 密钥：访问 [Anthropic Console](https://console.anthropic.com/)

## 使用方法

**命令行：**
```bash
# 为当前目录生成文档
codeviewx

# 指定项目和语言
codeviewx -w /path/to/project -l Chinese -o docs

# 浏览文档
codeviewx --serve -o docs
```

**Python API：**
```python
from codeviewx import generate_docs, start_document_web_server

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese"
)

# 启动 Web 服务器
start_document_web_server("docs")
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码质量
black codeviewx/
flake8 codeviewx/
```

## 贡献

欢迎贡献！详情请参阅[贡献指南](CONTRIBUTING.zh.md)。

## 许可证

GNU General Public License v3.0 - 详见 [LICENSE](LICENSE) 文件。

## 致谢

基于 [Anthropic Claude](https://www.anthropic.com/)、[DeepAgents](https://github.com/langchain-ai/deepagents)、[LangChain](https://www.langchain.com/) 和 [ripgrep](https://github.com/BurntSushi/ripgrep) 构建。

---

⭐ 如果这个项目对您有帮助，请给个星标！
