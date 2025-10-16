# CodeViewX 快速开始指南

## ✅ 重构已完成！

CodeViewX 现在是一个标准的 Python 包，可以通过 pip 安装并使用。

---

## 🚀 立即开始

### 1. 验证安装

```bash
# 检查版本
codeviewx --version
# 输出: CodeViewX 0.1.0 ✅

# 查看帮助
codeviewx --help
```

### 2. 命令行使用

```bash
# 分析当前项目
codeviewx

# 分析指定项目
codeviewx -w /path/to/project -o docs

# 显示详细日志
codeviewx --verbose
```

### 3. Python API 使用

```python
# 导入包
from codeviewx import generate_docs, load_prompt

# 生成文档
generate_docs(
    working_directory=".",
    output_directory=".wiki"
)
```

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_core.py -v
```

---

## 📊 验证结果

### ✅ 包安装
```bash
$ pip show codeviewx
Name: codeviewx
Version: 0.1.0
Location: /Users/deanlu/Desktop/projects/codeviewx
```

### ✅ 命令行工具
```bash
$ which codeviewx
.venv/bin/codeviewx
```

### ✅ Python 导入
```python
>>> from codeviewx import load_prompt, generate_docs
>>> print("✅ Import successful!")
✅ Import successful!
```

### ✅ 测试
```bash
$ pytest tests/ -v
16 passed in 0.21s ✅
```

---

## 📁 新的目录结构

```
codeviewx/                          # ✅ 标准包结构
├── codeviewx/                     # 包目录
│   ├── __init__.py               # 包初始化
│   ├── cli.py                    # CLI 工具
│   ├── core.py                   # 核心功能
│   ├── tools/                    # 工具模块
│   └── prompts/                  # 提示词资源
├── tests/                        # 测试
├── docs/                         # 文档
├── examples/                     # 示例
├── pyproject.toml               # 包配置 ⭐
├── LICENSE                      # MIT 许可证
└── README.md                    # 项目说明
```

---

## 🎯 主要特性

| 特性 | 状态 | 说明 |
|-----|------|------|
| pip 安装 | ✅ | `pip install -e .` |
| CLI 工具 | ✅ | `codeviewx --help` |
| Python API | ✅ | `from codeviewx import ...` |
| 单元测试 | ✅ | 16/16 通过 |
| 文档 | ✅ | 完整的 README |
| PyPI 就绪 | ✅ | 可发布 |

---

## 📚 更多资源

- [完整 README](README.md) - 项目完整说明
- [重构完成报告](REFACTORING_COMPLETE.md) - 详细的重构报告
- [使用示例](docs/usage-examples.md) - 更多使用示例
- [重构方案](docs/refactoring-plan.md) - 重构技术文档

---

## 🔥 下一步

### 立即可用
```bash
# 1. 分析您的项目
codeviewx -w /path/to/your/project -o docs

# 2. 或在 Python 中使用
python -c "from codeviewx import generate_docs; generate_docs()"
```

### 清理（可选）
```bash
# 旧的目录可以删除了（已被新包替代）
rm -rf tools/ prompt/ main.py  # 可选
```

### 发布（可选）
```bash
# 构建包
python -m build

# 上传到 PyPI
twine upload dist/*
```

---

## 💡 提示

- 🔑 别忘了设置 API 密钥：`export ANTHROPIC_API_KEY='your-key'`
- 🚀 使用 `--verbose` 查看详细日志
- 📦 运行 `pip install -e ".[dev]"` 安装开发依赖
- 🧪 运行 `pytest` 确保一切正常

---

**享受 CodeViewX！** 🎉

