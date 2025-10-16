# DeepAgents 实例项目

这个项目展示了如何创建和使用 DeepAgents 来构建智能 AI Agent。

## 项目结构

```
codeviewx/
├── main.py              # 基础示例：展示 DeepAgents 的基本用法
├── advanced_example.py  # 高级示例：展示流式响应、多轮对话等
├── requirements.txt     # 项目依赖
└── README.md           # 项目说明文档
```

## 安装

1. 克隆或下载此项目

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置 API 密钥：
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

在 Windows 上使用：
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

## 使用方法

### 基础示例

运行 `main.py` 查看基本功能：

```bash
python main.py
```

这个示例展示了：
- 如何创建 Agent 实例
- 如何定义和注册工具函数
- 如何进行单次对话
- 如何实现交互式对话模式

### 高级示例

运行 `advanced_example.py` 查看高级功能：

```bash
python advanced_example.py
```

这个示例展示了：
- 流式响应
- 多轮对话上下文保持
- 复杂任务处理
- 错误处理机制

## 核心概念

### Agent 创建

```python
from deepagents import Agent
from anthropic import Anthropic

client = Anthropic()
agent = Agent(
    client=client,
    tools=[tool1, tool2, tool3],
    model="claude-3-5-sonnet-20241022"
)
```

### 工具定义

工具是普通的 Python 函数，需要：
- 明确的类型提示
- 详细的文档字符串（docstring）
- 返回值说明

```python
def my_tool(param1: str, param2: int) -> str:
    """
    工具描述
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
    
    Returns:
        返回值说明
    """
    # 实现逻辑
    return result
```

### 运行 Agent

```python
# 单次查询
response = agent.run("你的问题或指令")
print(response['content'])

# 流式响应（如果支持）
for chunk in agent.stream("你的问题或指令"):
    print(chunk, end='', flush=True)
```

## 自定义你的 Agent

### 添加新工具

1. 在代码中定义新的工具函数
2. 添加类型提示和文档字符串
3. 在创建 Agent 时添加到 tools 列表中

### 选择不同的模型

DeepAgents 支持多种 Claude 模型：
- `claude-3-5-sonnet-20241022` (推荐，平衡性能和成本)
- `claude-3-opus-20240229` (最强大，成本较高)
- `claude-3-sonnet-20240229` (中等)
- `claude-3-haiku-20240307` (最快，成本最低)

### 配置选项

```python
agent = Agent(
    client=client,
    tools=tools,
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,  # 最大响应长度
    temperature=0.7,  # 随机性控制 (0-1)
)
```

## 常见问题

### API 密钥错误

如果遇到 API 密钥相关错误，请确保：
1. 已正确设置 `ANTHROPIC_API_KEY` 环境变量
2. API 密钥有效且有足够的配额

### 工具未被调用

如果 Agent 没有调用预期的工具：
1. 检查工具函数的文档字符串是否清晰
2. 确保参数类型提示正确
3. 尝试更明确地描述你的需求

### 响应速度慢

如果响应较慢：
1. 考虑使用更快的模型（如 Haiku）
2. 减少工具数量
3. 优化工具函数的执行速度

## 最佳实践

1. **工具设计**
   - 保持工具函数单一职责
   - 提供清晰的文档字符串
   - 添加适当的错误处理

2. **提示词优化**
   - 使用清晰、具体的指令
   - 提供必要的上下文信息
   - 分步骤描述复杂任务

3. **性能优化**
   - 缓存常用数据
   - 异步处理耗时操作
   - 选择合适的模型

## 更多资源

- [DeepAgents 官方文档](https://github.com/anthropics/deepagents)
- [Anthropic API 文档](https://docs.anthropic.com/)
- [Claude 模型说明](https://www.anthropic.com/claude)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

