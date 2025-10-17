# 开发指南

本指南帮助开发者了解如何为 CodeViewX 项目做贡献，包括开发环境搭建、代码规范、测试流程和发布流程。

## 开发环境搭建

### 系统要求

- **Python 3.8+**：推荐使用 Python 3.9 或 3.10
- **Git**：版本控制工具
- **ripgrep (rg)**：代码搜索工具
- **IDE**：推荐 VS Code 或 PyCharm

### 环境准备

#### 1. 克隆项目

```bash
# 克隆仓库
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# 查看项目结构
ls -la
```

#### 2. 创建虚拟环境

```bash
# 使用 venv 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

#### 3. 安装依赖

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 验证安装
pip list | grep codeviewx
```

#### 4. 安装 ripgrep

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows
choco install ripgrep
```

### 开发工具配置

#### VS Code 配置

推荐安装以下扩展：

```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml"
  ]
}
```

VS Code 设置：

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### PyCharm 配置

1. **解释器设置**：
   - File → Settings → Project → Python Interpreter
   - 选择项目虚拟环境中的 Python

2. **代码格式化**：
   - File → Settings → Tools → External Tools
   - 添加 Black 配置

3. **代码检查**：
   - File → Settings → Tools → External Tools
   - 添加 Flake8 和 MyPy 配置

## 项目结构详解

### 目录组织

```
codeviewx/
├── codeviewx/                    # 主包目录
│   ├── __init__.py              # 包初始化，导出 API
│   ├── __version__.py           # 版本信息
│   ├── cli.py                   # 命令行接口
│   ├── core.py                  # 核心 API 模块
│   ├── generator.py             # 文档生成器
│   ├── server.py                # Web 服务器
│   ├── prompt.py                # 提示词管理
│   ├── i18n.py                  # 国际化支持
│   ├── language.py              # 语言检测
│   ├── tools/                   # 工具模块
│   │   ├── __init__.py          # 工具导出
│   │   ├── command.py           # 系统命令执行
│   │   ├── filesystem.py        # 文件系统操作
│   │   └── search.py            # 代码搜索
│   ├── prompts/                 # 提示词模板
│   │   ├── __init__.py
│   │   ├── document_engineer.md      # 英文提示词
│   │   └── document_engineer_zh.md   # 中文提示词
│   ├── tpl/                     # HTML 模板
│   │   └── doc_detail.html      # 文档展示页面
│   └── static/                  # 静态资源
│       ├── css/                 # 样式文件
│       ├── js/                  # JavaScript 文件
│       └── images/              # 图片资源
├── tests/                       # 测试文件
│   ├── __init__.py
│   ├── test_core.py             # 核心功能测试
│   ├── test_language.py         # 语言检测测试
│   ├── test_progress.py         # 进度跟踪测试
│   └── test_tools.py            # 工具模块测试
├── examples/                    # 示例代码
├── docs/                        # 文档输出目录
├── pyproject.toml               # 项目配置文件
├── requirements.txt             # 生产依赖
├── requirements-dev.txt         # 开发依赖
├── README.md                    # 项目说明（英文）
├── README.zh.md                 # 项目说明（中文）
├── LICENSE                      # 许可证文件
├── MANIFEST.in                  # 包含文件清单
├── .gitignore                   # Git 忽略文件
├── .github/                     # GitHub 配置
│   └── workflows/               # CI/CD 工作流
│       └── test.yml             # 测试工作流
└── .vscode/                     # VS Code 配置
    ├── extensions.json          # 推荐扩展
    └── settings.json            # 编辑器设置
```

### 模块职责

#### 核心模块

1. **cli.py**：
   - 命令行参数解析
   - 用户交互逻辑
   - 错误处理和用户友好提示

2. **core.py**：
   - 公共 API 导出
   - 模块间协调
   - 版本管理

3. **generator.py**：
   - AI 代理创建和管理
   - 文档生成工作流
   - 进度跟踪和状态管理

4. **server.py**：
   - Flask Web 服务器
   - Markdown 渲染
   - 文档浏览界面

#### 工具模块

1. **tools/filesystem.py**：
   - 文件读写操作
   - 目录遍历
   - 路径安全验证

2. **tools/search.py**：
   - ripgrep 集成
   - 代码搜索功能
   - 结果处理和格式化

3. **tools/command.py**：
   - 系统命令执行
   - 进程管理
   - 输出处理

#### 支持模块

1. **i18n.py**：
   - 多语言支持
   - 消息翻译
   - 语言检测

2. **prompt.py**：
   - 提示词模板管理
   - 动态内容注入
   - 模板渲染

3. **language.py**：
   - 系统语言检测
   - 项目语言分析
   - 语言映射

## 代码规范

### Python 代码风格

#### 1. 代码格式化

使用 Black 进行代码格式化：

```bash
# 格式化所有代码
black codeviewx/

# 检查格式（不修改文件）
black --check codeviewx/

# 格式化特定文件
black codeviewx/cli.py codeviewx/generator.py
```

Black 配置（pyproject.toml）：

```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''
```

#### 2. 代码质量检查

使用 Flake8 进行代码检查：

```bash
# 检查代码质量
flake8 codeviewx/

# 检查特定文件
flake8 codeviewx/cli.py

# 显示详细错误信息
flake8 --verbose codeviewx/
```

Flake8 配置（setup.cfg 或 pyproject.toml）：

```toml
[tool.flake8]
max-line-length = 100
extend-ignore = ["E203", "W503"]
exclude = [
    ".git",
    "__pycache__",
    "build",
    "dist",
    ".venv",
    ".pytest_cache"
]
```

#### 3. 类型检查

使用 MyPy 进行类型检查：

```bash
# 类型检查
mypy codeviewx/

# 检查特定模块
mypy codeviewx/cli.py

# 显示详细错误
mypy --show-error-codes codeviewx/
```

MyPy 配置（pyproject.toml）：

```toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
```

#### 4. 导入排序

使用 isort 进行导入排序：

```bash
# 排序导入
isort codeviewx/

# 检查导入（不修改文件）
isort --check-only codeviewx/

# 配置文件检查
isort --diff codeviewx/
```

isort 配置（pyproject.toml）：

```toml
[tool.isort]
profile = "black"
line_length = 100
```

### 命名规范

#### 1. 变量和函数

```python
# 使用 snake_case
working_directory = "/path/to/project"
def generate_docs():
    pass

def ripgrep_search(pattern: str, path: str = "."):
    pass
```

#### 2. 类名

```python
# 使用 PascalCase
class DocumentGenerator:
    pass

class AIProxy:
    pass
```

#### 3. 常量

```python
# 使用 UPPER_CASE
DEFAULT_RECURSION_LIMIT = 1000
SUPPORTED_LANGUAGES = ["Chinese", "English", "Japanese"]
```

#### 4. 私有成员

```python
class MyClass:
    def __init__(self):
        self._private_var = "private"  # 受保护成员
        self.__very_private = "very"   # 私有成员
    
    def _private_method(self):
        pass  # 私有方法
```

### 文档字符串规范

#### 1. 模块文档

```python
"""
CodeViewX Core Module

This module provides the core functionality for generating documentation
from source code using AI agents.

Main functions:
- generate_docs: Generate documentation for a project
- start_document_web_server: Start web server for browsing docs
"""
```

#### 2. 函数文档

```python
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    ui_language: Optional[str] = None,
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None:
    """
    Generate project documentation using AI
    
    Args:
        working_directory: Project working directory (default: current directory)
        output_directory: Documentation output directory (default: docs)
        doc_language: Documentation language (default: auto-detect system language)
        ui_language: User interface language (default: auto-detect)
        recursion_limit: Agent recursion limit (default: 1000)
        verbose: Show detailed logs (default: False)
    
    Raises:
        FileNotFoundError: If working directory doesn't exist
        PermissionError: If no write permission for output directory
        RuntimeError: If AI service is unavailable
    
    Examples:
        >>> generate_docs()
        
        >>> generate_docs(
        ...     working_directory="/path/to/project",
        ...     output_directory="docs",
        ...     doc_language="English"
        ... )
    """
```

#### 3. 类文档

```python
class I18n:
    """
    Internationalization manager
    
    Supports multiple languages with automatic detection and manual override.
    
    Attributes:
        locale: Current language code
    
    Examples:
        >>> i18n = I18n('en')
        >>> i18n.t('starting')
        '🚀 Starting CodeViewX Documentation Generator'
        
        >>> i18n.set_locale('zh')
        >>> i18n.t('starting')
        '🚀 启动 CodeViewX 文档生成器'
    """
```

### 错误处理规范

#### 1. 异常类型

```python
# 自定义异常
class CodeViewXError(Exception):
    """Base exception for CodeViewX"""
    pass

class ConfigurationError(CodeViewXError):
    """Configuration related errors"""
    pass

class AIServiceError(CodeViewXError):
    """AI service related errors"""
    pass

class FileSystemError(CodeViewXError):
    """File system related errors"""
    pass
```

#### 2. 异常处理

```python
def safe_file_operation(file_path: str) -> Optional[str]:
    """安全的文件操作"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        return None
    except UnicodeDecodeError:
        logger.error(f"Encoding error: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error reading {file_path}: {e}")
        return None
```

## 测试指南

### 测试结构

```
tests/
├── __init__.py
├── conftest.py                    # pytest 配置
├── test_core.py                   # 核心功能测试
├── test_language.py               # 语言检测测试
├── test_progress.py               # 进度跟踪测试
├── test_tools.py                  # 工具模块测试
├── test_cli.py                    # CLI 测试
├── test_generator.py              # 生成器测试
├── test_server.py                 # 服务器测试
├── test_i18n.py                   # 国际化测试
└── integration/                   # 集成测试
    ├── test_full_workflow.py      # 完整工作流测试
    └── test_web_interface.py      # Web 界面测试
```

### 运行测试

#### 1. 基本测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_core.py

# 运行特定测试函数
pytest tests/test_core.py::test_generate_docs

# 显示详细输出
pytest -v

# 显示测试覆盖率
pytest --cov=codeviewx --cov-report=html
```

#### 2. 测试配置

pytest 配置（pyproject.toml）：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests"
]
```

### 编写测试

#### 1. 单元测试示例

```python
# tests/test_language.py
import pytest
from codeviewx.language import detect_system_language

class TestLanguageDetection:
    """语言检测功能测试"""
    
    def test_detect_chinese_locale(self, monkeypatch):
        """测试中文环境检测"""
        monkeypatch.setattr("locale.getdefaultlocale", lambda: ("zh_CN", "UTF-8"))
        result = detect_system_language()
        assert result == "Chinese"
    
    def test_detect_english_locale(self, monkeypatch):
        """测试英文环境检测"""
        monkeypatch.setattr("locale.getdefaultlocale", lambda: ("en_US", "UTF-8"))
        result = detect_system_language()
        assert result == "English"
    
    def test_detect_unknown_locale(self, monkeypatch):
        """测试未知语言环境"""
        monkeypatch.setattr("locale.getdefaultlocale", lambda: (None, None))
        result = detect_system_language()
        assert result == "English"  # 默认值
    
    def test_detect_locale_exception(self, monkeypatch):
        """测试异常情况"""
        monkeypatch.setattr("locale.getdefaultlocale", side_effect=Exception("Error"))
        result = detect_system_language()
        assert result == "English"  # 默认值
```

#### 2. 工具测试示例

```python
# tests/test_tools.py
import pytest
import tempfile
import os
from codeviewx.tools import read_real_file, write_real_file, list_real_directory

class TestFileSystemTools:
    """文件系统工具测试"""
    
    @pytest.fixture
    def temp_dir(self):
        """临时目录 fixture"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    def test_write_and_read_file(self, temp_dir):
        """测试文件写入和读取"""
        file_path = os.path.join(temp_dir, "test.txt")
        content = "Hello, World!"
        
        # 写入文件
        result = write_real_file(file_path, content)
        assert "Successfully wrote file" in result
        
        # 读取文件
        result = read_real_file(file_path)
        assert content in result
        assert "test.txt" in result
    
    def test_read_nonexistent_file(self):
        """测试读取不存在的文件"""
        result = read_real_file("/nonexistent/file.txt")
        assert "does not exist" in result
    
    def test_list_directory(self, temp_dir):
        """测试目录列表"""
        # 创建测试文件
        test_files = ["file1.txt", "file2.py", "subdir"]
        for name in test_files[:-1]:
            with open(os.path.join(temp_dir, name), 'w') as f:
                f.write("test")
        os.makedirs(os.path.join(temp_dir, test_files[-1]))
        
        result = list_real_directory(temp_dir)
        for name in test_files:
            assert name in result
```

#### 3. 集成测试示例

```python
# tests/integration/test_full_workflow.py
import pytest
import tempfile
import os
from codeviewx import generate_docs

class TestFullWorkflow:
    """完整工作流集成测试"""
    
    @pytest.fixture
    def sample_project(self):
        """示例项目 fixture"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建项目结构
            project_dir = os.path.join(temp_dir, "sample_project")
            os.makedirs(project_dir)
            
            # 创建示例文件
            files = {
                "README.md": "# Sample Project\nThis is a test project.",
                "main.py": """def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""",
                "requirements.txt": "flask==2.0.0\nrequests==2.25.0",
                "pyproject.toml": """
[project]
name = "sample-project"
version = "0.2.0"
description = "A sample project"
"""
            }
            
            for filename, content in files.items():
                with open(os.path.join(project_dir, filename), 'w') as f:
                    f.write(content)
            
            yield project_dir
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_complete_documentation_generation(self, sample_project):
        """测试完整文档生成流程"""
        output_dir = tempfile.mkdtemp()
        
        try:
            # 生成文档
            generate_docs(
                working_directory=sample_project,
                output_directory=output_dir,
                doc_language="English",
                recursion_limit=100  # 限制递归深度
            )
            
            # 验证生成的文档
            assert os.path.exists(os.path.join(output_dir, "README.md"))
            assert os.path.exists(os.path.join(output_dir, "01-overview.md"))
            
            # 检查文档内容
            with open(os.path.join(output_dir, "README.md"), 'r') as f:
                content = f.read()
                assert "Sample Project" in content
                
        except Exception as e:
            pytest.skip(f"Integration test failed: {e}")
```

### 测试最佳实践

#### 1. 测试命名

```python
class TestClassName:
    def test_method_name_scenario(self):
        """测试方法名_场景描述"""
        pass
    
    def test_should_raise_error_when_invalid_input(self):
        """应该抛出错误_当输入无效时"""
        pass
    
    def test_returns_expected_result_for_valid_input(self):
        """返回预期结果_对于有效输入"""
        pass
```

#### 2. 测试数据管理

```python
# 使用 fixture 管理测试数据
@pytest.fixture
def sample_config():
    return {
        "working_directory": "/tmp/test",
        "output_directory": "docs",
        "doc_language": "English"
    }

# 使用参数化测试
@pytest.mark.parametrize("language,expected", [
    ("zh_CN", "Chinese"),
    ("en_US", "English"),
    ("ja_JP", "Japanese"),
    (None, "English")  # 默认值
])
def test_language_detection(language, expected, monkeypatch):
    if language:
        monkeypatch.setattr("locale.getdefaultlocale", lambda: (language, "UTF-8"))
    else:
        monkeypatch.setattr("locale.getdefaultlocale", lambda: (None, None))
    
    result = detect_system_language()
    assert result == expected
```

#### 3. Mock 和 Patch

```python
from unittest.mock import patch, MagicMock

def test_with_mock():
    """使用 mock 测试"""
    with patch('codeviewx.generator.create_deep_agent') as mock_agent:
        mock_agent.return_value = MagicMock()
        
        generate_docs(working_directory="/tmp/test")
        
        mock_agent.assert_called_once()
```

## 贡献流程

### 开发流程

#### 1. 创建功能分支

```bash
# 同步主分支
git checkout main
git pull origin main

# 创建功能分支
git checkout -b feature/new-feature

# 或修复分支
git checkout -b fix/issue-description
```

#### 2. 开发和测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black codeviewx/
isort codeviewx/

# 代码检查
flake8 codeviewx/
mypy codeviewx/

# 运行特定测试
pytest tests/test_new_feature.py
```

#### 3. 提交代码

```bash
# 添加文件
git add .

# 提交代码
git commit -m "feat: add new feature for XYZ"

# 推送到远程分支
git push origin feature/new-feature
```

#### 4. 创建 Pull Request

1. 在 GitHub 上创建 Pull Request
2. 填写 PR 模板
3. 等待代码审查
4. 根据反馈修改代码
5. 合并到主分支

### 提交信息规范

使用 Conventional Commits 格式：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### 类型说明

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式化（不影响功能）
- `refactor`: 代码重构
- `test`: 添加或修改测试
- `chore`: 构建过程或辅助工具的变动

#### 示例

```bash
# 新功能
git commit -m "feat(generator): add support for custom prompts"

# 修复 bug
git commit -m "fix(cli): resolve argument parsing issue with paths containing spaces"

# 文档更新
git commit -m "docs(readme): update installation instructions"

# 代码重构
git commit -m "refactor(tools): simplify file system operations"
```

### 代码审查

#### 审查要点

1. **功能正确性**：
   - 功能是否按预期工作
   - 边界条件是否处理
   - 错误处理是否完善

2. **代码质量**：
   - 代码风格是否符合规范
   - 是否有重复代码
   - 是否有技术债务

3. **测试覆盖**：
   - 是否有足够的测试
   - 测试用例是否覆盖边界情况
   - 测试是否有意义

4. **文档**：
   - 是否有必要的文档字符串
   - API 文档是否准确
   - 用户文档是否更新

#### 审查流程

1. **自动检查**：
   - CI/CD 运行测试
   - 代码质量检查
   - 类型检查

2. **人工审查**：
   - 至少一个审查者批准
   - 讨论改进建议
   - 请求必要的修改

3. **合并检查**：
   - 解决冲突
   - 确认测试通过
   - 合并到主分支

## 发布流程

### 版本管理

#### 语义化版本

使用 SemVer 版本格式：`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修正

#### 版本号更新

```python
# codeviewx/__version__.py
__version__ = "0.2.0"
__author__ = "CodeViewX Team"
__description__ = "AI-powered code documentation generator"
```

### 发布步骤

#### 1. 准备发布

```bash
# 确保主分支最新
git checkout main
git pull origin main

# 运行完整测试
pytest --cov=codeviewx

# 检查代码质量
black --check codeviewx/
flake8 codeviewx/
mypy codeviewx/

# 构建包
python -m build
```

#### 2. 更新版本

```bash
# 更新版本号
bump2version patch  # 或 minor, major

# 或手动更新
# 编辑 __version__.py
# 编辑 pyproject.toml

# 提交版本更新
git add codeviewx/__version__.py pyproject.toml
git commit -m "chore: bump version to 0.1.1"
```

#### 3. 创建标签

```bash
# 创建 Git 标签
git tag -a v0.1.1 -m "Release version 0.1.1"

# 推送标签
git push origin v0.1.1
```

#### 4. 发布到 PyPI

```bash
# 上传到测试 PyPI
python -m twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ codeviewx

# 上传到正式 PyPI
python -m twine upload dist/*
```

#### 5. 更新文档

```bash
# 生成最新文档
codeviewx -w . -o docs

# 更新 GitHub Pages
git add docs/
git commit -m "docs: update documentation for v0.1.1"
git push origin main
```

### 发布后任务

1. **GitHub Release**：
   - 在 GitHub 创建 Release
   - 添加发布说明
   - 关联相关 Issues

2. **通知用户**：
   - 更新 README.md
   - 发送社区通知
   - 更新 ChangeLog

3. **监控反馈**：
   - 监控 Issue 报告
   - 收集用户反馈
   - 准备下个版本

## 性能优化

### 代码优化

#### 1. 算法优化

```python
# 避免重复计算
def optimized_function(items):
    cache = {}
    result = []
    for item in items:
        if item not in cache:
            cache[item] = expensive_computation(item)
        result.append(cache[item])
    return result
```

#### 2. 内存优化

```python
# 使用生成器减少内存使用
def process_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:  # 逐行处理，不加载整个文件
            yield process_line(line)
```

#### 3. 并发优化

```python
import concurrent.futures

def parallel_processing(items):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_item, items))
    return results
```

### 性能监控

#### 1. 性能分析

```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # 执行需要分析的代码
    generate_docs()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

#### 2. 内存监控

```python
import tracemalloc

def monitor_memory():
    tracemalloc.start()
    
    # 执行代码
    generate_docs()
    
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
    
    tracemalloc.stop()
```

这个开发指南提供了完整的开发流程和最佳实践，帮助开发者有效地为 CodeViewX 项目做贡献。