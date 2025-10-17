"""
文件系统工具模块
提供真实文件系统的读写和目录操作功能
"""

import os


def write_real_file(file_path: str, content: str) -> str:
    """
    写入真实文件系统中的文件
    
    Args:
        file_path: 文件路径（相对或绝对路径）
        content: 要写入的内容
    
    Returns:
        操作结果消息
    
    Examples:
        - write_real_file("docs/README.md", "# 文档标题")
        - write_real_file("output/data.json", json_string)
    
    Features:
        - 自动创建不存在的目录
        - 支持相对路径和绝对路径
        - 返回文件大小信息
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024
        
        return f"✅ 成功写入文件: {file_path} ({file_size_kb:.2f} KB)"
    
    except Exception as e:
        return f"❌ 写入文件失败: {str(e)}"


def read_real_file(file_path: str) -> str:
    """
    读取真实文件系统中的文件内容
    
    Args:
        file_path: 文件路径（相对或绝对路径）
    
    Returns:
        文件内容，如果出错则返回错误信息
    
    Examples:
        - read_real_file("main.py")
        - read_real_file("config/settings.json")
        - read_real_file("/absolute/path/to/file.txt")
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加文件信息
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024
        lines_count = len(content.split('\n'))
        
        header = f"文件: {file_path} ({file_size_kb:.2f} KB, {lines_count} 行)\n{'=' * 60}\n"
        return header + content
    
    except FileNotFoundError:
        return f"❌ 错误: 文件 '{file_path}' 不存在"
    except PermissionError:
        return f"❌ 错误: 没有权限读取文件 '{file_path}'"
    except UnicodeDecodeError:
        return f"❌ 错误: 文件 '{file_path}' 不是文本文件或编码不是 UTF-8"
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def list_real_directory(directory: str = ".") -> str:
    """
    列出真实文件系统中的目录内容
    
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

