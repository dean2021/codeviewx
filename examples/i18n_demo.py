#!/usr/bin/env python3
"""
i18n (Internationalization) Demo
i18n（国际化）演示

This example demonstrates how to use the i18n system in CodeViewX.
此示例演示如何在 CodeViewX 中使用 i18n 系统。
"""

from codeviewx import get_i18n, t, set_locale, detect_ui_language


def demo_auto_detection():
    """Demonstrate automatic language detection / 演示自动语言检测"""
    print("=" * 60)
    print("1. Auto Language Detection / 自动语言检测")
    print("=" * 60)
    
    ui_lang = detect_ui_language()
    print(f"Detected system language / 检测到的系统语言: {ui_lang}")
    print()


def demo_english():
    """Demonstrate English messages / 演示英文消息"""
    print("=" * 60)
    print("2. English Messages / 英文消息")
    print("=" * 60)
    
    set_locale('en')
    print(t('starting'))
    print(t('working_dir') + ': /path/to/project')
    print(t('generated_files', count=5))
    print(t('analyzing_structure'))
    print(t('completed'))
    print()


def demo_chinese():
    """Demonstrate Chinese messages / 演示中文消息"""
    print("=" * 60)
    print("3. Chinese Messages / 中文消息")
    print("=" * 60)
    
    set_locale('zh')
    print(t('starting'))
    print(t('working_dir') + ': /path/to/project')
    print(t('generated_files', count=5))
    print(t('analyzing_structure'))
    print(t('completed'))
    print()


def demo_dynamic_switching():
    """Demonstrate dynamic language switching / 演示动态语言切换"""
    print("=" * 60)
    print("4. Dynamic Language Switching / 动态语言切换")
    print("=" * 60)
    
    # Get i18n instance
    i18n = get_i18n()
    
    for lang in ['en', 'zh', 'en']:
        i18n.set_locale(lang)
        print(f"\nLanguage / 语言: {lang}")
        print(f"  {t('cli_description')}")
        print(f"  {t('completed')}")
    print()


def demo_error_messages():
    """Demonstrate error messages / 演示错误消息"""
    print("=" * 60)
    print("5. Error Messages / 错误消息")
    print("=" * 60)
    
    # English error messages
    set_locale('en')
    print("English:")
    print(f"  {t('error_file_not_found', filename='test.md')}")
    print(f"  {t('error_template_variable', variable='working_directory')}")
    
    print()
    
    # Chinese error messages
    set_locale('zh')
    print("中文:")
    print(f"  {t('error_file_not_found', filename='test.md')}")
    print(f"  {t('error_template_variable', variable='working_directory')}")
    print()


def demo_cli_messages():
    """Demonstrate CLI messages / 演示 CLI 消息"""
    print("=" * 60)
    print("6. CLI Messages / CLI 消息")
    print("=" * 60)
    
    # English CLI messages
    set_locale('en')
    print("English:")
    print(f"  {t('cli_starting_server')}")
    print(f"  {t('cli_server_address')}")
    print(f"  {t('cli_server_stop')}")
    
    print()
    
    # Chinese CLI messages
    set_locale('zh')
    print("中文:")
    print(f"  {t('cli_starting_server')}")
    print(f"  {t('cli_server_address')}")
    print(f"  {t('cli_server_stop')}")
    print()


def main():
    """
    Main demo function
    主演示函数
    """
    print("\n" + "=" * 60)
    print("CodeViewX i18n System Demo")
    print("CodeViewX 国际化系统演示")
    print("=" * 60)
    print()
    
    # Run all demos
    demo_auto_detection()
    demo_english()
    demo_chinese()
    demo_dynamic_switching()
    demo_error_messages()
    demo_cli_messages()
    
    print("=" * 60)
    print("✓ Demo completed! / 演示完成!")
    print("=" * 60)
    print()
    
    print("Available locales / 可用语言:", get_i18n().available_locales())
    print("Current locale / 当前语言:", get_i18n().get_locale())
    print()


if __name__ == "__main__":
    main()

