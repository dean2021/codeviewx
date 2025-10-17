"""Test document language functionality"""

import pytest
from codeviewx import detect_system_language, load_prompt


def test_detect_system_language():
    """Test system language detection"""
    language = detect_system_language()
    
    assert isinstance(language, str)
    assert len(language) > 0
    
    supported_languages = [
        'Chinese', 'English', 'Japanese', 'Korean',
        'French', 'German', 'Spanish', 'Russian'
    ]
    assert language in supported_languages


def test_load_prompt_with_language():
    """Test loading prompt with language parameter"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test/path",
        output_directory="docs",
        doc_language="English"
    )
    
    assert "/test/path" in prompt
    assert "docs" in prompt
    assert "English" in prompt
    
    assert "{working_directory}" not in prompt
    assert "{output_directory}" not in prompt
    assert "{doc_language}" not in prompt


def test_load_prompt_chinese():
    """Test Chinese language injection"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test/path",
        output_directory="docs",
        doc_language="Chinese"
    )
    
    assert "Chinese" in prompt


def test_load_prompt_multiple_languages():
    """Test multiple languages"""
    languages = ['English', 'Chinese', 'Japanese', 'French']
    
    for lang in languages:
        prompt = load_prompt(
            "DocumentEngineer",
            working_directory="/test",
            output_directory="docs",
            doc_language=lang
        )
        
        assert lang in prompt
        assert "{doc_language}" not in prompt


def test_language_in_prompt_context():
    """Test language position in prompt context"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test",
        output_directory="docs",
        doc_language="English"
    )
    
    assert "doc_language" in prompt.lower() or "English" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
