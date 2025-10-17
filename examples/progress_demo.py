#!/usr/bin/env python3
"""
CodeViewX Progress Display Demo

Demonstrates progress information in two modes:
1. Standard mode (concise progress)
2. Verbose mode (detailed logging)
"""

from codeviewx import generate_docs


def demo_simple_progress():
    """Demo: Concise progress display (default mode)"""
    print("=" * 60)
    print("Demo 1: Concise Progress Display Mode")
    print("=" * 60)
    print()
    print("In this mode, you'll see:")
    print("  🔍 Analyzing project structure...")
    print("  📄 Generating document (1): README.md")
    print("  📄 Generating document (2): 01-overview.md")
    print("  📄 Generating document (3): 02-quickstart.md")
    print("  ...")
    print("  ✅ Documentation generation completed!")
    print("  📊 Summary: Generated 11 document files")
    print()
    
    # generate_docs(
    #     working_directory=".",
    #     output_directory="docs",
    #     verbose=False
    # )


def demo_verbose_progress():
    """Demo: Detailed progress logging (verbose mode)"""
    print("\n" + "=" * 60)
    print("Demo 2: Detailed Progress Logging Mode")
    print("=" * 60)
    print()
    print("In this mode, you'll see:")
    print("  📍 Step 1 - HumanMessage")
    print("  📍 Step 2 - AIMessage")
    print("  🔧 Called 3 tools:")
    print("     - list_real_directory")
    print("     - read_real_file")
    print("     - ripgrep_search")
    print("  📍 Step 3 - ToolMessage")
    print("  ...")
    print()
    
    # generate_docs(
    #     working_directory=".",
    #     output_directory="docs",
    #     verbose=True
    # )


def compare_modes():
    """Compare the two modes"""
    print("\n" + "=" * 60)
    print("Mode Comparison")
    print("=" * 60)
    
    print("\n【Standard Mode】- For daily use")
    print("Advantages:")
    print("  ✅ Concise output, easy to read")
    print("  ✅ Shows only key progress information")
    print("  ✅ Real-time document generation progress")
    print("  ✅ Clear summary upon completion")
    print("\nUse cases:")
    print("  - Daily use")
    print("  - Automated scripts")
    print("  - CI/CD pipelines")
    
    print("\n【Verbose Mode】- For debugging")
    print("Advantages:")
    print("  ✅ Shows every execution step")
    print("  ✅ Displays all tool calls")
    print("  ✅ Includes detailed message content")
    print("  ✅ Convenient for troubleshooting")
    print("\nUse cases:")
    print("  - Development debugging")
    print("  - Problem diagnosis")
    print("  - Understanding internal mechanisms")


def progress_output_example():
    """Example output during actual execution"""
    print("\n" + "=" * 60)
    print("Actual Execution Example")
    print("=" * 60)
    
    print("""
Output when running `codeviewx` in standard mode:

================================================================================
🚀 Starting CodeViewX Documentation Generator - 2024-10-16 14:30:00
================================================================================
📂 Working Directory: /Users/deanlu/projects/myapp
📝 Output Directory: docs
🌍 Document Language: Chinese (Auto-detected)
✓ Loaded system prompt (injected working directory, output directory, and document language)
✓ Created AI Agent
✓ Registered 5 custom tools: execute_command, ripgrep_search, write_real_file, read_real_file, list_real_directory
================================================================================

📝 Analyzing project and generating documentation...

🔍 Analyzing project structure...
📄 Generating document (1): README.md
📄 Generating document (2): 01-overview.md
📄 Generating document (3): 02-quickstart.md
📄 Generating document (4): 03-architecture.md
📄 Generating document (5): 04-core-mechanisms.md
📄 Generating document (6): 07-development-guide.md

================================================================================
✅ Documentation generation completed!
================================================================================

📊 Summary:
   ✓ Generated 6 document files
   ✓ Document location: docs/
   ✓ Execution steps: 42 steps
    """)


if __name__ == "__main__":
    demo_simple_progress()
    demo_verbose_progress()
    compare_modes()
    progress_output_example()
    
    print("\n" + "=" * 60)
    print("💡 Tips")
    print("=" * 60)
    print("\nTo actually run, uncomment the generate_docs() calls above")
    print("\nCommand line usage:")
    print("  codeviewx              # Standard mode (concise progress)")
    print("  codeviewx --verbose    # Verbose mode (full logging)")
    print()

