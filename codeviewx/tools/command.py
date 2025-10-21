"""
Command execution tool module
"""

import subprocess
from langchain_core.tools import tool


@tool
def execute_command(command: str, working_dir: str = None) -> str:
    """
    Execute system command and return result
    
    Args:
        command: Command string to execute
        working_dir: Working directory, uses current directory if None
    
    Returns:
        Command execution output, or error message if failed
    
    Examples:
        - execute_command("ls -la")
        - execute_command("cat main.py", "/path/to/project")
        - execute_command("find . -name '*.py' | head -20")
    
    Features:
        - Supports any shell command
        - Supports pipes and redirection
        - Automatically captures stdout and stderr
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=30
        )
        
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\n[Error Output]\n{result.stderr}"
        
        return output if output else "Command executed successfully, no output"
    
    except subprocess.TimeoutExpired:
        return "❌ Error: Command execution timeout (30 seconds)"
    except Exception as e:
        return f"❌ Error: {str(e)}"

