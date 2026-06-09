# 为 CodeViewX 做贡献

中文 | [English](CONTRIBUTING.md)

首先，感谢您考虑为 CodeViewX 做贡献！正是像您这样的人让 CodeViewX 成为如此出色的工具。

## 目录

- [行为准则](#行为准则)
- [如何贡献？](#如何贡献)
  - [报告错误](#报告错误)
  - [提出改进建议](#提出改进建议)
  - [第一次代码贡献](#第一次代码贡献)
  - [Pull Request](#pull-request)
- [开发环境设置](#开发环境设置)
- [编码规范](#编码规范)
- [提交规范](#提交规范)
- [测试指南](#测试指南)
- [文档](#文档)
- [社区](#社区)

## 行为准则

本项目及其参与者均受我们的行为准则约束。参与本项目即表示您同意遵守此准则。如发现不可接受的行为，请报告至 dean@csoio.com。

### 我们的承诺

我们承诺让参与本项目和社区的每个人都能享受无骚扰的体验，无论年龄、体型、残疾、民族、性别认同和表达、经验水平、国籍、个人外表、种族、宗教或性认同和取向如何。

### 我们的标准

**积极行为包括：**
- 使用欢迎和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表现出同理心

**不可接受的行为包括：**
- 恶意评论、侮辱性/贬损性评论以及人身或政治攻击
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息
- 其他可合理认为不适当的行为

## 如何贡献？

### 报告错误

在创建错误报告之前，请检查现有 issues 以避免重复。创建错误报告时，请尽可能包含详细信息：

**使用错误报告模板：**

```markdown
**错误描述**
清晰简洁地描述错误是什么。

**重现步骤**
重现该行为的步骤：
1. 进入 '...'
2. 运行命令 '...'
3. 看到错误

**预期行为**
您期望发生什么。

**截图/日志**
如果适用，添加截图或错误日志。

**环境信息：**
- 操作系统：[例如，macOS 13.0, Ubuntu 22.04]
- Python 版本：[例如，3.9.7]
- CodeViewX 版本：[例如，0.2.0]
- 安装方式：[pip, 源码]

**其他上下文**
关于问题的任何其他上下文信息。
```

### 提出改进建议

改进建议通过 GitHub issues 跟踪。创建改进建议时：

**使用功能请求模板：**

```markdown
**您的功能请求是否与问题相关？**
清楚描述问题。例如：当我 [...] 时总是感到沮丧

**描述您想要的解决方案**
清晰简洁地描述您希望发生什么。

**描述您考虑过的替代方案**
您考虑过的替代解决方案或功能。

**其他上下文**
任何其他上下文、模型图或示例。
```

### 第一次代码贡献

不确定从哪里开始？寻找标记为以下标签的 issues：
- `good first issue` - 适合新手
- `help wanted` - 需要额外关注
- `documentation` - 文档改进

#### 设置开发环境

1. **Fork 和克隆**
   ```bash
   git clone https://github.com/YOUR-USERNAME/codeviewx.git
   cd codeviewx
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows 上：.venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -e ".[dev]"
   ```

4. **配置环境**
   ```bash
   export ANTHROPIC_AUTH_TOKEN="your-api-key-here"
   ```

5. **验证设置**
   ```bash
   codeviewx --version
   pytest
   ```

### Pull Request

#### 提交之前

1. **检查现有 PRs** 以避免重复
2. **遵循编码规范**（见下文）
3. **为新功能编写测试**
4. **根据需要更新文档**
5. **运行所有测试**并确保通过

#### PR 流程

1. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

2. **进行更改**
   - 编写干净、有文档的代码
   - 遵循样式指南
   - 添加测试

3. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加惊人的功能"
   ```

4. **推送到您的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **提交 Pull Request**
   - 填写 PR 模板
   - 链接相关 issues
   - 请求审查

#### PR 模板

```markdown
## 描述
更改的简要描述

## 更改类型
- [ ] 错误修复（修复问题的非破坏性更改）
- [ ] 新功能（添加功能的非破坏性更改）
- [ ] 破坏性更改（会导致现有功能无法按预期工作的修复或功能）
- [ ] 文档更新

## 如何测试？
描述您运行的测试以及如何重现它们。

## 检查清单
- [ ] 我的代码遵循样式指南
- [ ] 我已进行自我审查
- [ ] 我已对代码进行注释，特别是在难以理解的地方
- [ ] 我已对文档进行相应更改
- [ ] 我的更改不会产生新的警告
- [ ] 我已添加证明我的修复有效或功能正常的测试
- [ ] 新的和现有的单元测试在本地通过我的更改

## 相关 Issues
Closes #(issue 编号)
```

## 开发环境设置

### 必需工具

- Python 3.11+
- Git
- 代码编辑器（推荐 VS Code 或 PyCharm）

### 推荐的 VS Code 扩展

- Python
- Pylance
- Black Formatter
- autoDocstring

### 开发依赖

所有开发依赖通过以下命令安装：
```bash
pip install -e ".[dev]"
```

包括：
- pytest（测试）
- pytest-cov（覆盖率）
- black（格式化）
- flake8（代码检查）
- mypy（类型检查）
- isort（导入排序）

## 编码规范

### Python 样式指南

我们遵循 PEP 8，并通过 Black 强制执行一些修改。

#### 代码格式化

**使用 Black 格式化：**
```bash
black codeviewx/
```

**配置（pyproject.toml）：**
```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
```

#### 代码检查

**运行 flake8：**
```bash
flake8 codeviewx/
```

#### 类型提示

为所有公共函数使用类型提示：
```python
def generate_docs(
    working_directory: str,
    output_directory: str = "docs",
    doc_language: str = "Chinese"
) -> None:
    """为项目生成文档。"""
    pass
```

#### 文档字符串

使用 Google 风格的文档字符串：
```python
def function_name(param1: str, param2: int) -> bool:
    """
    简要描述。
    
    如需要，可添加更长的描述。
    
    Args:
        param1: param1 的描述
        param2: param2 的描述
    
    Returns:
        返回值的描述
    
    Raises:
        ValueError: 当 param1 为空时
    
    Examples:
        >>> function_name("test", 42)
        True
    """
    pass
```

#### 导入组织

使用 isort 进行导入排序：
```bash
isort codeviewx/
```

导入顺序：
1. 标准库导入
2. 第三方导入
3. 本地应用导入

示例：
```python
import os
import sys
from typing import Dict, List

from langchain import LLMChain
from langchain_anthropic import ChatAnthropic

from codeviewx.core import generate_docs
from codeviewx.i18n import t
```

### 文件组织

- 每个文件一个类（除非密切相关）
- 分组相关函数
- 尽可能将文件保持在 500 行以下
- 使用描述性文件名

### 命名约定

- **模块**：`lowercase_with_underscores.py`
- **类**：`CapitalizedWords`
- **函数**：`lowercase_with_underscores()`
- **常量**：`UPPERCASE_WITH_UNDERSCORES`
- **私有**：`_leading_underscore`

## 提交规范

我们遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型

- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更改
- `style`: 代码样式更改（格式化等）
- `refactor`: 代码重构
- `test`: 添加或更新测试
- `chore`: 维护任务
- `perf`: 性能改进
- `ci`: CI/CD 更改

### 示例

```bash
# 功能
git commit -m "feat(generator): 添加对 TypeScript 项目的支持"

# 错误修复
git commit -m "fix(cli): 修正输出目录路径处理"

# 文档
git commit -m "docs(readme): 更新安装说明"

# 破坏性更改
git commit -m "feat(api)!: 更改 generate_docs 返回类型

BREAKING CHANGE: generate_docs 现在返回 dict 而不是 None"
```

### 提交最佳实践

1. **使用现在时**："add feature" 而不是 "added feature"
2. **简洁明了**：主题保持在 72 个字符以下
3. **具有描述性**：解释什么和为什么，而不是如何
4. **引用 issues**：使用 "Closes #123" 或 "Fixes #456"
5. **每次提交一个逻辑更改**

## 测试指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行并查看覆盖率
pytest --cov=codeviewx --cov-report=html

# 运行特定测试文件
pytest tests/test_core.py

# 运行特定测试
pytest tests/test_core.py::test_generate_docs

# 运行并显示详细输出
pytest -v
```

### 编写测试

#### 测试结构

```python
import pytest
from codeviewx.core import generate_docs

class TestGenerateDocs:
    """generate_docs 函数的测试。"""
    
    def test_basic_generation(self, tmp_path):
        """测试基本文档生成。"""
        # 准备
        working_dir = tmp_path / "project"
        working_dir.mkdir()
        output_dir = tmp_path / "docs"
        
        # 执行
        generate_docs(str(working_dir), str(output_dir))
        
        # 断言
        assert output_dir.exists()
        assert (output_dir / "README.md").exists()
    
    def test_invalid_directory(self):
        """测试不存在的目录。"""
        with pytest.raises(ValueError):
            generate_docs("/non/existent/path")
```

#### 测试指南

1. **使用描述性名称**：`test_should_raise_error_when_directory_not_found`
2. **遵循 AAA 模式**：准备（Arrange）、执行（Act）、断言（Assert）
3. **每个测试一个断言**（如果可能）
4. **使用 fixtures** 进行通用设置
5. **模拟外部依赖**（API 调用、文件系统等）

#### 测试覆盖率目标

- **最低**：整体覆盖率 70%
- **目标**：80%+ 覆盖率
- **关键路径**：100% 覆盖率

### 测试 Fixtures

```python
import pytest

@pytest.fixture
def sample_project(tmp_path):
    """创建示例项目结构。"""
    project_dir = tmp_path / "sample"
    project_dir.mkdir()
    
    # 创建示例文件
    (project_dir / "main.py").write_text("print('hello')")
    (project_dir / "README.md").write_text("# Sample")
    
    return project_dir
```

## 文档

### 代码文档

- 所有公共 API 必须有文档字符串
- 使用 Google 风格的文档字符串
- 在有帮助时包含示例
- 记录可能引发的异常

### 用户文档

添加功能时，更新：
- `README.md` - 面向用户的功能
- `docs/` - 详细文档
- API 参考 - 如果适用
- 示例 - 添加到 `examples/` 目录

### 文档构建

```bash
# 生成 API 文档（如果使用 Sphinx）
cd docs
make html

# 本地查看文档
python -m http.server --directory docs/_build/html
```

## 社区

### 获取帮助

- **GitHub Discussions**：用于问题和讨论
- **GitHub Issues**：用于错误和功能请求
- **电子邮件**：dean@csoio.com 用于私人事务

### 沟通指南

- 尊重和建设性
- 保持主题
- 发布前先搜索
- 提供上下文和详细信息
- 跟进您的 issues/PRs

### 认可

贡献者将被认可于：
- GitHub Contributors 页面
- 发布说明（对于重大贡献）
- 项目文档

## 许可证

通过为 CodeViewX 做贡献，您同意您的贡献将在 GNU General Public License v3.0 下获得许可。

---

## 快速链接

- [问题跟踪](https://github.com/dean2021/codeviewx/issues)
- [Pull Requests](https://github.com/dean2021/codeviewx/pulls)
- [讨论区](https://github.com/dean2021/codeviewx/discussions)
- [文档](https://github.com/dean2021/codeviewx/tree/main/docs)

---

感谢您为 CodeViewX 做贡献！🎉
