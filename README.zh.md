# CodeViewX

> AI 驱动的代码文档生成器

中文 | [English](README.md)

[![PyPI version](https://img.shields.io/pypi/v/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![Python Version](https://img.shields.io/pypi/pyversions/codeviewx.svg)](https://pypi.org/project/codeviewx/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://img.shields.io/pypi/dm/codeviewx.svg)](https://pypi.org/project/codeviewx/)

CodeViewX 使用 AI（Anthropic Claude + DeepAgents + LangChain）自动分析您的代码库并生成专业的技术文档。

## 功能特性

- 🤖 AI 智能代码分析与文档生成
- 📝 生成完整文档体系（8个章节：项目概览、快速开始、系统架构、核心机制、数据模型、API参考、开发指南、测试文档）
- 🌐 多语言支持（中文、英文、日文、韩文、法文、德文、西班牙文、俄文）
- 🖥️ 内置 Web 服务器用于浏览文档
- ⚡ 集成 ripgrep 实现快速代码搜索

## 安装

**从 PyPI 安装（推荐）：**
```bash
# 安装 CodeViewX
pip install codeviewx

# 安装 ripgrep
brew install ripgrep  # macOS
# sudo apt install ripgrep  # Ubuntu/Debian

# 配置 API 密钥
export ANTHROPIC_API_KEY='your-api-key-here'

# 或使用提供的设置脚本（推荐）
bash scripts/setup_api_key.sh
```

**从源码安装（开发）：**
```bash
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx
pip install -e .
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

## 常见问题

### API 密钥相关错误

**Q: 提示"ANTHROPIC_API_KEY environment variable not found"怎么办？**

A: 这表示您还没有设置 Anthropic API 密钥。解决方法：

1. 从 [Anthropic Console](https://console.anthropic.com/) 获取 API 密钥
2. 设置环境变量：
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```
3. 或使用提供的设置脚本：
   ```bash
   bash scripts/setup_api_key.sh
   ```

**Q: API 密钥格式不正确怎么办？**

A: 确保您的 API 密钥以 `sk-ant-api` 开头，并且完整复制。如果问题仍然存在，请重新生成密钥。

### 改进的错误处理

CodeViewX 现在提供更友好的错误提示：

- 🔍 **自动检测**：自动验证 API 密钥格式和有效性
- 📝 **清晰提示**：具体的错误原因和解决步骤
- 🔗 **直接链接**：提供获取 API 密钥的直接链接
- 🌐 **双语支持**：中英文错误提示
- ⚙️ **设置脚本**：自动化的 API 密钥配置工具

## 贡献

欢迎贡献！详情请参阅[贡献指南](CONTRIBUTING.zh.md)。

## 许可证

GNU General Public License v3.0 - 详见 [LICENSE](LICENSE) 文件。

## 致谢

基于 [Anthropic Claude](https://www.anthropic.com/)、[DeepAgents](https://github.com/langchain-ai/deepagents)、[LangChain](https://www.langchain.com/) 和 [ripgrep](https://github.com/BurntSushi/ripgrep) 构建。

---

⭐ 如果这个项目对您有帮助，请给个星标！
