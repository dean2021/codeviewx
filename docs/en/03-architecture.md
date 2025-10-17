# System Architecture

## Overview

CodeViewX follows a modular, layered architecture that combines AI-driven analysis with traditional software engineering principles. The system is designed to be extensible, maintainable, and efficient while providing powerful documentation generation capabilities.

## High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[Command Line Interface]
        WEB[Web Documentation Browser]
        API[Python API]
    end
    
    subgraph "Core Processing Layer"
        CORE[Core Engine]
        AGENT[AI Agent Orchestrator]
        LANG[LangChain Integration]
    end
    
    subgraph "Tool Layer"
        FS[File System Tools]
        SEARCH[Code Search Tools]
        CMD[Command Tools]
    end
    
    subgraph "Data Layer"
        PROMPTS[Prompt Templates]
        CONFIG[Configuration]
        CACHE[Local Cache]
    end
    
    subgraph "External Services"
        AI[AI Models<br/>Claude/OpenAI]
        RG[ripgrep System Tool]
    end
    
    CLI --> CORE
    WEB --> CORE
    API --> CORE
    
    CORE --> AGENT
    AGENT --> LANG
    
    AGENT --> FS
    AGENT --> SEARCH
    AGENT --> CMD
    
    FS --> CONFIG
    SEARCH --> RG
    LANG --> AI
    
    CORE --> PROMPTS
    CORE --> CONFIG
    
    LANG --> CACHE
```

## Component Architecture

### 1. User Interface Layer

The interface layer provides multiple ways to interact with CodeViewX:

#### Command Line Interface (CLI)
- **File**: `codeviewx/cli.py`
- **Framework**: argparse
- **Responsibilities**: 
  - Command parsing and validation
  - Argument processing
  - Error handling and user feedback
  - Mode selection (generate vs. serve)

```python
# File: codeviewx/cli.py | Line: 15-30 | Description: CLI main function
def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        prog="codeviewx",
        description="CodeViewX - AI 驱动的代码文档生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # ... argument setup
    )
```

#### Web Documentation Browser
- **File**: `codeviewx/core.py` (routes section)
- **Framework**: Flask
- **Template Engine**: Jinja2
- **Responsibilities**:
  - Document rendering and display
  - File tree navigation
  - Markdown to HTML conversion
  - Static asset serving

```python
# File: codeviewx/core.py | Line: 33-37 | Description: Web server routes
@app.route("/")
def home():
    return index("README.md")

@app.route("/<path:filename>")
def index(filename):
    # Document rendering logic
```

#### Python API
- **File**: `codeviewx/__init__.py`
- **Framework**: Native Python
- **Responsibilities**:
  - Programmatic access
  - Integration support
  - Function exports

### 2. Core Processing Layer

The core layer contains the main business logic and orchestration:

#### Core Engine
- **File**: `codeviewx/core.py`
- **Key Functions**:
  - `generate_docs()`: Main documentation generation orchestrator
  - `start_document_web_server()`: Web server initialization
  - `detect_system_language()`: Automatic language detection
  - `load_prompt()`: Prompt template management

#### AI Agent Orchestrator
- **Framework**: DeepAgents
- **Integration**: LangChain
- **Responsibilities**:
  - Tool coordination
  - Workflow management
  - Context maintenance
  - Decision making

```python
# File: codeviewx/core.py | Line: 312-330 | Description: Agent creation
# Create Agent
agent = create_deep_agent(tools, prompt)
print("✓ 已创建 AI Agent")
print(f"✓ 已注册 {len(tools)} 个自定义工具: {', '.join([t.__name__ for t in tools])}")
```

#### LangChain Integration
- **Components**:
  - PromptTemplate for dynamic prompt formatting
  - Message handling for AI communication
  - Tool binding for agent capabilities

### 3. Tool Layer

The tool layer provides specialized capabilities for the AI agent:

#### File System Tools (`tools/filesystem.py`)
- **Functions**:
  - `write_real_file()`: File writing with directory creation
  - `read_real_file()`: File reading with metadata
  - `list_real_directory()`: Directory listing with categorization

```python
# File: codeviewx/tools/filesystem.py | Line: 20-35 | Description: File writing tool
def write_real_file(file_path: str, content: str) -> str:
    """写入真实文件系统中的文件"""
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
```

#### Search Tools (`tools/search.py`)
- **Primary Function**: `ripgrep_search()`
- **Integration**: ripgrepy library
- **Features**:
  - Pattern matching with regular expressions
  - File type filtering
  - Case-insensitive search
  - Performance optimization

```python
# File: codeviewx/tools/search.py | Line: 25-45 | Description: Search implementation
def ripgrep_search(pattern: str, path: str = ".", 
                   file_type: str = None, 
                   ignore_case: bool = False,
                   max_count: int = 100) -> str:
    """使用 ripgrep 在文件中搜索文本模式（比 grep 更快）"""
    try:
        # 创建 Ripgrepy 实例
        rg = Ripgrepy(pattern, path)
        
        # 配置选项
        rg = rg.line_number()  # 显示行号
        rg = rg.with_filename()  # 显示文件名
```

#### Command Tools (`tools/command.py`)
- **Function**: `execute_command()`
- **Purpose**: System command execution
- **Features**: Output capture, error handling

### 4. Data Layer

The data layer manages configuration, templates, and caching:

#### Prompt Templates
- **Location**: `codeviewx/prompts/`
- **Templates**:
  - `DocumentEngineer.md`: Full-featured analysis prompt
  - `DocumentEngineer_compact.md`: Optimized compact version
  - `DocumentEngineer_original.md`: Original comprehensive version

#### Configuration Management
- **File**: `pyproject.toml`
- **Environment Variables**: API keys, language settings
- **Runtime Settings**: Recursion limits, output preferences

#### Caching System
- **Purpose**: Performance optimization
- **Implementation**: LangChain caching
- **Scope**: API responses, processed data

## Data Flow Architecture

### Documentation Generation Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Core
    participant Agent
    participant Tools
    participant AI
    participant FileSystem
    
    User->>CLI: codeviewx -w /project
    CLI->>Core: generate_docs()
    Core->>Core: detect_system_language()
    Core->>Core: load_prompt()
    Core->>Agent: create_deep_agent()
    
    loop Analysis Phase
        Agent->>Tools: list_real_directory()
        Tools->>FileSystem: Read project structure
        FileSystem-->>Tools: Directory listing
        Tools-->>Agent: Structure data
        
        Agent->>Tools: read_real_file()
        Tools->>FileSystem: Read configuration
        FileSystem-->>Tools: File content
        Tools-->>Agent: Configuration data
        
        Agent->>Tools: ripgrep_search()
        Tools->>AI: Search patterns
        AI-->>Tools: Search results
        Tools-->>Agent: Code analysis
    end
    
    loop Documentation Generation
        Agent->>AI: Generate documentation
        AI-->>Agent: Document content
        Agent->>Tools: write_real_file()
        Tools->>FileSystem: Save documents
        FileSystem-->>Tools: Confirmation
        Tools-->>Agent: Success status
    end
    
    Agent-->>Core: Generation complete
    Core-->>CLI: Status report
    CLI-->>User: Documentation ready
```

### Web Server Flow

```mermaid
sequenceDiagram
    participant Browser
    participant Flask
    participant Core
    participant FileSystem
    participant Markdown
    
    Browser->>Flask: GET /README.md
    Flask->>Core: index("README.md")
    Core->>FileSystem: Read README.md
    FileSystem-->>Core: File content
    Core->>Core: generate_file_tree()
    Core->>Markdown: Parse content
    Markdown-->>Core: HTML with TOC
    Core->>Flask: Render template
    Flask->>Browser: HTML response
    
    Browser->>Flask: GET static/css/style.css
    Flask->>FileSystem: Read CSS file
    FileSystem-->>Flask: CSS content
    Flask->>Browser: CSS response
```

## Component Interaction Patterns

### 1. Agent-Tool Pattern

The AI agent uses a tool-based architecture to interact with the system:

```mermaid
graph LR
    subgraph "AI Agent"
        ORCHESTRATOR[Tool Orchestrator]
        CONTEXT[Context Manager]
    end
    
    subgraph "Tool Registry"
        FS_TOOL[File System Tools]
        SEARCH_TOOL[Search Tools]
        CMD_TOOL[Command Tools]
    end
    
    subgraph "System Interface"
        FILES[File System]
        RIPGREP[ripgrep]
        SHELL[System Shell]
    end
    
    ORCHESTRATOR --> FS_TOOL
    ORCHESTRATOR --> SEARCH_TOOL
    ORCHESTRATOR --> CMD_TOOL
    
    FS_TOOL --> FILES
    SEARCH_TOOL --> RIPGREP
    CMD_TOOL --> SHELL
    
    CONTEXT --> ORCHESTRATOR
```

### 2. Plugin Architecture

The system supports extensible tool registration:

```python
# File: codeviewx/tools/__init__.py | Line: 6-16 | Description: Tool exports
from .command import execute_command
from .search import ripgrep_search
from .filesystem import write_real_file, read_real_file, list_real_directory

__all__ = [
    # 命令执行工具
    'execute_command',
    
    # 搜索工具
    'ripgrep_search',
    
    # 文件系统工具
    'write_real_file',
    'read_real_file',
    'list_real_directory',
]
```

### 3. Configuration-Driven Behavior

The system behavior is controlled through multiple configuration layers:

```mermaid
graph TD
    subgraph "Configuration Layers"
        PYPROJECT[pyproject.toml]
        ENV[Environment Variables]
        CLI_ARGS[CLI Arguments]
        RUNTIME[Runtime Settings]
    end
    
    subgraph "Configuration Consumers"
        CORE[Core Engine]
        AGENT[AI Agent]
        TOOLS[Tools]
        WEB[Web Server]
    end
    
    PYPROJECT --> CORE
    ENV --> CORE
    CLI_ARGS --> CORE
    RUNTIME --> CORE
    
    CORE --> AGENT
    CORE --> TOOLS
    CORE --> WEB
```

## Security Architecture

### 1. API Key Management

```mermaid
graph LR
    subgraph "Security Layer"
        ENV_VAR[Environment Variables]
        VAULT[Key Vault]
        CACHE[Secure Cache]
    end
    
    subgraph "Application Layer"
        CORE[Core Engine]
        LANGCHAIN[LangChain]
        AI[AI Models]
    end
    
    ENV_VAR --> CORE
    VAULT --> CORE
    CACHE --> CORE
    
    CORE --> LANGCHAIN
    LANGCHAIN --> AI
```

### 2. File System Access Control

- **Sandboxing**: Limited to specified working directory
- **Path Validation**: Prevents directory traversal attacks
- **Permission Checks**: Validates read/write permissions
- **File Type Restrictions**: Limits file access to safe types

### 3. Command Execution Security

- **Command Whitelisting**: Only allows approved commands
- **Argument Sanitization**: Prevents command injection
- **Resource Limits**: Constrains execution time and memory

## Performance Architecture

### 1. Caching Strategy

```mermaid
graph TB
    subgraph "Cache Layers"
        L1[Memory Cache]
        L2[Disk Cache]
        L3[API Response Cache]
    end
    
    subgraph "Cache Management"
        INVALIDATION[Cache Invalidation]
        EVICTION[Cache Eviction]
        METRICS[Performance Metrics]
    end
    
    L1 --> L2
    L2 --> L3
    
    INVALIDATION --> L1
    EVICTION --> L2
    METRICS --> L3
```

### 2. Parallel Processing

- **Tool Parallelization**: Multiple tools can run simultaneously
- **File Processing**: Parallel analysis of multiple files
- **API Batching**: Batch processing for AI requests

### 3. Resource Management

- **Memory Limits**: Configurable memory constraints
- **Rate Limiting**: API call throttling
- **Timeout Management**: Operation timeouts

## Scalability Architecture

### 1. Horizontal Scaling

```mermaid
graph LR
    subgraph "Load Balancer"
        LB[Load Balancer]
    end
    
    subgraph "Application Instances"
        APP1[App Instance 1]
        APP2[App Instance 2]
        APP3[App Instance N]
    end
    
    subgraph "Shared Resources"
        CACHE[Shared Cache]
        STORAGE[File Storage]
        AI_SERVICE[AI Services]
    end
    
    LB --> APP1
    LB --> APP2
    LB --> APP3
    
    APP1 --> CACHE
    APP2 --> CACHE
    APP3 --> CACHE
    
    APP1 --> STORAGE
    APP2 --> STORAGE
    APP3 --> STORAGE
    
    APP1 --> AI_SERVICE
    APP2 --> AI_SERVICE
    APP3 --> AI_SERVICE
```

### 2. Vertical Scaling

- **Resource Allocation**: Dynamic resource assignment
- **Performance Monitoring**: Real-time performance tracking
- **Auto-scaling**: Automatic capacity adjustment

## Deployment Architecture

### 1. Development Environment

```mermaid
graph TB
    subgraph "Development Machine"
        DEV_CODE[Source Code]
        VENV[Virtual Environment]
        LOCAL_AI[Local AI Models]
    end
    
    subgraph "Development Tools"
        IDE[IDE/Editor]
        DEBUGGER[Debugger]
        TESTS[Unit Tests]
    end
    
    DEV_CODE --> VENV
    VENV --> LOCAL_AI
    
    IDE --> DEV_CODE
    DEBUGGER --> DEV_CODE
    TESTS --> DEV_CODE
```

### 2. Production Environment

```mermaid
graph TB
    subgraph "Production Infrastructure"
        APP_SERVER[Application Server]
        WEB_SERVER[Web Server]
        CACHE_SERVER[Cache Server]
    end
    
    subgraph "External Services"
        AI_API[AI API Services]
        CDN[Content Delivery Network]
    end
    
    subgraph "Monitoring"
        LOGS[Logging]
        METRICS[Metrics Collection]
        ALERTS[Alerting]
    end
    
    WEB_SERVER --> APP_SERVER
    APP_SERVER --> CACHE_SERVER
    APP_SERVER --> AI_API
    
    CDN --> WEB_SERVER
    
    APP_SERVER --> LOGS
    APP_SERVER --> METRICS
    METRICS --> ALERTS
```

## Integration Architecture

### 1. AI Model Integration

```mermaid
graph LR
    subgraph "CodeViewX"
        LANGCHAIN[LangChain Layer]
        AGENT[Agent Layer]
        TOOLS[Tool Layer]
    end
    
    subgraph "AI Providers"
        ANTHROPIC[Anthropic Claude]
        OPENAI[OpenAI GPT]
        LOCAL[Local Models]
    end
    
    LANGCHAIN --> ANTHROPIC
    LANGCHAIN --> OPENAI
    LANGCHAIN --> LOCAL
    
    AGENT --> LANGCHAIN
    TOOLS --> AGENT
```

### 2. Tool Integration

```mermaid
graph TB
    subgraph "Core System"
        AGENT[AI Agent]
        REGISTRY[Tool Registry]
    end
    
    subgraph "System Tools"
        RG[ripgrep]
        FILESYSTEM[File System]
        SHELL[System Shell]
    end
    
    subgraph "Custom Tools"
        CUSTOM1[Custom Tool 1]
        CUSTOM2[Custom Tool 2]
        CUSTOMN[Custom Tool N]
    end
    
    AGENT --> REGISTRY
    REGISTRY --> RG
    REGISTRY --> FILESYSTEM
    REGISTRY --> SHELL
    REGISTRY --> CUSTOM1
    REGISTRY --> CUSTOM2
    REGISTRY --> CUSTOMN
```

## Architecture Decisions and Trade-offs

### 1. Technology Choices

| Decision | Reason | Trade-off |
|----------|--------|-----------|
| **Python 3.8+** | Rich ecosystem, AI framework support | Performance vs. development speed |
| **DeepAgents** | Specialized for AI agents | Dependency on external framework |
| **Flask** | Lightweight, flexible | Limited built-in features |
| **ripgrep** | Superior performance | System dependency required |

### 2. Design Patterns

| Pattern | Benefit | Implementation Cost |
|---------|---------|-------------------|
| **Tool-based Architecture** | Flexibility, extensibility | Increased complexity |
| **Plugin System** | Easy customization | Plugin management overhead |
| **Configuration-driven** | Runtime flexibility | Configuration complexity |

### 3. Performance Considerations

| Aspect | Approach | Impact |
|--------|----------|---------|
| **Caching** | Multi-level caching | Improved response times |
| **Parallel Processing** | Concurrent tool execution | Better resource utilization |
| **Streaming** | Real-time progress updates | Enhanced user experience |

---

*This architecture documentation provides a comprehensive view of the CodeViewX system design. For implementation details, see the [Core Mechanisms](04-core-mechanisms.md) documentation.*