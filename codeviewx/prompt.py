"""
Prompt loading module
提示词加载模块
"""

from pathlib import Path
from langchain_core.prompts import PromptTemplate
from .i18n import t


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
                           output_directory="docs")
    
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
        # Development mode: read directly from file system
        # 开发模式：直接从文件系统读取
        package_dir = Path(__file__).parent
        prompt_path = package_dir / "prompts" / f"{name}.md"
        if not prompt_path.exists():
            raise FileNotFoundError(t('error_file_not_found', filename=f"{name}.md"))
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()
    
    # If variables are provided, format using PromptTemplate
    # 如果提供了变量，使用 PromptTemplate 进行格式化
    if kwargs:
        try:
            template = PromptTemplate.from_template(template_text)
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(t('error_template_variable', variable=str(e))) from e
    
    return template_text

