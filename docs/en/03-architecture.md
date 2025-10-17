# System Architecture

## Architecture Overview

CodeViewX follows a modular, layered architecture that separates concerns between AI processing, user interface, and core functionality. The system is designed around the principle of using AI agents as the primary driver for documentation generation, with supporting modules for file operations, web serving, and user interaction.

## High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[CLI Interface]
        WEB[Web Server]
    end
    
    subgraph "Core Processing Layer"
        CORE[Core API]
        GEN[Document Generator]
        AI[AI Agent Engine]
    end
    
    subgraph "Support Layer"
        TOOLS[Custom Tools]
        PROMPT[Prompt Manager]
        I18N[Internationalization]
        LANG[Language Detection]
    end
    
    subgraph "External Services"
        ANTHROPIC[Anthropic Claude]
        RIPGREP[ripgrep]
        FILESYSTEM[File System]
    end
    
    CLI --> CORE
    WEB --> CORE
    CORE --> GEN
    GEN --> AI
    AI --> TOOLS
    AI --> PROMPT
    GEN --> I18N
    GEN --> LANG
    
    TOOLS --> RIPGREP
    TOOLS --> FILESYSTEM
    AI --> ANTHROPIC
```

## Core Components

### 1. CLI Interface (`cli.py`)

**Purpose**: Command-line interface for user interaction
**Key Functions**:
- Argument parsing and validation
- User interface language detection
- Workflow orchestration
- Error handling and user feedback

```python
# File: codeviewx/cli.py | Lines: 16-134 | Description: Main CLI entry point
def main():
    ui_lang = detect_ui_language()
    get_i18n().set_locale(ui_lang)
    
    parser = argparse.ArgumentParser(
        prog="codeviewx",
        description=t('cli_description'),
        # ... argument definitions
    )
```

### 2. Document Generator (`generator.py`)

**Purpose**: Core documentation generation engine
**Key Functions**:
- AI agent creation and management
- Documentation workflow orchestration
- Progress tracking and logging
- File output management

```python
# File: codeviewx/generator.py | Lines: 24-324 | Description: Main generation function
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    ui_language: Optional[str] = None,
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None:
```

### 3. Web Server (`server.py`)

**Purpose**: Documentation browsing interface
**Key Functions**:
- Flask web application
- Markdown rendering with extensions
- File tree generation
- Static asset serving

```python
# File: codeviewx/server.py | Lines: 105-190 | Description: Web server startup
def start_document_web_server(output_directory):
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    @app.route("/")
    def home():
        return index("README.md")
```

### 4. Internationalization (`i18n.py`)

**Purpose**: Multi-language support system
**Key Functions**:
- Message translation
- Locale detection
- Language switching
- UI string management

```python
# File: codeviewx/i18n.py | Lines: 200-325 | Description: I18n class implementation
class I18n:
    def __init__(self, locale: str = 'en'):
        self.locale = locale if locale in MESSAGES else 'en'
    
    def t(self, key: str, **kwargs) -> str:
        msg = MESSAGES.get(self.locale, {}).get(key, key)
        return msg.format(**kwargs) if kwargs else msg
```

## AI Agent Architecture

### Agent Design Pattern

CodeViewX uses the DeepAgents framework to create AI agents that can use tools for code analysis and document generation.

```mermaid
sequenceDiagram
    participant User as User
    participant CLI as CLI Interface
    participant Gen as Generator
    participant Agent as AI Agent
    participant Tools as Custom Tools
    participant Anthropic as Anthropic Claude
    
    User->>CLI: codeviewx command
    CLI->>Gen: generate_docs()
    Gen->>Agent: create_deep_agent(tools, prompt)
    Gen->>Agent: Stream task execution
    
    loop Analysis & Generation
        Agent->>Anthropic: Think about next action
        Anthropic->>Agent: Tool calls needed
        Agent->>Tools: Execute tools (read, search, write)
        Tools->>Agent: Tool results
        Agent->>Anthropic: Continue with context
    end
    
    Agent->>Gen: Completion signal
    Gen->>CLI: Success/Failure
    CLI->>User: Final output
```

### Tool System Architecture

The tool system provides AI agents with capabilities to interact with the file system and execute commands.

```mermaid
graph LR
    subgraph "AI Agent"
        AGENT[Agent Logic]
    end
    
    subgraph "Tool Interface"
        CMD[Command Tool]
        SEARCH[Search Tool]
        FS[Filesystem Tool]
    end
    
    subgraph "External Tools"
        RG[ripgrep]
        SHELL[System Shell]
        FILES[File System]
    end
    
    AGENT --> CMD
    AGENT --> SEARCH
    AGENT --> FS
    
    CMD --> SHELL
    SEARCH --> RG
    FS --> FILES
```

**Tool Implementations**:

```python
# File: codeviewx/tools/command.py | Description: System command execution
def execute_command(command: str, working_dir: str = None) -> str:
    """Execute system command and return result"""

# File: codeviewx/tools/search.py | Description: Code searching with ripgrep  
def ripgrep_search(pattern: str, path: str = ".", 
                   file_type: str = None, 
                   ignore_case: bool = False,
                   max_count: int = 100) -> str:
    """Search for text patterns in files using ripgrep"""

# File: codeviewx/tools/filesystem.py | Description: File operations
def write_real_file(file_path: str, content: str) -> str:
    """Write file to real filesystem"""

def read_real_file(file_path: str) -> str:
    """Read file content from real filesystem"""

def list_real_directory(directory: str = ".") -> str:
    """List directory contents in real filesystem"""
```

## Data Flow Architecture

### Documentation Generation Flow

```mermaid
flowchart TD
    START([Start Generation]) --> PARSE[Parse CLI Arguments]
    PARSE --> DETECT[Detect Languages]
    DETECT --> LOAD[Load Prompt Template]
    LOAD --> CREATE[Create AI Agent]
    CREATE --> REGISTER[Register Tools]
    REGISTER --> ANALYZE[Analyze Project Structure]
    
    ANALYZE --> READ_CONFIG[Read Configuration Files]
    READ_CONFIG --> SEARCH_CODE[Search Core Patterns]
    SEARCH_CODE --> READ_FILES[Read Core Files]
    READ_FILES --> GENERATE{Generate Documents}
    
    GENERATE --> README[Generate README.md]
    GENERATE --> OVERVIEW[Generate 01-overview.md]
    GENERATE --> QUICKSTART[Generate 02-quickstart.md]
    GENERATE --> ARCH[Generate 03-architecture.md]
    GENERATE --> CORE[Generate 04-core-mechanisms.md]
    
    README --> COMPLETE[Generation Complete]
    OVERVIEW --> COMPLETE
    QUICKSTART --> COMPLETE
    ARCH --> COMPLETE
    CORE --> COMPLETE
    
    COMPLETE --> SERVE{Start Web Server?}
    SERVE -->|Yes| WEB[Start Flask Server]
    SERVE -->|No| END([End])
    WEB --> END
```

### Web Server Request Flow

```mermaid
sequenceDiagram
    participant Browser as Browser
    participant Flask as Flask App
    participant Renderer as Markdown Renderer
    participant FileSystem as File System
    
    Browser->>Flask: GET /README.md
    Flask->>FileSystem: Read README.md
    FileSystem->>Flask: File content
    Flask->>Renderer: Render markdown with extensions
    Renderer->>Flask: HTML content
    Flask->>Browser: HTML response with template
    
    Browser->>Flask: GET /static/css/style.css
    Flask->>Browser: Static CSS file
```

## Configuration Architecture

### Configuration Sources (Priority Order)

1. **Command Line Arguments** - Highest priority
2. **Environment Variables** - Medium priority  
3. **Default Values** - Lowest priority

```mermaid
graph TD
    subgraph "Configuration Sources"
        CLI_ARGS[CLI Arguments]
        ENV_VARS[Environment Variables]
        DEFAULTS[Default Values]
    end
    
    subgraph "Configuration Processing"
        PARSER[Argument Parser]
        VALIDATOR[Configuration Validator]
        MERGER[Configuration Merger]
    end
    
    subgraph "Configuration Output"
        FINAL_CONFIG[Final Configuration]
    end
    
    CLI_ARGS --> PARSER
    ENV_VARS --> PARSER
    DEFAULTS --> PARSER
    
    PARSER --> VALIDATOR
    VALIDATOR --> MERGER
    MERGER --> FINAL_CONFIG
```

## Error Handling Architecture

### Exception Handling Strategy

```python
# File: codeviewx/cli.py | Lines: 108-126 | Description: CLI error handling
try:
    # Main execution logic
    if args.serve:
        start_document_web_server(args.output_directory)
    else:
        generate_docs(...)
        
except KeyboardInterrupt:
    print("\n\n⚠️  User interrupted", file=sys.stderr)
    sys.exit(130)
except Exception as e:
    print(f"\n❌ Error: {e}", file=sys.stderr)
    if args.verbose:
        import traceback
        traceback.print_exc()
    sys.exit(1)
```

### Error Recovery Mechanisms

1. **Graceful Degradation**: Continue with partial functionality when possible
2. **User Guidance**: Provide clear error messages and solutions
3. **Debug Mode**: Verbose logging for troubleshooting
4. **Safe Defaults**: Fallback to default configurations

## Performance Architecture

### Optimization Strategies

1. **Streaming Processing**: Process documentation generation in chunks
2. **Lazy Loading**: Load files and resources only when needed
3. **Caching**: Cache file system operations and search results
4. **Parallel Processing**: Execute independent operations concurrently

### Memory Management

```mermaid
graph LR
    subgraph "Memory Management"
        INPUT[Input Processing]
        BUFFER[Stream Buffer]
        OUTPUT[Output Writing]
    end
    
    subgraph "AI Processing"
        CONTEXT[Context Window]
        CHUNKS[Text Chunks]
        PROMPTS[Prompt Templates]
    end
    
    INPUT --> BUFFER
    BUFFER --> CONTEXT
    CONTEXT --> CHUNKS
    CHUNKS --> OUTPUT
```

## Security Architecture

### Security Considerations

1. **Input Validation**: Validate all user inputs and file paths
2. **Sandboxing**: Limit AI agent tool access to specified directories
3. **API Key Protection**: Secure handling of API credentials
4. **File Access Control**: Restrict file system access patterns

### Security Implementation

```python
# File: codeviewx/tools/filesystem.py | Security controls in file operations
def write_real_file(file_path: str, content: str) -> str:
    # Path validation and sanitization
    # Output directory restriction
    # Content validation
```

## Extensibility Architecture

### Plugin System Design

CodeViewX is designed to be extensible through:

1. **Custom Tools**: Add new tools for AI agents
2. **Prompt Templates**: Modify AI behavior through prompts
3. **Output Formats**: Support new documentation formats
4. **Language Support**: Add new languages for internationalization

### Extension Points

```mermaid
graph TB
    subgraph "Core System"
        AI_ENGINE[AI Engine]
        TOOL_SYSTEM[Tool System]
        OUTPUT_RENDERER[Output Renderer]
    end
    
    subgraph "Extension Points"
        CUSTOM_TOOLS[Custom Tools]
        PROMPTS[Prompt Templates]
        FORMATS[Output Formats]
        LANGUAGES[Language Packs]
    end
    
    AI_ENGINE -.-> PROMPTS
    TOOL_SYSTEM -.-> CUSTOM_TOOLS
    OUTPUT_RENDERER -.-> FORMATS
    I18N -.-> LANGUAGES
```

---

*Next: [Core Mechanisms](04-core-mechanisms.md) - Deep dive into implementation details*