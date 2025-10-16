"""
代码搜索工具模块
提供基于 ripgrep 的高性能代码搜索功能
"""

from ripgrepy import Ripgrepy


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
        - 使用 ripgrepy 库，需要系统安装 ripgrep: brew install ripgrep
    """
    try:
        # 创建 Ripgrepy 实例
        rg = Ripgrepy(pattern, path)
        
        # 配置选项
        rg = rg.line_number()  # 显示行号
        rg = rg.with_filename()  # 显示文件名
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

