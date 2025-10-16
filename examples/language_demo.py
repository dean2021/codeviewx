#!/usr/bin/env python3
"""
CodeViewX 多语言文档生成示例
"""

import os
from codeviewx import generate_docs, detect_system_language, load_prompt


def demo_detect_language():
    """演示系统语言检测"""
    print("=" * 60)
    print("示例 1: 系统语言检测")
    print("=" * 60)
    
    detected_lang = detect_system_language()
    print(f"检测到的系统语言: {detected_lang}")
    print()


def demo_auto_language():
    """演示自动检测语言生成文档"""
    print("=" * 60)
    print("示例 2: 自动检测语言")
    print("=" * 60)
    print("生成文档时自动检测系统语言...")
    print("用法: generate_docs()  # 不指定 doc_language")
    print()


def demo_specify_language():
    """演示指定语言生成文档"""
    print("=" * 60)
    print("示例 3: 指定文档语言")
    print("=" * 60)
    
    languages = ['Chinese', 'English', 'Japanese']
    
    for lang in languages:
        print(f"  • 使用 {lang}:")
        print(f"    generate_docs(doc_language='{lang}')")
    print()


def demo_load_prompt_with_language():
    """演示加载带语言的提示词"""
    print("=" * 60)
    print("示例 4: 加载带语言参数的提示词")
    print("=" * 60)
    
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/path/to/project",
        output_directory="docs",
        doc_language="English"
    )
    
    print(f"提示词长度: {len(prompt)} 字符")
    print("✅ 语言参数已成功注入到提示词中")
    print()


def demo_cli_usage():
    """演示 CLI 命令行用法"""
    print("=" * 60)
    print("示例 5: CLI 命令行用法")
    print("=" * 60)
    
    examples = [
        ("自动检测语言", "codeviewx"),
        ("指定中文", "codeviewx -l Chinese"),
        ("指定英文", "codeviewx -l English -o docs"),
        ("日语文档", "codeviewx -l Japanese -o .wiki"),
        ("完整配置", "codeviewx -w /path/to/project -o docs -l Chinese --verbose"),
    ]
    
    for desc, cmd in examples:
        print(f"  {desc:12} → {cmd}")
    print()


def demo_supported_languages():
    """演示支持的语言列表"""
    print("=" * 60)
    print("支持的语言")
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
    """实际应用示例"""
    print("=" * 60)
    print("实际应用场景")
    print("=" * 60)
    
    print("\n场景 1: 国际化项目")
    print("  # 生成中文文档")
    print("  generate_docs(output_directory='docs/zh', doc_language='Chinese')")
    print()
    print("  # 生成英文文档")
    print("  generate_docs(output_directory='docs/en', doc_language='English')")
    
    print("\n场景 2: 面向中国用户的项目")
    print("  # 使用中文")
    print("  generate_docs(doc_language='Chinese')")
    
    print("\n场景 3: 开源项目（国际用户）")
    print("  # 使用英文")
    print("  generate_docs(doc_language='English')")
    
    print("\n场景 4: 自动适配")
    print("  # 根据用户系统语言自动选择")
    print("  generate_docs()  # 自动检测")
    print()


if __name__ == "__main__":
    print("\n🌍 CodeViewX 多语言文档生成演示\n")
    
    demo_detect_language()
    demo_auto_language()
    demo_specify_language()
    demo_load_prompt_with_language()
    demo_cli_usage()
    demo_supported_languages()
    demo_practical_examples()
    
    print("=" * 60)
    print("✨ 演示完成！")
    print("=" * 60)
    print("\n💡 提示:")
    print("  - 默认情况下会自动检测系统语言")
    print("  - 使用 -l/--language 参数可以指定语言")
    print("  - 支持 8 种主要语言")
    print("  - 可以为不同语言生成多份文档\n")

