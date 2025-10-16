"""测试文档语言功能"""

import pytest
from codeviewx import detect_system_language, load_prompt


def test_detect_system_language():
    """测试系统语言检测"""
    language = detect_system_language()
    
    # 应该返回一个语言字符串
    assert isinstance(language, str)
    assert len(language) > 0
    
    # 应该是支持的语言之一
    supported_languages = [
        'Chinese', 'English', 'Japanese', 'Korean',
        'French', 'German', 'Spanish', 'Russian'
    ]
    assert language in supported_languages


def test_load_prompt_with_language():
    """测试带语言参数的提示词加载"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test/path",
        output_directory=".wiki",
        doc_language="English"
    )
    
    # 检查所有变量都被注入
    assert "/test/path" in prompt
    assert ".wiki" in prompt
    assert "English" in prompt
    
    # 检查占位符被完全替换
    assert "{working_directory}" not in prompt
    assert "{output_directory}" not in prompt
    assert "{doc_language}" not in prompt


def test_load_prompt_chinese():
    """测试中文语言注入"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test",
        output_directory="docs",
        doc_language="Chinese"
    )
    
    assert "Chinese" in prompt
    assert "中文" in prompt or "Chinese" in prompt


def test_load_prompt_multiple_languages():
    """测试多种语言"""
    languages = ['English', 'Chinese', 'Japanese', 'French']
    
    for lang in languages:
        prompt = load_prompt(
            "DocumentEngineer",
            working_directory="/test",
            output_directory="docs",
            doc_language=lang
        )
        
        # 每种语言都应该被正确注入
        assert lang in prompt
        assert "{doc_language}" not in prompt


def test_language_in_prompt_context():
    """测试语言在提示词上下文中的位置"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test",
        output_directory="docs",
        doc_language="English"
    )
    
    # 应该在项目信息部分出现
    assert "项目信息" in prompt or "# 项目信息" in prompt
    
    # 应该有文档语言规范章节
    assert "文档语言" in prompt or "doc_language" in prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

