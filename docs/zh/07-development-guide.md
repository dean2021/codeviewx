# 开发指南

## 概述

本指南旨在帮助开发者参与 CodeViewX 项目的开发，包括环境搭建、代码规范、测试流程、贡献方式等内容。CodeViewX 是一个开源项目，欢迎社区贡献。

## 开发环境搭建

### 1. 系统要求

- **Python**: 3.8 或更高版本
- **Git**: 用于版本控制
- **ripgrep**: 代码搜索工具
- **IDE**: 推荐 VS Code 或 PyCharm

### 2. 克隆项目

```bash
# 克隆仓库
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# 查看项目结构
ls -la
```

### 3. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 使用 conda
conda create -n codeviewx python=3.9
conda activate codeviewx
```

### 4. 安装依赖

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 安装项目（可编辑模式）
pip install -e .
```

### 5. 安装 ripgrep

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt-get install ripgrep

# Windows
scoop install ripgrep  # 或 choco install ripgrep
```

### 6. 配置开发环境

#### 配置 API 密钥

```bash
# 设置测试用的 API 密钥
export ANTHROPIC_AUTH_TOKEN='your-test-api-key'

# 或创建 .env 文件
echo 'ANTHROPIC_AUTH_TOKEN=your-test-api-key' > .env
```

#### IDE 配置

**VS Code 配置** (`.vscode/settings.json`):

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

**PyCharm 配置**:
- 设置 Python 解释器为项目虚拟环境
- 启用 Black 代码格式化
- 启用 flake8 代码检查
- 启用 mypy 类型检查

## 项目结构详解

```
codeviewx/
├── codeviewx/                    # 主要源代码包
│   ├── __init__.py              # 包初始化，导出公共 API
│   ├── __version__.py           # 版本号定义
│   ├── cli.py                   # 命令行接口
│   ├── core.py                  # 核心模块，公共 API 入口
│   ├── generator.py             # 文档生成器核心逻辑
│   ├── i18n.py                  # 国际化支持
│   ├── language.py              # 语言检测
│   ├── prompt.py                # 提示词管理
│   ├── server.py                # Web 服务器
│   ├── tools/                   # 工具模块包
│   │   ├── __init__.py          # 工具导出
│   │   ├── command.py           # 系统命令执行工具
│   │   ├── filesystem.py        # 文件系统操作工具
│   │   └── search.py            # 代码搜索工具
│   ├── prompts/                 # AI 提示词模板
│   │   ├── document_engineer.md # 英文提示词
│   │   └── document_engineer_zh.md # 中文提示词
│   ├── static/                  # Web 静态资源
│   │   ├── css/                 # 样式文件
│   │   └── js/                  # JavaScript 文件
│   └── tpl/                     # HTML 模板
│       └── doc_detail.html      # 文档展示模板
├── tests/                       # 测试文件
├── docs/                        # 项目文档
├── examples/                    # 示例项目
├── pyproject.toml              # 项目配置
├── requirements.txt            # 生产依赖
├── requirements-dev.txt        # 开发依赖
└── README.md                   # 项目说明
```

## 代码规范

### 1. Python 代码规范

项目使用以下工具确保代码质量：

- **Black**: 代码格式化
- **flake8**: 代码风格检查
- **mypy**: 静态类型检查
- **isort**: 导入语句排序

#### 配置文件

**pyproject.toml**:
```toml
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
```

#### 代码风格指南

1. **行长度**: 最多 100 个字符
2. **缩进**: 4 个空格
3. **引号**: 优先使用双引号
4. **导入**: 按标准库、第三方库、本地模块的顺序导入

```python
# 正确的导入顺序
import os
import sys
from typing import Optional, Dict, List

from langchain_anthropic import ChatAnthropic
from deepagents import create_deep_agent

from .tools import execute_command, ripgrep_search
from .i18n import t
```

### 2. 文档字符串规范

使用 Google 风格的文档字符串：

```python
def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    verbose: bool = False
) -> None:
    """生成项目技术文档
    
    Args:
        working_directory: 项目工作目录，默认为当前目录
        output_directory: 文档输出目录，默认为 'docs'
        doc_language: 文档语言，支持中文、英文等
        verbose: 是否显示详细日志
        
    Raises:
        ValueError: 当 API 密钥未配置时
        FileNotFoundError: 当工作目录不存在时
        
    Examples:
        >>> generate_docs()
        >>> generate_docs(working_directory="/path/to/project", doc_language="English")
    """
```

### 3. 类型提示规范

所有公共 API 都应包含类型提示：

```python
from typing import Optional, Dict, List, Union

def process_files(
    file_paths: List[str],
    options: Optional[Dict[str, Union[str, bool]]] = None
) -> Dict[str, str]:
    """处理文件列表"""
    pass
```

## 开发流程

### 1. 分支管理

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 创建修复分支
git checkout -b fix/bug-fix

# 创建文档分支
git checkout -b docs/update-docs
```

### 2. 开发步骤

1. **需求分析**: 明确要实现的功能或修复的问题
2. **设计讨论**: 在 Issues 中讨论设计方案
3. **编码实现**: 按照代码规范实现功能
4. **测试验证**: 编写和运行测试
5. **文档更新**: 更新相关文档
6. **代码审查**: 提交 Pull Request

### 3. 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```bash
# 功能提交
git commit -m "feat: 添加新的文档格式支持"

# 修复提交
git commit -m "fix: 修复 API 密钥验证问题"

# 文档提交
git commit -m "docs: 更新 API 参考文档"

# 样式提交
git commit -m "style: 代码格式化"

# 重构提交
git commit -m "refactor: 重构工具模块结构"

# 测试提交
git commit -m "test: 添加工具模块单元测试"

# 构建提交
git commit -m "build: 更新依赖版本"
```

### 4. 代码质量检查

提交前运行质量检查：

```bash
# 代码格式化
black codeviewx/

# 导入排序
isort codeviewx/

# 代码风格检查
flake8 codeviewx/

# 类型检查
mypy codeviewx/

# 运行测试
pytest tests/ -v

# 生成覆盖率报告
pytest tests/ --cov=codeviewx --cov-report=html
```

## 测试指南

### 1. 测试结构

```
tests/
├── __init__.py
├── test_cli.py              # CLI 测试
├── test_generator.py        # 生成器测试
├── test_tools.py            # 工具模块测试
├── test_i18n.py             # 国际化测试
├── test_server.py           # Web 服务器测试
├── test_integration.py      # 集成测试
└── fixtures/                # 测试数据
    ├── sample_project/      # 示例项目
    └── expected_docs/       # 期望的文档输出
```

### 2. 单元测试

使用 pytest 框架编写单元测试：

```python
# tests/test_tools.py
import pytest
from codeviewx.tools import read_real_file, write_real_file, list_real_directory

class TestFileSystemTools:
    """文件系统工具测试"""
    
    def test_read_real_file_success(self, tmp_path):
        """测试成功读取文件"""
        # 创建测试文件
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")
        
        # 测试读取
        result = read_real_file(str(test_file))
        assert "Hello, World!" in result
        assert "1 lines" in result
    
    def test_read_real_file_not_found(self):
        """测试文件不存在的情况"""
        result = read_real_file("nonexistent.txt")
        assert "does not exist" in result
    
    def test_write_real_file_success(self, tmp_path):
        """测试成功写入文件"""
        test_file = tmp_path / "output.txt"
        content = "Test content"
        
        result = write_real_file(str(test_file), content)
        assert "Successfully wrote file" in result
        assert test_file.read_text() == content
```

### 3. 集成测试

```python
# tests/test_integration.py
import pytest
import tempfile
import os
from codeviewx import generate_docs

class TestIntegration:
    """集成测试"""
    
    def test_full_documentation_generation(self, tmp_path):
        """测试完整的文档生成流程"""
        # 创建测试项目
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # 创建测试文件
        (project_dir / "README.md").write_text("# Test Project")
        (project_dir / "main.py").write_text("""
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
        """)
        
        # 生成文档
        output_dir = tmp_path / "docs"
        
        # 注意：集成测试需要真实的 API 密钥
        # 在 CI/CD 中应该使用模拟或跳过
        if os.getenv("ANTHROPIC_AUTH_TOKEN"):
            generate_docs(
                working_directory=str(project_dir),
                output_directory=str(output_dir),
                doc_language="English"
            )
            
            # 验证生成的文件
            assert (output_dir / "README.md").exists()
            assert (output_dir / "01-overview.md").exists()
```

### 4. 测试配置

**pytest.ini**:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --cov=codeviewx
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
```

### 5. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_tools.py

# 运行特定测试类
pytest tests/test_tools.py::TestFileSystemTools

# 运行特定测试方法
pytest tests/test_tools.py::TestFileSystemTools::test_read_real_file_success

# 运行带标记的测试
pytest -m unit
pytest -m "not slow"

# 生成覆盖率报告
pytest --cov=codeviewx --cov-report=html

# 并行运行测试
pytest -n auto
```

## 调试指南

### 1. 日志配置

```python
import logging

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# 启用特定模块的详细日志
logging.getLogger("langchain").setLevel(logging.DEBUG)
logging.getLogger("langgraph").setLevel(logging.DEBUG)
```

### 2. 调试模式

使用 `--verbose` 参数启用详细输出：

```bash
codeviewx --verbose -w ./test-project
```

### 3. 常见问题调试

#### API 调用问题

```python
import os
from codeviewx.generator import validate_api_key

# 验证 API 密钥
try:
    validate_api_key()
    print("API 密钥配置正确")
except ValueError as e:
    print(f"API 密钥错误: {e}")
    print(f"当前密钥: {os.getenv('ANTHROPIC_AUTH_TOKEN', '未设置')}")
```

#### 工具调用问题

```python
from codeviewx.tools import read_real_file, ripgrep_search

# 测试文件读取
result = read_real_file("/path/to/file")
print(result)

# 测试搜索功能
result = ripgrep_search("def main", "/path/to/project", "py")
print(result)
```

## 贡献指南

### 1. 报告问题

- 使用 [GitHub Issues](https://github.com/dean2021/codeviewx/issues) 报告问题
- 提供详细的错误信息和复现步骤
- 包含系统环境信息（Python 版本、操作系统等）

### 2. 功能请求

- 在 Issues 中描述期望的功能
- 说明使用场景和预期行为
- 讨论实现方案

### 3. 提交代码

1. **Fork 项目**: 在 GitHub 上 Fork 项目到个人账户
2. **创建分支**: 基于主分支创建功能分支
3. **开发测试**: 实现功能并编写测试
4. **提交 PR**: 提交 Pull Request 到主分支

### 4. 代码审查

Pull Request 需要通过以下检查：

- [ ] 所有测试通过
- [ ] 代码覆盖率达标
- [ ] 代码风格检查通过
- [ ] 类型检查通过
- [ ] 文档已更新
- [ ] 提交信息符合规范

### 5. 文档贡献

- 修复文档错误
- 改进文档说明
- 添加使用示例
- 翻译文档内容

## 发布流程

### 1. 版本管理

使用语义化版本控制：

- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 2. 发布步骤

```bash
# 1. 更新版本号
vim codeviewx/__version__.py

# 2. 更新 CHANGELOG
vim CHANGELOG.md

# 3. 运行完整测试
pytest
flake8 codeviewx/
mypy codeviewx/

# 4. 构建包
python -m build

# 5. 上传到 PyPI（测试环境）
python -m twine upload --repository testpypi dist/*

# 6. 上传到 PyPI（生产环境）
python -m twine upload dist/*

# 7. 创建 Git 标签
git tag v0.2.8
git push origin v0.2.8
```

### 3. 发布检查清单

- [ ] 版本号已更新
- [ ] CHANGELOG 已更新
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] 包构建成功
- [ ] 测试发布验证
- [ ] Git 标签已创建

## 性能优化

### 1. 代码优化

- **避免重复计算**: 缓存计算结果
- **使用合适的数据结构**: 选择最优的数据结构
- **减少 I/O 操作**: 批量处理文件操作

### 2. 内存优化

- **流式处理**: 处理大文件时使用流式读取
- **及时释放**: 不再需要的对象及时释放
- **监控内存**: 使用工具监控内存使用

### 3. 性能测试

```python
import time
import psutil
from codeviewx import generate_docs

def performance_test():
    """性能测试"""
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss
    
    generate_docs(working_directory="./test-project")
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss
    
    print(f"执行时间: {end_time - start_time:.2f} 秒")
    print(f"内存使用: {(end_memory - start_memory) / 1024 / 1024:.2f} MB")
```

## 社区参与

### 1. 讨论渠道

- **GitHub Issues**: 问题报告和功能讨论
- **GitHub Discussions**: 一般讨论和问答
- **Wiki**: 详细文档和教程

### 2. 行为准则

- 尊重所有参与者
- 保持友好和专业
- 接受建设性的反馈
- 专注于对社区最有利的事情

### 3. 认可贡献者

所有贡献者都会在项目中得到认可：

- **AUTHORS**: 贡献者列表
- **CHANGELOG**: 版本更新中的贡献说明
- **GitHub**: 贡献统计和展示

---

💡 **感谢**: 感谢所有为 CodeViewX 项目做出贡献的开发者！每一个 Issue、Pull Request 和建议都让这个项目变得更好。