# 数据模型

## 概述

CodeViewX 作为一个文档生成工具，其数据模型主要围绕配置管理、文档结构和工具交互展开。本文档详细描述了系统中使用的主要数据结构、配置模式和接口规范。

## 配置数据模型

### 1. 项目配置模型

#### pyproject.toml 配置结构

```toml
# 项目基本配置
[project]
name = "codeviewx"
version = "0.1.0"
description = "AI 驱动的代码文档生成器"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "CodeViewX Team"}
]
keywords = [
    "documentation", 
    "ai", 
    "code-analysis", 
    "deepagents", 
    "langchain"
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    # ... 更多分类器
]

# 依赖配置
dependencies = [
    "langchain>=0.3.27",
    "deepagents>=0.0.5",
    "ripgrepy>=2.0.0",
    "flask>=2.0.0",
    "markdown>=3.4.0",
]

# 开发依赖
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "flake8>=6.0",
    "mypy>=1.0",
    "isort>=5.0",
]

# 命令行入口
[project.scripts]
codeviewx = "codeviewx.cli:main"

# 工具配置
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
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v"
```

#### 配置数据模型类

```python
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from pathlib import Path

@dataclass
class ProjectConfig:
    """项目配置数据模型"""
    name: str
    version: str
    description: str
    readme: Optional[str] = None
    requires_python: Optional[str] = None
    license: Optional[str] = None
    authors: Optional[List[Dict[str, str]]] = None
    keywords: Optional[List[str]] = None
    classifiers: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None
    optional_dependencies: Optional[Dict[str, List[str]]] = None
    scripts: Optional[Dict[str, str]] = None

@dataclass
class ToolConfig:
    """工具配置数据模型"""
    black_line_length: int = 100
    isort_profile: str = "black"
    isort_line_length: int = 100
    mypy_python_version: str = "3.8"
    pytest_testpaths: List[str] = None
    pytest_python_files: List[str] = None
```

### 2. 运行时配置模型

```python
@dataclass
class RuntimeConfig:
    """运行时配置数据模型"""
    working_directory: Path
    output_directory: Path
    doc_language: str
    recursion_limit: int = 1000
    verbose: bool = False
    api_key: Optional[str] = None
    model_name: Optional[str] = None
    
    def __post_init__(self):
        """配置验证和默认值设置"""
        if not self.working_directory.exists():
            raise ValueError(f"工作目录不存在: {self.working_directory}")
        
        if self.doc_language not in [
            'Chinese', 'English', 'Japanese', 'Korean', 
            'French', 'German', 'Spanish', 'Russian'
        ]:
            raise ValueError(f"不支持的语言: {self.doc_language}")
        
        # 确保输出目录存在
        self.output_directory.mkdir(parents=True, exist_ok=True)
```

## 文档数据模型

### 1. 文档结构模型

```python
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class DocumentType(Enum):
    """文档类型枚举"""
    README = "README.md"
    OVERVIEW = "01-overview.md"
    QUICKSTART = "02-quickstart.md"
    ARCHITECTURE = "03-architecture.md"
    CORE_MECHANISMS = "04-core-mechanisms.md"
    DATA_MODELS = "05-data-models.md"
    API_REFERENCE = "06-api-reference.md"
    DEVELOPMENT_GUIDE = "07-development-guide.md"
    TESTING = "08-testing.md"

@dataclass
class DocumentMetadata:
    """文档元数据"""
    title: str
    description: str
    file_name: str
    document_type: DocumentType
    order: int
    required: bool = True
    estimated_size: Optional[int] = None  # 预估字符数
    generation_time: Optional[float] = None  # 生成耗时（秒）

@dataclass
class DocumentSection:
    """文档章节模型"""
    title: str
    level: int  # 标题级别 1-6
    content: str
    subsections: List['DocumentSection'] = None
    
    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []

@dataclass
class Document:
    """完整文档模型"""
    metadata: DocumentMetadata
    sections: List[DocumentSection]
    toc: Optional[str] = None  # 目录内容
    raw_content: Optional[str] = None  # 原始 Markdown 内容
    
    def add_section(self, section: DocumentSection):
        """添加章节"""
        self.sections.append(section)
    
    def get_section_by_title(self, title: str) -> Optional[DocumentSection]:
        """根据标题查找章节"""
        for section in self.sections:
            if section.title == title:
                return section
            # 递归查找子章节
            found = self.get_section_by_title_recursive(section, title)
            if found:
                return found
        return None
    
    def get_section_by_title_recursive(self, parent: DocumentSection, title: str) -> Optional[DocumentSection]:
        """递归查找章节"""
        for subsection in parent.subsections:
            if subsection.title == title:
                return subsection
            found = self.get_section_by_title_recursive(subsection, title)
            if found:
                return found
        return None
```

### 2. 文档模板模型

```python
@dataclass
class TemplateVariable:
    """模板变量模型"""
    name: str
    value: str
    required: bool = True
    description: Optional[str] = None

@dataclass
class DocumentTemplate:
    """文档模板模型"""
    name: str
    template_path: Path
    variables: List[TemplateVariable]
    output_pattern: str  # 输出文件名模式
    
    def render(self, variables: Dict[str, str]) -> str:
        """渲染模板"""
        # 模板渲染逻辑
        pass

# 预定义的文档模板
DOCUMENT_TEMPLATES = {
    "README": DocumentTemplate(
        name="README",
        template_path=Path("templates/README.md.template"),
        variables=[
            TemplateVariable("project_name", "", True, "项目名称"),
            TemplateVariable("description", "", True, "项目描述"),
            TemplateVariable("version", "", True, "版本号"),
        ],
        output_pattern="README.md"
    ),
    "OVERVIEW": DocumentTemplate(
        name="OVERVIEW",
        template_path=Path("templates/01-overview.md.template"),
        variables=[
            TemplateVariable("tech_stack", "", True, "技术栈"),
            TemplateVariable("project_structure", "", True, "项目结构"),
        ],
        output_pattern="01-overview.md"
    )
}
```

## 工具数据模型

### 1. 工具调用模型

```python
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class ToolStatus(Enum):
    """工具执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

@dataclass
class ToolParameter:
    """工具参数模型"""
    name: str
    type: str  # "string", "integer", "boolean", "array", "object"
    required: bool = True
    default_value: Any = None
    description: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None

@dataclass
class ToolCall:
    """工具调用模型"""
    tool_name: str
    parameters: Dict[str, Any]
    call_id: Optional[str] = None
    timestamp: Optional[float] = None
    status: ToolStatus = ToolStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

@dataclass
class ToolDefinition:
    """工具定义模型"""
    name: str
    description: str
    parameters: List[ToolParameter]
    function: callable
    category: str  # "filesystem", "search", "command", "utility"
    timeout: int = 30  # 超时时间（秒）
    retry_count: int = 0  # 重试次数
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """验证参数有效性"""
        for param in self.parameters:
            if param.required and param.name not in parameters:
                return False
            # 添加更多验证逻辑
        return True
```

### 2. 搜索结果模型

```python
@dataclass
class SearchResult:
    """搜索结果模型"""
    file_path: str
    line_number: int
    content: str
    match_text: str
    context_before: List[str] = None
    context_after: List[str] = None
    
    def __post_init__(self):
        if self.context_before is None:
            self.context_before = []
        if self.context_after is None:
            self.context_after = []

@dataclass
class SearchQuery:
    """搜索查询模型"""
    pattern: str
    path: str = "."
    file_type: Optional[str] = None
    ignore_case: bool = False
    max_count: int = 100
    context_lines: int = 0
    
    def to_command_args(self) -> List[str]:
        """转换为命令行参数"""
        args = [self.pattern, self.path]
        if self.file_type:
            args.extend(["--type", self.file_type])
        if self.ignore_case:
            args.append("--ignore-case")
        args.extend(["--max-count", str(self.max_count)])
        if self.context_lines > 0:
            args.extend(["--context", str(self.context_lines)])
        return args
```

## 任务管理数据模型

### 1. 任务跟踪模型

```python
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """任务模型"""
    id: str
    content: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    updated_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    dependencies: List[str] = None  # 依赖的任务ID
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.dependencies is None:
            self.dependencies = []
        if self.metadata is None:
            self.metadata = {}
    
    def start(self):
        """开始任务"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self.updated_at = datetime.now()
    
    def complete(self):
        """完成任务"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def fail(self, error_message: str = None):
        """任务失败"""
        self.status = TaskStatus.FAILED
        self.updated_at = datetime.now()
        if error_message:
            self.metadata['error'] = error_message

@dataclass
class TaskList:
    """任务列表模型"""
    tasks: List[Task]
    name: str
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def add_task(self, task: Task):
        """添加任务"""
        self.tasks.append(task)
        self.updated_at = datetime.now()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """根据状态获取任务"""
        return [task for task in self.tasks if task.status == status]
    
    def get_progress(self) -> Dict[str, int]:
        """获取进度统计"""
        total = len(self.tasks)
        completed = len(self.get_tasks_by_status(TaskStatus.COMPLETED))
        in_progress = len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS))
        failed = len(self.get_tasks_by_status(TaskStatus.FAILED))
        pending = len(self.get_tasks_by_status(TaskStatus.PENDING))
        
        return {
            'total': total,
            'completed': completed,
            'in_progress': in_progress,
            'failed': failed,
            'pending': pending,
            'progress_percentage': (completed / total * 100) if total > 0 else 0
        }
```

## Web 服务数据模型

### 1. 文件树模型

```python
@dataclass
class FileNode:
    """文件树节点模型"""
    name: str
    path: str
    type: str  # "file", "directory"
    file_type: str = "file"  # "markdown", "code", "image", etc.
    display_name: str = ""
    active: bool = False
    children: List['FileNode'] = None
    size: Optional[int] = None
    modified_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.display_name == "":
            self.display_name = self.name
        if self.children is None:
            self.children = []
    
    def add_child(self, child: 'FileNode'):
        """添加子节点"""
        self.children.append(child)
    
    def is_leaf(self) -> bool:
        """是否是叶子节点"""
        return len(self.children) == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'name': self.name,
            'path': self.path,
            'type': self.type,
            'file_type': self.file_type,
            'display_name': self.display_name,
            'active': self.active,
            'size': self.size,
            'modified_time': self.modified_time.isoformat() if self.modified_time else None,
            'children': [child.to_dict() for child in self.children]
        }

@dataclass
class FileTree:
    """文件树模型"""
    root: FileNode
    base_path: Path
    
    def get_node_by_path(self, path: str) -> Optional[FileNode]:
        """根据路径获取节点"""
        if path == "" or path == self.root.path:
            return self.root
        
        path_parts = path.split('/')
        current_node = self.root
        
        for part in path_parts:
            found = False
            for child in current_node.children:
                if child.name == part:
                    current_node = child
                    found = True
                    break
            if not found:
                return None
        
        return current_node
    
    def flatten(self) -> List[FileNode]:
        """展平文件树"""
        result = []
        
        def traverse(node: FileNode):
            result.append(node)
            for child in node.children:
                traverse(child)
        
        traverse(self.root)
        return result
```

### 2. Web 请求/响应模型

```python
@dataclass
class DocumentRequest:
    """文档请求模型"""
    filename: str
    output_directory: str
    
    def validate(self) -> bool:
        """验证请求参数"""
        if not self.filename:
            return False
        if not self.output_directory:
            return False
        return True

@dataclass
class DocumentResponse:
    """文档响应模型"""
    success: bool
    content: Optional[str] = None
    file_tree: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def success_response(cls, content: str, file_tree: List[Dict[str, Any]]) -> 'DocumentResponse':
        """创建成功响应"""
        return cls(
            success=True,
            content=content,
            file_tree=file_tree
        )
    
    @classmethod
    def error_response(cls, error: str) -> 'DocumentResponse':
        """创建错误响应"""
        return cls(
            success=False,
            error=error
        )
```

## 分析结果数据模型

### 1. 项目分析模型

```python
@dataclass
class ProjectAnalysis:
    """项目分析结果模型"""
    project_path: Path
    project_name: str
    project_type: str  # "web", "cli", "library", "api"
    language: str  # 主要编程语言
    frameworks: List[str]  # 使用的框架
    dependencies: List[str]  # 主要依赖
    file_count: int
    line_count: int
    directory_structure: Dict[str, Any]
    analysis_time: datetime
    
    def to_summary(self) -> str:
        """生成分析摘要"""
        return f"""
项目分析结果：
- 项目名称: {self.project_name}
- 项目类型: {self.project_type}
- 主要语言: {self.language}
- 框架: {', '.join(self.frameworks) if self.frameworks else '无'}
- 文件数量: {self.file_count}
- 代码行数: {self.line_count}
- 分析时间: {self.analysis_time.strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()

@dataclass
class CodeStructure:
    """代码结构模型"""
    classes: List[Dict[str, Any]]
    functions: List[Dict[str, Any]]
    modules: List[Dict[str, Any]]
    imports: List[str]
    exports: List[str]
    
    def get_complexity_score(self) -> float:
        """计算复杂度分数"""
        class_count = len(self.classes)
        function_count = len(self.functions)
        module_count = len(self.modules)
        
        # 简单的复杂度计算公式
        return (class_count * 2 + function_count * 1 + module_count * 0.5) / 10
```

### 2. 质量评估模型

```python
@dataclass
class QualityMetrics:
    """代码质量指标模型"""
    coverage_percentage: float  # 测试覆盖率
    maintainability_index: float  # 可维护性指数
    complexity_score: float  # 复杂度分数
    documentation_score: float  # 文档完整性分数
    dependency_health: float  # 依赖健康度
    
    def get_overall_score(self) -> float:
        """获取总体质量分数"""
        return (
            self.coverage_percentage * 0.3 +
            self.maintainability_index * 0.25 +
            (100 - self.complexity_score) * 0.2 +
            self.documentation_score * 0.15 +
            self.dependency_health * 0.1
        )
    
    def get_recommendations(self) -> List[str]:
        """获取改进建议"""
        recommendations = []
        
        if self.coverage_percentage < 80:
            recommendations.append("建议增加测试覆盖率到80%以上")
        
        if self.maintainability_index < 70:
            recommendations.append("建议重构代码提高可维护性")
        
        if self.complexity_score > 50:
            recommendations.append("建议降低代码复杂度")
        
        if self.documentation_score < 60:
            recommendations.append("建议完善代码文档")
        
        if self.dependency_health < 70:
            recommendations.append("建议更新或替换不健康的依赖")
        
        return recommendations
```

## 数据验证和序列化

### 1. 数据验证器

```python
from typing import Any, Dict, List
import re
from pathlib import Path

class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_project_name(name: str) -> bool:
        """验证项目名称"""
        if not name or len(name.strip()) == 0:
            return False
        # 项目名称只能包含字母、数字、连字符和下划线
        pattern = r'^[a-zA-Z0-9_-]+$'
        return re.match(pattern, name) is not None
    
    @staticmethod
    def validate_path(path: str) -> bool:
        """验证路径"""
        try:
            Path(path)
            return True
        except (OSError, ValueError):
            return False
    
    @staticmethod
    def validate_language(language: str) -> bool:
        """验证语言代码"""
        supported_languages = [
            'Chinese', 'English', 'Japanese', 'Korean',
            'French', 'German', 'Spanish', 'Russian'
        ]
        return language in supported_languages
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱地址"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

class ValidationError(Exception):
    """数据验证错误"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"验证失败 [{field}]: {message}")
```

### 2. 序列化工具

```python
import json
from datetime import datetime
from typing import Any, Dict

class JSONEncoder(json.JSONEncoder):
    """自定义JSON编码器"""
    
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Path):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

class DataSerializer:
    """数据序列化工具"""
    
    @staticmethod
    def serialize_to_json(data: Any) -> str:
        """序列化为JSON"""
        return json.dumps(data, cls=JSONEncoder, ensure_ascii=False, indent=2)
    
    @staticmethod
    def deserialize_from_json(json_str: str) -> Any:
        """从JSON反序列化"""
        return json.loads(json_str)
    
    @staticmethod
    def serialize_document(document: Document) -> Dict[str, Any]:
        """序列化文档对象"""
        return {
            'metadata': {
                'title': document.metadata.title,
                'description': document.metadata.description,
                'file_name': document.metadata.file_name,
                'document_type': document.metadata.document_type.value,
                'order': document.metadata.order,
                'required': document.metadata.required
            },
            'sections': [
                {
                    'title': section.title,
                    'level': section.level,
                    'content': section.content,
                    'subsections': [
                        {
                            'title': sub.title,
                            'level': sub.level,
                            'content': sub.content
                        }
                        for sub in section.subsections
                    ]
                }
                for section in document.sections
            ]
        }
```

## 数据存储模型

### 1. 缓存模型

```python
from typing import Any, Optional
from datetime import datetime, timedelta
import hashlib

@dataclass
class CacheEntry:
    """缓存条目模型"""
    key: str
    value: Any
    created_at: datetime
    expires_at: Optional[datetime] = None
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def access(self) -> Any:
        """访问缓存条目"""
        self.access_count += 1
        self.last_accessed = datetime.now()
        return self.value

class Cache:
    """简单内存缓存"""
    
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
    
    def generate_key(self, *args, **kwargs) -> str:
        """生成缓存键"""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """设置缓存"""
        expires_at = None
        if ttl:
            expires_at = datetime.now() + timedelta(seconds=ttl)
        
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=datetime.now(),
            expires_at=expires_at
        )
        self._cache[key] = entry
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if entry.is_expired():
            del self._cache[key]
            return None
        
        return entry.access()
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()
    
    def cleanup_expired(self):
        """清理过期缓存"""
        expired_keys = [
            key for key, entry in self._cache.items() 
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self._cache[key]
```

这些数据模型为 CodeViewX 提供了完整的数据结构基础，支持配置管理、文档生成、工具交互、任务跟踪等各个方面的功能需求。通过类型化的数据模型，系统具备了良好的可维护性和扩展性。