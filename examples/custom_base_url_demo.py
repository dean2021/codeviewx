#!/usr/bin/env python3
"""
Custom Base URL Demo

This example demonstrates how to use CodeViewX with a custom Anthropic API base URL.
This is useful for:
- Using a proxy server
- Using a custom API endpoint
- Testing with a mock server
"""

import os
from codeviewx import generate_docs


def demo_with_environment_variable():
    """
    方法 1: 使用环境变量设置自定义 base URL
    Method 1: Set custom base URL using environment variable
    """
    print("=" * 80)
    print("Demo 1: Using environment variable")
    print("=" * 80)
    
    # 设置自定义 base URL / Set custom base URL
    os.environ['ANTHROPIC_BASE_URL'] = 'https://your-custom-api.example.com'
    
    # 生成文档 / Generate documentation
    # generate_docs(
    #     working_directory=".",
    #     output_directory="docs",
    #     doc_language="Chinese"
    # )
    
    print("✓ Environment variable ANTHROPIC_BASE_URL set to: https://your-custom-api.example.com")
    print("✓ You can now run generate_docs() and it will use this base URL")
    print()


def demo_with_parameter():
    """
    方法 2: 通过参数传递自定义 base URL
    Method 2: Pass custom base URL as parameter
    """
    print("=" * 80)
    print("Demo 2: Using parameter")
    print("=" * 80)
    
    # 通过参数传递自定义 base URL / Pass custom base URL as parameter
    # generate_docs(
    #     working_directory=".",
    #     output_directory="docs",
    #     doc_language="English",
    #     base_url="https://your-custom-api.example.com"
    # )
    
    print("✓ You can pass base_url parameter directly to generate_docs()")
    print("✓ Example: generate_docs(base_url='https://your-custom-api.example.com')")
    print()


def demo_common_use_cases():
    """
    常见使用场景 / Common use cases
    """
    print("=" * 80)
    print("Common Use Cases / 常见使用场景")
    print("=" * 80)
    print()
    
    print("1. Using a proxy server / 使用代理服务器:")
    print("   base_url='https://proxy.example.com/anthropic'")
    print()
    
    print("2. Using a custom API gateway / 使用自定义 API 网关:")
    print("   base_url='https://api-gateway.company.com/ai'")
    print()
    
    print("3. Using a local mock server for testing / 使用本地模拟服务器测试:")
    print("   base_url='http://localhost:8000'")
    print()
    
    print("4. Using a regional endpoint / 使用区域端点:")
    print("   base_url='https://api-eu.anthropic.com'")
    print()


def main():
    print("\n")
    print("CodeViewX - Custom Base URL Demo")
    print("CodeViewX - 自定义 Base URL 演示")
    print("=" * 80)
    print()
    
    demo_with_environment_variable()
    demo_with_parameter()
    demo_common_use_cases()
    
    print("=" * 80)
    print("Note / 注意:")
    print("=" * 80)
    print("• The base URL should be a valid HTTPS endpoint")
    print("  Base URL 应该是一个有效的 HTTPS 端点")
    print()
    print("• Your custom endpoint should be compatible with Anthropic API")
    print("  您的自定义端点应该与 Anthropic API 兼容")
    print()
    print("• You still need to set ANTHROPIC_AUTH_TOKEN")
    print("  您仍然需要设置 ANTHROPIC_AUTH_TOKEN")
    print("=" * 80)


if __name__ == "__main__":
    main()

