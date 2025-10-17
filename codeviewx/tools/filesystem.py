"""
Filesystem tool module
"""

import os


def write_real_file(file_path: str, content: str) -> str:
    """
    Write file to real filesystem
    
    Args:
        file_path: File path (relative or absolute)
        content: Content to write
    
    Returns:
        Operation result message
    
    Examples:
        - write_real_file("docs/README.md", "# Documentation Title")
        - write_real_file("output/data.json", json_string)
    
    Features:
        - Automatically creates non-existent directories
        - Supports relative and absolute paths
        - Returns file size information
    """
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024
        
        return f"✅ Successfully wrote file: {file_path} ({file_size_kb:.2f} KB)"
    
    except Exception as e:
        return f"❌ Failed to write file: {str(e)}"


def read_real_file(file_path: str) -> str:
    """
    Read file content from real filesystem
    
    Args:
        file_path: File path (relative or absolute)
    
    Returns:
        File content, or error message if failed
    
    Examples:
        - read_real_file("main.py")
        - read_real_file("config/settings.json")
        - read_real_file("/absolute/path/to/file.txt")
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024
        lines_count = len(content.split('\n'))
        
        header = f"File: {file_path} ({file_size_kb:.2f} KB, {lines_count} lines)\n{'=' * 60}\n"
        return header + content
    
    except FileNotFoundError:
        return f"❌ Error: File '{file_path}' does not exist"
    except PermissionError:
        return f"❌ Error: No permission to read file '{file_path}'"
    except UnicodeDecodeError:
        return f"❌ Error: File '{file_path}' is not a text file or not UTF-8 encoded"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def list_real_directory(directory: str = ".") -> str:
    """
    List directory contents in real filesystem
    
    Args:
        directory: Directory path, defaults to current directory
    
    Returns:
        Directory content list, or error message if failed
    
    Examples:
        - list_real_directory("/Users/deanlu/Desktop/projects/codeviewx")
        - list_real_directory(".")
    """
    try:
        items = os.listdir(directory)
        dirs = [f"📁 {item}/" for item in items if os.path.isdir(os.path.join(directory, item))]
        files = [f"📄 {item}" for item in items if os.path.isfile(os.path.join(directory, item))]
        
        result = f"Directory: {os.path.abspath(directory)}\n"
        result += f"Total {len(dirs)} directories, {len(files)} files\n\n"
        
        if dirs:
            result += "Directories:\n" + "\n".join(sorted(dirs)) + "\n\n"
        if files:
            result += "Files:\n" + "\n".join(sorted(files))
        
        return result if result else "Directory is empty"
    except FileNotFoundError:
        return f"❌ Error: Directory '{directory}' does not exist"
    except PermissionError:
        return f"❌ Error: No permission to access directory '{directory}'"
    except Exception as e:
        return f"❌ Error: {str(e)}"

