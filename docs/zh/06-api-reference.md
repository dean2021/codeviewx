# API 参考文档

本文档提供 CodeViewX 的完整 API 参考，包括命令行接口、Python API、和 Web API 的详细说明。

## 命令行接口 (CLI)

### 基本语法

```bash
codeviewx [选项] [参数]
```

### 主要选项

| 选项 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--working-dir` | `-w` | 字符串 | 当前目录 | 指定要分析的项目目录 |
| `--output-dir` | `-o` | 字符串 | `docs` | 指定文档输出目录 |
| `--language` | `-l` | 字符串 | 自动检测 | 指定文档语言 |
| `--ui-lang` | - | 字符串 | 自动检测 | 指定界面语言 |
| `--serve` | - | 布尔值 | `False` | 启动 Web 服务器 |
| `--verbose` | - | 布尔值 | `False` | 显示详细日志 |
| `--recursion-limit` | - | 整数 | `1000` | AI 代理递归限制 |
| `--version` | `-v` | - | - | 显示版本信息 |
| `--help` | `-h` | - | - | 显示帮助信息 |

### 支持的语言

#### 文档语言 (`--language`)
- `Chinese` - 中文（简体）
- `English` - 英文
- `Japanese` - 日文
- `Korean` - 韩文
- `French` - 法文
- `German` - 德文
- `Spanish` - 西班牙文
- `Russian` - 俄文

#### 界面语言 (`--ui-lang`)
- `en` - 英文界面
- `zh` - 中文界面

### 使用示例

#### 基本使用
```bash
# 分析当前目录，自动检测语言
codeviewx

# 分析指定项目
codeviewx -w /path/to/project

# 生成英文文档
codeviewx -l English

# 输出到指定目录
codeviewx -o /path/to/output
```

#### 高级配置
```bash
# 完整配置示例
codeviewx \
  --working-dir /path/to/project \
  --output-dir docs \
  --language Chinese \
  --ui-lang zh \
  --verbose \
  --recursion-limit 500

# 启动文档服务器
codeviewx --serve -o docs

# 调试模式
codeviewx --verbose --recursion-limit 100
```

### 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API 密钥 | `sk-ant-api...` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | `sk-...` |
| `PYTHONPATH` | Python 路径 | `/path/to/codeviewx` |
| `LANG` | 系统语言 | `zh_CN.UTF-8` |

## Python API

### 核心模块导入

```python
from codeviewx import (
    generate_docs,
    start_document_web_server,
    load_prompt,
    detect_system_language
)

from codeviewx.i18n import (
    get_i18n,
    t,
    set_locale,
    detect_ui_language
)

from codeviewx.tools import (
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory
)
```

### 主要函数

#### generate_docs()

生成项目文档的核心函数。

```python
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    ui_language: Optional[str] = None,
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None
```

**参数**:
- `working_directory`: 项目工作目录，默认为当前目录
- `output_directory`: 文档输出目录，默认为 "docs"
- `doc_language`: 文档语言，默认自动检测
- `ui_language`: 界面语言，默认自动检测
- `recursion_limit`: AI 代理递归限制，默认 1000
- `verbose`: 是否显示详细日志，默认 False

**示例**:
```python
# 基本使用
generate_docs()

# 完整配置
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese",
    ui_language="zh",
    recursion_limit=500,
    verbose=True
)
```

#### start_document_web_server()

启动文档浏览 Web 服务器。

```python
def start_document_web_server(output_directory: str) -> None
```

**参数**:
- `output_directory`: 文档目录路径

**示例**:
```python
# 启动服务器
start_document_web_server("docs")

# 在生成文档后启动服务器
generate_docs(output_directory="docs")
start_document_web_server("docs")
```

#### detect_system_language()

自动检测系统语言。

```python
def detect_system_language() -> str
```

**返回值**: 语言名称字符串

**示例**:
```python
lang = detect_system_language()
print(f"Detected language: {lang}")  # 输出: Detected language: Chinese
```

### 国际化 API

#### get_i18n()

获取国际化管理器实例。

```python
def get_i18n() -> I18n
```

**返回值**: I18n 实例

**示例**:
```python
i18n = get_i18n()
i18n.set_locale('zh')
message = i18n.t('starting')
```

#### t()

翻译消息的快捷函数。

```python
def t(key: str, **kwargs) -> str
```

**参数**:
- `key`: 消息键
- `**kwargs`: 格式化参数

**示例**:
```python
# 基本翻译
message = t('starting')

# 带参数的翻译
message = t('generated_files', count=5)
```

#### set_locale()

设置界面语言。

```python
def set_locale(locale: str) -> None
```

**参数**:
- `locale`: 语言代码 ('en' 或 'zh')

**示例**:
```python
set_locale('zh')
message = t('starting')  # 输出中文消息
```

### 工具函数 API

#### execute_command()

执行系统命令。

```python
def execute_command(command: str, working_dir: str = None) -> str
```

**参数**:
- `command`: 要执行的命令
- `working_dir`: 工作目录，可选

**示例**:
```python
# 列出文件
result = execute_command("ls -la")

# 在指定目录执行命令
result = execute_command("git status", working_dir="/path/to/repo")
```

#### ripgrep_search()

使用 ripgrep 搜索代码。

```python
def ripgrep_search(
    pattern: str,
    path: str = ".",
    file_type: str = None,
    ignore_case: bool = False,
    max_count: int = 100
) -> str
```

**参数**:
- `pattern`: 搜索模式（正则表达式）
- `path`: 搜索路径，默认当前目录
- `file_type`: 文件类型过滤，如 'py', 'js'
- `ignore_case`: 是否忽略大小写，默认 False
- `max_count`: 最大结果数，默认 100

**示例**:
```python
# 搜索 Python 类定义
result = ripgrep_search("class \w+", ".", "py")

# 忽略大小写搜索
result = ripgrep_search("TODO", ".", ignore_case=True)

# 搜索特定文件类型
result = ripgrep_search("import.*flask", ".", "py", max_count=50)
```

#### read_real_file()

读取文件内容。

```python
def read_real_file(file_path: str) -> str
```

**参数**:
- `file_path`: 文件路径

**示例**:
```python
# 读取文件内容
content = read_real_file("README.md")

# 读取配置文件
config = read_real_file("pyproject.toml")
```

#### write_real_file()

写入文件内容。

```python
def write_real_file(file_path: str, content: str) -> str
```

**参数**:
- `file_path`: 文件路径
- `content`: 文件内容

**示例**:
```python
# 写入文档
result = write_real_file("docs/README.md", "# Documentation")

# 写入配置文件
config_content = "[tool.black]\nline-length = 100\n"
result = write_real_file("pyproject.toml", config_content)
```

#### list_real_directory()

列出目录内容。

```python
def list_real_directory(directory: str = ".") -> str
```

**参数**:
- `directory`: 目录路径，默认当前目录

**示例**:
```python
# 列出当前目录
result = list_real_directory()

# 列出指定目录
result = list_real_directory("/path/to/project")
```

### 高级用法

#### 批量处理多个项目

```python
import os
from codeviewx import generate_docs

def batch_analyze_projects(projects_dir, output_base_dir):
    """批量分析多个项目"""
    for project_name in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project_name)
        if os.path.isdir(project_path):
            output_dir = os.path.join(output_base_dir, project_name)
            
            print(f"Analyzing {project_name}...")
            generate_docs(
                working_directory=project_path,
                output_directory=output_dir,
                doc_language="Chinese",
                verbose=True
            )
            print(f"Completed {project_name}")

# 使用示例
batch_analyze_projects("/path/to/projects", "/path/to/docs")
```

#### 自定义文档生成

```python
from codeviewx import generate_docs
from codeviewx.i18n import set_locale, t

def custom_documentation_generator():
    """自定义文档生成流程"""
    
    # 设置中文界面
    set_locale('zh')
    
    # 项目配置
    projects = [
        {
            'path': '/path/to/frontend',
            'output': 'docs/frontend',
            'language': 'Chinese'
        },
        {
            'path': '/path/to/backend',
            'output': 'docs/backend',
            'language': 'English'
        }
    ]
    
    # 生成文档
    for project in projects:
        print(t('starting'))
        generate_docs(
            working_directory=project['path'],
            output_directory=project['output'],
            doc_language=project['language'],
            verbose=True
        )
        print(t('completed'))

custom_documentation_generator()
```

## Web API

### HTTP 服务器

CodeViewX 的 Web 服务器基于 Flask，提供文档浏览功能。

#### 默认配置

```python
# 服务器配置
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 5000
DEBUG_MODE = True
```

#### 路由结构

| 路径 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 显示主页（README.md） |
| `/<filename>` | GET | 显示指定文档文件 |
| `/static/<path>` | GET | 静态资源服务 |

#### 请求示例

```bash
# 访问主页
curl http://127.0.0.1:5000/

# 访问特定文档
curl http://127.0.0.1:5000/01-overview.md

# 访问静态资源
curl http://127.0.0.1:5000/static/css/style.css
```

### 响应格式

#### 成功响应
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
```

#### 文件不存在
```http
HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=utf-8

File not found: /path/to/file.md
```

## 错误处理

### 常见错误类型

#### 1. 配置错误

```python
# 文件路径错误
try:
    generate_docs(working_directory="/nonexistent/path")
except FileNotFoundError as e:
    print(f"Directory not found: {e}")

# 权限错误
try:
    generate_docs(output_directory="/protected/path")
except PermissionError as e:
    print(f"Permission denied: {e}")
```

#### 2. API 错误

```python
# API 密钥未设置
if not os.getenv('ANTHROPIC_API_KEY'):
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")

# ripgrep 未安装
try:
    result = ripgrep_search("pattern", ".")
except RuntimeError as e:
    if "ripgrep" in str(e):
        print("Please install ripgrep: brew install ripgrep")
```

#### 3. 生成错误

```python
# 递归限制错误
try:
    generate_docs(recursion_limit=10)  # 太小的限制
except RuntimeError as e:
    if "recursion limit" in str(e):
        print("Consider increasing recursion limit")
```

### 错误恢复策略

```python
import time
from codeviewx import generate_docs

def robust_generate_docs(config, max_retries=3):
    """带重试机制的文档生成"""
    for attempt in range(max_retries):
        try:
            generate_docs(**config)
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                raise
    return False

# 使用示例
config = {
    'working_directory': '/path/to/project',
    'output_directory': 'docs',
    'verbose': True
}

robust_generate_docs(config)
```

## 性能优化

### 缓存配置

```python
# 启用详细日志进行性能监控
generate_docs(verbose=True)

# 限制递归深度避免性能问题
generate_docs(recursion_limit=500)

# 分批处理大型项目
def process_large_project(project_path, output_path):
    # 先分析主要文件
    generate_docs(
        working_directory=project_path,
        output_directory=output_path,
        recursion_limit=300
    )
```

### 内存优化

```python
import gc
from codeviewx import generate_docs

def memory_efficient_generation():
    """内存友好的文档生成"""
    try:
        generate_docs(verbose=False)  # 减少日志输出
    finally:
        gc.collect()  # 强制垃圾回收

memory_efficient_generation()
```

## 扩展和插件

### 自定义工具

```python
from codeviewx.tools import register_tool

@register_tool
def custom_analyzer(file_path: str) -> str:
    """自定义分析工具"""
    # 实现自定义分析逻辑
    return f"Analysis result for {file_path}"
```

### 自定义模板

```python
from codeviewx.prompt import load_prompt

# 使用自定义提示词模板
custom_prompt = load_prompt(
    "custom_template",
    working_directory="/path/to/project",
    doc_language="Chinese"
)
```

这个 API 参考文档提供了 CodeViewX 所有可用接口的详细说明，帮助开发者充分利用系统功能。