#!/usr/bin/env python3
"""
CodeViewX 基本使用示例
"""

import os
from codeviewx import generate_docs, load_prompt


def example1_simple_usage():
    """示例 1: 最简单的使用方式"""
    print("=" * 60)
    print("示例 1: 分析当前目录")
    print("=" * 60)
    
    # 分析当前目录，文档输出到 docs/
    generate_docs()


def example2_custom_paths():
    """示例 2: 自定义路径"""
    print("\n" + "=" * 60)
    print("示例 2: 自定义工作目录和输出目录")
    print("=" * 60)
    
    # 分析指定项目，输出到 docs 目录
    generate_docs(
        working_directory="/path/to/your/project",
        output_directory="docs"
    )


def example3_verbose_mode():
    """示例 3: 显示详细日志"""
    print("\n" + "=" * 60)
    print("示例 3: 详细日志模式")
    print("=" * 60)
    
    # 启用详细日志
    generate_docs(
        working_directory=os.getcwd(),
        output_directory="docs",
        verbose=True
    )


def example4_load_prompt():
    """示例 4: 单独加载提示词"""
    print("\n" + "=" * 60)
    print("示例 4: 加载提示词")
    print("=" * 60)
    
    # 加载提示词并查看
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/my/project",
        output_directory="docs"
    )
    
    print(f"提示词长度: {len(prompt)} 字符")
    print(f"提示词前 500 字符:\n{prompt[:500]}...")


def example5_custom_config():
    """示例 5: 完整配置"""
    print("\n" + "=" * 60)
    print("示例 5: 完整配置")
    print("=" * 60)
    
    # 完整配置
    generate_docs(
        working_directory="/path/to/project",
        output_directory="documentation/technical",
        recursion_limit=1500,  # 增加递归限制
        verbose=True
    )


if __name__ == "__main__":
    # 运行示例 1（最安全）
    example1_simple_usage()
    
    # 取消注释以运行其他示例
    # example2_custom_paths()
    # example3_verbose_mode()
    # example4_load_prompt()
    # example5_custom_config()

