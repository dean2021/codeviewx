# 更新日志 (Changelog)

所有 CodeViewX 的重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

---

## [未发布] (Unreleased)

### 新增 (Added)
- 🌍 **多语言文档生成支持**
  - 支持 8 种主要语言：Chinese, English, Japanese, Korean, French, German, Spanish, Russian
  - 自动检测系统语言功能 (`detect_system_language()`)
  - CLI 新增 `-l/--language` 参数
  - Python API 新增 `doc_language` 参数
  - 完整的语言功能测试套件 (`tests/test_language.py`)
  - 多语言功能文档 (`docs/multi-language-support.md`)
  - 语言使用演示脚本 (`examples/language_demo.py`)

### 变更 (Changed)
- 📝 更新 `DocumentEngineer.md` 提示词模板
  - 添加 `{doc_language}` 占位符
  - 添加"文档语言规范"章节
  - 明确要求使用指定语言生成文档内容
  
- 🔧 更新 `generate_docs()` 函数
  - 新增 `doc_language` 参数（可选，默认自动检测）
  - 显示当前使用的文档语言和来源（自动检测/用户指定）
  
- 📦 更新 `codeviewx.__init__.py`
  - 导出 `detect_system_language` 函数
  
- 🧪 更新现有测试
  - 所有 `load_prompt()` 调用现在需要 `doc_language` 参数
  - 修复 `test_core.py` 中的 3 个测试

### 修复 (Fixed)
- 无

---

## [0.1.0] - 2024-10-16

### 新增 (Added)
- 🎉 CodeViewX 首个正式版本
- 📦 标准 Python 包结构
  - 使用 `pyproject.toml` 进行现代化包管理
  - 支持 `pip install -e .` 安装
  - 提供 `codeviewx` CLI 命令
  
- 🛠️ 核心功能
  - AI 驱动的代码文档生成
  - 基于 DeepAgents 和 LangChain
  - 支持多文件结构文档输出
  
- 🔧 自定义工具集
  - `execute_command` - 执行系统命令
  - `ripgrep_search` - 快速代码搜索
  - `write_real_file` - 写入真实文件系统
  - `read_real_file` - 读取真实文件
  - `list_real_directory` - 列出目录内容
  
- 📝 动态提示词系统
  - 使用 LangChain `PromptTemplate` 支持变量注入
  - 支持 `working_directory` 和 `output_directory` 动态配置
  
- 🎨 CLI 命令行工具
  - `-w/--working-dir` - 指定项目目录
  - `-o/--output-dir` - 指定输出目录
  - `--recursion-limit` - Agent 递归限制
  - `--verbose` - 详细日志输出
  - `-v/--version` - 显示版本信息
  
- 📚 完整文档
  - README.md - 项目说明和快速开始
  - 使用示例 (`examples/basic_usage.py`)
  - 技术文档 (`docs/`)
  
- 🧪 测试套件
  - `tests/test_core.py` - 核心功能测试
  - `tests/test_tools.py` - 工具测试
  - 使用 pytest 测试框架

### 技术栈 (Tech Stack)
- Python 3.8+
- DeepAgents 0.0.5+
- LangChain 0.3.27+
- LangGraph 0.6.10+
- ripgrepy 2.0.0

---

## 版本历史概览

| 版本 | 发布日期 | 主要变更 |
|------|---------|---------|
| 未发布 | - | 多语言文档生成支持 🌍 |
| 0.1.0 | 2024-10-16 | 首个正式版本 🎉 |

---

## 升级指南

### 升级到未发布版本（多语言功能）

如果您从 0.1.0 升级到最新版本：

#### 代码更新

**之前**:
```python
from codeviewx import generate_docs

generate_docs(
    working_directory="/path/to/project",
    output_directory="docs"
)
```

**现在**:
```python
from codeviewx import generate_docs

# 选项 1: 自动检测语言（推荐）
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs"
)

# 选项 2: 明确指定语言
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese"  # 新参数
)
```

#### CLI 更新

**之前**:
```bash
codeviewx -w /path/to/project -o docs
```

**现在**:
```bash
# 自动检测（行为不变）
codeviewx -w /path/to/project -o docs

# 或指定语言
codeviewx -w /path/to/project -o docs -l Chinese
```

#### 测试更新

如果您使用 `load_prompt()` 函数，现在需要提供 `doc_language` 参数：

**之前**:
```python
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/test",
    output_directory=".wiki"
)
```

**现在**:
```python
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/test",
    output_directory=".wiki",
    doc_language="English"  # 必需
)
```

---

## 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献代码。

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

