# CodeViewX 包结构重构方案

## 目标
将当前项目重构为标准的 Python pip 包，符合 PyPI 发布规范。

---

## 当前问题总结

| 问题 | 严重性 | 说明 |
|-----|--------|------|
| 缺少包目录 | 🔴 高 | 代码在根目录，没有命名空间 |
| 缺少 pyproject.toml | 🔴 高 | 无法通过 pip 安装 |
| 缺少 LICENSE | 🟡 中 | 不符合开源规范 |
| 入口点不明确 | 🟡 中 | main.py 不适合作为包入口 |
| 缺少测试目录 | 🟡 中 | 没有单元测试 |
| 提示词文件位置 | 🟢 低 | prompt/ 应该在包内 |

---

## 重构步骤

### 步骤 1: 创建包目录结构

```bash
mkdir -p codeviewx/tools
mkdir -p codeviewx/prompts
mkdir -p tests
mkdir -p examples
```

### 步骤 2: 移动现有文件

```bash
# 移动工具模块
mv tools/* codeviewx/tools/

# 移动提示词
mv prompt/* codeviewx/prompts/

# 重命名 main.py 为 core.py 并移动
mv main.py codeviewx/core.py
```

### 步骤 3: 创建包初始化文件

**`codeviewx/__init__.py`**:
```python
"""
CodeViewX - AI 驱动的代码文档生成器

基于 DeepAgents 和 LangChain 的智能文档生成工具。
"""

from .core import load_prompt, generate_docs
from .__version__ import __version__

__all__ = ["load_prompt", "generate_docs", "__version__"]
```

**`codeviewx/__version__.py`**:
```python
"""版本信息"""
__version__ = "0.1.0"
```

### 步骤 4: 创建 CLI 入口

**`codeviewx/cli.py`**:
```python
#!/usr/bin/env python3
"""
CodeViewX 命令行工具
"""

import argparse
import os
import sys
from pathlib import Path

from .core import load_prompt, generate_docs
from .__version__ import __version__


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description="CodeViewX - AI 驱动的代码文档生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  codeviewx                           # 分析当前目录
  codeviewx -w /path/to/project       # 分析指定项目
  codeviewx -o docs                   # 输出到 docs 目录
  codeviewx -w . -o .wiki             # 完整配置
        """
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"CodeViewX {__version__}"
    )
    
    parser.add_argument(
        "-w", "--working-dir",
        default=os.getcwd(),
        help="项目工作目录（默认：当前目录）"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default=".wiki",
        help="文档输出目录（默认：.wiki）"
    )
    
    parser.add_argument(
        "--recursion-limit",
        type=int,
        default=1000,
        help="Agent 递归限制（默认：1000）"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细日志"
    )
    
    args = parser.parse_args()
    
    try:
        generate_docs(
            working_directory=args.working_dir,
            output_directory=args.output_dir,
            recursion_limit=args.recursion_limit,
            verbose=args.verbose
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 步骤 5: 更新 core.py

**`codeviewx/core.py`** (从 main.py 重构):
```python
"""
CodeViewX 核心功能模块
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from deepagents import create_deep_agent
from langchain_core.prompts import PromptTemplate

from .tools import (
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
)


def load_prompt(name: str, **kwargs) -> str:
    """
    加载 AI 文档生成的系统提示词
    
    使用 LangChain 的 PromptTemplate 支持变量插值和动态参数。
    
    Args:
        name: 提示词文件名（不含扩展名）
        **kwargs: 模板变量
    
    Returns:
        格式化后的提示词文本
    """
    # 使用包资源读取提示词
    from importlib import resources
    
    try:
        # Python 3.9+
        with resources.files("codeviewx.prompts").joinpath(f"{name}.md").open("r", encoding="utf-8") as f:
            template_text = f.read()
    except AttributeError:
        # Python 3.7-3.8 兼容
        with resources.open_text("codeviewx.prompts", f"{name}.md", encoding="utf-8") as f:
            template_text = f.read()
    
    if kwargs:
        try:
            template = PromptTemplate.from_template(template_text)
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"模板需要变量 {e}，但未在参数中提供") from e
    
    return template_text


def generate_docs(
    working_directory: str,
    output_directory: str = ".wiki",
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None:
    """
    生成项目文档
    
    Args:
        working_directory: 项目工作目录
        output_directory: 文档输出目录
        recursion_limit: Agent 递归限制
        verbose: 是否显示详细日志
    """
    # 配置日志
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    if verbose:
        logging.getLogger("langchain").setLevel(logging.DEBUG)
        logging.getLogger("langgraph").setLevel(logging.DEBUG)
    
    print("=" * 80)
    print(f"🚀 启动 CodeViewX 文档生成器 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print(f"📂 工作目录: {working_directory}")
    print(f"📝 输出目录: {output_directory}")
    
    # 加载提示词
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory=working_directory,
        output_directory=output_directory
    )
    print("✓ 已加载系统提示词（已注入工作目录和输出目录）")
    
    # 创建工具列表
    tools = [
        execute_command,
        ripgrep_search,
        write_real_file,
        read_real_file,
        list_real_directory,
    ]
    
    # 创建 Agent
    agent = create_deep_agent(tools, prompt)
    print("✓ 已创建 AI Agent")
    print(f"✓ 已注册 {len(tools)} 个自定义工具: {', '.join([t.__name__ for t in tools])}")
    print("=" * 80)
    
    # 生成文档
    print("\n📝 开始分析项目并生成文档...\n")
    
    step_count = 0
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": "请根据系统提示词中的工作目录，分析该项目并生成深度技术文档"}]},
        stream_mode="values",
        config={"recursion_limit": recursion_limit}
    ):
        if "messages" in chunk:
            step_count += 1
            last_message = chunk["messages"][-1]
            
            if verbose:
                print(f"\n{'='*80}")
                print(f"📍 步骤 {step_count} - {last_message.__class__.__name__}")
                print(f"{'='*80}")
                last_message.pretty_print()
                
                if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    print(f"\n🔧 调用了 {len(last_message.tool_calls)} 个工具:")
                    for tool_call in last_message.tool_calls:
                        print(f"   - {tool_call.get('name', 'unknown')}")
    
    print("\n" + "=" * 80)
    print("✅ 文档生成完成!")
    print("=" * 80)
    
    if "files" in chunk:
        print("\n📄 生成的文件:")
        for filename in chunk["files"].keys():
            print(f"   - {filename}")
```

### 步骤 6: 更新工具包的 __init__.py

**`codeviewx/tools/__init__.py`**:
```python
"""CodeViewX 工具模块"""

from .command import execute_command
from .search import ripgrep_search
from .filesystem import write_real_file, read_real_file, list_real_directory

__all__ = [
    "execute_command",
    "ripgrep_search",
    "write_real_file",
    "read_real_file",
    "list_real_directory",
]
```

### 步骤 7: 创建提示词包初始化文件

**`codeviewx/prompts/__init__.py`**:
```python
"""CodeViewX 提示词模块"""

# 提示词作为包资源，通过 load_prompt 函数访问
```

### 步骤 8: 创建 pyproject.toml

**`pyproject.toml`**:
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "codeviewx"
version = "0.1.0"
description = "AI 驱动的代码文档生成器"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["documentation", "ai", "code-analysis", "deepagents"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Documentation",
    "Topic :: Software Development :: Documentation",
]

dependencies = [
    "langchain>=0.3.27",
    "langchain-anthropic>=0.3.22",
    "langchain-core>=0.3.79",
    "langchain-text-splitters>=0.3.11",
    "langgraph>=0.6.10",
    "langgraph-checkpoint>=2.1.2",
    "langgraph-prebuilt>=0.6.4",
    "langgraph-sdk>=0.2.9",
    "langsmith>=0.4.34",
    "deepagents>=0.0.5",
    "ripgrepy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "flake8>=6.0",
    "mypy>=1.0",
    "isort>=5.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/codeviewx"
Documentation = "https://github.com/yourusername/codeviewx/docs"
Repository = "https://github.com/yourusername/codeviewx"
"Bug Tracker" = "https://github.com/yourusername/codeviewx/issues"

[project.scripts]
codeviewx = "codeviewx.cli:main"

[tool.setuptools]
package-dir = {"" = "."}

[tool.setuptools.packages.find]
where = ["."]
include = ["codeviewx*"]
exclude = ["tests*", "docs*", "examples*"]

[tool.setuptools.package-data]
codeviewx = ["prompts/*.md"]

[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=codeviewx --cov-report=html --cov-report=term"
```

### 步骤 9: 创建 MANIFEST.in

**`MANIFEST.in`**:
```
include README.md
include LICENSE
include requirements.txt
recursive-include codeviewx/prompts *.md
recursive-include docs *.md
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

### 步骤 10: 创建 LICENSE

**`LICENSE`** (MIT 许可证):
```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 步骤 11: 创建开发依赖文件

**`requirements-dev.txt`**:
```
# 开发和测试依赖
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
isort>=5.0.0
```

### 步骤 12: 创建基础测试

**`tests/__init__.py`**: 空文件

**`tests/test_core.py`**:
```python
"""测试核心功能"""

import pytest
from codeviewx import load_prompt


def test_load_prompt():
    """测试提示词加载"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test/path",
        output_directory=".wiki"
    )
    
    assert "/test/path" in prompt
    assert ".wiki" in prompt
    assert "{working_directory}" not in prompt
    assert "{output_directory}" not in prompt


def test_load_prompt_missing_variable():
    """测试缺少必需变量时的错误处理"""
    with pytest.raises(ValueError, match="模板需要变量"):
        load_prompt("DocumentEngineer", working_directory="/test")
```

**`tests/test_tools.py`**:
```python
"""测试工具函数"""

import pytest
from codeviewx.tools import execute_command, ripgrep_search


def test_execute_command():
    """测试命令执行"""
    result = execute_command("echo 'test'")
    assert "test" in result


def test_ripgrep_search():
    """测试代码搜索"""
    # 这里可以添加实际的测试
    pass
```

---

## 重构后的目录结构

```
codeviewx/                          
├── codeviewx/                      # 包目录 ⭐
│   ├── __init__.py                 
│   ├── __version__.py              
│   ├── cli.py                      # 命令行入口
│   ├── core.py                     # 核心功能（原 main.py）
│   ├── config.py                   # 配置（可选）
│   ├── tools/                      
│   │   ├── __init__.py
│   │   ├── command.py
│   │   ├── filesystem.py
│   │   └── search.py
│   └── prompts/                    # 提示词作为包资源
│       ├── __init__.py
│       └── DocumentEngineer.md
├── tests/                          # 测试目录 ⭐
│   ├── __init__.py
│   ├── test_core.py
│   └── test_tools.py
├── docs/                           
│   └── ...
├── examples/                       # 使用示例
│   └── basic_usage.py
├── .gitignore
├── LICENSE                         # 许可证 ⭐
├── MANIFEST.in                     # 打包清单 ⭐
├── README.md
├── pyproject.toml                  # 包配置 ⭐
├── requirements.txt                
└── requirements-dev.txt            # 开发依赖 ⭐
```

---

## 执行重构的命令脚本

创建 `scripts/refactor.sh`:

```bash
#!/bin/bash

echo "🚀 开始重构 CodeViewX 包结构..."

# 1. 创建新目录
mkdir -p codeviewx/tools
mkdir -p codeviewx/prompts
mkdir -p tests
mkdir -p examples
mkdir -p scripts

# 2. 移动文件
echo "📦 移动代码文件..."
cp -r tools/* codeviewx/tools/
cp -r prompt/* codeviewx/prompts/
cp main.py codeviewx/core.py

# 3. 创建 __init__.py 文件
touch codeviewx/__init__.py
touch codeviewx/tools/__init__.py
touch codeviewx/prompts/__init__.py
touch tests/__init__.py

echo "✅ 重构完成！"
echo ""
echo "⚠️  请手动完成以下步骤："
echo "  1. 创建 pyproject.toml"
echo "  2. 创建 LICENSE"
echo "  3. 创建 MANIFEST.in"
echo "  4. 更新 codeviewx/__init__.py"
echo "  5. 创建 codeviewx/cli.py"
echo "  6. 更新 codeviewx/core.py"
echo "  7. 添加测试"
echo "  8. 测试安装: pip install -e ."
```

---

## 使用重构后的包

### 安装方式

```bash
# 开发安装（推荐）
pip install -e .

# 带开发依赖
pip install -e ".[dev]"

# 从 PyPI 安装（发布后）
pip install codeviewx
```

### 使用方式

**方式 1: 命令行**
```bash
# 分析当前目录
codeviewx

# 指定项目和输出目录
codeviewx -w /path/to/project -o docs

# 显示帮助
codeviewx --help

# 显示版本
codeviewx --version
```

**方式 2: Python API**
```python
from codeviewx import generate_docs, load_prompt

# 生成文档
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs"
)

# 或单独加载提示词
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/path/to/project",
    output_directory="docs"
)
```

---

## 发布到 PyPI

```bash
# 1. 安装构建工具
pip install build twine

# 2. 构建包
python -m build

# 3. 检查包
twine check dist/*

# 4. 上传到 TestPyPI（测试）
twine upload --repository testpypi dist/*

# 5. 上传到 PyPI（正式发布）
twine upload dist/*
```

---

## 优势对比

| 特性 | 当前结构 | 重构后 |
|-----|---------|--------|
| 可 pip 安装 | ❌ | ✅ |
| 命令行工具 | ❌ | ✅ `codeviewx` |
| 标准包结构 | ❌ | ✅ |
| 测试支持 | ❌ | ✅ |
| 开源许可 | ❌ | ✅ |
| PyPI 发布 | ❌ | ✅ |
| 包命名空间 | ❌ | ✅ |
| 资源管理 | ❌ | ✅ |

---

## 下一步行动

### 立即执行（高优先级）

1. ✅ 创建 `pyproject.toml`
2. ✅ 创建包目录结构
3. ✅ 移动代码文件
4. ✅ 创建 CLI 入口
5. ✅ 添加 LICENSE

### 短期执行（中优先级）

6. ⏳ 添加单元测试
7. ⏳ 更新 README 说明安装方式
8. ⏳ 本地测试安装 (`pip install -e .`)
9. ⏳ 添加 CI/CD（GitHub Actions）

### 长期执行（低优先级）

10. 📅 发布到 TestPyPI
11. 📅 发布到 PyPI
12. 📅 添加文档网站（Sphinx/MkDocs）
13. 📅 添加类型提示
14. 📅 代码质量工具集成

---

## 总结

当前结构**不适合**作为 pip 包，需要进行重构。重构后将获得：

- ✅ 标准的 Python 包结构
- ✅ 可通过 `pip install` 安装
- ✅ 提供命令行工具 `codeviewx`
- ✅ 支持作为库导入使用
- ✅ 符合 PyPI 发布规范
- ✅ 易于测试和维护

**建议立即开始重构！** 🚀

