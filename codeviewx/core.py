"""
CodeViewX 核心功能模块
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from deepagents import create_deep_agent
from langchain_core.prompts import PromptTemplate

from .tools import (
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
)


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
        
        # 带变量替换
        prompt = load_prompt("DocumentEngineer", 
                           working_directory="/path/to/project",
                           output_directory=".wiki")
    
    Note:
        - 如果模板中包含 {variable} 占位符，必须提供对应的 kwargs
        - 如果不提供 kwargs，将直接返回原始模板文本
        - 使用 LangChain PromptTemplate 的默认格式（{variable}）
    """
    # 使用包资源读取提示词文件
    try:
        # 尝试使用 importlib.resources (Python 3.9+)
        try:
            from importlib.resources import files
            prompt_file = files("codeviewx.prompts").joinpath(f"{name}.md")
            with prompt_file.open("r", encoding="utf-8") as f:
                template_text = f.read()
        except (ImportError, AttributeError):
            # 向后兼容 Python 3.7-3.8
            from importlib.resources import open_text
            with open_text("codeviewx.prompts", f"{name}.md", encoding="utf-8") as f:
                template_text = f.read()
    except (FileNotFoundError, ModuleNotFoundError):
        # 开发模式：直接从文件系统读取
        import sys
        package_dir = Path(__file__).parent
        prompt_path = package_dir / "prompts" / f"{name}.md"
        if not prompt_path.exists():
            raise FileNotFoundError(f"找不到提示词文件: {name}.md")
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()
    
    # 如果提供了变量，使用 PromptTemplate 进行格式化
    if kwargs:
        try:
            template = PromptTemplate.from_template(template_text)
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"模板需要变量 {e}，但未在参数中提供") from e
    
    return template_text


def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = ".wiki",
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None:
    """
    生成项目文档
    
    Args:
        working_directory: 项目工作目录（默认：当前目录）
        output_directory: 文档输出目录（默认：.wiki）
        recursion_limit: Agent 递归限制（默认：1000）
        verbose: 是否显示详细日志（默认：False）
    
    Examples:
        # 分析当前目录
        generate_docs()
        
        # 分析指定项目
        generate_docs(
            working_directory="/path/to/project",
            output_directory="docs"
        )
        
        # 显示详细日志
        generate_docs(verbose=True)
    """
    # 配置日志
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    if verbose:
        logging.getLogger("langchain").setLevel(logging.DEBUG)
        logging.getLogger("langgraph").setLevel(logging.DEBUG)
    
    # 获取工作目录
    if working_directory is None:
        working_directory = os.getcwd()
    
    print("=" * 80)
    print(f"🚀 启动 CodeViewX 文档生成器 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print(f"📂 工作目录: {working_directory}")
    print(f"📝 输出目录: {output_directory}")
    
    # 加载提示词
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory=working_directory,
        output_directory=output_directory
    )
    print("✓ 已加载系统提示词（已注入工作目录和输出目录）")
    
    # 创建工具列表
    tools = [
        execute_command,
        ripgrep_search,
        write_real_file,
        read_real_file,
        list_real_directory,
    ]
    
    # 创建 Agent
    agent = create_deep_agent(tools, prompt)
    print("✓ 已创建 AI Agent")
    print(f"✓ 已注册 {len(tools)} 个自定义工具: {', '.join([t.__name__ for t in tools])}")
    print("=" * 80)
    
    # 生成文档
    print("\n📝 开始分析项目并生成文档...\n")
    
    step_count = 0
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": "请根据系统提示词中的工作目录，分析该项目并生成深度技术文档"}]},
        stream_mode="values",
        config={"recursion_limit": recursion_limit}
    ):
        if "messages" in chunk:
            step_count += 1
            last_message = chunk["messages"][-1]
            
            if verbose:
                print(f"\n{'='*80}")
                print(f"📍 步骤 {step_count} - {last_message.__class__.__name__}")
                print(f"{'='*80}")
                last_message.pretty_print()
                
                if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    print(f"\n🔧 调用了 {len(last_message.tool_calls)} 个工具:")
                    for tool_call in last_message.tool_calls:
                        print(f"   - {tool_call.get('name', 'unknown')}")
    
    print("\n" + "=" * 80)
    print("✅ 文档生成完成!")
    print("=" * 80)
    
    if "files" in chunk:
        print("\n📄 生成的文件:")
        for filename in chunk["files"].keys():
            print(f"   - {filename}")


# 向后兼容：保持原有的脚本执行方式
if __name__ == "__main__":
    generate_docs(verbose=True)

