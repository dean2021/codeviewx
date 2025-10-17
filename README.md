# CodeViewX

> AI 驱动的代码文档生成器，基于 DeepAgents 和 LangChain

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/dean2021/codeviewx/releases)

CodeViewX 是一个智能的代码文档生成工具，它使用 AI 技术深入分析您的代码库，自动生成全面、专业的技术文档。支持多语言文档生成，内置美观的 Web 文档浏览器。

---

**📚 完整技术文档：** [中文文档](docs/zh/README.md) | [English Documentation](docs/en/README.md)

---

## 📑 目录

- [✨ 特性](#-特性)
- [📦 安装](#-安装)
- [🎬 功能演示](#-功能演示)
- [🚀 快速开始](#-快速开始)
- [📖 文档结构](#-文档结构)
- [🏗️ 项目结构](#️-项目结构)
- [🧪 测试](#-测试)
- [🔧 开发](#-开发)
- [🎯 最新亮点](#-最新亮点)
- [💡 使用技巧](#-使用技巧)
- [🗺️ 路线图](#️-路线图)
- [🤝 贡献](#-贡献)
- [📄 许可证](#-许可证)
- [🙏 致谢](#-致谢)
- [📮 联系方式](#-联系方式)

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

## 🎬 功能演示

### 命令行界面

```bash
$ codeviewx -w /path/to/project

🔍 分析项目结构...
📖 read_file: pyproject.toml ✓ 119 行 | [build-system] requires = ["setuptools>=45"...
📁 list_directory: . ✓ 15 项 | codeviewx, tests, docs ... (+12)
🔎 search_code: "from deepagents" ✓ 5 处匹配 | from deepagents import Agent...

📋 任务规划:
  ✓ [完成] 分析项目结构
  ⏳ [进行中] 生成架构文档
  ⏸ [待处理] 生成 API 文档

📄 正在生成文档 (1/8): 01-overview.md
📄 正在生成文档 (2/8): 02-quickstart.md
...

✅ 文档生成完成！
📊 统计: 共生成 8 个文档文件，执行 45 个步骤
📂 输出目录: /path/to/project/docs
```

### Web 浏览器

启动 Web 服务器后，在浏览器中访问 `http://127.0.0.1:5000`：

**功能特点：**
- ✅ 左侧文件树导航，快速切换文档
- ✅ 右侧内容区域，美观的 Markdown 渲染
- ✅ 自动生成的目录（TOC），方便跳转
- ✅ 代码语法高亮，支持多种编程语言
- ✅ Mermaid 图表实时渲染（架构图、流程图、时序图等）
- ✅ 响应式设计，支持桌面和移动设备

### 文档示例

生成的文档包含丰富的内容：

**项目概览（01-overview.md）**
- 📋 项目基本信息和技术栈
- 📁 目录结构树状图
- 🔑 核心功能和特性

**系统架构（03-architecture.md）**
- 🎨 Mermaid 架构图
- 📦 模块依赖关系
- 🔄 数据流向分析

**API 文档（06-api-reference.md）**
- 📚 完整的 API 列表
- 📝 参数和返回值说明
- 💡 使用示例代码

## 🚀 快速开始

### 命令行使用

```bash
# 分析当前目录，输出到 docs/（默认显示简洁进度）
codeviewx

# 分析指定项目
codeviewx -w /path/to/project

# 自定义输出目录
codeviewx -o docs

# 指定文档语言（支持 8 种语言）
codeviewx -l English  # 英文文档
codeviewx -l Japanese  # 日文文档
codeviewx --language Chinese  # 中文文档（默认自动检测系统语言）

# 显示详细日志（开发调试用）
codeviewx --verbose

# 完整配置
codeviewx -w /path/to/project -o docs -l English --verbose

# 启动 Web 服务器查看已生成的文档（推荐）🌐
codeviewx --serve

# 指定文档目录启动服务器
codeviewx --serve -o docs

# 查看帮助信息
codeviewx --help
```

**支持的语言：**
- `Chinese` (中文) - 默认，自动检测系统语言
- `English` (英文)
- `Japanese` (日文)
- `Korean` (韩文)
- `French` (法文)
- `German` (德文)
- `Spanish` (西班牙文)
- `Russian` (俄文)

**说明：**
- 默认使用简洁进度模式，智能跟踪任务执行状态
- 使用 `--verbose` 显示完整的执行日志
- 自动检测系统语言，也可通过 `-l/--language` 参数指定

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
from codeviewx import load_prompt, generate_docs, detect_system_language

# 示例 1: 分析当前目录（自动检测系统语言）
generate_docs()

# 示例 2: 自定义路径和语言
generate_docs(
    working_directory="/Users/user/myproject",
    output_directory="documentation",
    language="English"  # 指定英文文档
)

# 示例 3: 检测系统语言
lang = detect_system_language()
print(f"检测到系统语言：{lang}")
generate_docs(language=lang)

# 示例 4: 只加载提示词
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/path/to/project",
    output_directory="docs"
)
```

---

**💡 提示：** 想了解更多详细信息？查看我们的完整技术文档：
- 📖 [中文完整文档](docs/zh/README.md) - 包含架构设计、核心机制、API 参考等
- 📖 [English Documentation](docs/en/README.md) - Architecture, mechanisms, API reference and more

---

## 📖 文档结构

本项目使用 CodeViewX 自动生成了完整的技术文档，包含中文和英文两个版本。

### 📚 中文文档（docs/zh/）

| 文档 | 说明 | 链接 |
|------|------|------|
| 📖 文档导航 | 文档索引和快速导航 | [README.md](docs/zh/README.md) |
| 01 项目概览 | 技术栈、目录结构、核心功能 | [01-overview.md](docs/zh/01-overview.md) |
| 02 快速开始 | 安装配置、基本使用、示例 | [02-quickstart.md](docs/zh/02-quickstart.md) |
| 03 系统架构 | 架构设计、模块关系、数据流 | [03-architecture.md](docs/zh/03-architecture.md) |
| 04 核心机制 | 工作原理、实现细节、流程图 | [04-core-mechanisms.md](docs/zh/04-core-mechanisms.md) |
| 05 数据模型 | 数据结构、类定义、关系图 | [05-data-models.md](docs/zh/05-data-models.md) |
| 06 API 参考 | 完整 API 文档、参数说明 | [06-api-reference.md](docs/zh/06-api-reference.md) |
| 07 开发指南 | 环境配置、贡献指南、规范 | [07-development-guide.md](docs/zh/07-development-guide.md) |
| 08 测试文档 | 测试策略、框架、覆盖率 | [08-testing.md](docs/zh/08-testing.md) |

### 📚 English Documentation (docs/en/)

| Document | Description | Link |
|----------|-------------|------|
| 📖 Documentation | Index and navigation | [README.md](docs/en/README.md) |
| 01 Overview | Tech stack, structure, features | [01-overview.md](docs/en/01-overview.md) |
| 02 Quick Start | Installation, usage, examples | [02-quickstart.md](docs/en/02-quickstart.md) |
| 03 Architecture | System design, modules, data flow | [03-architecture.md](docs/en/03-architecture.md) |
| 04 Core Mechanisms | Working principles, implementation | [04-core-mechanisms.md](docs/en/04-core-mechanisms.md) |
| 05 Data Models | Data structures, classes, diagrams | [05-data-models.md](docs/en/05-data-models.md) |
| 06 API Reference | Complete API docs, parameters | [06-api-reference.md](docs/en/06-api-reference.md) |
| 07 Development Guide | Setup, contribution, standards | [07-development-guide.md](docs/en/07-development-guide.md) |
| 08 Testing | Testing strategy, framework, coverage | [08-testing.md](docs/en/08-testing.md) |

### ✨ 文档特点

- 📊 **丰富图表** - 支持 Mermaid 架构图、流程图、类图等
- 🎨 **语法高亮** - 代码块自动高亮，支持多种编程语言
- 📑 **自动目录** - 每个文档自动生成目录（TOC）
- 🔍 **结构清晰** - 分层合理，易于导航和查找
- 🌍 **多语言版本** - 中英文对照，方便国际团队使用
- 🤖 **AI 生成** - 基于代码自动分析生成，内容全面准确

### 🌐 在线浏览

使用内置 Web 服务器浏览文档：

```bash
# 浏览中文文档
codeviewx --serve -o docs/zh

# 浏览英文文档
codeviewx --serve -o docs/en

# 访问 http://127.0.0.1:5000
```

## 🏗️ 项目结构

```
codeviewx/
├── codeviewx/                 # 包目录
│   ├── __init__.py           # 包初始化（导出 API）
│   ├── __version__.py        # 版本信息
│   ├── cli.py                # 命令行工具（Click CLI）
│   ├── core.py               # 核心功能（文档生成、语言检测）
│   ├── tools/                # 工具模块（Agent 工具集）
│   │   ├── command.py        # 命令执行工具
│   │   ├── filesystem.py     # 文件系统操作工具
│   │   └── search.py         # 代码搜索工具（ripgrep）
│   ├── prompts/              # 提示词模板
│   │   ├── DocumentEngineer.md          # 主提示词（压缩版）
│   │   ├── DocumentEngineer_compact.md  # 紧凑版
│   │   └── DocumentEngineer_original.md # 原始版
│   ├── tpl/                  # Web 模板
│   │   └── doc_detail.html   # 文档详情页模板
│   └── static/               # 静态资源
│       ├── css/              # 样式文件
│       └── README.md         # 静态文件说明
├── tests/                    # 测试套件
│   ├── test_core.py         # 核心功能测试
│   ├── test_language.py     # 语言检测测试
│   ├── test_progress.py     # 进度提示测试
│   └── test_tools.py        # 工具模块测试
├── docs/                     # 项目文档（自动生成）
│   ├── zh/                  # 中文文档
│   │   ├── README.md        # 文档导航
│   │   ├── 01-overview.md   # 项目概览
│   │   ├── 02-quickstart.md # 快速开始
│   │   └── ...              # 其他文档章节
│   └── en/                  # 英文文档
│       ├── README.md        # Documentation index
│       ├── 01-overview.md   # Overview
│       ├── 02-quickstart.md # Quick start
│       └── ...              # Other sections
├── examples/                 # 使用示例
│   ├── basic_usage.py       # 基础用法
│   ├── language_demo.py     # 多语言示例
│   └── progress_demo.py     # 进度显示示例
├── pyproject.toml           # 包配置（PEP 621）
├── requirements.txt         # 依赖清单
├── CHANGELOG.md            # 变更日志
├── LICENSE                  # GPL-3.0 许可证
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

## 🎯 最新亮点

### v0.1.0 版本新增功能

#### 🌐 Web 文档浏览器
内置 Flask Web 服务器，提供优雅的文档浏览体验：
- 美观的 Markdown 渲染（支持代码高亮、表格）
- Mermaid 图表自动渲染
- 文件树导航和目录（TOC）
- 一键启动：`codeviewx --serve`

#### 🌍 多语言支持
支持 8 种主要语言的文档生成：
- 自动检测系统语言
- 通过 `-l/--language` 参数指定语言
- 支持：中文、英文、日文、韩文、法文、德文、西班牙文、俄文

#### 📊 智能进度提示
实时显示文档生成进度：
- 简洁一行式工具调用显示
- 智能 TODO 任务跟踪
- AI 思考过程展示
- 文档生成状态实时更新
- 详细/简洁模式切换（`--verbose`）

#### ⚡ 系统优化
- 提示词压缩 70%（从 33KB → 10KB）
- 提升 API 调用成功率
- 更快的响应速度
- 减少 token 消耗

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

## 💡 使用技巧

### 最佳实践

1. **首次使用**
   ```bash
   # 先生成文档
   codeviewx -w /path/to/project
   
   # 再启动 Web 服务器浏览
   codeviewx --serve
   ```

2. **查看项目文档**
   ```bash
   # 本项目已包含完整的技术文档示例
   # 查看中文文档
   codeviewx --serve -o docs/zh
   
   # 查看英文文档
   codeviewx --serve -o docs/en
   
   # 浏览器访问 http://127.0.0.1:5000
   # 可以看到包括架构图、API 文档、开发指南等完整内容
   ```

3. **多语言项目**
   ```bash
   # 为国际团队生成英文文档
   codeviewx -l English -o docs/en
   
   # 生成中文文档
   codeviewx -l Chinese -o docs/zh
   ```

4. **调试模式**
   ```bash
   # 使用 verbose 模式查看详细日志
   codeviewx --verbose
   ```

5. **Python 集成**
   ```python
   from codeviewx import generate_docs
   
   # 在 CI/CD 流程中自动生成文档
   generate_docs(
       working_directory=".",
       output_directory="docs",
       language="English"
   )
   ```

### 常见问题

**Q: 如何查看 CodeViewX 生成的文档示例？**  
A: 本项目自带完整的文档示例！运行 `codeviewx --serve -o docs/zh` 查看中文文档，或 `codeviewx --serve -o docs/en` 查看英文文档。也可以直接浏览 [docs/zh/](docs/zh/README.md) 或 [docs/en/](docs/en/README.md) 目录。

**Q: 支持哪些 AI 模型？**  
A: 默认使用 Anthropic Claude，也支持 OpenAI 模型。通过设置相应的 API 密钥即可。

**Q: 生成的文档可以自定义吗？**  
A: 可以修改 `codeviewx/prompts/DocumentEngineer.md` 提示词模板来自定义文档风格和内容。

**Q: 如何提高文档生成质量？**  
A: 确保项目代码注释完整、结构清晰。CodeViewX 会分析代码注释、README、配置文件等信息。

**Q: Web 服务器可以部署到生产环境吗？**  
A: 内置服务器仅用于本地预览。生产环境建议使用静态站点生成器（如 MkDocs）或部署到 GitHub Pages。

**Q: 支持增量更新吗？**  
A: 当前版本会重新生成所有文档。增量更新功能计划在未来版本中添加。

## 🗺️ 路线图

我们计划在未来版本中添加以下功能：

### v0.2.0（计划中）
- [ ] 🔄 增量文档更新（只更新修改的部分）
- [ ] 📦 PyPI 正式发布（通过 `pip install codeviewx` 安装）
- [ ] 🎨 自定义文档模板支持
- [ ] 📊 文档质量评分和改进建议
- [ ] 🔌 插件系统（支持自定义工具和分析器）

### v0.3.0（规划中）
- [ ] 🌐 更多 AI 模型支持（Google Gemini、本地 LLM）
- [ ] 📈 文档版本对比和变更追踪
- [ ] 🔍 代码质量分析和最佳实践建议
- [ ] 🎯 特定领域文档生成（API 文档、数据库文档等）
- [ ] 🤝 团队协作功能（文档评审、注释）

### 长期目标
- [ ] 🔐 企业级安全和隐私保护
- [ ] ☁️ 云端服务版本
- [ ] 🎓 智能学习功能（从反馈中改进文档质量）
- [ ] 🌍 更多语言支持（20+ 种语言）
- [ ] 📱 桌面应用和 IDE 插件

**欢迎贡献想法！** 如果你有好的建议，请在 [Issues](https://github.com/dean2021/codeviewx/issues) 中告诉我们。

## 🙏 致谢

- [DeepAgents](https://github.com/langchain-ai/deepagents) - 强大的 AI Agent 框架
- [LangChain](https://github.com/langchain-ai/langchain) - AI 应用开发框架
- [ripgrep](https://github.com/BurntSushi/ripgrep) - 超快的代码搜索工具
- [Anthropic Claude](https://www.anthropic.com) - 优秀的 AI 模型
- [Flask](https://flask.palletsprojects.com/) - 轻量级 Web 框架
- [Markdown](https://python-markdown.github.io/) - Markdown 解析库

## 📮 联系方式

- GitHub Issues: [https://github.com/dean2021/codeviewx/issues](https://github.com/dean2021/codeviewx/issues)
- Email: dean@csoio.com

---

⭐ 如果这个项目对您有帮助，请给个星标！
