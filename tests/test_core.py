"""Test core functionality"""

import pytest
from codeviewx import load_prompt
from codeviewx.__version__ import __version__


def test_version():
    """Test version number"""
    assert __version__ == "0.2.0"
    assert isinstance(__version__, str)


def test_load_prompt_with_variables():
    """Test prompt loading and variable substitution"""
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
    
    assert len(prompt) > 0


def test_load_prompt_missing_required_variable():
    """Test error handling when required variables are missing"""
    with pytest.raises(ValueError, match="variable"):
        load_prompt("DocumentEngineer", working_directory="/test")


def test_load_prompt_no_variables():
    """Test returns original template when no variables provided"""
    prompt = load_prompt("DocumentEngineer")
    
    assert "{working_directory}" in prompt
    assert "{output_directory}" in prompt
    assert len(prompt) > 0


def test_load_prompt_nonexistent_file():
    """Test loading non-existent prompt file"""
    with pytest.raises(FileNotFoundError):
        load_prompt("NonExistentPrompt", test_var="value")


def test_load_prompt_multiple_variables():
    """Test multiple variable substitution"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/my/project",
        output_directory="docs",
        doc_language="Chinese"
    )
    
    assert "/my/project" in prompt
    assert "docs" in prompt
    assert "Chinese" in prompt
    
    assert prompt.count("/my/project") > 5
    assert prompt.count("docs") > 5


def test_prompt_content_structure():
    """Test prompt content structure"""
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/test",
        output_directory="docs",
        doc_language="Chinese"
    )
    
    assert "Chinese" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
