#!/usr/bin/env python3
"""
CodeViewX 命令行工具
"""

import argparse
import os
import sys
from pathlib import Path

from .core import generate_docs, start_document_web_server
from .__version__ import __version__


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        prog="codeviewx",
        description="CodeViewX - AI 驱动的代码文档生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  codeviewx                           # 分析当前目录（自动检测语言）
  codeviewx -w /path/to/project       # 分析指定项目
  codeviewx -o docs                   # 输出到 docs 目录
  codeviewx -l English                # 使用英文生成文档
  codeviewx -l Chinese -o docs        # 使用中文，输出到 docs
  codeviewx -w . -o docs --verbose   # 完整配置 + 详细日志
  codeviewx --serve                   # 启动文档 Web 服务器（默认 docs 目录）
  codeviewx --serve -o docs           # 启动服务器并指定文档目录
  
支持的语言:
  Chinese, English, Japanese, Korean, French, German, Spanish, Russian
  
环境变量:
  OPENAI_API_KEY     OpenAI API 密钥（如使用 OpenAI 模型）
  ANTHROPIC_API_KEY  Anthropic API 密钥（如使用 Claude）
        """
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"CodeViewX {__version__}"
    )
    
    parser.add_argument(
        "-w", "--working-dir",
        dest="working_directory",
        default=None,
        help="项目工作目录（默认：当前目录）"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        dest="output_directory",
        default="docs",
        help="文档输出目录（默认：docs）"
    )
    
    parser.add_argument(
        "-l", "--language",
        dest="doc_language",
        default=None,
        choices=['Chinese', 'English', 'Japanese', 'Korean', 'French', 'German', 'Spanish', 'Russian'],
        help="文档语言（默认：自动检测系统语言）"
    )
    
    parser.add_argument(
        "--recursion-limit",
        type=int,
        default=1000,
        help="Agent 递归限制（默认：1000）"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细日志"
    )
    
    parser.add_argument(
        "--serve",
        action="store_true",
        help="启动文档 Web 服务器（查看已生成的文档）"
    )
    
    args = parser.parse_args()
    
    try:
        print(f"CodeViewX v{__version__}")
        print()
        
        # 如果是 serve 模式，启动 Web 服务器
        if args.serve:
            print("=" * 80)
            print("🌐 启动文档 Web 服务器")
            print("=" * 80)
            print(f"📂 文档目录: {args.output_directory}")
            print(f"🔗 访问地址: http://127.0.0.1:5000")
            print("=" * 80)
            print()
            print("💡 提示: 按 Ctrl+C 停止服务器")
            print()
            
            start_document_web_server(args.output_directory)
        else:
            # 生成文档模式
            generate_docs(
                working_directory=args.working_directory,
                output_directory=args.output_directory,
                doc_language=args.doc_language,
                recursion_limit=args.recursion_limit,
                verbose=args.verbose
            )
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

