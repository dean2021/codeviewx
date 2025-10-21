# API 参考文档

## 概述

CodeViewX 提供了完整的 Python API 和命令行接口，支持灵活的文档生成和配置。本文档详细介绍了所有可用的 API 函数、参数和用法示例。

## 核心 API

### 1. 文档生成 API

#### `generate_docs()`

**功能**: 生成项目技术文档

**签名**:
```python
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    ui_language: Optional[str] = None,
    recursion_limit: int = 1000,
    verbose: bool = False,
    base_url: Optional[str] = None
) -> None
```

**参数说明**:

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `working_directory` | `Optional[str]` | `None` | 项目工作目录，默认为当前目录 |
| `output_directory` | `str` | `"docs"` | 文档输出目录 |
| `doc_language` | `Optional[str]` | `None` | 文档语言，支持：`Chinese`, `English`, `Japanese`, `Korean`, `French`, `German`, `Spanish`, `Russian` |
| `ui_language` | `Optional[str]` | `None` | 界面语言，支持：`en`, `zh` |
| `recursion_limit` | `int` | `1000` | Agent 递归限制，控制最大执行步骤 |
| `verbose` | `bool` | `False` | 是否显示详细日志 |
| `base_url` | `Optional[str]` | `None` | 自定义 Anthropic API 基础 URL |

**使用示例**:

```python
from codeviewx import generate_docs

# 基本用法
generate_docs()

# 完整配置
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese",
    ui_language="zh",
    recursion_limit=1500,
    verbose=True,
    base_url="https://api.anthropic.com/v1"
)

# 生成英文文档
generate_docs(
    working_directory="./my-project",
    doc_language="English",
    verbose=True
)
```

**异常处理**:
```python
try:
    generate_docs(working_directory="/path/to/project")
except ValueError as e:
    print(f"配置错误: {e}")
except Exception as e:
    print(f"生成失败: {e}")
```

### 2. Web 服务器 API

#### `start_document_web_server()`

**功能**: 启动文档浏览 Web 服务器

**签名**:
```python
def start_document_web_server(output_directory: str) -> None
```

**参数说明**:

| 参数 | 类型 | 描述 |
|------|------|------|
| `output_directory` | `str` | 文档目录路径 |

**使用示例**:

```python
from codeviewx import start_document_web_server

# 启动服务器
start_document_web_server("docs")

# 服务器将在 http://127.0.0.1:5000 启动
```

**特性**:
- **自动路由**: 支持 `/` 和 `/<filename>` 路由
- **Markdown 渲染**: 自动渲染 Markdown 文件
- **文件树导航**: 生成文档导航树
- **目录支持**: 自动生成 TOC（目录）

### 3. 语言检测 API

#### `detect_system_language()`

**功能**: 自动检测系统语言

**签名**:
```python
def detect_system_language() -> str
```

**返回值**:
- `str`: 检测到的语言代码（`Chinese`, `English`, `Japanese`, `Korean`, `French`, `German`, `Spanish`, `Russian`）

**使用示例**:

```python
from codeviewx import detect_system_language

language = detect_system_language()
print(f"检测到的系统语言: {language}")
```

### 4. 提示词加载 API

#### `load_prompt()`

**功能**: 加载和处理提示词模板

**签名**:
```python
def load_prompt(name: str, **kwargs) -> str
```

**参数说明**:

| 参数 | 类型 | 描述 |
|------|------|------|
| `name` | `str` | 提示词名称（如：`"document_engineer"`） |
| `**kwargs` | `dict` | 模板变量 |

**使用示例**:

```python
from codeviewx import load_prompt

# 加载英文提示词
prompt = load_prompt(
    "document_engineer",
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="English"
)

# 加载中文提示词
prompt_zh = load_prompt(
    "document_engineer",
    working_directory="/path/to/project", 
    output_directory="docs",
    doc_language="Chinese"
)
```

## 工具 API

### 1. 文件系统工具

#### `write_real_file()`

**功能**: 写入文件到文件系统

**签名**:
```python
def write_real_file(file_path: str, content: str) -> str
```

**参数说明**:

| 参数 | 类型 | 描述 |
|------|------|------|
| `file_path` | `str` | 文件路径（支持相对和绝对路径） |
| `content` | `str` | 文件内容 |

**返回值**:
- `str`: 操作结果消息

**使用示例**:

```python
from codeviewx.tools import write_real_file

# 写入文档
result = write_real_file(
    "docs/README.md",
    "# 项目文档\n\n这是一个示例文档。"
)
print(result)  # ✅ Successfully wrote file: docs/README.md (X.XX KB)
```

#### `read_real_file()`

**功能**: 从文件系统读取文件

**签名**:
```python
def read_real_file(file_path: str) -> str
```

**参数说明**:

| 参数 | 类型 | 描述 |
|------|------|------|
| `file_path` | `str` | 文件路径 |

**返回值**:
- `str`: 文件内容和元信息

**使用示例**:

```python
from codeviewx.tools import read_real_file

# 读取文件
content = read_real_file("README.md")
print(content)  # 包含文件大小和行数的头部信息
```

#### `list_real_directory()`

**功能**: 列出目录内容

**签名**:
```python
def list_real_directory(directory: str = ".") -> str
```

**参数说明**:

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `directory` | `str` | `"."` | 目录路径 |

**返回值**:
- `str`: 目录内容列表

**使用示例**:

```python
from codeviewx.tools import list_real_directory

# 列出当前目录
content = list_real_directory(".")
print(content)

# 列出指定目录
content = list_real_directory("/path/to/project")
print(content)
```

### 2. 代码搜索工具

#### `ripgrep_search()`

**功能**: 高性能代码搜索

**签名**:
```python
def ripgrep_search(
    pattern: str,
    path: str = ".",
    file_type: Optional[str] = None,
    ignore_case: bool = False,
    max_count: int = 100
) -> str
```

**参数说明**:

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `pattern` | `str` | - | 搜索模式（支持正则表达式） |
| `path` | `str` | `"."` | 搜索路径 |
| `file_type` | `Optional[str]` | `None` | 文件类型过滤（如：`"py"`, `"js"`） |
| `ignore_case` | `bool` | `False` | 是否忽略大小写 |
| `max_count` | `int` | `100` | 最大结果数量 |

**使用示例**:

```python
from codeviewx.tools import ripgrep_search

# 搜索函数定义
results = ripgrep_search("def main", ".", "py")

# 搜索类定义（忽略大小写）
results = ripgrep_search("class.*controller", "./src", "py", ignore_case=True)

# 搜索导入语句
results = ripgrep_search("^import|^from.*import", ".", "py")

# 搜索路由定义
results = ripgrep_search("@app\.route|@GetMapping", ".", "py")
```

**高级搜索模式**:

```python
# 搜索入口点
entry_points = ripgrep_search("if __name__|def main|@SpringBootApplication", ".")

# 搜索数据库模型
models = ripgrep_search("class.*Model|@Entity|@Table", ".", "py")

# 搜索 API 端点
api_endpoints = ripgrep_search("@app\.(get|post|put|delete)|router\.", ".", "py")

# 搜索配置文件
configs = ripgrep_search("config|settings|environment", ".", "yml")
```

### 3. 命令执行工具

#### `execute_command()`

**功能**: 执行系统命令

**签名**:
```python
def execute_command(command: str, working_dir: Optional[str] = None) -> str
```

**参数说明**:

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `command` | `str` | - | 要执行的命令 |
| `working_dir` | `Optional[str]` | `None` | 工作目录 |

**返回值**:
- `str`: 命令执行结果

**使用示例**:

```python
from codeviewx.tools import execute_command

# 列出文件
result = execute_command("ls -la")

# 获取项目统计信息
result = execute_command("find . -name '*.py' | wc -l")

# 检查 Git 状态
result = execute_command("git status")

# 在指定目录执行命令
result = execute_command("npm list", working_dir="/path/to/frontend")
```

## 国际化 API

### 1. 翻译函数

#### `t()`

**功能**: 翻译消息

**签名**:
```python
def t(key: str, **kwargs) -> str
```

**参数说明**:

| 参数 | 类型 | 描述 |
|------|------|------|
| `key` | `str` | 消息键 |
| `**kwargs` | `dict` | 格式化变量 |

**使用示例**:

```python
from codeviewx.i18n import t

# 基本翻译
message = t('starting')  # 🚀 启动 CodeViewX 文档生成器

# 带变量的翻译
message = t('generated_files', count=5)  # ✅ 共生成 5 个文档文件

# 多变量翻译
message = t('cli_server_address')  # 🔗 服务器地址: http://127.0.0.1:5000
```

### 2. 语言设置

#### `set_locale()`

**功能**: 设置当前语言

**签名**:
```python
def set_locale(locale: str) -> None
```

**使用示例**:

```python
from codeviewx.i18n import set_locale

# 设置为中文
set_locale('zh')

# 设置为英文
set_locale('en')
```

#### `detect_ui_language()`

**功能**: 自动检测界面语言

**签名**:
```python
def detect_ui_language() -> str
```

**使用示例**:

```python
from codeviewx.i18n import detect_ui_language, set_locale

# 自动检测并设置语言
ui_lang = detect_ui_language()
set_locale(ui_lang)
print(f"界面语言设置为: {ui_lang}")
```

## 配置 API

### 1. 环境变量

CodeViewX 支持通过环境变量进行配置：

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `ANTHROPIC_AUTH_TOKEN` | Anthropic API 密钥 | 必需 |
| `ANTHROPIC_BASE_URL` | API 基础 URL | `https://api.anthropic.com/v1` |
| `CODEVIEWX_LANGUAGE` | 默认文档语言 | 自动检测 |

**使用示例**:

```python
import os
from codeviewx import generate_docs

# 设置环境变量
os.environ['ANTHROPIC_AUTH_TOKEN'] = 'your-api-key-here'
os.environ['ANTHROPIC_BASE_URL'] = 'https://api.anthropic.com/v1'
os.environ['CODEVIEWX_LANGUAGE'] = 'Chinese'

# 使用环境变量配置
generate_docs()
```

### 2. 配置验证

#### `validate_api_key()`

**功能**: 验证 API 密钥配置

**签名**:
```python
def validate_api_key() -> None
```

**异常**:
- `ValueError`: API 密钥未配置或无效

**使用示例**:

```python
from codeviewx.generator import validate_api_key

try:
    validate_api_key()
    print("API 密钥配置正确")
except ValueError as e:
    print(f"API 密钥配置错误: {e}")
```

## 错误处理

### 常见异常类型

| 异常类型 | 描述 | 解决方法 |
|----------|------|----------|
| `ValueError` | 配置错误（如 API 密钥缺失） | 检查环境变量设置 |
| `FileNotFoundError` | 文件或目录不存在 | 确认路径正确 |
| `PermissionError` | 权限不足 | 检查文件/目录权限 |
| `UnicodeDecodeError` | 文件编码问题 | 确保文件为 UTF-8 编码 |
| `ConnectionError` | 网络连接问题 | 检查网络和 API 配置 |

### 错误处理示例

```python
from codeviewx import generate_docs
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

def safe_generate_docs(working_dir, output_dir):
    try:
        generate_docs(
            working_directory=working_dir,
            output_directory=output_dir,
            doc_language="Chinese",
            verbose=True
        )
        print("文档生成成功！")
    except ValueError as e:
        if "ANTHROPIC_AUTH_TOKEN" in str(e):
            print("❌ API 密钥未配置，请设置环境变量 ANTHROPIC_AUTH_TOKEN")
        else:
            print(f"❌ 配置错误: {e}")
    except FileNotFoundError as e:
        print(f"❌ 文件或目录不存在: {e}")
    except PermissionError as e:
        print(f"❌ 权限不足: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        logging.exception("详细错误信息:")

# 使用示例
safe_generate_docs("/path/to/project", "docs")
```

## 使用模式

### 1. 基本文档生成

```python
from codeviewx import generate_docs

# 最简单的用法
generate_docs()
```

### 2. 高级配置

```python
from codeviewx import generate_docs
import os

# 环境配置
os.environ['ANTHROPIC_AUTH_TOKEN'] = 'your-api-key'

# 高级配置
generate_docs(
    working_directory="/path/to/large-project",
    output_directory="/path/to/output",
    doc_language="English",
    recursion_limit=2000,  # 大项目需要更多步骤
    verbose=True,          # 显示详细日志
    base_url="https://custom-api.example.com"  # 自定义 API
)
```

### 3. 批量处理

```python
from codeviewx import generate_docs
import os

projects = [
    {"path": "/path/to/project1", "lang": "Chinese"},
    {"path": "/path/to/project2", "lang": "English"},
    {"path": "/path/to/project3", "lang": "Japanese"}
]

for project in projects:
    print(f"正在处理项目: {project['path']}")
    try:
        generate_docs(
            working_directory=project['path'],
            output_directory=f"docs-{project['path'].split('/')[-1]}",
            doc_language=project['lang'],
            verbose=False
        )
        print(f"✅ {project['path']} 处理完成")
    except Exception as e:
        print(f"❌ {project['path']} 处理失败: {e}")
```

### 4. 集成到工作流

```python
from codeviewx import generate_docs, start_document_web_server
import time
import webbrowser

def docs_workflow(project_path):
    """完整的文档生成和浏览工作流"""
    
    # 1. 生成文档
    print("🚀 开始生成文档...")
    generate_docs(
        working_directory=project_path,
        doc_language="Chinese",
        verbose=True
    )
    print("✅ 文档生成完成")
    
    # 2. 启动服务器
    print("🌐 启动文档服务器...")
    import threading
    
    def start_server():
        start_document_web_server("docs")
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 等待服务器启动
    time.sleep(2)
    
    # 3. 打开浏览器
    print("🔗 打开文档页面...")
    webbrowser.open("http://127.0.0.1:5000")
    
    print("📚 文档已准备就绪！访问 http://127.0.0.1:5000 查看文档")

# 使用示例
docs_workflow("/path/to/your/project")
```

---

💡 **提示**: 更多使用示例和最佳实践，请参考 [开发指南](07-development-guide.md)。如果遇到问题，请查看 [快速开始指南](02-quickstart.md) 中的常见问题解决部分。