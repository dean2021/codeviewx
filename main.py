# 标准库导入
import os  # 用于访问环境变量
import logging  # 日志记录
from datetime import datetime

# 第三方库导入
from typing import Literal  # 用于类型提示，限制参数的可选值
from deepagents import create_deep_agent  # 创建深度代理的工具

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# 启用 LangChain 相关的详细日志
logging.getLogger("langchain").setLevel(logging.DEBUG)
logging.getLogger("langgraph").setLevel(logging.DEBUG)


def load_prompt(name):
    """加载 AI 文档生成的系统提示词"""
    with open(f"prompt/{name}.md", "r") as f:
        return f.read()


print("=" * 80)
print(f"🚀 启动 CodeViewX 文档生成器 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

prompt = load_prompt("DocumentEngineer")
print("✓ 已加载系统提示词")

agent = create_deep_agent(
    [],
    prompt,
)
print("✓ 已创建 AI Agent")
print("=" * 80)

# 使用流式输出来查看实时进度（参考文档中的例子）
print("\n📝 开始分析项目并生成文档...\n")

step_count = 0
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "当前工作目录为:/Users/deanlu/Desktop/projects/codeviewx,请生成一份该项目的深度技术文档"}]},
    stream_mode="values"  # 使用 values 模式
):
    if "messages" in chunk:
        step_count += 1
        last_message = chunk["messages"][-1]
        
        print(f"\n{'='*80}")
        print(f"📍 步骤 {step_count} - {last_message.__class__.__name__}")
        print(f"{'='*80}")
        
        # 使用 pretty_print() 方法显示消息（这是 LangChain 的推荐方式）
        last_message.pretty_print()
        
        # 如果有工具调用，额外显示工具信息
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            print(f"\n🔧 调用了 {len(last_message.tool_calls)} 个工具:")
            for tool_call in last_message.tool_calls:
                print(f"   - {tool_call.get('name', 'unknown')}: {str(tool_call.get('args', {}))[:100]}...")

print("\n" + "=" * 80)
print("✅ 文档生成完成!")
print("=" * 80)

# 打印最终结果中的文件
if "files" in chunk:
    print("\n📄 生成的文件:")
    for filename in chunk["files"].keys():
        print(f"   - {filename}")
