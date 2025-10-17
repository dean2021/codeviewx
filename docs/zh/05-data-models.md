# 数据模型

本文档详细描述 CodeViewX 系统中的数据模型、配置结构和数据流设计。

## 核心数据模型

### 1. 配置模型

#### CLI 配置模型
**文件位置**: `codeviewx/cli.py`

```python
# CLI 参数配置结构
class CLIConfig:
    working_directory: Optional[str]      # 项目工作目录
    output_directory: str                 # 文档输出目录
    doc_language: Optional[str]           # 文档语言
    ui_language: Optional[str]            # 界面语言
    recursion_limit: int                  # 递归限制
    verbose: bool                         # 详细日志
    serve: bool                           # 服务模式
```

**默认值配置**:
```python
DEFAULT_CONFIG = {
    'working_directory': None,           # 当前目录
    'output_directory': 'docs',          # docs 目录
    'doc_language': None,                # 自动检测
    'ui_language': None,                 # 自动检测
    'recursion_limit': 1000,             # 1000 步递归限制
    'verbose': False,                    # 简洁输出
    'serve': False                       # 生成模式
}
```

#### 生成器配置模型
**文件位置**: `codeviewx/generator.py`

```python
# 生成器配置结构
class GeneratorConfig:
    working_directory: str               # 工作目录路径
    output_directory: str                # 输出目录路径
    doc_language: str                    # 文档语言
    ui_language: str                     # 界面语言
    doc_language_source: str             # 文档语言来源
    ui_language_source: str              # 界面语言来源
    recursion_limit: int                 # 递归限制
    verbose: bool                        # 详细日志
    log_level: int                       # 日志级别
```

### 2. 文档数据模型

#### 文档元数据模型
```python
# 文档元数据结构
class DocumentMetadata:
    title: str                           # 文档标题
    filename: str                        # 文件名
    file_path: str                       # 完整路径
    language: str                        # 文档语言
    generated_at: datetime               # 生成时间
    file_size: int                       # 文件大小
    sections: List[str]                  # 章节列表
    toc: str                             # 目录内容
```

#### 文档内容模型
```python
# 文档内容结构
class DocumentContent:
    metadata: DocumentMetadata           # 元数据
    raw_content: str                     # 原始 Markdown 内容
    html_content: str                    # 渲染后的 HTML
    sections: List[DocumentSection]      # 章节列表
    references: List[str]                # 引用链接
    code_blocks: List[CodeBlock]         # 代码块列表
```

#### 章节模型
```python
# 章节结构
class DocumentSection:
    level: int                           # 章节级别 (1-6)
    title: str                           # 章节标题
    anchor: str                          # 锚点 ID
    content: str                         # 章节内容
    subsections: List['DocumentSection'] # 子章节
```

### 3. 项目分析模型

#### 项目信息模型
```python
# 项目信息结构
class ProjectInfo:
    name: str                            # 项目名称
    version: str                         # 项目版本
    description: str                     # 项目描述
    language: str                        # 主要编程语言
    frameworks: List[str]                # 使用框架
    dependencies: List[Dependency]       # 依赖列表
    file_count: int                      # 文件数量
    line_count: int                      # 代码行数
    directory_structure: Dict            # 目录结构
```

#### 依赖模型
```python
# 依赖信息结构
class Dependency:
    name: str                            # 依赖名称
    version: str                         # 版本号
    type: str                            # 依赖类型 (runtime/dev)
    source: str                          # 来源 (pip/npm/maven等)
```

### 4. 工具调用模型

#### 工具请求模型
```python
# 工具调用请求
class ToolCallRequest:
    tool_name: str                       # 工具名称
    arguments: Dict[str, Any]            # 调用参数
    call_id: str                         # 调用 ID
    timestamp: datetime                  # 调用时间
```

#### 工具响应模型
```python
# 工具调用响应
class ToolCallResponse:
    call_id: str                         # 调用 ID
    tool_name: str                       # 工具名称
    success: bool                        # 执行状态
    result: Any                          # 执行结果
    error: Optional[str]                 # 错误信息
    execution_time: float                # 执行时间
    timestamp: datetime                  # 响应时间
```

## 配置数据结构

### 1. pyproject.toml 配置解析

```toml
[project]
name = "codeviewx"
version = "0.1.0"
description = "AI-powered code documentation generator"
requires-python = ">=3.8"
license = {text = "GPL-3.0-or-later"}

dependencies = [
    "langchain>=0.3.27",
    "langchain-anthropic>=0.3.22",
    "deepagents>=0.0.5",
    "ripgrepy>=2.0.0",
    "flask>=2.0.0",
    "markdown>=3.4.0",
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

[project.scripts]
codeviewx = "codeviewx.cli:main"
```

**配置模型映射**:
```python
class PyProjectConfig:
    name: str
    version: str
    description: str
    requires_python: str
    license: str
    dependencies: List[str]
    dev_dependencies: List[str]
    scripts: Dict[str, str]
```

### 2. 国际化数据模型

#### 消息数据结构
**文件位置**: `codeviewx/i18n.py`

```python
# 国际化消息结构
MESSAGES: Dict[str, Dict[str, str]] = {
    'en': {
        # 生成器消息
        'starting': '🚀 Starting CodeViewX Documentation Generator',
        'working_dir': '📂 Working Directory',
        'output_dir': '📝 Output Directory',
        # ... 更多消息
    },
    'zh': {
        # 生成器消息
        'starting': '🚀 启动 CodeViewX 文档生成器',
        'working_dir': '📂 工作目录',
        'output_dir': '📝 输出目录',
        # ... 更多消息
    }
}
```

#### 语言配置模型
```python
# 语言配置结构
class LanguageConfig:
    code: str                            # 语言代码 (en/zh)
    name: str                            # 语言名称 (English/Chinese)
    messages: Dict[str, str]             # 消息字典
    date_format: str                     # 日期格式
    number_format: str                   # 数字格式
```

## 文件系统数据模型

### 1. 文件树模型

```python
# 文件树节点
class FileTreeNode:
    name: str                            # 文件/目录名
    path: str                            # 相对路径
    type: str                            # 类型 (file/directory)
    size: Optional[int]                  # 文件大小
    modified_time: Optional[datetime]    # 修改时间
    children: List['FileTreeNode']       # 子节点
    parent: Optional['FileTreeNode']     # 父节点
```

### 2. 搜索结果模型

```python
# 搜索结果项
class SearchResultItem:
    file_path: str                       # 文件路径
    line_number: int                     # 行号
    line_content: str                    # 行内容
    match_start: int                     # 匹配开始位置
    match_end: int                       # 匹配结束位置
    context_before: str                  # 前置上下文
    context_after: str                   # 后置上下文
```

```python
# 搜索结果集合
class SearchResults:
    pattern: str                         # 搜索模式
    search_path: str                     # 搜索路径
    file_type: Optional[str]             # 文件类型过滤
    total_matches: int                   # 总匹配数
    items: List[SearchResultItem]        # 匹配项列表
    truncated: bool                      # 是否截断
```

## Web 服务器数据模型

### 1. 请求模型

```python
# HTTP 请求模型
class DocumentRequest:
    filename: str                        # 请求的文件名
    file_path: str                       # 完整文件路径
    file_exists: bool                    # 文件是否存在
    is_markdown: bool                    # 是否为 Markdown 文件
    request_time: datetime               # 请求时间
    user_agent: str                      # 用户代理
```

### 2. 响应模型

```python
# HTTP 响应模型
class DocumentResponse:
    status_code: int                     # HTTP 状态码
    content_type: str                    # 内容类型
    content: str                         # 响应内容
    file_tree: List[FileTreeItem]        # 文件树数据
    metadata: Dict[str, Any]             # 元数据
    generation_time: float               # 生成时间
```

### 3. 文件树项模型

```python
# 文件树项结构
class FileTreeItem:
    name: str                            # 文件名
    display_name: str                    # 显示名称
    path: str                            # 相对路径
    type: str                            # 类型 (markdown/file)
    active: bool                         # 是否为当前文件
    title: Optional[str]                 # 文档标题
    size: Optional[int]                  # 文件大小
```

## AI 代理数据模型

### 1. 消息模型

```python
# AI 消息基类
class BaseMessage:
    content: str                         # 消息内容
    timestamp: datetime                  # 时间戳
    message_id: str                      # 消息 ID
    metadata: Dict[str, Any]             # 元数据
```

```python
# 用户消息
class UserMessage(BaseMessage):
    role: str = "user"                   # 消息角色
```

```python
# AI 消息
class AIMessage(BaseMessage):
    role: str = "assistant"              # 消息角色
    tool_calls: List[ToolCallRequest]    # 工具调用
    reasoning: Optional[str]             # 推理过程
```

```python
# 工具消息
class ToolMessage(BaseMessage):
    tool_call_id: str                    # 工具调用 ID
    tool_name: str                       # 工具名称
    success: bool                        # 执行状态
    result: Any                          # 执行结果
```

### 2. 任务模型

```python
# 任务项模型
class TodoItem:
    content: str                         # 任务内容
    status: str                          # 状态 (pending/in_progress/completed)
    priority: int                        # 优先级
    created_at: datetime                 # 创建时间
    updated_at: datetime                 # 更新时间
    dependencies: List[str]              # 依赖任务
```

```python
# 任务列表模型
class TodoList:
    items: List[TodoItem]                # 任务项列表
    created_at: datetime                 # 创建时间
    updated_at: datetime                 # 更新时间
    completed_count: int                 # 完成数量
    total_count: int                     # 总数量
```

## 数据验证模型

### 1. 配置验证

```python
# 配置验证规则
class ConfigValidator:
    @staticmethod
    def validate_working_directory(path: str) -> bool:
        """验证工作目录"""
        return os.path.exists(path) and os.path.isdir(path)
    
    @staticmethod
    def validate_output_directory(path: str) -> bool:
        """验证输出目录"""
        return isinstance(path, str) and len(path) > 0
    
    @staticmethod
    def validate_language(lang: str) -> bool:
        """验证语言代码"""
        valid_languages = [
            'Chinese', 'English', 'Japanese', 
            'Korean', 'French', 'German', 'Spanish', 'Russian'
        ]
        return lang in valid_languages
```

### 2. 文件验证

```python
# 文件验证规则
class FileValidator:
    @staticmethod
    def is_safe_path(path: str, base_path: str) -> bool:
        """验证路径安全性"""
        try:
            abs_path = os.path.abspath(path)
            abs_base = os.path.abspath(base_path)
            return abs_path.startswith(abs_base)
        except:
            return False
    
    @staticmethod
    def is_text_file(file_path: str) -> bool:
        """判断是否为文本文件"""
        text_extensions = {
            '.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c',
            '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.html',
            '.css', '.scss', '.less', '.sql', '.sh', '.bat'
        }
        _, ext = os.path.splitext(file_path)
        return ext.lower() in text_extensions
```

## 数据持久化模型

### 1. 缓存模型

```python
# 缓存项
class CacheItem:
    key: str                             # 缓存键
    value: Any                           # 缓存值
    created_at: datetime                 # 创建时间
    accessed_at: datetime                # 访问时间
    ttl: int                            # 生存时间
    size: int                            # 数据大小
```

```python
# 缓存管理器
class CacheManager:
    cache: Dict[str, CacheItem]          # 缓存存储
    max_size: int                        # 最大大小
    max_items: int                       # 最大项目数
    eviction_policy: str                 # 淘汰策略
```

### 2. 日志模型

```python
# 日志项
class LogEntry:
    timestamp: datetime                  # 时间戳
    level: str                           # 日志级别
    logger_name: str                     # 日志器名称
    message: str                         # 日志消息
    module: str                          # 模块名称
    function: str                        # 函数名称
    line_number: int                     # 行号
    extra: Dict[str, Any]                # 额外信息
```

## 数据转换模型

### 1. 格式转换

```python
# Markdown 转换器
class MarkdownConverter:
    def to_html(self, content: str) -> str:
        """Markdown 转 HTML"""
        pass
    
    def to_json(self, content: str) -> Dict:
        """Markdown 转 JSON 结构"""
        pass
    
    def extract_metadata(self, content: str) -> Dict:
        """提取元数据"""
        pass
```

### 2. 数据序列化

```python
# 序列化配置
class SerializationConfig:
    format: str                          # 序列化格式 (json/yaml/pickle)
    encoding: str                        # 字符编码
    indent: Optional[int]                # 缩进
    sort_keys: bool                      # 键排序
```

这些数据模型构成了 CodeViewX 系统的核心数据结构，确保了数据的一致性、完整性和可维护性。每个模型都有明确的职责和约束，支持系统的稳定运行和扩展。