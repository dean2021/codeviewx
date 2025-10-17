"""
Prompt loading module
"""

from pathlib import Path
from langchain_core.prompts import PromptTemplate
from .i18n import t


def load_prompt(name: str, **kwargs) -> str:
    """
    Load AI documentation generation system prompt
    
    Uses LangChain's PromptTemplate to support variable interpolation and dynamic parameters.
    Supports {variable_name} placeholders in the prompt template.
    
    Args:
        name: Prompt file name (without extension)
        **kwargs: Optional template variables for replacing placeholders in the prompt
                 e.g., project_type="Web App", language="Python"
    
    Returns:
        Formatted prompt text
    
    Examples:
        prompt = load_prompt("DocumentEngineer")
        
        prompt = load_prompt("DocumentEngineer", 
                           working_directory="/path/to/project",
                           output_directory="docs")
    
    Note:
        - If the template contains {variable} placeholders, corresponding kwargs must be provided
        - If kwargs are not provided, the original template text is returned
        - Uses LangChain PromptTemplate's default format ({variable})
    """
    try:
        try:
            from importlib.resources import files
            prompt_file = files("codeviewx.prompts").joinpath(f"{name}.md")
            with prompt_file.open("r", encoding="utf-8") as f:
                template_text = f.read()
        except (ImportError, AttributeError):
            from importlib.resources import open_text
            with open_text("codeviewx.prompts", f"{name}.md", encoding="utf-8") as f:
                template_text = f.read()
    except (FileNotFoundError, ModuleNotFoundError):
        package_dir = Path(__file__).parent
        prompt_path = package_dir / "prompts" / f"{name}.md"
        if not prompt_path.exists():
            raise FileNotFoundError(t('error_file_not_found', filename=f"{name}.md"))
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()
    
    if kwargs:
        try:
            template = PromptTemplate.from_template(template_text)
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(t('error_template_variable', variable=str(e))) from e
    
    return template_text

