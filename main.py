# 标准库导入
import os  # 用于访问环境变量
import logging  # 日志记录
import subprocess  # 执行系统命令
from datetime import datetime

# 第三方库导入
from typing import Literal  # 用于类型提示，限制参数的可选值
from deepagents import create_deep_agent  # 创建深度代理的工具
from ripgrepy import Ripgrepy  # ripgrep Python 接口

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# 启用 LangChain 相关的详细日志
logging.getLogger("langchain").setLevel(logging.DEBUG)
logging.getLogger("langgraph").setLevel(logging.DEBUG)


def execute_command(command: str, working_dir: str = None) -> str:
    """
    执行系统命令并返回输出结果
    
    Args:
        command: 要执行的命令（如 'ls -la', 'cat file.txt', 'find . -name "*.py"'）
        working_dir: 命令执行的工作目录，默认为当前目录
    
    Returns:
        命令的输出结果（stdout），如果出错则返回错误信息
    
    Examples:
        - execute_command("ls -la /Users/deanlu/Desktop/projects/codeviewx")
        - execute_command("cat README.md", "/Users/deanlu/Desktop/projects/codeviewx")
        - execute_command("find . -name '*.py' -type f")
    """
    try:
        # 如果没有指定工作目录，使用当前目录
        cwd = working_dir if working_dir else os.getcwd()
        
        # 执行命令
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30  # 30秒超时
        )
        
        # 返回输出
        if result.returncode == 0:
            return result.stdout if result.stdout else "命令执行成功，无输出"
        else:
            return f"命令执行失败 (返回码: {result.returncode})\n错误信息: {result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "错误: 命令执行超时（超过30秒）"
    except Exception as e:
        return f"错误: {str(e)}"


def ripgrep_search(pattern: str, path: str = ".", 
                   file_type: str = None, 
                   ignore_case: bool = False,
                   max_count: int = 100) -> str:
    """
    使用 ripgrep 在文件中搜索文本模式（比 grep 更快）
    
    Args:
        pattern: 要搜索的正则表达式模式
        path: 搜索路径，默认为当前目录
        file_type: 文件类型过滤（如 'py', 'js', 'md'），为 None 则搜索所有文件
        ignore_case: 是否忽略大小写，默认 False
        max_count: 最大返回结果数量，默认 100
    
    Returns:
        搜索结果，包含匹配的文件路径和内容
    
    Examples:
        - ripgrep_search("def main", ".", "py") - 在所有 Python 文件中搜索 "def main"
        - ripgrep_search("TODO", "/path/to/project") - 搜索所有包含 TODO 的行
        - ripgrep_search("import.*Agent", ".", "py", ignore_case=True) - 不区分大小写搜索导入
    
    Features:
        - 自动忽略 .git, .venv, node_modules 等目录
        - 支持正则表达式
        - 显示行号和上下文
        - 速度比传统 grep 快很多
        - 使用 ripgrepy 库，无需单独安装 ripgrep
    """
    try:
        # 创建 Ripgrepy 实例
        rg = Ripgrepy(pattern, path)
        
        # 配置选项
        rg = rg.line_number()  # 显示行号
        rg = rg.heading()      # 文件名作为标题
        rg = rg.max_count(max_count)  # 限制每个文件的结果数
        
        # 忽略大小写
        if ignore_case:
            rg = rg.ignore_case()
        
        # 文件类型过滤
        if file_type:
            rg = rg.type_add(file_type)
        
        # 自动忽略的目录和文件
        ignore_patterns = [
            ".git", ".venv", "venv", "env", "node_modules", 
            "__pycache__", ".pytest_cache", ".mypy_cache",
            "dist", "build", "target", ".cache", "*.pyc",
            ".DS_Store", "Thumbs.db", "*.log"
        ]
        for ignore_pattern in ignore_patterns:
            rg = rg.glob(f"!{ignore_pattern}")
        
        # 执行搜索
        result = rg.run().as_string
        
        if result.strip():
            lines = result.strip().split('\n')
            if len(lines) > max_count:
                return result + f"\n\n... (结果太多，已截断到前 {max_count} 行)"
            return result
        else:
            return f"未找到匹配 '{pattern}' 的内容"
    
    except Exception as e:
        error_msg = str(e)
        # 检查是否是 ripgrep 未安装的错误
        if "rg" in error_msg.lower() and ("not found" in error_msg.lower() or "cannot find" in error_msg.lower()):
            return "错误: ripgrep (rg) 未安装。请先安装: brew install ripgrep (macOS) 或 apt install ripgrep (Linux)"
        return f"搜索错误: {error_msg}"


def write_real_file(file_path: str, content: str) -> str:
    """
    写入真实文件系统中的文件
    
    Args:
        file_path: 文件的绝对路径或相对路径
        content: 文件内容
    
    Returns:
        操作结果，成功或错误信息
    
    Examples:
        - write_real_file(".wiki/README.md", "# 文档")
        - write_real_file("/path/to/file.txt", "内容")
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ 成功写入文件: {file_path} ({len(content)} 字符)"
    
    except PermissionError:
        return f"❌ 错误: 没有权限写入文件 '{file_path}'"
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def read_real_file(file_path: str) -> str:
    """
    读取真实文件系统中的文件内容
    
    Args:
        file_path: 文件的绝对路径或相对路径
    
    Returns:
        文件内容，如果出错则返回错误信息
    
    Examples:
        - read_real_file("/Users/deanlu/Desktop/projects/codeviewx/main.py")
        - read_real_file("README.md")
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 如果文件太大，只返回前10000个字符
            if len(content) > 10000:
                return content[:10000] + f"\n\n... (文件太大，已截断，总共 {len(content)} 字符)"
            return content
    except FileNotFoundError:
        return f"❌ 错误: 文件 '{file_path}' 不存在"
    except PermissionError:
        return f"❌ 错误: 没有权限读取文件 '{file_path}'"
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def list_real_directory(directory: str = ".") -> str:
    """
    列出真实文件系统中目录的内容
    
    Args:
        directory: 目录路径，默认为当前目录
    
    Returns:
        目录内容列表，如果出错则返回错误信息
    
    Examples:
        - list_real_directory("/Users/deanlu/Desktop/projects/codeviewx")
        - list_real_directory(".")
    """
    try:
        items = os.listdir(directory)
        # 分类显示
        dirs = [f"📁 {item}/" for item in items if os.path.isdir(os.path.join(directory, item))]
        files = [f"📄 {item}" for item in items if os.path.isfile(os.path.join(directory, item))]
        
        result = f"目录: {os.path.abspath(directory)}\n"
        result += f"共 {len(dirs)} 个目录, {len(files)} 个文件\n\n"
        
        if dirs:
            result += "目录:\n" + "\n".join(sorted(dirs)) + "\n\n"
        if files:
            result += "文件:\n" + "\n".join(sorted(files))
        
        return result if result else "目录为空"
    except FileNotFoundError:
        return f"❌ 错误: 目录 '{directory}' 不存在"
    except PermissionError:
        return f"❌ 错误: 没有权限访问目录 '{directory}'"
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def load_prompt(name):
    """加载 AI 文档生成的系统提示词"""
    with open(f"prompt/{name}.md", "r") as f:
        return f.read()


print("=" * 80)
print(f"🚀 启动 CodeViewX 文档生成器 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

prompt = load_prompt("DocumentEngineer")
print("✓ 已加载系统提示词")

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
    {"messages": [{"role": "user", "content": "当前工作目录为:/Users/deanlu/Desktop/projects/codeviewx,请生成一份该项目的深度技术文档"}]},
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
