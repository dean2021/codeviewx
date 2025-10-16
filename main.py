# 标准库导入
import os  # 操作系统接口
import logging  # 日志记录
from datetime import datetime
from pathlib import Path

# 第三方库导入
from deepagents import create_deep_agent  # 创建深度代理的工具
from langchain_core.prompts import PromptTemplate  # LangChain Prompt 模板

# 项目工具导入
from tools import (
    execute_command,      # 命令执行工具
    ripgrep_search,       # 代码搜索工具
    write_real_file,      # 文件写入工具
    read_real_file,       # 文件读取工具
    list_real_directory,  # 目录列表工具
)

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# 启用 LangChain 相关的详细日志
logging.getLogger("langchain").setLevel(logging.DEBUG)
logging.getLogger("langgraph").setLevel(logging.DEBUG)


def load_prompt(name: str, **kwargs) -> str:
    """
    加载 AI 文档生成的系统提示词
    
    使用 LangChain 的 PromptTemplate 支持变量插值和动态参数。
    支持在提示词模板中使用 {variable_name} 占位符。
    
    Args:
        name: 提示词文件名（不含扩展名）
        **kwargs: 可选的模板变量，用于替换提示词中的占位符
                 例如: project_type="Web应用", language="Python"
    
    Returns:
        格式化后的提示词文本
    
    Examples:
        # 简单加载（无变量替换）
        prompt = load_prompt("DocumentEngineer")
        
        # 带变量替换（需要模板中有对应的 {project_type} 占位符）
        prompt = load_prompt("DocumentEngineer", 
                           project_type="Web应用", 
                           language="Python")
    
    Note:
        - 如果模板中包含 {variable} 占位符，必须提供对应的 kwargs
        - 如果不提供 kwargs，将直接返回原始模板文本
        - 使用 LangChain PromptTemplate 的默认格式（{variable}）
    """
    prompt_path = Path(f"prompt/{name}.md")
    
    # 读取提示词文件
    with open(prompt_path, "r", encoding="utf-8") as f:
        template_text = f.read()
    
    # 如果提供了变量，使用 PromptTemplate 进行格式化
    if kwargs:
        try:
            # 创建 PromptTemplate（使用默认格式：{variable}）
            template = PromptTemplate.from_template(template_text)
            return template.format(**kwargs)
        except KeyError as e:
            # 如果模板中需要的变量未提供，抛出更友好的错误
            raise ValueError(f"模板需要变量 {e}，但未在参数中提供") from e
    
    # 如果没有提供变量，直接返回原始文本
    return template_text


if __name__ == "__main__":

    print("=" * 80)
    print(f"🚀 启动 CodeViewX 文档生成器 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 获取当前工作目录
    working_directory = os.getcwd()
    output_directory = ".wiki"  # 文档输出目录
    
    print(f"📂 工作目录: {working_directory}")
    print(f"📝 输出目录: {output_directory}")
    
    # 加载系统提示词并注入工作目录和输出目录
    prompt = load_prompt(
        "DocumentEngineer", 
        working_directory=working_directory,
        output_directory=output_directory
    )
    print("✓ 已加载系统提示词（已注入工作目录和输出目录）")

    # 创建工具列表
    tools = [
        execute_command,      # 执行系统命令（通用）
        ripgrep_search,       # 快速文本搜索
        write_real_file,      # 写入真实文件 ⭐ 直接保存到文件系统
        read_real_file,       # 读取真实文件
        list_real_directory,  # 列出真实目录
    ]

    agent = create_deep_agent(
        tools,
        prompt,
    )
    print("✓ 已创建 AI Agent")
    print(f"✓ 已注册 {len(tools)} 个自定义工具: {', '.join([t.__name__ for t in tools])}")
    print("=" * 80)

    # 使用流式输出来查看实时进度（参考文档中的例子）
    print("\n📝 开始分析项目并生成文档...\n")

    step_count = 0
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": "请根据系统提示词中的工作目录，分析该项目并生成深度技术文档"}]},
        stream_mode="values",  # 使用 values 模式
        config={"recursion_limit": 1000}  # 增加递归限制到1000步
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
                    print(f"   - {tool_call.get('name', 'unknown')}: {str(tool_call.get('args', {}))}")

    print("\n" + "=" * 80)
    print("✅ 文档生成完成!")
    print("=" * 80)

    # 打印最终结果中的文件
    if "files" in chunk:
        print("\n📄 生成的文件:")
        for filename in chunk["files"].keys():
            print(f"   - {filename}")
