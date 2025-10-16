# 标准库导入
import os  # 用于访问环境变量

# 第三方库导入
from typing import Literal  # 用于类型提示，限制参数的可选值
from deepagents import create_deep_agent  # 创建深度代理的工具


def load_prompt(name):
    """加载 AI 文档生成的系统提示词"""
    with open(f"prompt/{name}.md", "r") as f:
        return f.read()

prompt = load_prompt("DocumentEngineer")

agent = create_deep_agent(
    [],
    prompt,
)

# 调用代理执行研究任务
# 向代理发送用户消息，代理将：
#   1. 理解用户的查询意图
#   2. 使用 internet_search 工具进行多次搜索
#   3. 分析和综合搜索结果
#   4. 生成详细的研究报告
result = agent.invoke({"messages": [{"role": "user", "content": "当前工作目录为:/Users/deanlu/Desktop/projects/codeviewx,请生成一份该项目的深度技术文档"}]})
print(result)