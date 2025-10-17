# CodeViewX

> AI 驱动的代码文档生成器，基于 DeepAgents 和 LangChain

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/dean2021/codeviewx/releases)

CodeViewX 是一个智能的代码文档生成工具，它使用 AI 技术深入分析您的代码库，自动生成全面、专业的技术文档。支持多语言文档生成，内置美观的 Web 文档浏览器。

**📚 完整文档：** [中文](docs/zh/README.md) | [English](docs/en/README.md)

## ✨ 特性

- 🤖 **AI 驱动** - 基于 DeepAgents 和 LangChain 的智能分析
- 📝 **完整文档** - 生成项目概览、架构图、核心机制等多维度文档
- 🌐 **Web 服务器** - 内置文档浏览服务器，美观的 Markdown 渲染（支持 Mermaid 图表）
- 🌍 **多语言支持** - 支持 8 种语言的文档生成（中文、英文、日文、韩文、法文、德文、西班牙文、俄文）
- 📊 **智能进度提示** - 实时显示文档生成进度和分析状态
- 🔧 **命令行工具** - 简单易用的 CLI 接口
- 🐍 **Python API** - 可作为库集成到您的项目中
- 🚀 **快速搜索** - 集成 ripgrep 实现超快代码搜索

## 📦 安装

```bash
# 克隆项目
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# 安装依赖
pip install -e .

# 安装 ripgrep（代码搜索工具）
brew install ripgrep  # macOS
# sudo apt install ripgrep  # Ubuntu/Debian

# 配置 API 密钥
export ANTHROPIC_API_KEY='your-api-key-here'
```

## 🚀 快速开始

```bash
# 生成文档
codeviewx -w /path/to/project -o docs

# 指定语言（支持中、英、日、韩、法、德、西、俄 8 种语言）
codeviewx -w /path/to/project -l English

# 启动 Web 服务器浏览文档
codeviewx --serve -o docs
# 访问 http://127.0.0.1:5000

# 查看本项目的文档示例
codeviewx --serve -o docs/zh  # 中文
codeviewx --serve -o docs/en  # 英文
```

### Python API

```python
from codeviewx import generate_docs

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    language="Chinese"
)
```

## 📖 生成的文档

生成的文档包含 8 个章节：项目概览、快速开始、系统架构、核心机制、数据模型、API 参考、开发指南、测试文档。

**查看文档：** [中文文档](docs/zh/) | [English](docs/en/)

## 🔧 开发

```bash
# 克隆项目
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 🤝 贡献

欢迎贡献！请 Fork 项目并提交 Pull Request。

## 📄 许可证

本项目采用 GPL-3.0 许可证。详见 [LICENSE](LICENSE) 文件。

## 📮 联系方式

- GitHub Issues: https://github.com/dean2021/codeviewx/issues
- Email: dean@csoio.com

---

⭐ 如果这个项目对您有帮助，请给个星标！
