# 开发指南

## 概述

本指南为希望参与 CodeViewX 项目开发的贡献者提供详细的开发环境配置、代码规范、测试方法和发布流程说明。

## 开发环境配置

### 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows, macOS, Linux
- **内存**: 至少 4GB RAM（推荐 8GB）
- **存储**: 至少 2GB 可用空间
- **网络**: 稳定的互联网连接（用于 AI API 调用）

### 必需工具

#### 1. Python 和包管理

```bash
# 检查 Python 版本
python --version
# 或
python3 --version

# 安装 pip（如果尚未安装）
python -m ensurepip --upgrade
```

#### 2. Git

```bash
# 安装 Git
# macOS
brew install git

# Ubuntu/Debian
sudo apt update
sudo apt install git

# Windows
# 下载并安装 Git for Windows: https://git-scm.com/download/win
```

#### 3. ripgrep

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows (使用 Chocolatey)
choco install ripgrep

# 验证安装
rg --version
```

#### 4. 代码编辑器

推荐使用支持 Python 的现代代码编辑器：

- **VS Code** + Python 扩展
- **PyCharm** (Community 或 Professional)
- **Vim/Neovim** + Python 插件
- **Sublime Text** + Anaconda 插件

### 项目设置

#### 1. 克隆项目

```bash
# 克隆项目仓库
git clone https://github.com/dean2021/codeviewx.git
cd codeviewx

# 查看项目结构
ls -la
```

#### 2. 创建虚拟环境

```bash
# 使用 venv 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 验证虚拟环境
which python
# 应该显示 .venv 目录下的 Python 路径
```

#### 3. 安装依赖

```bash
# 安装开发依赖（推荐）
pip install -e ".[dev]"

# 或者分别安装
pip install -e .
pip install -r requirements-dev.txt

# 验证安装
pip list
```

#### 4. 配置 API 密钥

```bash
# 设置 Anthropic API 密钥（推荐）
export ANTHROPIC_API_KEY='your-api-key-here'

# 或设置 OpenAI API 密钥
export OPENAI_API_KEY='your-api-key-here'

# Windows 用户
set ANTHROPIC_API_KEY=your-api-key-here
```

#### 5. 验证安装

```bash
# 运行基本测试
python -m codeviewx --help

# 测试文档生成（当前目录）
codeviewx -w . -o test_docs --verbose

# 测试 Web 服务器
codeviewx --serve -o test_docs
```

## 项目结构详解

```
codeviewx/
├── codeviewx/                    # 主包目录
│   ├── __init__.py              # 包初始化，导出主要接口
│   ├── __version__.py           # 版本信息
│   ├── cli.py                   # 命令行工具实现
│   ├── core.py                  # 核心功能模块
│   ├── tools/                   # 工具包模块
│   │   ├── __init__.py          # 工具包初始化
│   │   ├── command.py           # 系统命令执行工具
│   │   ├── filesystem.py        # 文件系统操作工具
│   │   └── search.py            # 代码搜索工具
│   ├── prompts/                 # AI 提示词模板
│   │   ├── DocumentEngineer_compact.md  # 精简版提示词（生产用）
│   │   ├── DocumentEngineer.md         # 完整版提示词
│   │   └── DocumentEngineer_original.md # 原始版提示词
│   ├── static/                  # 静态资源文件
│   │   └── css/
│   │       └── typo.css         # 文档样式
│   └── tpl/                     # Web 模板文件
│       └── doc_detail.html      # 文档渲染模板
├── tests/                       # 测试文件目录
│   ├── test_core.py             # 核心功能测试
│   ├── test_tools.py            # 工具模块测试
│   ├── test_language.py         # 语言检测测试
│   └── test_progress.py         # 进度跟踪测试
├── examples/                    # 使用示例
│   ├── basic_usage.py           # 基础使用示例
│   ├── language_demo.py         # 语言检测示例
│   └── progress_demo.py         # 进度显示示例
├── scripts/                     # 构建和部署脚本
├── docs/                        # 项目文档（生成）
├── pyproject.toml              # 项目配置文件
├── requirements.txt            # 生产环境依赖
├── requirements-dev.txt        # 开发环境依赖
├── MANIFEST.in                 # 包含文件清单
├── LICENSE                     # MIT 许可证
├── CHANGELOG.md               # 变更日志
└── README.md                  # 项目说明
```

## 开发工作流

### 1. 分支管理

#### 主要分支

- **main**: 主分支，稳定版本
- **develop**: 开发分支，最新功能
- **feature/***: 功能分支
- **bugfix/***: 修复分支
- **release/***: 发布分支

#### 分支操作

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交更改
git add .
git commit -m "feat: 添加新功能"

# 推送分支
git push origin feature/new-feature

# 合并到开发分支
git checkout develop
git merge feature/new-feature

# 删除功能分支
git branch -d feature/new-feature
```

### 2. 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```bash
# 格式: <type>[optional scope]: <description>

# 功能提交
git commit -m "feat(cli): 添加新的命令行选项"

# 修复提交
git commit -m "fix(tools): 修复文件读取编码问题"

# 文档提交
git commit -m "docs(api): 更新 API 文档"

# 样式提交
git commit -m "style(core): 统一代码格式"

# 重构提交
git commit -m "refactor(core): 重构提示词加载逻辑"

# 测试提交
git commit -m "test(core): 添加核心功能单元测试"

# 构建提交
git commit -m "build(deps): 更新依赖版本"
```

#### 提交类型

| 类型 | 描述 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(api): 添加新接口` |
| `fix` | 修复问题 | `fix(cli): 修复参数解析错误` |
| `docs` | 文档更新 | `docs(readme): 更新安装说明` |
| `style` | 代码格式 | `style(core): 统一代码风格` |
| `refactor` | 重构 | `refactor(tools): 重构工具接口` |
| `test` | 测试 | `test(search): 添加搜索功能测试` |
| `build` | 构建/依赖 | `build(deps): 更新依赖版本` |
| `chore` | 其他 | `chore: 更新配置文件` |

### 3. 代码质量工具

#### Black (代码格式化)

```bash
# 格式化所有代码
black .

# 格式化特定文件
black codeviewx/cli.py

# 检查格式（不修改文件）
black --check .

# 配置文件: pyproject.toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
```

#### isort (导入排序)

```bash
# 排序导入语句
isort .

# 检查导入排序
isort --check-only .

# 配置文件: pyproject.toml
[tool.isort]
profile = "black"
line_length = 100
```

#### flake8 (代码检查)

```bash
# 运行代码检查
flake8 codeviewx/

# 忽略特定错误
flake8 --ignore=E501,W503 codeviewx/

# 配置文件: setup.cfg 或 .flake8
[flake8]
max-line-length = 100
ignore = E501, W503
exclude = .git,__pycache__,docs/source/conf.py,old,build,dist
```

#### MyPy (类型检查)

```bash
# 运行类型检查
mypy codeviewx/

# 配置文件: pyproject.toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
```

### 4. 预提交钩子

安装 pre-commit 来自动化代码质量检查：

```bash
# 安装 pre-commit
pip install pre-commit

# 安装钩子
pre-commit install

# 手动运行所有钩子
pre-commit run --all-files
```

创建 `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## 测试

### 测试框架

使用 pytest 作为主要测试框架：

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_core.py

# 运行特定测试函数
pytest tests/test_core.py::test_generate_docs

# 显示详细输出
pytest -v

# 显示覆盖率
pytest --cov=codeviewx --cov-report=html

# 运行特定标记的测试
pytest -m "unit"  # 单元测试
pytest -m "integration"  # 集成测试
```

### 测试结构

```
tests/
├── conftest.py              # pytest 配置和共享 fixtures
├── test_core.py             # 核心功能测试
├── test_tools.py            # 工具模块测试
├── test_language.py         # 语言检测测试
├── test_progress.py         # 进度跟踪测试
├── unit/                    # 单元测试
│   ├── test_cli.py
│   ├── test_filesystem.py
│   └── test_search.py
├── integration/             # 集成测试
│   ├── test_full_workflow.py
│   └── test_web_server.py
└── fixtures/                # 测试数据
    ├── sample_project/
    └── expected_outputs/
```

### 编写测试

#### 1. 单元测试示例

```python
# tests/test_language.py
import pytest
from codeviewx.core import detect_system_language

class TestLanguageDetection:
    """语言检测功能测试"""
    
    def test_detect_chinese(self, mocker):
        """测试中文检测"""
        mock_locale = mocker.patch('codeviewx.core.locale.getdefaultlocale')
        mock_locale.return_value = ('zh_CN', 'UTF-8')
        
        result = detect_system_language()
        assert result == 'Chinese'
    
    def test_detect_english(self, mocker):
        """测试英文检测"""
        mock_locale = mocker.patch('codeviewx.core.locale.getdefaultlocale')
        mock_locale.return_value = ('en_US', 'UTF-8')
        
        result = detect_system_language()
        assert result == 'English'
    
    def test_detect_fallback(self, mocker):
        """测试检测失败时的回退"""
        mock_locale = mocker.patch('codeviewx.core.locale.getdefaultlocale')
        mock_locale.side_effect = Exception("模拟错误")
        
        result = detect_system_language()
        assert result == 'English'
```

#### 2. 集成测试示例

```python
# tests/integration/test_full_workflow.py
import pytest
import tempfile
import os
from pathlib import Path
from codeviewx import generate_docs

class TestFullWorkflow:
    """完整工作流集成测试"""
    
    @pytest.fixture
    def temp_project(self):
        """创建临时测试项目"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "test_project"
            project_dir.mkdir()
            
            # 创建测试文件
            (project_dir / "main.py").write_text("""
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
            """)
            
            (project_dir / "README.md").write_text("""
# Test Project

This is a test project for CodeViewX.
            """)
            
            yield project_dir
    
    def test_generate_docs_integration(self, temp_project):
        """测试完整文档生成流程"""
        output_dir = temp_project / "docs"
        
        # 生成文档
        generate_docs(
            working_directory=str(temp_project),
            output_directory=str(output_dir),
            doc_language="English",
            verbose=False
        )
        
        # 验证生成的文件
        assert output_dir.exists()
        assert (output_dir / "README.md").exists()
        assert (output_dir / "01-overview.md").exists()
        
        # 验证文档内容
        readme_content = (output_dir / "README.md").read_text()
        assert "Test Project" in readme_content
```

#### 3. Mock 和 Fixture 使用

```python
# tests/conftest.py
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

@pytest.fixture
def mock_api_key():
    """模拟 API 密钥"""
    with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
        yield

@pytest.fixture
def sample_project():
    """提供示例项目结构"""
    with tempfile.TemporaryDirectory() as temp_dir:
        project = Path(temp_dir)
        
        # 创建目录结构
        (project / "src").mkdir()
        (project / "tests").mkdir()
        
        # 创建文件
        (project / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "1.0.0"
        """)
        
        (project / "src" / "main.py").write_text("""
def main():
    pass
        """)
        
        yield project

@pytest.fixture
def mock_agent():
    """模拟 AI Agent"""
    agent = Mock()
    agent.stream.return_value = iter([
        {"messages": [Mock(tool_calls=[], content="分析完成")]}
    ])
    return agent
```

### 测试配置

#### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=codeviewx
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80

markers =
    unit: 单元测试
    integration: 集成测试
    slow: 慢速测试
    external: 需要外部依赖的测试
```

### 测试覆盖率

```bash
# 生成覆盖率报告
pytest --cov=codeviewx --cov-report=html

# 查看报告
open htmlcov/index.html

# 设置覆盖率阈值
pytest --cov=codeviewx --cov-fail-under=80
```

## 调试

### 1. 日志调试

启用详细日志：

```python
import logging

# 设置日志级别
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 或在代码中
logger = logging.getLogger(__name__)
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
```

### 2. Python 调试器

使用 pdb 进行断点调试：

```python
import pdb

def debug_function():
    # 设置断点
    pdb.set_trace()
    
    # 或使用条件断点
    if some_condition:
        pdb.set_trace()
    
    # 继续执行
    result = some_calculation()
    return result
```

常用的 pdb 命令：

- `n` (next): 执行下一行
- `c` (continue): 继续执行到下一个断点
- `l` (list): 显示当前代码
- `p variable` (print): 打印变量值
- `q` (quit): 退出调试器

### 3. IDE 调试

#### VS Code 调试配置

创建 `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug CodeViewX CLI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/codeviewx/cli.py",
            "args": ["-w", "${workspaceFolder}", "--verbose"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/test_core.py", "-v"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

#### PyCharm 调试配置

1. 创建 "Python" 运行配置
2. 设置脚本路径为 `codeviewx/cli.py`
3. 添加参数 `-w . --verbose`
4. 设置工作目录为项目根目录
5. 点击调试按钮启动

### 4. 性能分析

使用 cProfile 进行性能分析：

```python
import cProfile
import pstats

def profile_function():
    """性能分析示例"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # 执行要分析的代码
    generate_docs(verbose=True)
    
    profiler.disable()
    
    # 保存分析结果
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # 显示前 20 个最耗时的函数
    
    # 保存到文件
    stats.dump_stats('profile_results.prof')

# 运行分析
if __name__ == "__main__":
    profile_function()
```

## 贡献指南

### 1. 报告问题

使用 GitHub Issues 报告问题：

1. 检查是否已有类似问题
2. 使用合适的模板
3. 提供详细信息：
   - 操作系统和 Python 版本
   - CodeViewX 版本
   - 重现步骤
   - 预期行为和实际行为
   - 错误信息和日志

### 2. 提交代码

#### Fork 项目

1. 在 GitHub 上 Fork 项目
2. 克隆你的 Fork：
   ```bash
   git clone https://github.com/your-username/codeviewx.git
   cd codeviewx
   git remote add upstream https://github.com/dean2021/codeviewx.git
   ```

#### 创建分支

```bash
# 同步最新代码
git fetch upstream
git checkout main
git merge upstream/main

# 创建功能分支
git checkout -b feature/your-feature-name
```

#### 开发和测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 运行代码质量检查
black --check .
isort --check-only .
flake8 .
mypy codeviewx/
```

#### 提交 Pull Request

1. 确保所有测试通过
2. 更新相关文档
3. 提交代码并推送：
   ```bash
   git add .
   git commit -m "feat: 添加新功能"
   git push origin feature/your-feature-name
   ```
4. 在 GitHub 上创建 Pull Request
5. 填写 PR 模板，描述更改内容
6. 等待代码审查

### 3. 代码审查标准

#### 必须满足的条件

- [ ] 所有测试通过
- [ ] 代码覆盖率不低于 80%
- [ ] 通过所有代码质量检查
- [ ] 更新相关文档
- [ ] 遵循代码风格规范
- [ ] 添加适当的测试

#### 审查要点

1. **功能正确性**: 代码是否按预期工作
2. **代码质量**: 是否清晰、可维护
3. **性能影响**: 是否有性能问题
4. **安全性**: 是否存在安全隐患
5. **文档完整性**: 文档是否更新
6. **向后兼容性**: 是否破坏现有功能

## 发布流程

### 1. 版本管理

使用语义化版本控制 (Semantic Versioning):

- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

#### 版本示例

- `0.1.0`: 初始版本
- `0.1.1`: 修复版本
- `0.2.0`: 新功能版本
- `1.0.0`: 稳定版本

### 2. 发布检查清单

发布前检查：

- [ ] 所有测试通过
- [ ] 文档更新完成
- [ ] CHANGELOG.md 更新
- [ ] 版本号更新
- [ ] 安全检查完成
- [ ] 性能测试通过
- [ ] 兼容性测试完成

### 3. 发布步骤

```bash
# 1. 更新版本号
vim codeviewx/__version__.py
vim pyproject.toml

# 2. 更新 CHANGELOG.md
vim CHANGELOG.md

# 3. 运行完整测试
pytest
black --check .
isort --check-only .
flake8 .
mypy codeviewx/

# 4. 构建包
python -m build

# 5. 检查包
twine check dist/*

# 6. 上传到测试 PyPI
twine upload --repository testpypi dist/*

# 7. 安装测试版本
pip install --index-url https://test.pypi.org/simple/ codeviewx

# 8. 测试功能
codeviewx --help
codeviewx -w . -o test_docs

# 9. 上传到正式 PyPI
twine upload dist/*

# 10. 创建 Git 标签
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# 11. 更新 GitHub Releases
# 在 GitHub 上创建 Release，上传构建的包
```

### 4. 发布后任务

- [ ] 更新文档网站
- [ ] 发布博客文章（如需要）
- [ ] 通知用户社区
- [ ] 监控用户反馈
- [ ] 准备下一个版本

## 性能优化

### 1. 代码优化

#### 使用性能分析工具

```python
import time
import cProfile
from functools import wraps

def profile_performance(func):
    """性能分析装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # 使用 cProfile 分析
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        
        # 输出性能数据
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # 显示前 10 个最耗时函数
        
        elapsed_time = time.time() - start_time
        print(f"函数 {func.__name__} 执行时间: {elapsed_time:.2f} 秒")
        
        return result
    return wrapper

# 使用示例
@profile_performance
def slow_function():
    # 模拟耗时操作
    time.sleep(1)
    return "完成"
```

#### 优化建议

1. **减少文件 I/O**: 使用缓存机制
2. **优化搜索**: 使用更精确的搜索模式
3. **并行处理**: 使用多线程/多进程
4. **内存管理**: 及时释放不需要的对象

### 2. 内存优化

```python
import gc
import psutil
import os

def monitor_memory():
    """监控内存使用"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")

def optimize_memory():
    """内存优化示例"""
    # 强制垃圾回收
    gc.collect()
    
    # 监控内存使用
    monitor_memory()
    
    # 执行内存密集操作
    # ...
    
    # 操作完成后再次清理
    gc.collect()
    monitor_memory()
```

## 故障排除

### 常见问题

#### 1. 安装问题

**问题**: `ModuleNotFoundError: No module named 'codeviewx'`

**解决方案**:
```bash
# 确保在虚拟环境中
source .venv/bin/activate

# 重新安装
pip install -e .

# 检查 Python 路径
which python
python -c "import sys; print(sys.path)"
```

#### 2. API 密钥问题

**问题**: API 调用失败

**解决方案**:
```bash
# 检查环境变量
echo $ANTHROPIC_API_KEY

# 重新设置
export ANTHROPIC_API_KEY='your-key'

# 在 Python 中检查
import os
print(os.getenv('ANTHROPIC_API_KEY'))
```

#### 3. ripgrep 问题

**问题**: `rg: command not found`

**解决方案**:
```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# 验证安装
rg --version
```

#### 4. 性能问题

**问题**: 文档生成速度慢

**解决方案**:
```bash
# 使用精简模式
codeviewx --recursion-limit 500

# 启用详细日志查看瓶颈
codeviewx --verbose

# 分析小项目测试
codeviewx -w ./small_project
```

### 日志分析

启用详细日志进行分析：

```python
import logging

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('codeviewx_debug.log'),
        logging.StreamHandler()
    ]
)

# 运行并查看日志
codeviewx --verbose > debug_output.log 2>&1
```

### 获取帮助

1. **查看文档**: 生成项目文档
2. **GitHub Issues**: 搜索已有问题或创建新问题
3. **社区讨论**: 参与项目讨论
4. **邮件联系**: dean@csoio.com

---

通过遵循本开发指南，您可以有效地参与 CodeViewX 项目的开发，贡献高质量的代码，并帮助改进这个 AI 驱动的文档生成工具。