"""
Code search tool module
"""

from ripgrepy import Ripgrepy


def ripgrep_search(pattern: str, path: str = ".", 
                   file_type: str = None, 
                   ignore_case: bool = False,
                   max_count: int = 100) -> str:
    """
    Search for text patterns in files using ripgrep (faster than grep)
    
    Args:
        pattern: Regular expression pattern to search for
        path: Search path, defaults to current directory
        file_type: File type filter (e.g., 'py', 'js', 'md'), searches all files if None
        ignore_case: Whether to ignore case, defaults to False
        max_count: Maximum number of results to return, defaults to 100
    
    Returns:
        Search results, including matched file paths and content
    
    Examples:
        - ripgrep_search("def main", ".", "py") - Search for "def main" in all Python files
        - ripgrep_search("TODO", "/path/to/project") - Search for all lines containing TODO
        - ripgrep_search("import.*Agent", ".", "py", ignore_case=True) - Case-insensitive import search
    
    Features:
        - Automatically ignores .git, .venv, node_modules, etc.
        - Supports regular expressions
        - Shows line numbers and context
        - Much faster than traditional grep
        - Uses ripgrepy library, requires ripgrep installed: brew install ripgrep
    """
    try:
        rg = Ripgrepy(pattern, path)
        
        rg = rg.line_number()
        rg = rg.with_filename()
        rg = rg.max_count(max_count)
        
        if ignore_case:
            rg = rg.ignore_case()
        
        if file_type:
            rg = rg.type_add(file_type)
        
        ignore_patterns = [
            ".git", ".venv", "venv", "env", "node_modules", 
            "__pycache__", ".pytest_cache", ".mypy_cache",
            "dist", "build", "target", ".cache", "*.pyc",
            ".DS_Store", "Thumbs.db", "*.log"
        ]
        for ignore_pattern in ignore_patterns:
            rg = rg.glob(f"!{ignore_pattern}")
        
        result = rg.run().as_string
        
        if result.strip():
            lines = result.strip().split('\n')
            if len(lines) > max_count:
                return result + f"\n\n... (Too many results, truncated to first {max_count} lines)"
            return result
        else:
            return f"No matches found for '{pattern}'"
    
    except Exception as e:
        error_msg = str(e)
        if "rg" in error_msg.lower() and ("not found" in error_msg.lower() or "cannot find" in error_msg.lower()):
            return "Error: ripgrep (rg) is not installed. Please install it: brew install ripgrep (macOS) or apt install ripgrep (Linux)"
        return f"Search error: {error_msg}"

