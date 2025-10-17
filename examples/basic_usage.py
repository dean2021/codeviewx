#!/usr/bin/env python3
"""
CodeViewX Basic Usage Examples
"""

import os
from codeviewx import generate_docs, load_prompt


def example1_simple_usage():
    """Example 1: Simplest usage"""
    print("=" * 60)
    print("Example 1: Analyze current directory")
    print("=" * 60)
    
    generate_docs()


def example2_custom_paths():
    """Example 2: Custom paths"""
    print("\n" + "=" * 60)
    print("Example 2: Custom working and output directories")
    print("=" * 60)
    
    generate_docs(
        working_directory="/path/to/your/project",
        output_directory="docs"
    )


def example3_verbose_mode():
    """Example 3: Verbose logging"""
    print("\n" + "=" * 60)
    print("Example 3: Verbose logging mode")
    print("=" * 60)
    
    generate_docs(
        working_directory=os.getcwd(),
        output_directory="docs",
        verbose=True
    )


def example4_load_prompt():
    """Example 4: Load prompt independently"""
    print("\n" + "=" * 60)
    print("Example 4: Load prompt")
    print("=" * 60)
    
    prompt = load_prompt(
        "DocumentEngineer",
        working_directory="/my/project",
        output_directory="docs"
    )
    
    print(f"Prompt length: {len(prompt)} characters")
    print(f"First 500 characters:\n{prompt[:500]}...")


def example5_custom_config():
    """Example 5: Full configuration"""
    print("\n" + "=" * 60)
    print("Example 5: Full configuration")
    print("=" * 60)
    
    generate_docs(
        working_directory="/path/to/project",
        output_directory="documentation/technical",
        recursion_limit=1500,
        verbose=True
    )


if __name__ == "__main__":
    example1_simple_usage()
    
    # Uncomment to run other examples
    # example2_custom_paths()
    # example3_verbose_mode()
    # example4_load_prompt()
    # example5_custom_config()

