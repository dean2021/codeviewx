# API 参考文档

## 概述

CodeViewX 提供了丰富的 API 接口，包括命令行接口、Python API 和 Web API。本文档详细描述了各个接口的使用方法、参数说明和返回值格式。

## 命令行接口 (CLI)

### 主命令：codeviewx

#### 语法

```bash
codeviewx [OPTIONS] [COMMAND]
```

#### 全局选项

| 选项 | 短选项 | 类型 | 默认值 | 描述 |
|------|--------|------|--------|------|
| `--version` | `-v` | flag | - | 显示版本信息并退出 |
| `--help` | `-h` | flag | - | 显示帮助信息并退出 |

#### 命令

### 1. 文档生成命令

#### 语法

```bash
codeviewx [OPTIONS]
```

#### 选项

| 选项 | 短选项 | 类型 | 默认值 | 描述 |
|------|--------|------|--------|------|
| `--working-dir` | `-w` | string | 当前目录 | 项目工作目录路径 |
| `--output-dir` | `-o` | string | "docs" | 文档输出目录路径 |
| `--language` | `-l` | choice | 自动检测 | 文档语言 |
| `--recursion-limit` | - | integer | 1000 | Agent 递归限制 |
| `--verbose` | - | flag | False | 显示详细日志 |

#### 语言选项

| 语言 | 代码 | 说明 |
|------|------|------|
| Chinese | Chinese | 中文 |
| English | English | 英文 |
| Japanese | Japanese | 日文 |
| Korean | Korean | 韩文 |
| French | French | 法文 |
| German | German | 德文 |
| Spanish | Spanish | 西班牙文 |
| Russian | Russian | 俄文 |

#### 使用示例

```bash
# 基本使用 - 分析当前目录
codeviewx

# 指定项目目录
codeviewx -w /path/to/project

# 自定义输出目录和语言
codeviewx -w ./my-project -o documentation -l Chinese

# 显示详细日志
codeviewx --verbose

# 设置递归限制
codeviewx --recursion-limit 500

# 完整配置
codeviewx -w ./project -o docs -l English --recursion-limit 800 --verbose
```

#### 返回值

- **成功**: 返回 0，输出生成的文档信息
- **失败**: 返回非 0，输出错误信息

### 2. Web 服务器命令

#### 语法

```bash
codeviewx --serve [OPTIONS]
```

#### 选项

| 选项 | 短选项 | 类型 | 默认值 | 描述 |
|------|--------|------|--------|------|
| `--output-dir` | `-o` | string | "docs" | 文档目录路径 |
| `--serve` | - | flag | False | 启动 Web 服务器模式 |

#### 使用示例

```bash
# 启动默认服务器
codeviewx --serve

# 指定文档目录
codeviewx --serve -o docs

# 组合使用：生成文档后启动服务器
codeviewx -w ./project -o docs && codeviewx --serve -o docs
```

#### 服务器信息

- **地址**: http://127.0.0.1:5000
- **端口**: 5000
- **停止方式**: Ctrl+C

## Python API

### 核心函数

#### 1. generate_docs()

生成项目文档的核心函数。

**语法**

```python
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None
```

**参数**

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|------|------|--------|------|------|
| `working_directory` | str | None | 否 | 项目工作目录，None 表示当前目录 |
| `output_directory` | str | "docs" | 否 | 文档输出目录 |
| `doc_language` | str | None | 否 | 文档语言，None 表示自动检测 |
| `recursion_limit` | int | 1000 | 否 | Agent 递归限制 |
| `verbose` | bool | False | 否 | 是否显示详细日志 |

**返回值**

- `None`: 无返回值，结果直接输出到文件

**异常**

- `ValueError`: 参数验证失败
- `FileNotFoundError`: 工作目录不存在
- `PermissionError`: 权限不足
- `Exception`: 其他运行时错误

**使用示例**

```python
from codeviewx import generate_docs

# 基本使用
generate_docs()

# 完整配置
generate_docs(
    working_directory="/path/to/project",
    output_directory="documentation",
    doc_language="Chinese",
    recursion_limit=800,
    verbose=True
)

# 批量处理
projects = ["/path/to/project1", "/path/to/project2"]
for project in projects:
    generate_docs(
        working_directory=project,
        output_directory=f"docs_{os.path.basename(project)}",
        doc_language="English"
    )
```

#### 2. load_prompt()

加载和格式化 AI 提示词模板。

**语法**

```python
def load_prompt(name: str, **kwargs) -> str
```

**参数**

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|------|------|--------|------|------|
| `name` | str | - | 是 | 提示词文件名（不含扩展名） |
| `**kwargs` | dict | - | 否 | 模板变量，用于替换提示词中的占位符 |

**返回值**

- `str`: 格式化后的提示词文本

**异常**

- `FileNotFoundError`: 提示词文件不存在
- `ValueError`: 模板变量缺失
- `Exception`: 其他处理错误

**使用示例**

```python
from codeviewx import load_prompt

# 基本加载
prompt = load_prompt("DocumentEngineer")

# 带变量替换
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese"
)

# 自定义变量
prompt = load_prompt(
    "CustomPrompt",
    project_name="MyProject",
    author="Developer Name",
    version="1.0.0"
)
```

#### 3. detect_system_language()

检测系统语言设置。

**语法**

```python
def detect_system_language() -> str
```

**参数**

无参数

**返回值**

- `str`: 语言代码，如 "Chinese", "English" 等

**使用示例**

```python
from codeviewx import detect_system_language

language = detect_system_language()
print(f"系统语言: {language}")

# 在生成文档时使用
generate_docs(doc_language=detect_system_language())
```

#### 4. start_document_web_server()

启动文档 Web 服务器。

**语法**

```python
def start_document_web_server(output_directory: str) -> None
```

**参数**

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|------|------|--------|------|------|
| `output_directory` | str | - | 是 | 文档目录路径 |

**返回值**

- `None`: 阻塞式运行服务器

**使用示例**

```python
from codeviewx import start_document_web_server

# 启动服务器
start_document_web_server("docs")

# 在单独线程中启动
import threading
server_thread = threading.Thread(
    target=start_document_web_server,
    args=("docs",)
)
server_thread.daemon = True
server_thread.start()
```

### 工具函数

#### 1. execute_command()

执行系统命令。

**语法**

```python
def execute_command(command: str, working_dir: str = None) -> str
```

**参数**

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|------|------|--------|------|------|
| `command` | str | - | 是 | 要执行的命令 |
| `working_dir` | str | None | 否 | 工作目录 |

**返回值**

- `str`: 命令执行结果

**使用示例**

```python
from codeviewx.tools import execute_command

# 基本使用
result = execute_command("ls -la")
print(result)

# 指定工作目录
result = execute_command("git status", "/path/to/repo")

# 复杂命令
result = execute_command("find . -name '*.py' | head -10")
```

#### 2. ripgrep_search()

使用 ripgrep 进行代码搜索。

**语法**

```python
def ripgrep_search(
    pattern: str,
    path: str = ".",
    file_type: str = None,
    ignore_case: bool = False,
    max_count: int = 100
) -> str
```

**参数**

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|------|------|--------|------|------|
| `pattern` | str | - | 是 | 搜索模式（正则表达式） |
| `path` | str | "." | 否 | 搜索路径 |
| `file_type` | str | None | 否 | 文件类型过滤 |
| `ignore_case` | bool | False | 否 | 忽略大小写 |
| `max_count` | int | 100 | 否 | 最大返回结果数 |

**返回值**

- `str`: 搜索结果

**使用示例**

```python
from codeviewx.tools import ripgrep_search

# 基本搜索
result = ripgrep_search("def main", ".", "py")

# 不区分大小写搜索
result = ripgrep_search("TODO", "/path/to/project", ignore_case=True)

# 文件类型过滤
result = ripgrep_search("class.*Controller", ".", "js")

# 限制结果数量
result = ripgrep_search("import", ".", "py", max_count=50)
```

#### 3. read_real_file()

读取文件内容。

**语法**

```python
def read_real_file(file_path: str) -> str
```

**参数**

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|------|------|--------|------|------|
| `file_path` | str | - | 是 | 文件路径 |

**返回值**

- `str`: 文件内容（包含文件信息头部）

**使用示例**

```python
from codeviewx.tools import read_real_file

# 读取文件
content = read_real_file("/path/to/file.py")

# 读取配置文件
config = read_real_file("pyproject.toml")
```

#### 4. write_real_file()

写入文件内容。

**语法**

```python
def write_real_file(file_path: str, content: str) -> str
```

**参数**

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|------|------|--------|------|------|
| `file_path` | str | - | 是 | 文件路径 |
| `content` | str | - | 是 | 文件内容 |

**返回值**

- `str`: 操作结果消息

**使用示例**

```python
from codeviewx.tools import write_real_file

# 写入文档
result = write_real_file("docs/README.md", "# 项目文档")

# 写入配置文件
config_content = """
[project]
name = "my-project"
version = "1.0.0"
"""
result = write_real_file("pyproject.toml", config_content)
```

#### 5. list_real_directory()

列出目录内容。

**语法**

```python
def list_real_directory(directory: str = ".") -> str
```

**参数**

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|------|------|--------|------|------|
| `directory` | str | "." | 否 | 目录路径 |

**返回值**

- `str`: 目录内容列表

**使用示例**

```python
from codeviewx.tools import list_real_directory

# 列出当前目录
content = list_real_directory()

# 列出指定目录
content = list_real_directory("/path/to/project")
```

## Web API

### 端点列表

#### 1. GET /

**描述**: 获取默认文档（README.md）

**语法**

```http
GET /
```

**查询参数**

无

**响应**

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head>
    <title>文档预览</title>
</head>
<body>
    <!-- 渲染的 HTML 内容 -->
</body>
</html>
```

#### 2. GET /<filename>

**描述**: 获取指定文档文件

**语法**

```http
GET /<filename>
```

**路径参数**

| 参数 | 类型 | 描述 |
|------|------|------|
| `filename` | string | 文档文件名 |

**响应**

成功 (200 OK):
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head>
    <title>文档预览</title>
</head>
<body>
    <!-- 渲染的 HTML 内容 -->
</body>
</html>
```

文件不存在 (404 Not Found):
```http
HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=utf-8

File not found: /path/to/file
```

### 静态资源

#### CSS 文件

```http
GET /static/css/typo.css
```

**响应**

```http
HTTP/1.1 200 OK
Content-Type: text/css

/* CSS 样式内容 */
```

## 错误处理

### 错误代码

| 代码 | 描述 | 解决方案 |
|------|------|----------|
| 0 | 成功 | - |
| 1 | 一般错误 | 检查参数和环境配置 |
| 130 | 用户中断 (Ctrl+C) | 正常退出，无需处理 |
| 2 | 参数错误 | 检查命令行参数格式 |
| 3 | 文件/目录不存在 | 检查路径是否正确 |
| 4 | 权限不足 | 检查文件和目录权限 |
| 5 | API 密钥错误 | 检查环境变量配置 |

### 异常类型

#### ValueError

**描述**: 参数值无效

**示例**:

```python
try:
    generate_docs(doc_language="InvalidLanguage")
except ValueError as e:
    print(f"参数错误: {e}")
```

#### FileNotFoundError

**描述**: 文件或目录不存在

**示例**:

```python
try:
    generate_docs(working_directory="/nonexistent/path")
except FileNotFoundError as e:
    print(f"路径不存在: {e}")
```

#### PermissionError

**描述**: 权限不足

**示例**:

```python
try:
    write_real_file("/protected/file.md", "content")
except PermissionError as e:
    print(f"权限不足: {e}")
```

## 配置和环境

### 环境变量

| 变量名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `ANTHROPIC_API_KEY` | string | - | Anthropic API 密钥 |
| `OPENAI_API_KEY` | string | - | OpenAI API 密钥 |
| `CODEVIEWX_LOG_LEVEL` | string | INFO | 日志级别 |
| `CODEVIEWX_OUTPUT_DIR` | string | docs | 默认输出目录 |
| `CODEVIEWX_RECURSION_LIMIT` | integer | 1000 | 递归限制 |

### 配置文件

#### pyproject.toml

```toml
[tool.codeviewx]
default_language = "English"
default_output_dir = "docs"
default_recursion_limit = 1000
auto_detect_language = true
verbose_by_default = false

[tool.codeviewx.server]
host = "127.0.0.1"
port = 5000
debug = false

[tool.codeviewx.search]
default_max_count = 100
ignore_patterns = [".git", ".venv", "__pycache__"]
```

## 使用示例

### 完整工作流示例

```python
#!/usr/bin/env python3
"""
CodeViewX 使用示例
"""

import os
import sys
from pathlib import Path
from codeviewx import (
    generate_docs, 
    load_prompt, 
    detect_system_language,
    start_document_web_server
)

def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 生成当前目录的文档
    generate_docs()
    print("✓ 基本文档生成完成")

def example_custom_configuration():
    """自定义配置示例"""
    print("=== 自定义配置示例 ===")
    
    project_path = "/path/to/your/project"
    output_path = "custom_docs"
    
    # 检测系统语言
    language = detect_system_language()
    print(f"检测到系统语言: {language}")
    
    # 生成文档
    generate_docs(
        working_directory=project_path,
        output_directory=output_path,
        doc_language=language,
        verbose=True
    )
    print(f"✓ 自定义文档生成完成: {output_path}")

def example_batch_processing():
    """批量处理示例"""
    print("=== 批量处理示例 ===")
    
    # 项目列表
    projects = [
        "/path/to/project1",
        "/path/to/project2", 
        "/path/to/project3"
    ]
    
    # 批量生成文档
    for i, project in enumerate(projects, 1):
        print(f"处理项目 {i}/{len(projects)}: {project}")
        
        try:
            generate_docs(
                working_directory=project,
                output_directory=f"docs_project_{i}",
                doc_language="English",
                verbose=False
            )
            print(f"✓ 项目 {i} 完成")
        except Exception as e:
            print(f"✗ 项目 {i} 失败: {e}")

def example_custom_prompt():
    """自定义提示词示例"""
    print("=== 自定义提示词示例 ===")
    
    # 加载并自定义提示词
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/path/to/project",
        output_directory="docs",
        doc_language="Chinese",
        project_type="Web API",
        focus_areas=["architecture", "api", "testing"]
    )
    
    print("提示词加载完成")
    print(f"提示词长度: {len(prompt)} 字符")

def example_web_server():
    """Web 服务器示例"""
    print("=== Web 服务器示例 ===")
    
    # 先生成文档
    generate_docs(output_directory="web_docs")
    
    # 启动服务器（这会阻塞当前线程）
    print("启动 Web 服务器...")
    print("访问地址: http://127.0.0.1:5000")
    print("按 Ctrl+C 停止服务器")
    
    start_document_web_server("web_docs")

def example_error_handling():
    """错误处理示例"""
    print("=== 错误处理示例 ===")
    
    try:
        # 尝试分析不存在的目录
        generate_docs(working_directory="/nonexistent/directory")
    except FileNotFoundError as e:
        print(f"预期的错误: {e}")
    
    try:
        # 尝试使用无效的语言
        generate_docs(doc_language="InvalidLanguage")
    except ValueError as e:
        print(f"预期的错误: {e}")

if __name__ == "__main__":
    # 选择要运行的示例
    examples = {
        "1": example_basic_usage,
        "2": example_custom_configuration,
        "3": example_batch_processing,
        "4": example_custom_prompt,
        "5": example_web_server,
        "6": example_error_handling
    }
    
    print("CodeViewX API 使用示例")
    print("请选择要运行的示例:")
    for key, func in examples.items():
        print(f"{key}. {func.__name__}")
    
    choice = input("请输入选择 (1-6): ").strip()
    
    if choice in examples:
        examples[choice]()
    else:
        print("无效选择")
        sys.exit(1)
```

### 高级用法示例

```python
#!/usr/bin/env python3
"""
CodeViewX 高级用法示例
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from codeviewx import generate_docs
from codeviewx.tools import ripgrep_search, read_real_file

def advanced_project_analysis(project_path: str) -> dict:
    """高级项目分析"""
    
    analysis_result = {
        "project_path": project_path,
        "analysis_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file_count": 0,
        "python_files": 0,
        "main_functions": [],
        "class_definitions": [],
        "imports": []
    }
    
    # 搜索 Python 文件
    python_files = ripgrep_search("--type py -l .", project_path)
    analysis_result["python_files"] = len(python_files.split('\n')) if python_files else 0
    
    # 搜索主函数
    main_functions = ripgrep_search("def main|if __name__", project_path, "py")
    if main_functions:
        analysis_result["main_functions"] = main_functions.split('\n')[:10]  # 限制结果数量
    
    # 搜索类定义
    class_definitions = ripgrep_search("^class ", project_path, "py")
    if class_definitions:
        analysis_result["class_definitions"] = class_definitions.split('\n')[:10]
    
    # 搜索导入语句
    imports = ripgrep_search("^import |^from .* import", project_path, "py")
    if imports:
        analysis_result["imports"] = list(set(
            line.strip() for line in imports.split('\n')[:20]
        ))
    
    return analysis_result

def concurrent_document_generation(projects: list, max_workers: int = 3):
    """并发文档生成"""
    
    print(f"开始并发文档生成，项目数量: {len(projects)}, 最大并发: {max_workers}")
    
    def generate_single_doc(project):
        try:
            output_dir = f"docs_{project.replace('/', '_').replace('\\', '_')}"
            generate_docs(
                working_directory=project,
                output_directory=output_dir,
                doc_language="Chinese",
                verbose=False
            )
            return {"project": project, "status": "success", "output_dir": output_dir}
        except Exception as e:
            return {"project": project, "status": "error", "error": str(e)}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_project = {
            executor.submit(generate_single_doc, project): project 
            for project in projects
        }
        
        # 收集结果
        results = []
        for future in as_completed(future_to_project):
            project = future_to_project[future]
            try:
                result = future.result()
                results.append(result)
                print(f"✓ {project}: {result['status']}")
            except Exception as e:
                print(f"✗ {project}: {e}")
                results.append({
                    "project": project, 
                    "status": "error", 
                    "error": str(e)
                })
    
    return results

def custom_document_template(project_info: dict) -> str:
    """自定义文档模板"""
    
    template = f"""
# {project_info.get('name', '项目')} 技术文档

## 项目信息

- **项目名称**: {project_info.get('name', 'Unknown')}
- **项目路径**: {project_info.get('path', 'Unknown')}
- **生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **文档版本**: 1.0.0

## 项目概述

{project_info.get('description', '暂无描述')}

## 技术栈

{chr(10).join(f'- {tech}' for tech in project_info.get('tech_stack', []))}

## 快速开始

```bash
# 克隆项目
git clone {project_info.get('repository', '#')}

# 安装依赖
pip install -r requirements.txt

# 运行项目
{project_info.get('run_command', '# 查看项目说明')}
```

## 项目结构

```
{project_info.get('structure', '# 项目结构待分析')}
```

## 更多信息

- **文档目录**: docs/
- **API 文档**: docs/api/
- **开发指南**: docs/development/

---
*本文档由 CodeViewX 自动生成*
    """
    
    return template.strip()

if __name__ == "__main__":
    # 示例：高级项目分析
    print("=== 高级项目分析 ===")
    result = advanced_project_analysis("/path/to/project")
    print(f"分析结果: {result}")
    
    # 示例：并发文档生成
    print("\n=== 并发文档生成 ===")
    projects = ["/path/to/project1", "/path/to/project2", "/path/to/project3"]
    results = concurrent_document_generation(projects)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"完成: {success_count}/{len(results)} 个项目")
```

这份 API 参考文档为 CodeViewX 的所有接口提供了详细的说明，包括参数、返回值、异常处理和使用示例，帮助开发者快速集成和使用 CodeViewX 的各种功能。