# CodeViewX 使用示例

本文档展示 CodeViewX 的各种使用场景和配置方式。

---

## 目录

1. [基本使用](#基本使用)
2. [自定义输出目录](#自定义输出目录)
3. [分析不同类型的项目](#分析不同类型的项目)
4. [多语言文档生成](#多语言文档生成)
5. [批量处理多个项目](#批量处理多个项目)
6. [与 CI/CD 集成](#与-cicd-集成)

---

## 基本使用

### 默认配置

最简单的使用方式，文档保存到 `.wiki/` 目录：

```python
import os
from main import load_prompt
from deepagents import create_deep_agent
from tools import (
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
)

# 配置
working_directory = os.getcwd()
output_directory = ".wiki"

# 加载提示词
prompt = load_prompt(
    "DocumentEngineer",
    working_directory=working_directory,
    output_directory=output_directory
)

# 创建 Agent
tools = [execute_command, ripgrep_search, write_real_file, read_real_file, list_real_directory]
agent = create_deep_agent(tools, prompt)

# 运行
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "请根据系统提示词中的工作目录，分析该项目并生成深度技术文档"}]},
    stream_mode="values",
    config={"recursion_limit": 1000}
):
    # 处理输出
    pass
```

---

## 自定义输出目录

### 使用标准 `docs` 目录

```python
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/Users/username/projects/my-app",
    output_directory="docs"
)
```

**结果**：
```
my-app/
├── src/
├── tests/
└── docs/              ← 文档保存在这里
    ├── README.md
    ├── 01-overview.md
    ├── 02-quickstart.md
    └── ...
```

### 使用嵌套目录

```python
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/Users/username/projects/my-app",
    output_directory="documentation/technical"
)
```

**结果**：
```
my-app/
└── documentation/
    └── technical/     ← 文档保存在这里
        ├── README.md
        └── ...
```

### 使用绝对路径

```python
prompt = load_prompt(
    "DocumentEngineer",
    working_directory="/Users/username/projects/my-app",
    output_directory="/Users/username/Documents/project-docs"
)
```

---

## 分析不同类型的项目

### Python 项目

```python
def analyze_python_project(project_path: str):
    """分析 Python 项目"""
    
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory=project_path,
        output_directory="docs"
    )
    
    # 项目特征：
    # - requirements.txt 或 pyproject.toml
    # - setup.py
    # - Python 包结构
    
    return prompt
```

### Node.js 项目

```python
def analyze_nodejs_project(project_path: str):
    """分析 Node.js 项目"""
    
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory=project_path,
        output_directory="docs/wiki"
    )
    
    # 项目特征：
    # - package.json
    # - node_modules/
    # - JavaScript/TypeScript
    
    return prompt
```

### Web 应用

```python
def analyze_web_app(project_path: str):
    """分析 Web 应用"""
    
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory=project_path,
        output_directory="docs/technical"
    )
    
    # 重点分析：
    # - 路由配置
    # - API 端点
    # - 前后端交互
    # - 数据模型
    
    return prompt
```

---

## 多语言文档生成

### 中英文双语文档

```python
import os
from pathlib import Path

def generate_multilingual_docs(project_path: str):
    """生成中英文双语文档"""
    
    project_path = Path(project_path)
    
    # 生成中文文档
    print("📝 生成中文文档...")
    prompt_zh = load_prompt(
        "DocumentEngineer",
        working_directory=str(project_path),
        output_directory="docs/zh"
    )
    # ... 运行 agent 生成中文文档
    
    # 生成英文文档
    print("📝 生成英文文档...")
    prompt_en = load_prompt(
        "DocumentEngineer-EN",  # 英文版提示词
        working_directory=str(project_path),
        output_directory="docs/en"
    )
    # ... 运行 agent 生成英文文档
    
    print("✅ 双语文档生成完成！")

# 使用
generate_multilingual_docs("/Users/username/projects/my-app")
```

**结果**：
```
my-app/
└── docs/
    ├── zh/                ← 中文文档
    │   ├── README.md
    │   ├── 01-overview.md
    │   └── ...
    └── en/                ← 英文文档
        ├── README.md
        ├── 01-overview.md
        └── ...
```

---

## 批量处理多个项目

### 批量分析多个项目

```python
from pathlib import Path
from typing import List

def batch_analyze_projects(project_dirs: List[str], output_base: str = "docs"):
    """批量分析多个项目"""
    
    results = []
    
    for project_dir in project_dirs:
        project_path = Path(project_dir)
        project_name = project_path.name
        
        print(f"\n{'='*60}")
        print(f"📂 分析项目: {project_name}")
        print(f"{'='*60}")
        
        try:
            # 为每个项目生成文档
            prompt = load_prompt(
                "DocumentEngineer",
                working_directory=str(project_path),
                output_directory=output_base
            )
            
            # ... 运行 agent
            
            results.append({
                "project": project_name,
                "status": "success",
                "output": project_path / output_base
            })
            
            print(f"✅ {project_name} 分析完成")
            
        except Exception as e:
            print(f"❌ {project_name} 分析失败: {e}")
            results.append({
                "project": project_name,
                "status": "failed",
                "error": str(e)
            })
    
    # 生成总结报告
    print("\n" + "="*60)
    print("📊 批量分析总结")
    print("="*60)
    for result in results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"{status_icon} {result['project']}: {result['status']}")
    
    return results

# 使用
projects = [
    "/Users/username/projects/project-a",
    "/Users/username/projects/project-b",
    "/Users/username/projects/project-c",
]

batch_analyze_projects(projects, output_base=".wiki")
```

---

## 与 CI/CD 集成

### GitHub Actions

创建 `.github/workflows/generate-docs.yml`：

```yaml
name: 生成项目文档

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout 代码
      uses: actions/checkout@v3
    
    - name: 设置 Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: 安装依赖
      run: |
        pip install -r requirements.txt
        sudo apt-get install -y ripgrep
    
    - name: 生成文档
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        python -c "
        import os
        from main import load_prompt
        
        # 生成文档
        prompt = load_prompt(
            'DocumentEngineer',
            working_directory=os.getcwd(),
            output_directory='docs'
        )
        # ... 运行 agent
        "
    
    - name: 提交文档
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        git add docs/
        git commit -m "docs: 自动生成项目文档 [skip ci]" || echo "没有变化"
        git push
```

### GitLab CI

创建 `.gitlab-ci.yml`：

```yaml
stages:
  - docs

generate-docs:
  stage: docs
  image: python:3.10
  
  before_script:
    - pip install -r requirements.txt
    - apt-get update && apt-get install -y ripgrep
  
  script:
    - |
      python -c "
      import os
      from main import load_prompt
      
      prompt = load_prompt(
          'DocumentEngineer',
          working_directory=os.getcwd(),
          output_directory='documentation'
      )
      # ... 运行 agent
      "
    
    - git config user.email "gitlab-ci@example.com"
    - git config user.name "GitLab CI"
    - git add documentation/
    - git commit -m "docs: 自动生成文档 [skip ci]" || echo "没有变化"
    - git push origin HEAD:$CI_COMMIT_REF_NAME
  
  only:
    - main
```

---

## 高级配置

### 环境变量配置

```python
import os
from pathlib import Path

def get_config_from_env():
    """从环境变量获取配置"""
    
    working_dir = os.getenv("PROJECT_DIR", os.getcwd())
    output_dir = os.getenv("DOCS_OUTPUT_DIR", ".wiki")
    
    return {
        "working_directory": working_dir,
        "output_directory": output_dir
    }

# 使用
config = get_config_from_env()
prompt = load_prompt("DocumentEngineer", **config)
```

### 配置文件支持

创建 `.codeviewx.yaml`：

```yaml
# CodeViewX 配置文件
working_directory: .
output_directory: docs/wiki
recursion_limit: 1000
stream_mode: values
```

读取配置：

```python
import yaml
from pathlib import Path

def load_config(config_file: str = ".codeviewx.yaml"):
    """加载配置文件"""
    
    config_path = Path(config_file)
    if not config_path.exists():
        return {
            "working_directory": ".",
            "output_directory": ".wiki",
            "recursion_limit": 1000,
            "stream_mode": "values"
        }
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# 使用
config = load_config()
prompt = load_prompt(
    "DocumentEngineer",
    working_directory=config["working_directory"],
    output_directory=config["output_directory"]
)
```

---

## 命令行工具

创建 `cli.py`：

```python
#!/usr/bin/env python3
"""
CodeViewX 命令行工具
"""

import argparse
import os
from pathlib import Path
from main import load_prompt

def main():
    parser = argparse.ArgumentParser(
        description="CodeViewX - AI 驱动的代码文档生成器"
    )
    
    parser.add_argument(
        "-w", "--working-dir",
        default=os.getcwd(),
        help="项目工作目录（默认：当前目录）"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default=".wiki",
        help="文档输出目录（默认：.wiki）"
    )
    
    parser.add_argument(
        "--recursion-limit",
        type=int,
        default=1000,
        help="递归限制（默认：1000）"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print(f"🚀 CodeViewX 文档生成器")
    print("=" * 80)
    print(f"📂 工作目录: {args.working_dir}")
    print(f"📝 输出目录: {args.output_dir}")
    print("=" * 80)
    
    # 生成文档
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory=args.working_dir,
        output_directory=args.output_dir
    )
    
    # ... 运行 agent
    
    print("\n✅ 文档生成完成！")

if __name__ == "__main__":
    main()
```

使用：

```bash
# 默认配置
python cli.py

# 自定义工作目录
python cli.py --working-dir /path/to/project

# 自定义输出目录
python cli.py --output-dir docs

# 完整配置
python cli.py \
  --working-dir /path/to/project \
  --output-dir documentation/technical \
  --recursion-limit 1500
```

---

## 最佳实践

### 1. 目录命名规范

| 项目类型 | 推荐目录 |
|---------|---------|
| 开源项目 | `.wiki` 或 `docs` |
| 企业项目 | `documentation` |
| API 项目 | `docs/api` |
| 用户手册 | `docs/guide` |

### 2. 输出目录结构

```
project/
├── docs/
│   ├── api/           # API 文档
│   ├── guide/         # 用户指南
│   ├── technical/     # 技术文档
│   └── internal/      # 内部文档
```

### 3. Git 配置

在 `.gitignore` 中添加（如果文档是自动生成的）：

```gitignore
# 自动生成的文档（可选）
.wiki/
docs/auto-generated/
```

或者明确追踪文档：

```gitignore
# 不忽略文档
!docs/
!.wiki/
```

---

## 故障排除

### 问题 1: 输出目录权限错误

```python
# 确保目录可写
import os
from pathlib import Path

output_dir = Path(".wiki")
output_dir.mkdir(parents=True, exist_ok=True)
os.chmod(output_dir, 0o755)
```

### 问题 2: 路径中包含空格

```python
# 使用 Path 对象处理路径
from pathlib import Path

project_path = Path("/Users/username/My Projects/app")
prompt = load_prompt(
    "DocumentEngineer",
    working_directory=str(project_path),
    output_directory="docs"
)
```

---

## 总结

CodeViewX 提供了灵活的配置方式：

- ✅ **灵活的输出目录** - 适配各种项目结构
- ✅ **批量处理** - 支持多项目分析
- ✅ **CI/CD 集成** - 自动化文档生成
- ✅ **命令行工具** - 便于日常使用

根据你的具体需求选择合适的使用方式！🚀

