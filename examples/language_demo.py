#!/usr/bin/env python3
"""
CodeViewX Multi-language Documentation Generation Demo
"""

import os
from codeviewx import generate_docs, detect_system_language, load_prompt


def demo_detect_language():
    """Demonstrate system language detection"""
    print("=" * 60)
    print("Example 1: System Language Detection")
    print("=" * 60)
    
    detected_lang = detect_system_language()
    print(f"Detected system language: {detected_lang}")
    print()


def demo_auto_language():
    """Demonstrate auto-detecting language for documentation"""
    print("=" * 60)
    print("Example 2: Auto-detect Language")
    print("=" * 60)
    print("Auto-detect system language when generating docs...")
    print("Usage: generate_docs()  # No doc_language specified")
    print()


def demo_specify_language():
    """Demonstrate specifying language for documentation"""
    print("=" * 60)
    print("Example 3: Specify Documentation Language")
    print("=" * 60)
    
    languages = ['Chinese', 'English', 'Japanese']
    
    for lang in languages:
        print(f"  • Using {lang}:")
        print(f"    generate_docs(doc_language='{lang}')")
    print()


def demo_load_prompt_with_language():
    """Demonstrate loading prompt with language parameter"""
    print("=" * 60)
    print("Example 4: Load Prompt with Language Parameter")
    print("=" * 60)
    
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/path/to/project",
        output_directory="docs",
        doc_language="English"
    )
    
    print(f"Prompt length: {len(prompt)} characters")
    print("✅ Language parameter injected into prompt successfully")
    print()


def demo_cli_usage():
    """Demonstrate CLI command line usage"""
    print("=" * 60)
    print("Example 5: CLI Command Line Usage")
    print("=" * 60)
    
    examples = [
        ("Auto-detect", "codeviewx"),
        ("Chinese", "codeviewx -l Chinese"),
        ("English", "codeviewx -l English -o docs"),
        ("Japanese", "codeviewx -l Japanese -o docs"),
        ("Full config", "codeviewx -w /path/to/project -o docs -l Chinese --verbose"),
    ]
    
    for desc, cmd in examples:
        print(f"  {desc:12} → {cmd}")
    print()


def demo_supported_languages():
    """Demonstrate supported language list"""
    print("=" * 60)
    print("Supported Languages")
    print("=" * 60)
    
    languages = {
        'Chinese': '中文（简体）',
        'English': 'English',
        'Japanese': '日本語',
        'Korean': '한국어',
        'French': 'Français',
        'German': 'Deutsch',
        'Spanish': 'Español',
        'Russian': 'Русский'
    }
    
    for code, name in languages.items():
        print(f"  {code:12} - {name}")
    print()


def demo_practical_examples():
    """Practical application examples"""
    print("=" * 60)
    print("Practical Use Cases")
    print("=" * 60)
    
    print("\nScenario 1: Internationalized Project")
    print("  # Generate Chinese docs")
    print("  generate_docs(output_directory='docs/zh', doc_language='Chinese')")
    print()
    print("  # Generate English docs")
    print("  generate_docs(output_directory='docs/en', doc_language='English')")
    
    print("\nScenario 2: Chinese User-focused Project")
    print("  # Use Chinese")
    print("  generate_docs(doc_language='Chinese')")
    
    print("\nScenario 3: Open Source Project (International Users)")
    print("  # Use English")
    print("  generate_docs(doc_language='English')")
    
    print("\nScenario 4: Auto-adapt")
    print("  # Auto-select based on user's system language")
    print("  generate_docs()  # Auto-detect")
    print()


if __name__ == "__main__":
    print("\n🌍 CodeViewX Multi-language Documentation Generation Demo\n")
    
    demo_detect_language()
    demo_auto_language()
    demo_specify_language()
    demo_load_prompt_with_language()
    demo_cli_usage()
    demo_supported_languages()
    demo_practical_examples()
    
    print("=" * 60)
    print("✨ Demo completed!")
    print("=" * 60)
    print("\n💡 Tips:")
    print("  - Auto-detects system language by default")
    print("  - Use -l/--language parameter to specify language")
    print("  - Supports 8 major languages")
    print("  - Can generate multiple documentation versions for different languages\n")

