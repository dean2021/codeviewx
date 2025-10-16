"""
命令执行工具模块
提供系统命令执行功能
"""

import subprocess


def execute_command(command: str, working_dir: str = None) -> str:
    """
    执行系统命令并返回结果
    
    Args:
        command: 要执行的命令字符串
        working_dir: 工作目录，为 None 则使用当前目录
    
    Returns:
        命令执行的输出结果，如果出错则返回错误信息
    
    Examples:
        - execute_command("ls -la")
        - execute_command("cat main.py", "/path/to/project")
        - execute_command("find . -name '*.py' | head -20")
    
    Features:
        - 支持任何 shell 命令
        - 支持管道和重定向
        - 自动捕获标准输出和错误输出
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=30  # 30秒超时
        )
        
        # 组合标准输出和错误输出
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\n[错误输出]\n{result.stderr}"
        
        return output if output else "命令执行成功，无输出"
    
    except subprocess.TimeoutExpired:
        return "❌ 错误: 命令执行超时（30秒）"
    except Exception as e:
        return f"❌ 错误: {str(e)}"

