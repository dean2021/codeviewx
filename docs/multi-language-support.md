# CodeViewX 多语言文档生成功能

## 📝 功能概述

CodeViewX 现在支持多语言文档生成！您可以指定文档语言，或让系统自动检测并使用您的系统语言。

---

## ✨ 主要特性

### 1. 自动语言检测 🌍
- 系统会自动检测您的操作系统语言设置
- 无需手动指定，开箱即用

### 2. 支持 8 种主要语言
- 🇨🇳 Chinese (中文)
- 🇺🇸 English  
- 🇯🇵 Japanese (日本語)
- 🇰🇷 Korean (한국어)
- 🇫🇷 French (Français)
- 🇩🇪 German (Deutsch)
- 🇪🇸 Spanish (Español)
- 🇷🇺 Russian (Русский)

### 3. 灵活配置
- 命令行参数：`-l/--language`
- Python API：`doc_language` 参数
- 环境变量支持（未来）

---

## 🚀 使用方法

### 命令行 CLI

```bash
# 自动检测系统语言（推荐）
codeviewx

# 指定中文
codeviewx -l Chinese

# 指定英文
codeviewx -l English -o docs

# 完整配置
codeviewx -w /path/to/project -o docs -l Japanese --verbose
```

### Python API

```python
from codeviewx import generate_docs, detect_system_language

# 方式 1: 自动检测语言
generate_docs()

# 方式 2: 手动指定语言
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs",
    doc_language="Chinese"
)

# 方式 3: 先检测，再使用
current_lang = detect_system_language()
print(f"检测到的语言: {current_lang}")
generate_docs(doc_language=current_lang)
```

---

## 📊 实现细节

### 架构设计

```
用户调用
  ↓
CLI / Python API
  ↓
detect_system_language() ← 自动检测（如果未指定）
  ↓
load_prompt() ← 注入 doc_language 变量
  ↓
DocumentEngineer.md ← 包含 {doc_language} 占位符
  ↓
AI Agent ← 根据指定语言生成文档
```

### 核心函数

#### 1. `detect_system_language()`
```python
def detect_system_language() -> str:
    """
    检测系统语言
    
    Returns:
        语言名称，如 'Chinese', 'English', 'Japanese' 等
    """
```

**实现逻辑**:
- 读取系统 locale 设置
- 映射语言代码到标准名称
- 失败时默认返回 'English'

#### 2. `generate_docs(doc_language=...)`
```python
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = ".wiki",
    doc_language: Optional[str] = None,  # ← 新增参数
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None:
```

**处理流程**:
1. 如果 `doc_language` 为 None，调用 `detect_system_language()`
2. 将语言信息注入到提示词模板
3. AI Agent 使用指定语言生成文档

#### 3. CLI 参数
```python
parser.add_argument(
    "-l", "--language",
    dest="doc_language",
    choices=['Chinese', 'English', 'Japanese', ...],
    help="文档语言（默认：自动检测系统语言）"
)
```

---

## 🎯 应用场景

### 场景 1: 国际化项目
生成多语言版本的文档：

```python
# 中文版
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs/zh",
    doc_language="Chinese"
)

# 英文版
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs/en",
    doc_language="English"
)

# 日文版
generate_docs(
    working_directory="/path/to/project",
    output_directory="docs/ja",
    doc_language="Japanese"
)
```

**目录结构**:
```
project/
└── docs/
    ├── zh/          # 中文文档
    │   ├── README.md
    │   └── ...
    ├── en/          # 英文文档
    │   ├── README.md
    │   └── ...
    └── ja/          # 日文文档
        ├── README.md
        └── ...
```

### 场景 2: 面向特定用户群
```python
# 中国用户
generate_docs(doc_language="Chinese")

# 国际用户
generate_docs(doc_language="English")
```

### 场景 3: 自动适配用户环境
```python
# 根据用户系统语言自动选择
generate_docs()  # 自动检测
```

---

## 🔧 技术实现

### 提示词模板更新

在 `DocumentEngineer.md` 中添加：

```markdown
# 项目信息
- **工作目录**: `{working_directory}`
- **文档输出目录**: `{output_directory}`
- **文档语言**: `{doc_language}`  ← 新增

**重要**: 所有生成的文档内容必须使用 `{doc_language}` 语言编写

## 文档语言规范
**重要**: 所有生成的文档内容必须使用 `{doc_language}` 语言编写。

- **中文 (Chinese)**: 使用简体中文，专业术语可保留英文并添加中文注释
- **英文 (English)**: 使用美式英语，清晰准确的技术表达
- **日文 (Japanese)**: 使用日语，技术术语可保留英文
- **其他语言**: 根据指定语言生成文档

**注意**:
- 代码片段、文件名、命令等保持原样（英文）
- 技术术语在首次出现时可添加英文注释
- 所有章节标题、说明文字、分析内容都使用指定语言
```

### 系统语言检测

使用 Python 标准库 `locale`:

```python
import locale

def detect_system_language() -> str:
    try:
        lang, encoding = locale.getdefaultlocale()
        
        if lang:
            if lang.startswith('zh'):
                return 'Chinese'
            elif lang.startswith('ja'):
                return 'Japanese'
            # ... 其他语言映射
            else:
                return 'English'
        
        return 'English'
    except Exception:
        return 'English'
```

---

## ✅ 测试

### 测试覆盖

创建了 `tests/test_language.py`，包含：

1. **系统语言检测测试**
   ```python
   def test_detect_system_language():
       language = detect_system_language()
       assert language in supported_languages
   ```

2. **语言注入测试**
   ```python
   def test_load_prompt_with_language():
       prompt = load_prompt(..., doc_language="English")
       assert "English" in prompt
       assert "{doc_language}" not in prompt
   ```

3. **多语言测试**
   ```python
   def test_load_prompt_multiple_languages():
       for lang in ['English', 'Chinese', 'Japanese']:
           prompt = load_prompt(..., doc_language=lang)
           assert lang in prompt
   ```

### 测试结果

```bash
$ pytest tests/test_language.py -v
5 passed in 0.19s ✅
```

**总测试数**: 21 个测试全部通过 ✅

---

## 📈 输出示例

### 使用中文

```bash
$ codeviewx -l Chinese
================================================================================
🚀 启动 CodeViewX 文档生成器 - 2024-10-16 18:00:00
================================================================================
📂 工作目录: /Users/user/project
📝 输出目录: .wiki
🌍 文档语言: Chinese (用户指定)  ← 显示语言信息
✓ 已加载系统提示词（已注入工作目录、输出目录和文档语言）
...
```

### 自动检测

```bash
$ codeviewx
================================================================================
🚀 启动 CodeViewX 文档生成器 - 2024-10-16 18:00:00
================================================================================
📂 工作目录: /Users/user/project
📝 输出目录: .wiki
🌍 文档语言: English (自动检测)  ← 自动检测的语言
✓ 已加载系统提示词（已注入工作目录、输出目录和文档语言）
...
```

---

## 🔮 未来扩展

### 短期
- [ ] 支持更多语言（葡萄牙语、意大利语等）
- [ ] 优化语言检测算法（避免 deprecation warning）
- [ ] 添加语言代码映射表配置

### 中期
- [ ] 支持环境变量 `CODEVIEWX_LANGUAGE`
- [ ] 支持配置文件指定默认语言
- [ ] 添加语言回退机制

### 长期
- [ ] 支持自定义语言规则
- [ ] 混合语言文档（双语对照）
- [ ] AI 自动翻译现有文档

---

## 📚 相关文档

- [快速开始](../README.md#快速开始)
- [PromptTemplate 使用指南](./prompt-template-guide.md)
- [使用示例](./usage-examples.md)

---

## 💡 最佳实践

### 1. 团队协作
为国际团队生成各自语言的文档：
```bash
# CI/CD 中自动生成多语言文档
codeviewx -l Chinese -o docs/zh
codeviewx -l English -o docs/en
```

### 2. 开源项目
英文为主，中文为辅：
```bash
# 主文档（英文）
codeviewx -l English -o docs

# 中文文档（可选）
codeviewx -l Chinese -o docs/zh
```

### 3. 内部项目
使用团队主要语言：
```bash
# 中文团队
codeviewx -l Chinese

# 让系统自动选择
codeviewx  # 自动检测
```

---

## 🎉 总结

多语言支持让 CodeViewX 更加国际化和易用：

- ✅ **自动检测** - 开箱即用
- ✅ **8 种语言** - 覆盖主要市场
- ✅ **灵活配置** - CLI 和 API 双支持
- ✅ **完整测试** - 21 个测试全通过
- ✅ **易于扩展** - 可添加更多语言

**让文档以您熟悉的语言呈现！** 🌍✨

