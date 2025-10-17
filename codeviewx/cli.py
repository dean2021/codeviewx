#!/usr/bin/env python3
"""
CodeViewX Command Line Interface
CodeViewX 命令行工具
"""

import argparse
import os
import sys
from pathlib import Path

from .core import generate_docs, start_document_web_server
from .__version__ import __version__
from .i18n import get_i18n, t, detect_ui_language


def main():
    """
    Command line entry point
    命令行入口函数
    """
    # Auto-detect UI language / 自动检测界面语言
    ui_lang = detect_ui_language()
    get_i18n().set_locale(ui_lang)
    
    parser = argparse.ArgumentParser(
        prog="codeviewx",
        description=t('cli_description'),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=t('cli_examples')
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
        help=t('cli_working_dir_help')
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        dest="output_directory",
        default="docs",
        help=t('cli_output_dir_help')
    )
    
    parser.add_argument(
        "-l", "--language",
        dest="doc_language",
        default=None,
        choices=['Chinese', 'English', 'Japanese', 'Korean', 'French', 'German', 'Spanish', 'Russian'],
        help=t('cli_language_help')
    )
    
    parser.add_argument(
        "--ui-lang",
        dest="ui_language",
        default=None,
        choices=['en', 'zh'],
        help=t('cli_ui_language_help')
    )
    
    parser.add_argument(
        "--recursion-limit",
        type=int,
        default=1000,
        help="Agent recursion limit (default: 1000) / Agent 递归限制（默认：1000）"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help=t('cli_verbose_help')
    )
    
    parser.add_argument(
        "--serve",
        action="store_true",
        help=t('cli_serve_help')
    )
    
    args = parser.parse_args()
    
    try:
        print(f"CodeViewX v{__version__}")
        print()
        
        # Update UI language if specified / 如果指定了界面语言，更新设置
        if hasattr(args, 'ui_language') and args.ui_language:
            get_i18n().set_locale(args.ui_language)
        
        # If serve mode, start web server / 如果是 serve 模式，启动 Web 服务器
        if args.serve:
            # Check if documentation directory exists / 检查文档目录是否存在
            if not os.path.exists(args.output_directory):
                print(t('cli_missing_docs', path=args.output_directory))
                print(t('cli_serve_hint'))
                print()
                sys.exit(1)
            
            print("=" * 80)
            print(t('cli_starting_server'))
            print("=" * 80)
            print(t('cli_server_address'))
            print(t('cli_server_stop'))
            print("=" * 80)
            print()
            
            start_document_web_server(args.output_directory)
        else:
            # Generate documentation mode / 生成文档模式
            generate_docs(
                working_directory=args.working_directory,
                output_directory=args.output_directory,
                doc_language=args.doc_language,
                ui_language=getattr(args, 'ui_language', None),
                recursion_limit=args.recursion_limit,
                verbose=args.verbose
            )
        
    except KeyboardInterrupt:
        print("\n\n⚠️  User interrupted / 用户中断", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error / 错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

