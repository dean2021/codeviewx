#!/usr/bin/env python3
"""
CodeViewX 进度提示功能演示

展示两种模式下的进度信息：
1. 标准模式（简洁进度）
2. Verbose 模式（详细日志）
"""

from codeviewx import generate_docs


def demo_simple_progress():
    """演示：简洁的进度提示（默认模式）"""
    print("=" * 60)
    print("演示 1: 简洁进度提示模式")
    print("=" * 60)
    print()
    print("在这个模式下，你会看到：")
    print("  🔍 分析项目结构...")
    print("  📄 正在生成文档 (1): README.md")
    print("  📄 正在生成文档 (2): 01-overview.md")
    print("  📄 正在生成文档 (3): 02-quickstart.md")
    print("  ...")
    print("  ✅ 文档生成完成!")
    print("  📊 总结: 共生成 11 个文档文件")
    print()
    
    # 实际执行
    # generate_docs(
    #     working_directory=".",
    #     output_directory=".wiki",
    #     verbose=False  # 默认值，简洁模式
    # )


def demo_verbose_progress():
    """演示：详细进度日志（verbose 模式）"""
    print("\n" + "=" * 60)
    print("演示 2: 详细进度日志模式")
    print("=" * 60)
    print()
    print("在这个模式下，你会看到：")
    print("  📍 步骤 1 - HumanMessage")
    print("  📍 步骤 2 - AIMessage")
    print("  🔧 调用了 3 个工具:")
    print("     - list_real_directory")
    print("     - read_real_file")
    print("     - ripgrep_search")
    print("  📍 步骤 3 - ToolMessage")
    print("  ...")
    print()
    
    # 实际执行
    # generate_docs(
    #     working_directory=".",
    #     output_directory=".wiki",
    #     verbose=True  # 详细模式
    # )


def compare_modes():
    """对比两种模式的输出"""
    print("\n" + "=" * 60)
    print("两种模式对比")
    print("=" * 60)
    
    print("\n【标准模式】- 适合日常使用")
    print("优点：")
    print("  ✅ 输出简洁，易于阅读")
    print("  ✅ 只显示关键进度信息")
    print("  ✅ 实时显示文档生成进度")
    print("  ✅ 完成后有清晰的总结")
    print("\n适用场景：")
    print("  - 日常使用")
    print("  - 自动化脚本")
    print("  - CI/CD 流程")
    
    print("\n【Verbose 模式】- 适合调试")
    print("优点：")
    print("  ✅ 显示每个执行步骤")
    print("  ✅ 展示所有工具调用")
    print("  ✅ 包含详细的消息内容")
    print("  ✅ 便于问题排查")
    print("\n适用场景：")
    print("  - 开发调试")
    print("  - 问题诊断")
    print("  - 了解内部工作机制")


def progress_output_example():
    """实际运行时的输出示例"""
    print("\n" + "=" * 60)
    print("实际运行示例")
    print("=" * 60)
    
    print("""
标准模式运行 `codeviewx` 时的输出：

================================================================================
🚀 启动 CodeViewX 文档生成器 - 2024-10-16 14:30:00
================================================================================
📂 工作目录: /Users/deanlu/projects/myapp
📝 输出目录: .wiki
🌍 文档语言: Chinese (自动检测)
✓ 已加载系统提示词（已注入工作目录、输出目录和文档语言）
✓ 已创建 AI Agent
✓ 已注册 5 个自定义工具: execute_command, ripgrep_search, write_real_file, read_real_file, list_real_directory
================================================================================

📝 开始分析项目并生成文档...

🔍 分析项目结构...
📄 正在生成文档 (1): README.md
📄 正在生成文档 (2): 01-overview.md
📄 正在生成文档 (3): 02-quickstart.md
📄 正在生成文档 (4): 03-architecture.md
📄 正在生成文档 (5): 04-core-mechanisms.md
📄 正在生成文档 (6): 07-development-guide.md

================================================================================
✅ 文档生成完成!
================================================================================

📊 总结:
   ✓ 共生成 6 个文档文件
   ✓ 文档位置: .wiki/
   ✓ 执行步骤: 42 步
    """)


if __name__ == "__main__":
    # 演示不同的使用模式
    demo_simple_progress()
    demo_verbose_progress()
    compare_modes()
    progress_output_example()
    
    print("\n" + "=" * 60)
    print("💡 提示")
    print("=" * 60)
    print("\n要实际运行，请取消注释上面的 generate_docs() 调用")
    print("\n命令行使用：")
    print("  codeviewx              # 标准模式（简洁进度）")
    print("  codeviewx --verbose    # 详细模式（完整日志）")
    print()

