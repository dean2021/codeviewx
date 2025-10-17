"""测试核心功能"""

import pytest
from codeviewx import load_prompt
from codeviewx.__version__ import __version__


def test_version():
    """测试版本号"""
    assert __version__ == "0.1.0"
    assert isinstance(__version__, str)


def test_load_prompt_with_variables():
    """测试提示词加载和变量替换"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test/path",
        output_directory="docs",
        doc_language="English"
    )
    
    # 检查变量是否被替换
    assert "/test/path" in prompt
    assert "docs" in prompt
    assert "English" in prompt
    
    # 检查占位符是否被完全替换
    assert "{working_directory}" not in prompt
    assert "{output_directory}" not in prompt
    assert "{doc_language}" not in prompt
    
    # 检查提示词不为空
    assert len(prompt) > 0


def test_load_prompt_missing_required_variable():
    """测试缺少必需变量时的错误处理"""
    with pytest.raises(ValueError, match="模板需要变量"):
        # 只提供一个变量，应该会失败
        load_prompt("DocumentEngineer", working_directory="/test")


def test_load_prompt_no_variables():
    """测试没有提供变量时返回原始模板"""
    # 如果不提供变量，应该返回原始模板（包含占位符）
    prompt = load_prompt("DocumentEngineer")
    
    # 原始模板应该包含占位符
    assert "{working_directory}" in prompt
    assert "{output_directory}" in prompt
    assert len(prompt) > 0


def test_load_prompt_nonexistent_file():
    """测试加载不存在的提示词文件"""
    with pytest.raises(FileNotFoundError):
        load_prompt("NonExistentPrompt", test_var="value")


def test_load_prompt_multiple_variables():
    """测试多个变量替换"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/my/project",
        output_directory="docs",
        doc_language="Chinese"
    )
    
    # 检查所有变量都被正确替换
    assert "/my/project" in prompt
    assert "docs" in prompt
    assert "Chinese" in prompt
    
    # 统计出现次数（应该多次出现）
    assert prompt.count("/my/project") > 5
    assert prompt.count("docs") > 5


def test_prompt_content_structure():
    """测试提示词内容结构"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test",
        output_directory="docs",
        doc_language="Chinese"
    )
    
    # 检查是否包含关键章节
    assert "角色与使命" in prompt or "角色" in prompt
    assert "工具" in prompt or "Tools" in prompt
    assert "文档" in prompt or "Documentation" in prompt
    assert "Chinese" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

