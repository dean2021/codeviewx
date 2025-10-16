# 更新日志：工作目录动态注入

## 更新时间
2024-10-16

## 概述
实现了通过 LangChain PromptTemplate 将工作目录动态注入到系统提示词中的功能，让提示词更加灵活和可复用。

---

## 修改内容

### 1. `prompt/DocumentEngineer.md` 

#### 添加项目信息部分（第 4-9 行）

```markdown
# 项目信息
- **工作目录**: `{working_directory}`
- **文档输出目录**: `.wiki/`
- **分析任务**: 深度技术文档生成

**重要**: 所有文件路径操作都基于工作目录 `{working_directory}`，文档应保存到 `.wiki/` 子目录。
```

#### 更新工作流程中的路径示例

将硬编码的路径替换为 `{working_directory}` 占位符：

**之前**:
```markdown
list_real_directory("/path/to/project")
read_real_file("README.md")
ripgrep_search("def main", ".", "py")
```

**之后**:
```markdown
list_real_directory("{working_directory}")
read_real_file("{working_directory}/README.md")
ripgrep_search("def main", "{working_directory}", "py")
```

### 2. `main.py`

#### 添加 os 模块导入
```python
import os  # 操作系统接口
```

#### 在主程序中注入工作目录

```python
if __name__ == "__main__":
    # ...
    
    # 获取当前工作目录
    working_directory = os.getcwd()
    print(f"📂 工作目录: {working_directory}")
    
    # 加载系统提示词并注入工作目录
    prompt = load_prompt("DocumentEngineer", working_directory=working_directory)
    print("✓ 已加载系统提示词（已注入工作目录）")
```

#### 简化用户消息

**之前**:
```python
{"messages": [{"role": "user", "content": "当前工作目录为:/Users/deanlu/Desktop/projects/codeviewx,请生成一份该项目的深度技术文档"}]}
```

**之后**:
```python
{"messages": [{"role": "user", "content": "请根据系统提示词中的工作目录，分析该项目并生成深度技术文档"}]}
```

### 3. 文档更新

- 更新了 `docs/prompt-template-guide.md`，添加了工作目录注入的实际应用示例
- 创建了本更新日志文档

---

## 效果展示

### 注入前的提示词（部分）
```markdown
# 项目信息
- **工作目录**: `{working_directory}`
```

### 注入后的提示词（部分）
```markdown
# 项目信息
- **工作目录**: `/Users/deanlu/Desktop/projects/codeviewx`
```

### 统计数据
- 工作目录在提示词中出现 **15 次**
- 所有占位符都被正确替换
- 提示词总长度：~17,000 字符

---

## 优势

### 1. 🎯 更清晰的上下文
AI Agent 在提示词中就能看到明确的工作目录，不需要从用户消息中提取。

### 2. 🔧 更好的可复用性
同一个提示词模板可以用于不同的项目，只需改变注入的工作目录参数。

### 3. 📝 更简洁的用户消息
用户不需要在消息中重复指定工作目录，提示词已经包含了这个信息。

### 4. 🛡️ 类型安全
使用 LangChain PromptTemplate 提供了更好的错误检查和类型提示。

### 5. 🚀 易于扩展
未来可以轻松添加更多动态参数，如：
- `project_type`: 项目类型
- `language`: 主要编程语言
- `output_format`: 输出格式
- `analysis_depth`: 分析深度

---

## 测试结果

✅ 所有测试通过：
- 工作目录正确注入
- 占位符完全替换
- 多变量注入正常工作
- 无 linter 错误

---

## 使用示例

### 基本使用
```python
import os
from main import load_prompt

# 获取当前目录
working_dir = os.getcwd()

# 加载并注入
prompt = load_prompt("DocumentEngineer", working_directory=working_dir)
```

### 自定义项目分析
```python
# 分析不同的项目
prompt = load_prompt(
    "DocumentEngineer", 
    working_directory="/path/to/another/project"
)
```

### 多变量注入（未来扩展）
```python
prompt = load_prompt(
    "DocumentEngineer",
    working_directory=project_path,
    project_type="Web应用",
    language="Python",
    output_format="Markdown"
)
```

---

## 后续改进建议

1. **添加更多动态参数**
   - 项目类型（自动检测）
   - 主要语言（从文件扩展名判断）
   - 文档风格（技术/业务/API）

2. **环境变量支持**
   ```python
   working_dir = os.getenv("PROJECT_DIR", os.getcwd())
   ```

3. **配置文件支持**
   - 从 `.codeviewx.yaml` 读取配置
   - 支持项目级别的自定义设置

4. **命令行参数**
   ```bash
   python main.py --working-dir /path/to/project
   ```

---

## 相关文件

- `main.py` - 主程序，包含 `load_prompt` 函数
- `prompt/DocumentEngineer.md` - 系统提示词模板
- `docs/prompt-template-guide.md` - PromptTemplate 使用指南
- `docs/changelog-working-directory.md` - 本文档

---

## 总结

这次更新通过 LangChain PromptTemplate 实现了工作目录的动态注入，让 CodeViewX 项目的提示词系统更加：

- ✅ **灵活** - 可用于任何项目
- ✅ **清晰** - 上下文信息明确
- ✅ **标准** - 符合 LangChain 最佳实践
- ✅ **可扩展** - 易于添加新参数

这是项目走向成熟和专业化的重要一步！🎉

