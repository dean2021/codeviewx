# CodeViewX

> AI 驱动的代码文档生成器

中文 | [English](README.md)

[![PyPI version](https://img.shields.io/pypi/v/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![Python Version](https://img.shields.io/pypi/pyversions/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://img.shields.io/pypi/dm/codeviewx.svg)](https://pypi.org/project/codeviewx/)

CodeViewX 使用 AI（Anthropic Claude + DeepAgents + LangChain）自动分析您的代码库并生成专业的技术文档。

## ✨ 核心特性

- 🤖 **AI 智能分析**：自动理解代码结构和业务逻辑
- 📝 **完整文档体系**：生成 8 个标准章节（概览、快速开始、架构、核心机制、数据模型、API 参考、开发指南、测试）
- 🌐 **多语言支持**：支持中文、英文、日文、韩文、法文、德文、西班牙文、俄文
- 🖥️ **文档浏览器**：内置 Web 服务器，优雅展示文档
- ⚡ **快速搜索**：使用 DeepAgents 内置代码搜索工具

## 📦 快速开始

### 安装

```bash
# 安装 CodeViewX
pip install codeviewx

# 配置 API 密钥
export ANTHROPIC_AUTH_TOKEN='your-api-key-here'
export ANTHROPIC_BASE_URL='https://api.anthropic.com/v1'
```

获取 API 密钥：访问 [Anthropic Console](https://console.anthropic.com/)

### 基本使用

```bash
# 为当前目录生成文档
codeviewx

# 指定项目路径和语言
codeviewx -w /path/to/project -l Chinese -o docs

# 启动文档浏览器
codeviewx --serve -o docs
```

### Python API

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

## 📚 文档

完整文档请访问 [docs/zh](docs/zh/) 目录：

- [📖 项目概览](docs/zh/01-overview.md) - 技术栈、项目结构详解
- [🚀 快速开始](docs/zh/02-quickstart.md) - 详细安装和配置指南
- [🏗️ 系统架构](docs/zh/03-architecture.md) - 架构设计和组件说明
- [⚙️ 核心机制](docs/zh/04-core-mechanisms.md) - 深入理解工作原理
- [📊 数据模型](docs/zh/05-data-models.md) - 数据结构和流程
- [🔌 API 参考](docs/zh/06-api-reference.md) - 完整 API 文档
- [👨‍💻 开发指南](docs/zh/07-development-guide.md) - 开发和贡献指南
- [🧪 测试文档](docs/zh/08-testing.md) - 测试策略和用例

## 🔧 常见问题

遇到问题？查看[详细文档](docs/zh/02-quickstart.md#常见问题)获取帮助。

**快速提示：**
- API 密钥错误？确保正确设置 `ANTHROPIC_AUTH_TOKEN` 环境变量
- 搜索功能异常？升级 `deepagents` 并重新安装 CodeViewX 依赖
- 更多问题？查看 [docs/zh](docs/zh/) 完整文档

## 🤝 贡献

欢迎贡献！详情请参阅[贡献指南](CONTRIBUTING.zh.md)。

## 📄 许可证

GNU General Public License v3.0 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

基于 [Anthropic Claude](https://www.anthropic.com/)、[DeepAgents](https://github.com/langchain-ai/deepagents) 和 [LangChain](https://www.langchain.com/) 构建。

---

⭐ 如果这个项目对您有帮助，请给个星标！
