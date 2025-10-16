# Tools 工具包

这个目录包含了 AI Agent 使用的各种工具函数，用于与真实文件系统交互、执行命令和搜索代码。

## 目录结构

```
tools/
├── __init__.py       # 工具包导出
├── command.py        # 命令执行工具
├── filesystem.py     # 文件系统操作工具
└── search.py         # 代码搜索工具
```

## 工具模块

### 1. 命令执行工具 (`command.py`)

#### `execute_command(command, working_dir=None)`
执行系统命令并返回结果。

**功能特性**:
- 支持任何 shell 命令
- 支持管道和重定向
- 自动捕获标准输出和错误输出
- 30秒超时保护

**使用示例**:
```python
from tools import execute_command

# 列出目录内容
result = execute_command("ls -la")

# 在指定目录执行命令
result = execute_command("cat main.py", "/path/to/project")

# 使用管道
result = execute_command("find . -name '*.py' | head -20")
```

---

### 2. 代码搜索工具 (`search.py`)

#### `ripgrep_search(pattern, path=".", file_type=None, ignore_case=False, max_count=100)`
使用 ripgrep 进行高性能代码搜索。

**功能特性**:
- 速度比传统 grep 快 10-100 倍
- 自动忽略 `.git`, `.venv`, `node_modules` 等目录
- 支持正则表达式
- 显示行号和文件名
- 支持文件类型过滤

**使用示例**:
```python
from tools import ripgrep_search

# 搜索 Python 文件中的函数定义
result = ripgrep_search("def main", ".", "py")

# 搜索所有包含 TODO 的行
result = ripgrep_search("TODO", "/path/to/project")

# 不区分大小写搜索
result = ripgrep_search("import.*Agent", ".", "py", ignore_case=True)
```

**系统要求**:
需要系统中安装 ripgrep：
```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows
choco install ripgrep
```

---

### 3. 文件系统工具 (`filesystem.py`)

#### `write_real_file(file_path, content)`
写入真实文件系统中的文件。

**功能特性**:
- 自动创建不存在的目录
- 支持相对路径和绝对路径
- 返回文件大小信息

**使用示例**:
```python
from tools import write_real_file

# 写入文件（自动创建目录）
result = write_real_file(".wiki/README.md", "# 文档标题\n\n内容...")

# 写入 JSON 数据
import json
data = {"key": "value"}
result = write_real_file("output/data.json", json.dumps(data, indent=2))
```

#### `read_real_file(file_path)`
读取真实文件系统中的文件内容。

**功能特性**:
- 支持相对路径和绝对路径
- 显示文件大小和行数信息
- UTF-8 编码

**使用示例**:
```python
from tools import read_real_file

# 读取项目文件
content = read_real_file("main.py")

# 读取配置文件
config = read_real_file("config/settings.json")
```

#### `list_real_directory(directory=".")`
列出真实文件系统中的目录内容。

**功能特性**:
- 分类显示目录和文件
- 显示文件和目录数量
- 支持相对路径和绝对路径

**使用示例**:
```python
from tools import list_real_directory

# 列出当前目录
result = list_real_directory(".")

# 列出指定目录
result = list_real_directory("/path/to/project")
```

---

## 在 main.py 中使用

在 `main.py` 中导入工具：

```python
from tools import (
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
)

# 创建工具列表
tools = [
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
]

# 传递给 AI Agent
agent = create_deep_agent(tools, prompt)
```

---

## 开发指南

### 添加新工具

1. 在相应的模块文件中添加新函数
2. 在 `__init__.py` 中导出该函数
3. 在 `main.py` 中注册工具

### 工具函数规范

所有工具函数应该：
- 有清晰的文档字符串（docstring）
- 包含参数说明和返回值说明
- 提供使用示例
- 进行错误处理，返回友好的错误信息
- 使用类型提示（type hints）

---

## 许可证

本项目遵循与主项目相同的许可证。

