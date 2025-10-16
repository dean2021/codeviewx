# Prompt Template 使用指南

## 概述

`load_prompt()` 函数使用 **LangChain 的 PromptTemplate** 来加载和格式化系统提示词，支持动态变量替换。

## 改进优势

### 之前的实现
```python
def load_prompt(name):
    """简单读取文件"""
    with open(f"prompt/{name}.md", "r") as f:
        return f.read()
```

### 现在的实现
```python
def load_prompt(name: str, **kwargs) -> str:
    """
    支持变量替换的智能加载
    - 使用 LangChain PromptTemplate
    - 支持动态参数
    - 类型安全
    - 错误处理
    """
```

### 主要优势

1. ✅ **标准化** - 符合 LangChain 生态系统的最佳实践
2. ✅ **灵活性** - 支持动态变量替换
3. ✅ **类型安全** - 完整的类型提示
4. ✅ **错误处理** - 友好的错误提示
5. ✅ **向后兼容** - 不影响现有代码

---

## 使用方法

### 1. 基本用法（无变量）

```python
from main import load_prompt

# 加载静态提示词
prompt = load_prompt("DocumentEngineer")

# 直接使用
agent = create_deep_agent(tools, prompt)
```

### 1.5 实际应用：动态配置项目路径（推荐）⭐

CodeViewX 项目现在使用这种方式来动态注入工作目录和输出目录：

```python
import os
from main import load_prompt

# 获取当前工作目录
working_directory = os.getcwd()
output_directory = ".wiki"  # 文档输出目录

# 加载提示词并注入两个变量
prompt = load_prompt(
    "DocumentEngineer", 
    working_directory=working_directory,
    output_directory=output_directory
)

# DocumentEngineer.md 中的占位符会被替换：
# {working_directory} → /Users/deanlu/Desktop/projects/codeviewx
# {output_directory} → .wiki
```

**效果**：
- `{working_directory}` 占位符被替换为实际项目路径（出现约 15 次）
- `{output_directory}` 占位符被替换为文档保存路径（出现约 26 次）
- AI Agent 清楚知道：
  - 从哪里读取源代码（working_directory）
  - 往哪里写入文档（output_directory）

**职责分离**：
- **工作目录** - 源代码所在位置
- **输出目录** - 文档保存位置

### 2. 使用变量替换

#### 步骤 1: 在提示词模板中使用占位符

创建 `prompt/CustomTemplate.md`:

```markdown
# {project_name} 技术文档

## 项目信息
- **类型**: {project_type}
- **语言**: {language}
- **工作目录**: {working_dir}

## 分析要求
请分析 {working_dir} 目录下的代码，生成 {doc_type} 文档。

## 特殊说明
{special_instructions}
```

#### 步骤 2: 加载并传入变量

```python
prompt = load_prompt(
    "CustomTemplate",
    project_name="MyProject",
    project_type="Web应用",
    language="Python",
    working_dir="/path/to/project",
    doc_type="API文档",
    special_instructions="请重点关注 RESTful API 设计"
)
```

---

## 实际应用场景

### 场景 0: 自定义输出目录（新增）⭐

```python
import os
from main import load_prompt

# 场景A: 使用默认 .wiki 目录
prompt = load_prompt(
    "DocumentEngineer",
    working_directory=os.getcwd(),
    output_directory=".wiki"
)

# 场景B: 使用标准 docs 目录
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/path/to/project",
    output_directory="docs"
)

# 场景C: 使用嵌套目录结构
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/path/to/project",
    output_directory="documentation/api"
)

# 场景D: 多语言文档分离
prompt_zh = load_prompt(
    "DocumentEngineer",
    working_directory=project_path,
    output_directory="docs/zh"
)

prompt_en = load_prompt(
    "DocumentEngineer",
    working_directory=project_path,
    output_directory="docs/en"
)
```

**推荐的输出目录命名**：
- `.wiki` - GitHub Wiki 风格
- `docs` - 标准文档目录
- `documentation` - 企业项目
- `docs/api` - API 文档
- `docs/guide` - 用户指南

### 场景 1: 根据项目类型定制提示词

```python
def generate_docs(project_path: str, project_type: str):
    """根据项目类型生成文档"""
    
    prompt = load_prompt(
        "DocumentEngineer",
        # 如果模板支持这些变量
        project_type=project_type,
        working_directory=project_path,
        output_format="Markdown",
        language="中文"
    )
    
    agent = create_deep_agent(tools, prompt)
    # ... 运行 agent
```

### 场景 2: 动态配置分析深度

```python
def analyze_project(path: str, depth: str = "standard"):
    """根据深度等级分析项目"""
    
    depth_instructions = {
        "quick": "快速浏览，生成概览文档",
        "standard": "标准分析，生成完整技术文档",
        "deep": "深度分析，包含所有细节和设计决策"
    }
    
    prompt = load_prompt(
        "AnalysisTemplate",
        project_path=path,
        analysis_depth=depth,
        instructions=depth_instructions[depth]
    )
    
    # ... 使用 prompt
```

### 场景 3: 多语言支持

```python
def generate_multilang_docs(project_path: str, language: str):
    """生成多语言文档"""
    
    language_configs = {
        "zh": {"lang": "中文", "format": "简体中文技术文档"},
        "en": {"lang": "English", "format": "Technical Documentation"},
        "ja": {"lang": "日本語", "format": "技術ドキュメント"}
    }
    
    config = language_configs[language]
    
    prompt = load_prompt(
        "MultilingualTemplate",
        project_path=project_path,
        target_language=config["lang"],
        doc_format=config["format"]
    )
    
    # ... 使用 prompt
```

---

## 最佳实践

### 1. 模板设计

**推荐的模板结构**:

```markdown
# 角色定义
你是一个 {role}，专门负责 {responsibility}。

# 输入信息
- 项目路径: {project_path}
- 项目类型: {project_type}
- 分析范围: {analysis_scope}

# 任务要求
{task_description}

# 输出格式
{output_format}

# 特殊说明
{special_notes}
```

### 2. 变量命名规范

- 使用小写字母和下划线: `project_path`, `doc_type`
- 名称要有意义: ✅ `working_directory` ❌ `dir`
- 保持一致性: 在所有模板中使用相同的变量名

### 3. 提供默认值

```python
def load_prompt_with_defaults(name: str, **kwargs) -> str:
    """提供默认值的包装函数"""
    defaults = {
        "language": "中文",
        "output_format": "Markdown",
        "doc_type": "技术文档"
    }
    
    # 合并默认值和用户提供的值
    params = {**defaults, **kwargs}
    
    return load_prompt(name, **params)
```

### 4. 错误处理

```python
try:
    prompt = load_prompt("MyTemplate", required_param="value")
except ValueError as e:
    print(f"模板变量错误: {e}")
    # 使用后备方案
    prompt = load_prompt("DefaultTemplate")
```

---

## 常见问题

### Q1: 现有的 DocumentEngineer.md 需要修改吗？

**A**: 不需要！如果不传递变量参数，函数会直接返回原始文本：

```python
# 这样使用完全没问题
prompt = load_prompt("DocumentEngineer")
```

### Q2: 如何在模板中使用花括号 `{}`？

**A**: 使用双花括号转义：

```markdown
# 示例代码
\`\`\`python
def example():
    data = {{"key": "value"}}  # 使用 {{ }} 显示 {}
\`\`\`
```

### Q3: 可以部分替换变量吗？

**A**: 不推荐。如果模板中有 `{variable}`，必须提供该变量，否则会报错。建议：

```python
# 方案 1: 提供所有变量
prompt = load_prompt("Template", var1="a", var2="b")

# 方案 2: 创建不同版本的模板
prompt = load_prompt("TemplateSimple")  # 无变量版本
```

### Q4: 如何查看模板需要哪些变量？

**A**: 可以创建一个辅助函数：

```python
import re

def list_template_variables(template_name: str) -> list:
    """列出模板中的所有变量"""
    with open(f"prompt/{template_name}.md", "r") as f:
        content = f.read()
    
    # 查找所有 {variable} 模式
    variables = re.findall(r'\{(\w+)\}', content)
    return list(set(variables))

# 使用
vars = list_template_variables("MyTemplate")
print(f"需要的变量: {vars}")
```

---

## 进阶技巧

### 1. 条件内容

在模板中使用条件逻辑（需要自定义处理）：

```python
def load_conditional_prompt(name: str, include_advanced: bool = False, **kwargs):
    """加载带条件内容的提示词"""
    template = load_prompt(name, **kwargs)
    
    if not include_advanced:
        # 移除高级部分
        template = re.sub(r'<!-- ADVANCED START -->.*?<!-- ADVANCED END -->', 
                         '', template, flags=re.DOTALL)
    
    return template
```

### 2. 模板继承

```python
def load_extended_prompt(base: str, extension: str, **kwargs) -> str:
    """加载基础模板并扩展"""
    base_prompt = load_prompt(base, **kwargs)
    extension_content = load_prompt(extension, **kwargs)
    
    return f"{base_prompt}\n\n# 扩展内容\n{extension_content}"
```

### 3. 动态模板选择

```python
def smart_load_prompt(project_type: str, **kwargs) -> str:
    """根据项目类型智能选择模板"""
    template_map = {
        "web": "WebProjectTemplate",
        "cli": "CLIProjectTemplate",
        "library": "LibraryTemplate",
        "api": "APIProjectTemplate"
    }
    
    template_name = template_map.get(project_type, "DocumentEngineer")
    return load_prompt(template_name, project_type=project_type, **kwargs)
```

---

## 总结

使用 LangChain 的 PromptTemplate 让我们的提示词系统更加：

- 🎯 **专业** - 符合行业标准
- 🔧 **灵活** - 支持各种定制需求
- 🛡️ **安全** - 类型检查和错误处理
- 🚀 **强大** - 为未来扩展打下基础

这个改进让 CodeViewX 项目更加成熟和易于维护！

